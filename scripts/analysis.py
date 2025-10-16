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

# -------------------------------------------------------------------
# 1. Import Libraries
# -------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# -------------------------------------------------------------------
# 2. Load Data
# -------------------------------------------------------------------
print("Loading dataset...")
df = pd.read_csv('florida_rainfall_elevation.csv')
print(f"Data loaded successfully with {len(df)} rows and {len(df.columns)} columns.\n")

# Display first few rows
print("Preview of data:")
print(df.head(), "\n")

# -------------------------------------------------------------------
# 3. Compute Average Rainfall and Change Over Time
# -------------------------------------------------------------------
# Identify rainfall columns dynamically
rain_cols = [c for c in df.columns if 'rain' in c]
print("Rainfall columns detected:", rain_cols, "\n")

# Compute average rainfall (2019–2024)
df['rainfall_avg'] = df[rain_cols].mean(axis=1)

# Compute change between 2019 and 2024
df['rain_change'] = df['rain24_mean'] - df['rain19_mean']

# Preview derived columns
print("Derived rainfall columns added:")
print(df[['County', 'rainfall_avg', 'rain_change', 'elev_mean']].head(), "\n")

# -------------------------------------------------------------------
# 4. Correlation Between Rainfall and Elevation
# -------------------------------------------------------------------
corr = df['rainfall_avg'].corr(df['elev_mean'])
print(f"Correlation between average rainfall and elevation: {corr:.2f}\n")

# Scatter plot
plt.figure(figsize=(8,6))
plt.scatter(df['elev_mean'], df['rainfall_avg'], alpha=0.7)
plt.title('Rainfall vs Elevation – Florida Counties (2019–2024)')
plt.xlabel('Elevation (m)')
plt.ylabel('Average Rainfall (mm)')
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# 5. Top 10 Counties by Rainfall Change (2019–2024)
# -------------------------------------------------------------------
top10 = df.sort_values('rain_change', ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.barh(top10['County'], top10['rain_change'], color='cornflowerblue')
plt.title('Top 10 Counties – Rainfall Change (2019–2024)')
plt.xlabel('Change in Rainfall (mm)')
plt.ylabel('County')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# 6. Regression Analysis: Elevation vs. Average Rainfall
# -------------------------------------------------------------------
slope, intercept, r, p, std_err = linregress(df['elev_mean'], df['rainfall_avg'])

print("Linear Regression Results:")
print(f"  Slope: {slope:.3f}")
print(f"  Intercept: {intercept:.2f}")
print(f"  R-squared: {r**2:.2f}")
print(f"  P-value: {p:.4f}\n")

# Regression line visualization
plt.figure(figsize=(8,6))
plt.scatter(df['elev_mean'], df['rainfall_avg'], label='Counties', alpha=0.7)
plt.plot(df['elev_mean'], intercept + slope*df['elev_mean'], color='red', label='Regression Line')
plt.title('Elevation vs Average Rainfall (Linear Fit)')
plt.xlabel('Elevation (m)')
plt.ylabel('Average Rainfall (mm)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# 7. Correlation Heatmap
# -------------------------------------------------------------------
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), cmap="coolwarm", annot=True, fmt=".2f")
plt.title("Variable Correlations – Florida Rainfall Project")
plt.tight_layout()
plt.show()

# -------------------------------------------------------------------
# 8. Export Cleaned & Analyzed Dataset
# -------------------------------------------------------------------
output_file = 'florida_rainfall_analysis_results.csv'
df.to_csv(output_file, index=False)
print(f"Analysis results saved successfully to '{output_file}'.\n")

# -------------------------------------------------------------------
# ✅ End of Script
# -------------------------------------------------------------------
print("Analysis completed successfully! 🌤️")
