def reviews_transform(review_df):

    review_df["review_category"] = np.select(
        [
            review_df["review_score"] >= 4,
            review_df["review_score"] == 3,
            review_df["review_score"] <= 2
        ],
        [
            "POSITIVE",
            "NEUTRAL",
            "NEGATIVE"
        ]
    )

    review_df["review_sentiment_score"] = (
        review_df["review_score"] / 5
    )

    return review_df