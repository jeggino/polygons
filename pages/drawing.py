import geopandas as gpd
import osmnx as ox

# create exagons
from h3 import h3
from shapely.geometry import Polygon

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium


m = tost.explore(column='Oppervlakte (m2)',legend_kwds={'interval':True},k=5,scheme='Percentiles',cmap="Reds",  name="Afmeting gebouwen",legend=False,)
m = df_pol.explore(m=m,column='Aantal gebouwen',legend_kwds={'interval':True},k=5,scheme='Percentiles',cmap="Reds",name="Gebouwendichtheid",legend=False)
plugins.HeatMap(heat_data,name="Heat map",min_opacity=0.5,overlay=True,show=False,
    max_zoom=18,
    radius=10,
    blur=10,).add_to(m)

folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False).add_to(m)
folium.LayerControl().add_to(m)
Draw(export=True,position="topleft",show_geometry_on_click=True,
     draw_options={'marker': False, 'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True,}
    ).add_to(m)



folium.plugins.MeasureControl(position="topleft").add_to(m)

Fullscreen().add_to(m)

output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)

output
