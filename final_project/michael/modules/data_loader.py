import geopandas as gpd

def load_geodata():
    metro_buffer = gpd.read_file('data/Metro_One_Mile_Buffer_Py.shp')
    metro_stations = gpd.read_file('data/Metro_Stations_Regional.shp')
    muni_boundary = gpd.read_file('data/Municipal_Boundary_Py.shp')
    property_gdf = gpd.read_file('data/Property_Info_Py.shp')
    return metro_buffer, metro_stations, muni_boundary, property_gdf
