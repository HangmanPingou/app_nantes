import streamlit as st
import folium
import pandas as pd
import requests
from streamlit_folium import st_folium
from pathlib import Path

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Referer': 'https://www.example.com'
}
def API_address(postal_address):
    link_main = 'https://nominatim.openstreetmap.org/?q='
    address = postal_address
    link_end = '&format=json&limit=1'
    link = link_main + address.replace(" ", "+") + link_end
    r = requests.get(link, headers=headers).json()
    return float(r[0]["lat"]), float(r[0]["lon"])

st.title("Carte des défibrilateurs.")

add = Path.cwd()/"data"

df = pd.read_csv(add/"defibrilateur.csv")

liste_coor = [dict(eval(coor)).get("geometry").get("coordinates")[::-1] for coor in df.geo_shape]

liste_lieux = [lieux for lieux in df.designation]

liste_addresses = [adresse for adresse in df.adresse]

m = folium.Map((47.219940, -1.573184), zoom_start = 12)

for coord, lieux, adresse in zip(liste_coor, liste_lieux, liste_addresses):
    marker = folium.Marker(coord, popup= f"{lieux} / {adresse}", icon=folium.Icon(color='green'))
    marker.add_to(m)

if "marker2" in st.session_state:
    marker2 = st.session_state.marker2
    marker2.add_to(m)

here = st.text_input("Indiquez l'adresse où vous êtes.")

if st.button("Se localiser."):
    coor_here = API_address(here)
    marker2 = folium.Marker(coor_here, popup= "VOUS ÊTES ICI", icon= folium.Icon(color='red'))
    marker2.add_to(m)
    st.session_state["marker2"] = marker2

st_folium(m, width=725)