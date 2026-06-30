def products_transform(products_df):

    products_df["volume_cm3"] = (
        products_df["product_length_cm"]
        * products_df["product_width_cm"]
        * products_df["product_height_cm"]
    )

    products_df["density"] = np.where(
        products_df["volume_cm3"] > 0,
        products_df["product_weight_g"] /
        products_df["volume_cm3"],
        np.nan
    )

    products_df["size_category"] = np.select(
        [
            products_df["volume_cm3"] < 1000,
            products_df["volume_cm3"].between(1000,5000),
            products_df["volume_cm3"] > 5000
        ],
        [
            "SMALL",
            "MEDIUM",
            "LARGE"
        ],
        default="UNKNOWN"
    )

    products_df["weight_category"] = np.select(
        [
            products_df["product_weight_g"] < 500,
            products_df["product_weight_g"].between(500,2000),
            products_df["product_weight_g"] > 2000
        ],
        [
            "LIGHT",
            "MEDIUM",
            "HEAVY"
        ],
        default="UNKNOWN"
    )

    return products_df