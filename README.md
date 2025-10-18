Florida Rainfall and Elevation Analysis

This project combines GIS (Geographic Information Systems) and Python-based data analytics to analyze rainfall and elevation relationships across Florida counties between 2019 and 2024. It was completed as part of a CS50 Python project and serves as a practical portfolio piece showcasing geospatial data processing, visualization, and exploratory data analysis.

1. Project Overview

The goal of this project was to explore spatial and statistical relationships between average annual rainfall and county-level elevation across the state of Florida. The workflow integrates GIS tools (QGIS) for spatial data management and Python for data visualization, computation, and statistical insights.

2. Data Sources

The following datasets were used in this project:
- **GADM v4.1:** Administrative boundaries of U.S. states and counties.
- **CHIRPS Rainfall Dataset (2019–2024):** Monthly precipitation data (in .tif format).
- **SRTM DEM (Elevation Data):** Digital Elevation Model downloaded from OpenTopography.
- **OSM (GeoFabrik):** Vector data for waterways and basemaps (optional visualization layer).

3. QGIS Workflow

The GIS portion of the project was executed using QGIS 3.x. The steps below outline the full process:


1. **Load and Inspect Data**
   - Added GADM shapefile (`gadm41_usa_2.shp`) and extracted Florida counties using the “Extract by Attribute” tool.
   - Imported DEM rasters (SRTM) for both North and South Florida and merged them using “Merge Raster.”
   - Added CHIRPS rainfall rasters (2019–2024) in GeoTIFF format.


2. **Preprocessing**
   - All rasters were reprojected to a common CRS (EPSG:4326).
   - Clipped each rainfall raster and DEM to the Florida boundary using “Clip Raster by Mask Layer.”
   - Cleaned attribute tables to remove duplicate or null entries.


3. **Zonal Statistics**
   - Computed mean rainfall for each county using the “Zonal Statistics” tool.
   - Repeated for all years (2019–2024) and elevation raster.
   - Joined the outputs with the Florida county shapefile into a single `florida_counties_stats` layer.


4. **Visualization**
   - Created choropleth maps for rainfall and elevation.
   - Used “Graduated Symbology” with equal-interval classification for consistency.
   - Designed final layouts in the QGIS Layout Manager with legend, title, and scale bar.
   - Exported maps as PNGs for inclusion in the GitHub repository.

4. Python Workflow

After spatial preprocessing in QGIS, the data was exported as a CSV (`florida_rainfall_elevation.csv`) for Python analysis. The following steps were performed in Visual Studio Code using Python 3.11.


1. **Dependencies**
   - Required libraries: `pandas`, `matplotlib`, and `numpy`.
   - Installed via pip:
     ```bash
     pip install pandas matplotlib numpy
     ```


2. **Analysis Steps**
   - Loaded the CSV file with pandas.
   - Calculated average rainfall across all years per county.
   - Computed correlation between average rainfall and elevation.
   - Visualized relationships using scatter plots.
   - Generated trend plots to show rainfall change (2019–2024) for all counties and top 10 counties.


3. **Example Python Code**
   ```python
   import pandas as pd
   import matplotlib.pyplot as plt

   df = pd.read_csv('florida_rainfall_elevation.csv')

   rain_cols = [c for c in df.columns if 'rain' in c]
   df['rainfall_avg'] = df[rain_cols].mean(axis=1)

   corr = df['rainfall_avg'].corr(df['elev_mean'])
   print(f"Correlation between rainfall and elevation: {corr:.2f}")

   # Plot correlation
   plt.scatter(df['elev_mean'], df['rainfall_avg'], alpha=0.7)
   plt.title('Rainfall vs Elevation – Florida Counties')
   plt.xlabel('Elevation (m)')
   plt.ylabel('Average Rainfall (mm)')
   plt.grid(True)
   plt.show()
   ```

5. Repository Structure

```
florida-rainfall-elevation/
│
├── data/
│   ├── gadm41_usa_2.shp
│   ├── chirps_2019_2024.tif
│   ├── dem_florida.tif
│   └── florida_rainfall_elevation.csv
│
├── qgis_outputs/
│   ├── rainfall_maps/
│   └── elevation_maps/
│
├── results/
│   ├── correlation_plot.png
│   ├── county_trends.png
│   └── top10_trends.png
│
├── analysis.py
└── README.md
```

6. Results & Insights

- A moderate negative correlation was observed between elevation and rainfall, consistent with expected hydrological behavior in low-lying regions.
- The northern and southern counties showed distinctive rainfall patterns, influenced by topography and coastal proximity.
- Temporal rainfall variation (2019–2024) indicated spatially uneven trends, valuable for water management planning.

7. Future Improvements

- Integrate hydrological modeling using rainfall–runoff relationships.
- Include temperature, land use, and vegetation data for multi-variable analysis.
- Automate the GIS workflow with PyQGIS or geopandas.
- Expand dataset coverage to the entire southeastern U.S.

8. Author

Developed by Wasiq Attique as part of the CS50 Python Project.
The project demonstrates practical geospatial data handling, visualization, and analytical techniques applicable to environmental and water resource engineering.

