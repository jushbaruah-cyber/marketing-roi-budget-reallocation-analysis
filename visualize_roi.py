import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
ANALYSIS_PATH = BASE_PATH / "analysis"

roi = pd.read_csv(ANALYSIS_PATH / "campaign_roi_summary.csv")

plt.figure(figsize=(8,5))
plt.bar(roi.index.astype(str), roi["roi"])
plt.title("Campaign ROI Comparison")
plt.xlabel("Campaign")
plt.ylabel("ROI")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig(ANALYSIS_PATH / "campaign_roi_chart.png")

plt.show()