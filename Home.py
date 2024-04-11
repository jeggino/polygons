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

def insert_json(naam,opmerking,geometry_type,coordinates,geojson):

    return db.put({"naam":naam,"opmerking":opmerking,"geometry_type":geometry_type, "coordinates":coordinates,"geojson":geojson})



m = folium.Map()
Draw(draw_options={'marker':False,'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True,}).add_to(m)
Fullscreen().add_to(m)
LocateControl(auto_start=True).add_to(m)



output = st_folium(m, returned_objects=["all_drawings"])
output

output["features"] = output.pop("all_drawings")
geometry_type = output["features"][0]["geometry"]["type"]
coordinates = output["features"][0]["geometry"]["coordinates"]
naam = st.text_input("", placeholder="Vul hier een naam in ...")
opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")

output["features"][0]["properties"]["naam"] = naam
output["features"][0]["properties"]["opmerking"] = opmerking
geojson = output["features"][0]

submitted = st.button("Gegevens opslaan")
  
# if submitted:
  
#   insert_json(naam,opmerking,geometry_type,coordinates,geojson)

# try:
  
#   db_content = db.fetch().items
#   df_point = pd.DataFrame(db_content)
  
  
# except:
  
#   st.warning("Npo data")
#   st.stop()

# df_point

"---"

import json
s = df_point.geojson[0]
s
json_acceptable_string = s.replace("'", "\"")
d = json.loads(json_acceptable_string)
gdf_polygon_2 = gpd.GeoDataFrame(d)
gdf_polygon_2 = gdf_polygon_2.set_geometry("geometry")
gdf_polygon_2 = gdf_polygon_2.to_crs({'init': 'epsg:32633'})
gdf_polygon_2['Oppervlakte (Km2)'] = gdf_polygon_2['geometry'].map(lambda x: round(x.area / 10**6,2))
gdf_polygon_2 = gdf_polygon_2.to_crs({'init': 'epsg:4326'})




layers = [
 pdk.Layer(
     type = "GeoJsonLayer",
     data=gdf_polygon_2,
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

"---"

from sqlalchemy import create_engine
import pandas as pd
from ebird.api import get_observations




engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="Platinum79",
                               db="ebird"))

COLUMNS = ['comName', 'date', 'lat', 'lng', 'locId', 'sciName', 'subId']
API_KEY = 'm37q4mkeq3fj'
BACK = 7
COUNTRIES = ['IT','NL','FR','ES','BE','DE']

df_old = pd.read_sql("SELECT * FROM df",con=engine)[COLUMNS]

records = get_observations(API_KEY, COUNTRIES,back=BACK)
df_ebird = pd.DataFrame(records)
df_ebird['date'] = df_ebird.obsDt.str.split(" ",expand=True)[0]
df_ebird = df_ebird[COLUMNS]

df_updated = pd.concat([df_ebird,df_old],axis=0)
df_updated[['lat', 'lng']] = df_updated[['lat', 'lng']].astype("float")
df_updated.drop_duplicates(inplace=True)
df_updated.reset_index(drop=True,inplace=True)

df_updated.to_sql(con=engine, name='df', if_exists='replace')


  
  

