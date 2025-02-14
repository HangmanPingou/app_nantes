import streamlit as st
import folium
import pandas as pd
import requests
import geopy.distance
from streamlit_folium import st_folium, folium_static
from pathlib import Path

headers = {   # Pour se connecter à l'API openstreetmap.
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Referer': 'https://www.example.com'
}
def API_address(postal_address):   # Fonction qui récupère les coordonnées GPS à partir de l'adresse en intérogeant l'API.
    link_main = 'https://nominatim.openstreetmap.org/?q='
    address = postal_address
    link_end = '&format=json&limit=1'
    link = link_main + address.replace(" ", "+") + link_end
    r = requests.get(link, headers=headers).json()
    return float(r[0]["lat"]), float(r[0]["lon"])

def tri_liste(liste, indice, valeur): # Fonction de trie pour intégrer une valeur dans une liste pour rester en ordre croissant.
    longueur = len(liste)
    for _ in range(longueur, indice +1, -1):
        liste[_ - 1] = liste[_ - 2]
    liste[indice] = valeur
    return liste

st.title(":red[Carte des défibrilateurs.]")

add = Path.cwd()/"data"

df = pd.read_csv(add/"defibrilateur.csv")

liste_coor = [dict(eval(coor)).get("geometry").get("coordinates")[::-1] for coor in df.geo_shape]
liste_lieux = [lieux for lieux in df.designation]           # Création des différentes listes par rapport au fichier.
liste_addresses = [adresse for adresse in df.adresse]

m = folium.Map(zoom_start = 12)  # Initialisation de la carte.

for coord, lieux, adresse in zip(liste_coor, liste_lieux, liste_addresses):   # Ajout des marqueurs pour chaque défibrilateur.
    marker = folium.Marker(coord, popup= f"{lieux} / {adresse}", icon=folium.Icon(color="green"))
    marker.add_to(m)

if "markers" not in st.session_state:  # Liste des marqueurs à rajouter, la liste étant créée dans la session.
    st.session_state.markers = []

if "marker2" in st.session_state:  # Permet de gérer le marqueur "VOUS ETES ICI" dans la session.
    marker2 = st.session_state.marker2
    marker2.add_to(m)

if "coordonnees" not in st.session_state:  # La liste pour le centrage automatique de la carte.
    st.session_state.coordonnees = liste_coor

for indice in st.session_state.markers:  # Ajouts des marqueurs présent dans la liste de la session.
    folium.Marker(liste_coor[indice], popup= f"{liste_lieux[indice]} / {liste_addresses[indice]}").add_to(m)

here = st.text_input(":blue[Indiquez l'adresse où vous êtes.]")

if st.button("Se localiser."):
    coor_here = API_address(here)  # Utilise la fonction pour récupérer les coordonnées GPS à partir de l'adresse entrée dans le champ.
    marker2 = folium.Marker(coor_here, popup= "VOUS ÊTES ICI", icon= folium.Icon(color='red'))
    marker2.add_to(m)
    st.session_state["marker2"] = marker2 # Enregistre ce marqueur dans la session.
    nb_fois = 5  # Variable qui donne le nombre de marqueurs plus proches à afficher.
    liste_proche = [[50000, 0]] * nb_fois
    for coor in liste_coor:  # Calcule la distance de chaque point avec celui où on est et ressort une liste avec la distance et l'indice des 5 plus proche.
        for indice in range(len(liste_proche)):
            if round(geopy.distance.geodesic(coor_here, coor).m) < liste_proche[indice][0]:
                valeur = [round(geopy.distance.geodesic(coor_here, coor).m), liste_coor.index(coor)]
                liste_proche = tri_liste(liste_proche, indice, valeur)
                break
    liste_indice = [liste_proche[indice][1] for indice in range(len(liste_proche))]
    st.session_state.markers = []
    st.session_state.coordonnees = []
    for indice in liste_indice:  # Ajoute à la liste de la session les indices des 5 plus proches.
        st.session_state.markers.append(indice)
        st.session_state.coordonnees.append(liste_coor[indice])

m.fit_bounds(st.session_state.coordonnees)
st_folium(m, width=725)

