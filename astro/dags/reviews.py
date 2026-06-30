import pandas as pd
import numpy as np

def reviews_transform(reviews_df):

    conditions = [
        reviews_df["review_score"] >= 4,
        reviews_df["review_score"] == 3,
        reviews_df["review_score"] <= 2
    ]

    choices = [
        "POSITIVE",
        "NEUTRAL",
        "NEGATIVE"
    ]

    reviews_df["review_category"] = np.select(
        conditions,
        choices,
        default="UNKNOWN"
    )

    return reviews_df