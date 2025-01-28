import streamlit as st
import folium
from streamlit_folium import st_folium


if st.session_state["authenticated"]:
    st.success("Accès autorisé. Vous êtes connecté !")
    st.title("La belle carte folium")
    m1 = folium.Map((47,-1), tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri', zoom_start=10)
    st_data = st_folium(m1, width=725)
else:
    st.text("Vous devez vous connecter")