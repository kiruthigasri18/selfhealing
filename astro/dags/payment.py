import pandas as pd
import numpy as np
def payments_transform(payment_df):

    silver_payments = (
        payment_df.groupby("order_id")
        .agg(
            total_revenue=("payment_value","sum"),
            payment_count=("payment_value","count"),
            avg_installments=("payment_installments","mean")
        )
        .reset_index()
    )

    return silver_payments