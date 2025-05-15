# zoning_map.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd


def plot_zoning_map(zones_of_interest, greenbelt_geom, cpumd_geom, cp_geom, zone_color_map):
    """
    Plots the zoning map with color-coded zones and metro station buffers.

    Parameters:
    - zones_of_interest: GeoDataFrame of filtered parcels with a 'ZONE_1' column and 'zone_color'
    - greenbelt_geom: Shapely geometry for the Greenbelt buffer
    - cpumd_geom: Shapely geometry for the College Park-U of Md buffer
    - cp_geom: Shapely geometry of the College Park city boundary
    - zone_color_map: dict mapping zoning codes to colors
    """
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot zoning parcels by zone
    for zone, color in zone_color_map.items():
        subset = zones_of_interest[zones_of_interest['ZONE_1'] == zone]
        if not subset.empty:
            subset.plot(ax=ax, color=color, linewidth=0)

    # Plot buffer outlines
    gpd.GeoSeries(greenbelt_geom).boundary.plot(ax=ax, color='black', linestyle='--', linewidth=1.5)
    gpd.GeoSeries(cpumd_geom).boundary.plot(ax=ax, color='gray', linestyle='--', linewidth=1.5)

    # Plot city boundary
    gpd.GeoSeries(cp_geom).boundary.plot(ax=ax, color='black', linewidth=2)

    # Construct custom legend
    legend_patches = [mpatches.Patch(color=color, label=zone) for zone, color in zone_color_map.items()]
    legend_patches += [
        mpatches.Patch(edgecolor='black', facecolor='none', label='City Boundary'),
        mpatches.Patch(edgecolor='black', facecolor='none', linestyle='--', label='0.5 Mile Buffer (Metro)')
    ]
    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title='Zoning')

    ax.set_title("Zoning Map of College Park and Metro Buffer Areas", fontsize=16)
    ax.axis('off')
    plt.tight_layout()
    plt.show()
