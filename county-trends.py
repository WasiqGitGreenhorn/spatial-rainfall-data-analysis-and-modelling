import pandas as pd
import matplotlib.pyplot as plt
import re

# Load dataset
df = pd.read_csv('florida_rainfall_elevation.csv')

# Identify rainfall columns
rain_cols = [c for c in df.columns if 'rain' in c and '_mean' in c]
years = [int('20' + re.search(r'rain(\d+)_mean', c).group(1)) for c in rain_cols]

# Reshape to long format
rain_long = df.melt(
    id_vars=['county', 'elev_mean'],
    value_vars=rain_cols,
    var_name='year',
    value_name='rainfall_mm'
)
rain_long['year'] = rain_long['year'].apply(lambda x: int('20' + re.search(r'rain(\d+)_mean', x).group(1)))

# Compute rainfall change (2024 vs 2019)
rain_change = (
    rain_long[rain_long['year'].isin([2019, 2024])]
    .pivot(index='county', columns='year', values='rainfall_mm')
    .assign(change=lambda d: d[2024] - d[2019])
    .dropna()
)

# Sort and take top 10 counties
top10 = rain_change.sort_values('change', ascending=False).head(10)
# Plot
plt.figure(figsize=(10,6))
bars = plt.barh(top10.index, top10['change'], color='cornflowerblue')
plt.xlabel('Rainfall Change (mm, 2019 - 2024)')
plt.title('Top 10 Florida Counties by Rainfall Increase (2019–2024)')
plt.gca().invert_yaxis()  # highest on top
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Label each bar with value
for bar in bars:
    plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
             f"{bar.get_width():.1f}", va='center')

plt.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import re

# Load dataset
df = pd.read_csv('florida_rainfall_elevation.csv')

# Identify rainfall columns
rain_cols = [c for c in df.columns if 'rain' in c and '_mean' in c]
years = [int('20' + re.search(r'rain(\d+)_mean', c).group(1)) for c in rain_cols]

# Reshape to long format
rain_long = df.melt(
    id_vars=['county', 'elev_mean'],
    value_vars=rain_cols,
    var_name='year',
    value_name='rainfall_mm'
)
rain_long['year'] = rain_long['year'].apply(lambda x: int('20' + re.search(r'rain(\d+)_mean', x).group(1)))

# Compute rainfall change (2024 vs 2019)
rain_change = (
    rain_long[rain_long['year'].isin([2019, 2024])]
    .pivot(index='county', columns='year', values='rainfall_mm')
    .assign(change=lambda d: d[2024] - d[2019])
    .dropna()
)

# Sort and take top 10 counties
top10 = rain_change.sort_values('change', ascending=True).head(10)
# Plot
plt.figure(figsize=(10,6))
bars = plt.barh(top10.index, top10['change'], color='cornflowerblue')
plt.xlabel('Rainfall Change (mm, 2019 - 2024)')
plt.title('Top 10 Florida Counties by Rainfall Decrease (2019–2024)')
plt.gca().invert_yaxis()  # highest on top
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Label each bar with value
for bar in bars:
    plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
             f"{bar.get_width():.1f}", va='center')

plt.tight_layout()
plt.show()
