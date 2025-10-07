import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('florida_rainfall_elevation.csv')

# Compute average rainfall
rain_cols = [c for c in df.columns if 'rain' in c]
df['rainfall_avg'] = df[rain_cols].mean(axis=1)

# Correlation
corr = df['rainfall_avg'].corr(df['elev_mean'])
print(f"Correlation between rainfall and elevation: {corr:.2f}")

# Scatter plot
plt.figure(figsize=(8,6))
plt.scatter(df['elev_mean'], df['rainfall_avg'], alpha=0.7)
plt.title('Rainfall vs Elevation – Florida Counties (2019–2024)')
plt.xlabel('Elevation (m)')
plt.ylabel('Average Rainfall (mm)')
plt.grid(True)
plt.show(block=True)
input("Press Enter")
