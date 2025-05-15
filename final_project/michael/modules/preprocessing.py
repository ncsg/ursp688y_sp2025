def reproject_all(dfs, epsg=2248):
    return [df.to_crs(epsg=epsg) for df in dfs]

def create_buffer(gdf, station_name, radius=2640):
    station = gdf[gdf['NAME'] == station_name]
    return station.geometry.buffer(radius).iloc[0]

def filter_parcels(property_gdf, buffer_geom, city_geom=None):
    within_buffer = property_gdf[property_gdf.geometry.within(buffer_geom)]
    if city_geom is not None:
        return within_buffer[within_buffer.geometry.within(city_geom)]
    return within_buffer
