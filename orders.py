def delivery_delay_days(df):
    if "order_delivered_customer_date" in df.columns and "order_estimated_delivery_date" in df.columns:
        df["delivery_delay_days"] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days
    return df

TRANSFORMATIONS = {
    "delivery_delay_days": delivery_delay_days,
}

def apply_transformation(df, transformation_name):
    if transformation_name in TRANSFORMATIONS:
        return TRANSFORMATIONS[transformation_name](df)
    if transformation_name == "delivery_delay_days":
        return delivery_delay_days(df)
    raise ValueError(f"Unsupported transformation: {transformation_name}")