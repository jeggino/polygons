import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
import datetime
from datetime import date
import random

from deta import Deta

import pydeck as pdk

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

  gdf_polygon = gpd.read_file(uploaded_file)
  gdf_polygon = gdf_polygon.to_crs({'init': 'epsg:32633'})
  gdf_polygon['Oppervlakte (Km2)'] = gdf_polygon['geometry'].map(lambda x: round(x.area / 10**6))
  gdf_polygon = gdf_polygon.to_crs({'init': 'epsg:4326'})

else:

  st.stop()

with st.expander("See explanation"):
  st.dataframe(gdf_polygon.drop("geometry",axis=1),use_container_width=True,hide_index=True,)

layers = [
 pdk.Layer(
     type = "GeoJsonLayer",
     data=gdf_polygon,
     width_scale=20,
     width_min_pixels=5,
     get_width=5,
     get_fill_color=[180, 0, 200, 140],
     pickable=True,
     ),
 ]


INITIAL_VIEW_STATE = pdk.ViewState(
        latitude=gdf_polygon.centroid.y.mean(),
        longitude=gdf_polygon.centroid.x.mean(),
        zoom=11,
        min_zoom=5,
        max_zoom=15,
        pitch=0,
        bearing=0)

tooltip = {
    "text": "{naam} \nOppervlakte (Km2): {Oppervlakte (Km2)} \nAanvullende informatie: {extras}",
}


r = pdk.Deck(layers=[layers],initial_view_state=INITIAL_VIEW_STATE,map_style=pdk.map_styles.LIGHT,tooltip=tooltip)

st.pydeck_chart(r)
  
  

