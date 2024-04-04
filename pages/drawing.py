import streamlit as st

import geopandas as gpd
import osmnx as ox

# create exagons
from h3 import h3
from shapely.geometry import Polygon

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium


REGIONAL_NAME  = st.selectbox('Chose a location',('Terschelling', 'Amsterdam'))

region = ox.geocoder.geocode_to_gdf(REGIONAL_NAME)
buildings = ox.geometries.geometries_from_polygon(region['geometry'][0], tags = {'building': True})

tost = buildings[buildings.index.isin(['way'], level=0)].iloc[:,:1]
tost= tost.to_crs({'init': 'epsg:32633'})
tost['Oppervlakte (m2)'] = tost['geometry'].map(lambda x: round(x.area))


H3_LEVEL = st.number_input("Insert a H3 resolution", min_value=3, max_value=12, value="min", step=1)
 
def lat_lng_to_h3(row):
    return h3.geo_to_h3(row.centroid.y, row.centroid.x, H3_LEVEL)

def add_geometry(row):
    points = h3.h3_to_geo_boundary(
      row['h3'], True)
    return Polygon(points)


gdf_centroids = buildings[buildings.index.isin(['way'], level=0)].iloc[:,:1]
gdf_centroids["centroid"] = gdf_centroids["geometry"].centroid
gdf_centroids = gdf_centroids.set_geometry("centroid")
gdf_centroids.reset_index(drop=True,inplace=True)

gdf_centroids['h3'] = gdf_centroids.apply(lat_lng_to_h3, axis=1)

df_pol = gdf_centroids.groupby(['h3'],as_index=False).size().rename(columns={"size": "Aantal gebouwen"})
df_pol['geometry'] = df_pol.apply(add_geometry, axis=1)
df_pol = gpd.GeoDataFrame(df_pol, crs='EPSG:4326')

m = tost.explore(column='Oppervlakte (m2)',legend_kwds={'interval':True},k=5,scheme='Percentiles',cmap="Reds",  name="Afmeting gebouwen",legend=False,)
m = df_pol.explore(m=m,column='Aantal gebouwen',legend_kwds={'interval':True},k=5,scheme='Percentiles',cmap="Reds",name="Gebouwendichtheid",legend=False)
# plugins.HeatMap(heat_data,name="Heat map",min_opacity=0.5,overlay=True,show=False,
#     max_zoom=18,
#     radius=10,
#     blur=10,).add_to(m)

# folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False).add_to(m)
folium.LayerControl().add_to(m)
Draw(export=True,position="topleft",show_geometry_on_click=True,
     draw_options={'marker': False, 'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True,}
    ).add_to(m)



folium.plugins.MeasureControl(position="topleft").add_to(m)

Fullscreen().add_to(m)

output = st_folium(m,returned_objects=["all_drawings"])

output
