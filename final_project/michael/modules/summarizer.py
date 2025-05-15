import pandas as pd

def summarize(gdf, name, assign_func):
    total_units = gdf['DUS'].sum()
    total_acres = gdf['ACRES'].sum()
    built_density = total_units / total_acres if total_acres > 0 else 0

    gdf = gdf.copy()
    gdf['allowed_density_temp'] = gdf.apply(assign_func, axis=1)
    gdf['weighted_allowed_density'] = gdf['allowed_density_temp'] * gdf['ACRES']
    total_allowed_density = gdf['weighted_allowed_density'].sum()
    total_acres_with_density = gdf['ACRES'][gdf['allowed_density_temp'].notnull()].sum()
    allowed_density = total_allowed_density / total_acres_with_density if total_acres_with_density > 0 else 0

    underutilized = gdf['underutilized'].sum()
    underutilization_ratio = gdf['underutilization_ratio'].mean()

    zone_summary = (
        gdf['ZONE_1'].value_counts(normalize=True).mul(100).round(2).rename('Percent')
        .to_frame().assign(Count=gdf['ZONE_1'].value_counts())
    )

    print(f"\n{name} Summary")
    print(f" - Total Units: {total_units:.2f}")
    print(f" - Total Acres: {total_acres:.2f}")
    print(f" - Built Density: {built_density:.2f}")
    print(f" - Allowed Density: {allowed_density:.2f}")
    print(f" - Underutilized Parcels: {underutilized}")
    print(f" - Underutilization Ratio: {underutilization_ratio:.2f}")
    print(zone_summary)

    # Count subsidized (LIHTC Section 42) parcels
    if 'LAND_USE_D' in gdf.columns:
        gdf['LAND_USE_D'] = gdf['LAND_USE_D'].str.upper()
        lihtc_mask = gdf['LAND_USE_D'].str.contains('SUBSIDIZED HOUSING SECTION 42', na=False)
        num_lihtc = lihtc_mask.sum()
        print(f" - Section 42 (LIHTC) Parcels: {num_lihtc}")


