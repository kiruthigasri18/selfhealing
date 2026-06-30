from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(__file__))

from supabase_connection import supabase

from products import products_transform
from orders import orders_transform
from payment import payments_transform
from reviews import reviews_transform
from customer import customers_transform
from orderitems import order_items_transform


# =====================================================
# Common cleanup function
# =====================================================
# def clean_for_supabase(df):

#     df = (
#         df.replace([np.inf, -np.inf], None)
#           .astype(object)
#           .where(pd.notnull(df), None)
#     )

#     return df


import pandas as pd
import numpy as np

def clean_for_supabase(df):

    # Replace inf values
    df = df.replace([np.inf, -np.inf], np.nan)

    # Convert datetime columns to string
    for col in df.columns:

        if pd.api.types.is_datetime64_any_dtype(df[col]):

            df[col] = (
                pd.to_datetime(df[col], errors="coerce")
                .dt.strftime("%Y-%m-%d %H:%M:%S")
            )

    # Convert NaN and NaT to None
    df = (
        df.astype(object)
          .where(pd.notnull(df), None)
    )

    return df
# =====================================================
# Products
# =====================================================
def load_silver_products():

    response = (
        supabase
        .table("olist_products_dataset")
        .select("*")
        .execute()
    )

    df = pd.DataFrame(response.data)

    silver_df = products_transform(df)

    silver_df = clean_for_supabase(silver_df)

    records = silver_df.to_dict("records")

    supabase.table(
        "silver_products"
    ).upsert(records).execute()

    print("silver_products loaded")


# =====================================================
# Orders
# =====================================================
# def load_silver_orders():

#     response = (
#         supabase
#         .table("olist_orders_dataset")
#         .select("*")
#         .execute()
#     )

#     df = pd.DataFrame(response.data)

#     silver_df = orders_transform(df)

#     silver_df = clean_for_supabase(silver_df)

#     records = silver_df.to_dict("records")

#     supabase.table(
#         "silver_orders"
#     ).upsert(records).execute()

#     print("silver_orders loaded")


def load_silver_orders():

    response = (
        supabase
        .table("olist_orders_dataset")
        .select("*")
        .execute()
    )

    df = pd.DataFrame(response.data)

    silver_df = orders_transform(df)

    # Remove timestamp columns completely
    columns_to_drop = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    silver_df = silver_df.drop(
        columns=[col for col in columns_to_drop if col in silver_df.columns]
    )

    silver_df = clean_for_supabase(silver_df)

    records = silver_df.to_dict("records")

    supabase.table(
        "silver_orders"
    ).upsert(records).execute()

    print("silver_orders loaded")


    
# =====================================================
# Payments
# =====================================================
def load_silver_payments():

    response = (
        supabase
        .table("olist_order_payments_dataset")
        .select("*")
        .execute()
    )

    df = pd.DataFrame(response.data)

    silver_df = payments_transform(df)

    silver_df = clean_for_supabase(silver_df)

    records = silver_df.to_dict("records")

    supabase.table(
        "silver_payments"
    ).upsert(records).execute()

    print("silver_payments loaded")


# =====================================================
# Reviews
# =====================================================
def load_silver_reviews():

    response = (
        supabase
        .table("olist_order_reviews_dataset")
        .select("*")
        .execute()
    )

    df = pd.DataFrame(response.data)

    silver_df = reviews_transform(df)

    silver_df = clean_for_supabase(silver_df)

    records = silver_df.to_dict("records")

    supabase.table(
        "silver_reviews"
    ).upsert(records).execute()

    print("silver_reviews loaded")


# =====================================================
# Customers
# =====================================================
def load_silver_customers():

    response = (
        supabase
        .table("olist_customers_dataset")
        .select("*")
        .execute()
    )

    df = pd.DataFrame(response.data)

    silver_df = customers_transform(df)

    silver_df = clean_for_supabase(silver_df)

    records = silver_df.to_dict("records")

    supabase.table(
        "silver_customers"
    ).upsert(records).execute()

    print("silver_customers loaded")


# =====================================================
# Order Items
# =====================================================
def load_silver_order_items():

    response = (
        supabase
        .table("olist_order_items_dataset")
        .select("*")
        .execute()
    )

    df = pd.DataFrame(response.data)

    silver_df = order_items_transform(df)

    silver_df = clean_for_supabase(silver_df)

    records = silver_df.to_dict("records")

    supabase.table(
        "silver_order_items"
    ).upsert(records).execute()

    print("silver_order_items loaded")


# =====================================================
# DAG
# =====================================================
with DAG(
    dag_id="silver_layer_dag",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    schedule=None,
    tags=["silver", "self-healing"]
) as dag:

    products_task = PythonOperator(
        task_id="products_transform",
        python_callable=load_silver_products
    )

    orders_task = PythonOperator(
        task_id="orders_transform",
        python_callable=load_silver_orders
    )

    payments_task = PythonOperator(
        task_id="payments_transform",
        python_callable=load_silver_payments
    )

    reviews_task = PythonOperator(
        task_id="reviews_transform",
        python_callable=load_silver_reviews
    )

    customers_task = PythonOperator(
        task_id="customers_transform",
        python_callable=load_silver_customers
    )

    order_items_task = PythonOperator(
        task_id="order_items_transform",
        python_callable=load_silver_order_items
    )

    products_task >> orders_task >> payments_task >> reviews_task >> customers_task >> order_items_task