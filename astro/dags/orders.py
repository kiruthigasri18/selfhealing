import pandas as pd
import numpy as np



def orders_transform(orders_df):

    orders_df["order_purchase_timestamp"] = pd.to_datetime(
        orders_df["order_purchase_timestamp"],
        errors="coerce",
        utc=True
    ).dt.tz_localize(None)

    orders_df["order_approved_at"] = pd.to_datetime(
        orders_df["order_approved_at"],
        errors="coerce",
        utc=True
    ).dt.tz_localize(None)

    orders_df["order_delivered_customer_date"] = pd.to_datetime(
        orders_df["order_delivered_customer_date"],
        errors="coerce",
        utc=True
    ).dt.tz_localize(None)

    orders_df["order_estimated_delivery_date"] = pd.to_datetime(
        orders_df["order_estimated_delivery_date"],
        errors="coerce",
        utc=True
    ).dt.tz_localize(None)

    orders_df["delivery_days"] = (
        orders_df["order_delivered_customer_date"]
        - orders_df["order_purchase_timestamp"]
    ).dt.days

    orders_df["approval_hours"] = (
        orders_df["order_approved_at"]
        - orders_df["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600

    orders_df["delivery_delay_days"] = (
        orders_df["order_delivered_customer_date"]
        - orders_df["order_estimated_delivery_date"]
    ).dt.days

    orders_df["delivery_status"] = np.where(
        orders_df["delivery_delay_days"].isna(),
        np.nan,
        np.where(orders_df["delivery_delay_days"] <= 0, "ON_TIME", "DELAYED")
    )

    return orders_df