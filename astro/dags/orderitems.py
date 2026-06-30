import pandas as pd
import numpy as np
def order_items_transform(order_items_df):

    silver_items = (
        order_items_df.groupby("order_id")
        .agg(
            avg_freight_value=("freight_value","mean"),
            avg_price=("price","mean"),
            total_item_value=("price","sum")
        )
        .reset_index()
    )

    return silver_items