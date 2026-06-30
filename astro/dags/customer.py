import pandas as pd
import numpy as np

def customers_transform(customer_df):

    customer_df["customer_state"] = (
        customer_df["customer_state"]
        .str.upper()
    )

    southeast = ["SP","RJ","MG","ES"]
    south = ["PR","SC","RS"]
    northeast = ["BA","PE","CE","AL","PB","RN","PI","SE","MA"]

    customer_df["customer_region"] = np.select(
        [
            customer_df["customer_state"].isin(southeast),
            customer_df["customer_state"].isin(south),
            customer_df["customer_state"].isin(northeast)
        ],
        [
            "SOUTHEAST",
            "SOUTH",
            "NORTHEAST"
        ],
        default="OTHER"
    )

    return customer_df