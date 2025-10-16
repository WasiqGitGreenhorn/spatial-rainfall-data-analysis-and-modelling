"""
Florida Rainfall–Elevation Analysis (2019–2024)
Author: Wasiq Attique
Description:
    This script analyzes rainfall variation across Florida counties (2019–2024)
    and its relationship with elevation using data exported from QGIS.

    Requirements:
        pandas, matplotlib, seaborn, scipy

    Data:
        florida_rainfall_elevation.csv
        Columns: County, rain19_mean, rain20_mean, ..., rain24_mean, elev_mean
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === SETUP ===
folders = ["data", "results", "scripts"]
for f in folders:
    os.makedirs(f, exist_ok=True)

data_file = "data/florida_rainfall_elevation.csv"
output_dir = "results"
summary_file = os.path.join(output_dir, "summary_report.txt")

print("\n🌦️ Starting Florida Rainfall Analysis...\n")

# === LOAD DATA ===
try:
    df = pd.read_csv(data_file)
    print("✅ Data loaded successfully.")
except FileNotFoundError:
    raise SystemExit("❌ CSV file not found. Make sure it's in the 'data/' folder.")

# === CHECK COLUMNS ===
rain_cols = [c for c in df.columns if c.startswith("rain") and c.endswith("_mean")]
if not rain_cols:
    raise ValueError("❌ No rainfall columns found (expected like 'rain19_mean', 'rain20_mean').")

if "county" not in df.columns:
    raise ValueError("❌ Missing 'county' column in data.")

# === COMPUTE AVERAGE RAINFALL ===
df["rainfall_avg"] = df[rain_cols].mean(axis=1)
print("📊 Added 'rainfall_avg' column (average rainfall across years).")

# === CORRELATION ANALYSIS ===
corr_value = None
if "elev_mean" in df.columns:
    corr_value = df["rainfall_avg"].corr(df["elev_mean"])
    print(f"📈 Correlation (rainfall vs elevation): {corr_value:.2f}")

    plt.figure(figsize=(5, 4))
    sns.heatmap(
        df[["rainfall_avg", "elev_mean"]].corr(),
        annot=True, cmap="coolwarm", vmin=-1, vmax=1
    )
    plt.title("Correlation Heatmap – Rainfall vs Elevation")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"))
    plt.close()
else:
    print("⚠️ 'elev_mean' not found – skipping correlation heatmap.")

# === SCATTER PLOT: Rainfall vs Elevation ===
if "elev_mean" in df.columns:
    plt.figure(figsize=(8, 6))
    plt.scatter(df["elev_mean"], df["rainfall_avg"], alpha=0.7, color="royalblue")
    plt.title("Rainfall vs Elevation – Florida Counties (2019–2024)")
    plt.xlabel("Elevation (m)")
    plt.ylabel("Average Rainfall (mm)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "rainfall_vs_elevation.png"))
    plt.close()

# === STATEWIDE RAINFALL TREND ===
yearly_avg = df[rain_cols].mean()
plt.figure(figsize=(8, 6))
yearly_avg.plot(marker="o", color="darkgreen", linewidth=2)
plt.title("Average Rainfall Trend – Florida (2019–2024)")
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "rainfall_trend_statewide.png"))
plt.close()
print("📈 Saved statewide rainfall trend.")

# === COUNTY-LEVEL TREND ANALYSIS ===
df["rain_change"] = df[rain_cols[-1]] - df[rain_cols[0]]
top_counties = df.nlargest(10, "rain_change")

# Plot trends for top 10 counties
for _, row in top_counties.iterrows():
    county_name = row["county"]
    series = row[rain_cols].values
    years = [c[4:6] for c in rain_cols]

    plt.figure(figsize=(7, 5))
    plt.plot(years, series, marker="o", linewidth=2, color="teal")
    plt.title(f"Rainfall Trend – {county_name}")
    plt.xlabel("Year")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    fname = f"rainfall_trend_{county_name.replace(' ', '_')}.png"
    plt.savefig(os.path.join(output_dir, fname))
    plt.close()

print("📊 Saved top 10 county rainfall trend plots.")

# === MULTI-PANEL PLOT FOR TOP 6 COUNTIES ===
top6 = df.nlargest(6, "rain_change")
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for i, (_, row) in enumerate(top6.iterrows()):
    county_name = row["county"]
    series = row[rain_cols].values
    years = [c[4:6] for c in rain_cols]

    axes[i].plot(years, series, marker="o", linewidth=2, color="slateblue")
    axes[i].set_title(county_name)
    axes[i].set_xlabel("Year")
    axes[i].set_ylabel("Rainfall (mm)")
    axes[i].grid(True, linestyle="--", alpha=0.6)

plt.suptitle("Top 6 Florida Counties – Rainfall Trends (2019–2024)", fontsize=14, weight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(output_dir, "rainfall_trends_top6_panel.png"))
plt.close()

print("🖼️ Created multi-panel chart for top 6 counties.\n")

# === SUMMARY REPORT ===
print("🧾 Writing summary report...")
with open(summary_file, "w") as f:
    f.write("=== Florida Rainfall & Elevation Analysis Summary ===\n\n")

    # Correlation
    if corr_value is not None:
        f.write(f"Correlation between Rainfall and Elevation: {corr_value:.2f}\n\n")

    # Top wettest counties (by average rainfall)
    f.write("Top 5 Wettest Counties (Avg Rainfall):\n")
    top5_wet = df.nlargest(5, "rainfall_avg")[["county", "rainfall_avg"]]
    f.write(top5_wet.to_string(index=False))
    f.write("\n\n")

    # Largest rainfall increase/decrease
    f.write("Counties with Largest Rainfall Change (2019→2024):\n")
    top5_inc = df.nlargest(5, "rain_change")[["county", "rain_change"]]
    top5_dec = df.nsmallest(5, "rain_change")[["county", "rain_change"]]
    f.write("\n🔼 Largest Increases:\n")
    f.write(top5_inc.to_string(index=False))
    f.write("\n\n🔽 Largest Decreases:\n")
    f.write(top5_dec.to_string(index=False))
    f.write("\n\n")

    f.write("Analysis completed successfully.\n")
    f.write("All plots saved in /results folder.\n")

print("✅ All analyses and summary report completed!")
print(f"📄 Summary saved at: {summary_file}\n")
