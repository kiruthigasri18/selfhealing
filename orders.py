import pandas as pd
import numpy as np

def orders_transform(orders_df):
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in date_cols:
        orders_df[col] = pd.to_datetime(
            orders_df[col],
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

    orders_df["delivery_status"] = np.select(
        [
            orders_df["order_delivered_customer_date"].isna(),
            orders_df["delivery_delay_days"] <= 0
        ],
        [
            "PENDING",
            "ON_TIME"
        ],
        default="DELAYED"
    )

    return orders_df