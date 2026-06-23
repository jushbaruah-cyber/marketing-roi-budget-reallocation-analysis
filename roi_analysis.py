import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_PATH / "data"
ANALYSIS_PATH = BASE_PATH / "analysis"

# load aggregated campaign data
campaign = pd.read_csv(ANALYSIS_PATH / "fact_campaign_daily.csv")

# load ad spend
ad_spend = pd.read_csv(DATA_PATH / "ad_spend_daily.csv")

# merge revenue + spend
roi = campaign.merge(
    ad_spend,
    left_on=["date", "campaign_id"],
    right_on=["date", "campaign_id"],
    how="left"
)

# calculate ROI
roi["roi"] = roi["revenue"] / roi["spend"]

# campaign summary
roi_summary = roi.groupby("campaign_id").agg(
    total_revenue=("revenue","sum"),
    total_spend=("spend","sum")
)

roi_summary["roi"] = roi_summary["total_revenue"] / roi_summary["total_spend"]

roi_summary = roi_summary.sort_values("roi", ascending=False)

# save results
roi_summary.to_csv(ANALYSIS_PATH / "campaign_roi_summary.csv")

print("ROI analysis completed")