import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the data again
df = pd.read_csv('florida_rainfall_elevation.csv')

# Extract rainfall columns by year
rain_cols = [c for c in df.columns if 'rain' in c]
years = [re.search(r'rain(\d+)_mean', c).group(1) for c in rain_cols]

# Compute average rainfall across all counties per year
rain_means = df[rain_cols].mean().values

# Plot rainfall trend
plt.figure(figsize=(8,6))
plt.plot(years, rain_means, marker='o')
plt.title('Average Annual Rainfall Trend – Florida (2019–2024)')
plt.xlabel('Year')
plt.ylabel('Average Rainfall (mm)')
plt.grid(True)
plt.show()
