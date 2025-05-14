import pandas as pd
pd.set_option('display.max_columns', None)

df_payments = pd.read_csv("data/olist_order_payments_dataset.csv")
print(df_payments.info())
print(df_payments.describe())
print(df_payments["payment_sequential"].drop_duplicates())
print(df_payments["payment_type"].drop_duplicates())
print(df_payments["payment_installments"].drop_duplicates())
print(df_payments["payment_value"].drop_duplicates())

df_order = pd.read_csv("data/olist_orders_dataset.csv")
print(df_order.info())
print(df_order.describe(include="all"))
print(df_order["order_purchase_timestamp"].drop_duplicates().sort_values())
print(df_order["order_approved_at"].drop_duplicates().sort_values())
print(df_order["order_delivered_carrier_date"].drop_duplicates().sort_values())
print(df_order["order_delivered_customer_date"].drop_duplicates().sort_values())
print(df_order["order_estimated_delivery_date"].drop_duplicates().sort_values())

df_reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
print(df_reviews.info())
print(df_reviews.describe(include="all"))
print(df_reviews["review_score"].drop_duplicates().sort_values())
print(df_reviews["review_comment_title"].drop_duplicates().sort_values())
print(df_reviews["review_comment_message"].drop_duplicates().sort_values())
print(df_reviews["review_creation_date"].drop_duplicates().sort_values())
print(df_reviews["review_answer_timestamp"].drop_duplicates().sort_values())

col_lower = ["review_comment_title", "review_comment_message"]
for col in col_lower:
    df_reviews[col] = df_reviews[col].str.lower() 
l_ch_todelete = ['\n', '\r', 'nan']
for c in l_ch_todelete:
    df_reviews["review_comment_message"] = df_reviews["review_comment_message"].astype(str).apply(lambda x : x.replace(c, ""))

print(df_reviews.dropna())