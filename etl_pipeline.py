import pandas as pd
from pathlib import Path

# Paths
BASE_PATH = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_PATH / "data"
OUTPUT_PATH = BASE_PATH / "analysis"

OUTPUT_PATH.mkdir(exist_ok=True)

# Load data
sessions = pd.read_csv(DATA_PATH / "sessions.csv", parse_dates=["session_ts"])
orders = pd.read_csv(DATA_PATH / "orders.csv")
order_items = pd.read_csv(DATA_PATH / "order_items.csv")
campaigns = pd.read_csv(DATA_PATH / "campaigns.csv")
ad_spend = pd.read_csv(DATA_PATH / "ad_spend_daily.csv")

# Build fact table
fact_sessions = (
    sessions
    .merge(orders, on="session_id", how="left")
    .merge(order_items, on="order_id", how="left")
)

# Calculate revenue
fact_sessions["revenue"] = fact_sessions["unit_price"] * fact_sessions["quantity"]

# Create date column
fact_sessions["date"] = fact_sessions["session_ts"].dt.date

# Campaign daily aggregation
fact_campaign_daily = (
    fact_sessions
    .groupby(["date", "campaign_id"], as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )
)

# Channel daily aggregation
fact_channel_daily = (
    fact_sessions
    .groupby(["date", "channel"], as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )
)

# Save outputs
fact_sessions.to_csv(OUTPUT_PATH / "fact_sessions.csv", index=False)
fact_campaign_daily.to_csv(OUTPUT_PATH / "fact_campaign_daily.csv", index=False)
fact_channel_daily.to_csv(OUTPUT_PATH / "fact_channel_daily.csv", index=False)

print("ETL completed successfully")