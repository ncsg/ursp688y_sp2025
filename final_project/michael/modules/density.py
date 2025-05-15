import pandas as pd

def assign_allowed_density(row):
    zone_columns = ['ZONE_1', 'ZONE_2', 'ZONE_3', 'ZONE_4', 'ZONE_5']
    zone_values = [str(row[col]).upper() for col in zone_columns]
    land_use = str(row['LAND_USE']).upper()
    land_use_desc = str(row['LAND_USE_D']).upper()

    base_zone_density = {
        'RE': 1.08,
        'RR': 2.17,
        'RSF-95': 4.58,
        'RSF-65': 6.7,
        'RSF-A': 32.6,
        'RMF-20': {
            'APARTMENT': 20.0, 'SUBSIDIZED': 20.0, 'CONDO': 20.0, 'VACANT': 20.0,
            'STANDARD': 14.0, 'SPLIT': 14.0, 'SUBDIVIDED': 14.0
        },
        'RMF-48': {
            'HI RISE': 48.0, 'APARTMENT': 48.0, 'GARDEN': 48.0, 'SUBSIDIZED': 48.0,
            'CONDO': 30.0, 'RETAIL/APT': 30.0, 'VACANT': 48.0
        },
        'RMF-12': 12.0
    }

    tod_zone_density = {
        'NAC': 90.0,
        'TAC-C': 120.0,
        'TAC-E': 100.0,
        'LTO-C': 150.0,
        'LTO-E': 120.0,
        'RTO-L-C': 175.0,
        'RTO-L-E': 140.0,
        'RTO-H-C': 250.0,
        'RTO-H-E': 175.0
    }

    for zone in zone_values:
        if zone in base_zone_density:
            density = base_zone_density[zone]
            if isinstance(density, dict):
                for key in density:
                    if key in land_use or key in land_use_desc:
                        return density[key]
                return None
            return density
        elif zone in tod_zone_density:
            return tod_zone_density[zone]
    return None

def calculate_densities(property_gdf):
    property_gdf = property_gdf.copy()
    property_gdf['allowed_density'] = property_gdf.apply(assign_allowed_density, axis=1)
    property_gdf = property_gdf.dropna(subset=['allowed_density'])
    property_gdf['built_density'] = property_gdf['DUS'] / property_gdf['ACRES']
    property_gdf['underutilization_ratio'] = property_gdf['built_density'] / property_gdf['allowed_density']
    property_gdf['underutilized'] = property_gdf['underutilization_ratio'] < 0.5
    return property_gdf
