# In case of any missing libraties re-import them
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from sklearn.preprocessing import KBinsDiscretizer
from libpysal.weights import Queen
from spopt.region import Skater
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from scipy.stats import pearsonr
import contextily as ctx

# This function joins a DataFrame (df) to a GeoDataFrame (gdf) using a shared column (label)
def join_df_to_gdf(df, gdf, label):
    
    # 1. Check if the join column exists in the GeoDataFrame gdf
    if label not in gdf.columns:
        raise ValueError(f"'{label}' not found in GeoDataFrame columns.")
    
    # 2. Check if the join column exists in the regular DataFrame df
    if label not in df.columns:
        raise ValueError(f"'{label}' not found in DataFrame columns.")
    
    # Convert the join column in both dataframes to string and remove any extra spaces
    # to ensure that the join works correctly even if formats are inconsistent
    df[label] = df[label].astype(str).str.strip()
    gdf[label] = gdf[label].astype(str).str.strip()
    
    # Perform a left join: keep all rows from the GeoDataFrame and add matching data from the DataFrame
    return gdf.merge(df, how='left', on=label)
    




# This function creates a bivariate choropleth map using Jenks natural breaks for two variables.
# It also uses SKATER spatial clustering to group similar areas and visualize patterns across space.
# It also saves the map in ther directory

def bivariate_skater_map_jenks(gdf, var1, var2, figsize=(12, 10), save_path=None):
    # Import necessary packages
    import geopandas as gpd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from sklearn.preprocessing import KBinsDiscretizer
    from libpysal.weights import Queen
    from spopt.region import Skater
    import contextily as ctx
    import pandas as pd
    from mapclassify import NaturalBreaks  # For Jenks classification

    # Make a fresh copy of the GeoDataFrame to avoid changing the original
    gdf = gdf.copy().reset_index(drop=True)

    # If no CRS is defined, set it to WGS84, then reproject to EPSG:4326
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    gdf = gdf.to_crs(epsg=4326)

    # Create a column that flags rows with valid (non-null) values for both variables
    gdf['has_data'] = gdf[[var1, var2]].notnull().all(axis=1)

    # Extract rows that are valid and exclude infinities
    valid_data = gdf[gdf['has_data']][[var1, var2]].replace([np.inf, -np.inf], np.nan).dropna()
    valid_gdf = gdf.loc[valid_data.index]  # Match geometry to valid data rows

    # SKATER clustering (groups regions based on spatial and variable similarity)
    w = Queen.from_dataframe(valid_gdf)  # Queen contiguity spatial weights
    skater = Skater(valid_gdf, w, attrs_name=[var1, var2], n_clusters=9)
    skater.solve()
    gdf.loc[valid_data.index, 'cluster'] = skater.labels_  # Add cluster labels to gdf

    # Set number of bins for each variable
    n_bins = 3

    # Apply Jenks natural breaks classification for both variables
    jenks1 = NaturalBreaks(y=valid_data[var1], k=n_bins)
    jenks2 = NaturalBreaks(y=valid_data[var2], k=n_bins)
    x_bin = jenks1.yb  # Bin indices for var1
    y_bin = jenks2.yb  # Bin indices for var2

    # Create a bivariate class index for each feature (flipped for visual matrix orientation)
    bivariate_class = (2 - x_bin) * n_bins + y_bin

    # Initialize bivariate fields
    gdf['x_bin'] = np.nan
    gdf['y_bin'] = np.nan
    gdf['bivariate_class'] = np.nan

    # Assign binned values to valid rows
    gdf.loc[valid_data.index, 'x_bin'] = x_bin
    gdf.loc[valid_data.index, 'y_bin'] = y_bin
    gdf.loc[valid_data.index, 'bivariate_class'] = bivariate_class

    # Define a custom color palette for the 3×3 combinations (I got the color codes from photoshop)
    base_palette = [
        '#2ca25f', '#99d8c9', '#e5f5f9',  # Best: High var1, Low var2
        '#fee08b', '#fdae61', '#f46d43',  # Medium values
        '#d73027', '#a50026', '#7f0000'   # Worst: Low var1, High var2
    ]

    # Map each bivariate class index to a color
    base_colors = {i: base_palette[i] for i in range(n_bins * n_bins)}
    gdf['bivariate_category'] = gdf['bivariate_class'].map(lambda x: f"Bin {int(x)}" if pd.notnull(x) else "NA")
    gdf['color'] = gdf['bivariate_class'].map(base_colors).fillna('#d3d3d3')  # gray for missing

    # Reproject for web map compatibility going back to UTM (EPSG:3857)
    gdf_web = gdf.to_crs(epsg=3857)

    # Create plot
    fig, ax = plt.subplots(figsize=figsize)

    # Plot the colored polygons
    gdf_web.plot(ax=ax, color=gdf_web['color'], edgecolor='black', linewidth=0.2, zorder=2)

    # Set plot boundaries
    ax.set_xlim(gdf_web.total_bounds[0], gdf_web.total_bounds[2])
    ax.set_ylim(gdf_web.total_bounds[1], gdf_web.total_bounds[3])

    # Add a basemap under the data
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, alpha=0.6, zorder=1)

    # Add title and remove axes
    ax.set_title(f'Bivariate Map (Jenks): {var1} vs {var2}', fontsize=16)
    ax.axis('off')

    # Create a small 3×3 matrix legend in the corner
    legend_ax = fig.add_axes([0.72, 0.05, 0.2, 0.2])  # [left, bottom, width, height]
    for i in range(n_bins):
        for j in range(n_bins):
            cls = i * n_bins + j
            color = base_palette[cls]
            rect = Rectangle((j, i), 1, 1, color=color)
            legend_ax.add_patch(rect)

    # Style the legend matrix
    legend_ax.set_xlim(0, n_bins)
    legend_ax.set_ylim(0, n_bins)
    legend_ax.set_xticks([i + 0.5 for i in range(n_bins)])
    legend_ax.set_yticks([i + 0.5 for i in range(n_bins)])
    legend_ax.set_xticklabels(['Low', 'Med', 'High'])
    legend_ax.set_yticklabels(['Low', 'Med', 'High'])
    legend_ax.set_xlabel(var2)
    legend_ax.set_ylabel(var1)
    legend_ax.set_title('Category Matrix', fontsize=10)
    legend_ax.tick_params(axis='both', length=0)
    legend_ax.grid(False)

    # Write out the Jenks bin edges below the map to show their ranges
    text_lines = [f"{var1} (Jenks):"]
    for i in range(n_bins):
        text_lines.append(f"  Bin {i + 1}: {jenks1.bins[i]:.2f}")
    text_lines.append("")
    text_lines.append(f"{var2} (Jenks):")
    for i in range(n_bins):
        text_lines.append(f"  Bin {i + 1}: {jenks2.bins[i]:.2f}")

    # Add the text to the figure
    plt.figtext(0.01, 0.02, "\n".join(text_lines), ha='left', va='bottom', fontsize=9, fontfamily='monospace')

    # Save the figure to file if a path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show the final map
    plt.show()

    # Return the updated GeoDataFrame with binned values and colors
    return gdf


# This function creates a scatterplot with a trendline and shows the Pearson correlation
# between two numeric variables from a GeoDataFrame and it also shows the p-value

def scatter_with_trend_and_correlation(gdf, var1, var2, save_path=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import pearsonr

    # Keep only valid (finite and non-missing) values for both variables
    df = gdf[[var1, var2]].replace([np.inf, -np.inf], np.nan).dropna()

    # If no valid data exists, stop and raise an error
    if df.empty:
        raise ValueError(f"No valid (non-NaN, non-infinite) values found for {var1} and {var2}")

    # Calculate the Pearson correlation coefficient and p-value
    corr_coef, p_value = pearsonr(df[var1], df[var2])

    # Classify the strength of the correlation
    if abs(corr_coef) < 0.3:
        strength = "weak"
    elif abs(corr_coef) < 0.6:
        strength = "moderate"
    else:
        strength = "strong"

    # Determine if the correlation is positive or negative
    direction = "positive" if corr_coef > 0 else "negative"

    # Determine if the correlation is statistically significant
    significance = "significant" if p_value < 0.05 else "not significant"

    # Create the plot: scatter + trendline
    plt.figure(figsize=(8, 6))
    sns.regplot(x=var1, y=var2, data=df, scatter_kws={'alpha': 0.6}, line_kws={'color': 'red'})  # regression line in red

    # Set plot title and axis labels
    plt.title(f'Correlation Analysis: {var1} vs {var2}', fontsize=16)
    plt.xlabel(var1, fontsize=12)
    plt.ylabel(var2, fontsize=12)

    # Prepare annotation text showing correlation result
    annotation = (
        f"Pearson r: {corr_coef:.3f} ({strength}, {direction})\n"
        f"P-value: {p_value:.3g} → {significance}"
    )

    # Add annotation below the plot
    plt.figtext(0.5, -0.08, annotation, ha='center', fontsize=10, fontstyle='italic')

    plt.tight_layout()  # Adjust layout to avoid clipping

    # Optionally save the figure
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()
