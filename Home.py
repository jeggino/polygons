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
import altair as alt


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

  gdf_polygon = gpd.read_file(uploaded_file)

else:

  st.stop()


layers = [
 pdk.Layer(
     type = "GeoJsonLayer",
     data=gdf_polygon,
     width_scale=20,
     width_min_pixels=5,
     get_width=5,
     get_fill_color=[180, 0, 200, 140],
     pickable=False,
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



r = pdk.Deck(layers=[layers],initial_view_state=INITIAL_VIEW_STATE,map_style=pdk.map_styles.LIGHT,)

st.pydeck_chart(r)

regions = alt.topo_feature("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/italy/italy-regions.json", 'ITA_adm1')

map = alt.Chart(regions).mark_geoshape(
    stroke='white',
    strokeWidth=2
).encode(
    color=alt.value('#eee'),
)
st.altair_chart(map, use_container_width=False)

  
  

