import streamlit as st
import pandas as pd

import geopandas as gpd
import pydeck as pdk

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

  gdf_polygon = gpd.read_file(uploaded_file)
  gdf_polygon = gdf_polygon.to_crs({'init': 'epsg:32633'})
  gdf_polygon['Oppervlakte (Km2)'] = gdf_polygon['geometry'].map(lambda x: round(x.area / 10**6,2))
  gdf_polygon = gdf_polygon.to_crs({'init': 'epsg:4326'})

else:

  st.stop()

# with st.expander("See explanation"):
#   st.dataframe(gdf_polygon.drop("geometry",axis=1),use_container_width=True,hide_index=True,)

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
        pitch=0,
        bearing=0)

tooltip = {
    "text": "{naam} \nOppervlakte (Km2): {Oppervlakte (Km2)} \nAanvullende informatie: {extras}",
}


r = pdk.Deck(layers=[layers],initial_view_state=INITIAL_VIEW_STATE,tooltip=tooltip,
              map_style=pdk.map_styles.ROAD)


st.pydeck_chart(r)

"---"
import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

from deta import Deta

# --- CONNECT TO DETA ---
# deta = Deta(st.secrets["deta_key"])
deta = Deta("a0hz4ythxni_TNmhLV3CVtzR7a5PJ3gxADVeqPJQe9dc")
db = deta.Base("df_polygons")

def insert_json(naam,opmerking,geometry_type,coordinates):

    return db.put({"naam":naam,"opmerking":opmerking,"geometry_type":geometry_type, "coordinates":coordinates})



m = folium.Map()
Draw(draw_options={'marker':False,'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True,}).add_to(m)
Fullscreen().add_to(m)
LocateControl(auto_start=True).add_to(m)



output = st_folium(m, returned_objects=["all_drawings"])

output["features"] = output.pop("all_drawings")
output
geometry_type = output["features"][0]["geometry"]["type"]
coordinates = output["features"][0]["geometry"]["coordinates"]
naam = st.text_input("", placeholder="Vul hier een naam in ...")
opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")


submitted = st.button("Gegevens opslaan")
  
if submitted:
  
  insert_json(naam,opmerking,geometry_type,coordinates)

try:
  
  db_content = db.fetch().items
  df_point = pd.DataFrame(db_content)
  
  
except:
  
  st.warning("Npo data")
  st.stop()

df_point

"---"

gdf_polygon = gpd.GeoDataFrame(db_content)
gdf_polygon = gdf_polygon.to_crs({'init': 'epsg:32633'})
gdf_polygon['Oppervlakte (Km2)'] = gdf_polygon['coordinates'].map(lambda x: round(x.area / 10**6,2))
gdf_polygon = gdf_polygon.to_crs({'init': 'epsg:4326'})




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

        zoom=11,
        pitch=0,
        bearing=0)

tooltip = {
    "text": "{naam} \nOppervlakte (Km2): {Oppervlakte (Km2)} \nAanvullende informatie: {opmerking}",
}


r = pdk.Deck(layers=[layers],initial_view_state=INITIAL_VIEW_STATE,tooltip=tooltip,
              map_style=pdk.map_styles.ROAD)


st.pydeck_chart(r)





  
  

