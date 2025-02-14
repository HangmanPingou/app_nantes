import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from shapely.geometry import Polygon
from streamlit_folium import st_folium
from shapely.geometry import Point
from pathlib import Path

add = Path.cwd()/"data"

if st.session_state["authenticated"]:  # Test si la personne est connectée.
#zone que l'on veut garder 
    left = -1.75
    right = -1.4885065
    bottom = 47.1420006
    top = 47.323559
#enregistrer dans un polygon
    polygon = Polygon([(left, bottom), (right, bottom), (right, top), (left, top)])

# Charger le GeoDataFrame depuis le fichier Parquet
    gdf = gpd.read_parquet(add/"espaces_verts_20250128.parquet")  # Remplacez par le nom de votre fichier
# S'assurer que le GeoDataFrame est en EPSG:4326 (WGS 84)
    gdf = gdf.to_crs(epsg=4326)
#garde ceux qui sont dans la zone
    gdf = gpd.clip(gdf, polygon)

# filtrer les waterway "drain" (canaux artificiel d'évacuation)
    gdf = gdf.dropna(subset=['name'])
    gdf_filtered = gdf[gdf['fclass'] == 'park']


# Créer la carte Folium avec le fond de carte ArcGIS Ocean Base
    m2 = folium.Map(
    location=(47.214484, -1.558476),
    # tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
    # attr='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
    zoom_start=12)

# Style pour les rivières (optionnel, mais recommandé pour une meilleure visibilité)
    style_function = lambda x: {'color': 'green', 'weight': 1.5, 'opacity':0.7} #Couleur bleue, épaisseur 1.5, légère transparence

# Ajouter les rivières à la carte avec le style
#folium.GeoJson(gdf_filtered, style_function=style_function).add_to(m1)
#avec tootip (label) au survol
    for _, r in gdf_filtered.iterrows():
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = folium.GeoJson(
            data=sim_geo.to_json(),
            style_function=style_function,
            tooltip=r['name'] #Ajout du tooltip avec le nom de la waterway
        ).add_to(m2)

    st.title(":green[Parcs de la région Nantaise.]")
    st_folium(m2, width=725)



    data = {
    'name': [
        "Musée d'arts de Nantes",
        "Musée de la Poste",
        "Musée d'Histoire de Nantes",
        "Musée Dobrée",
        "Muséum d'Histoire Naturelle",
        "Musée de l'Imprimerie",
        "Maison des Hommes et des techniques",
        "Planétarium de Nantes",
        "Musée Jules Verne",
        "Le Chronographe",
        "Musée Compagnonique",
        "Musée Maillé Brézé",
        "Mémorial de l'abolition de l'esclavage"
    ],
    'Type' : [
        "museum",
        "museum",
        "museum",
        "museum",
        "museum",
        "museum",
        "museum",
        "museum",
        "museum",
        'museum',
        'museum',
        'museum',
        'museum'
    ],
    'adresse': [
        "10 Rue Georges Clemenceau, 44000 Nantes",
        "2B Rue Président Edouard Herriot, 44000 Nantes",
        "4 Place Marc Elder, 44000 Nantes",
        "18 Rue Voltaire, 44000 Nantes",
        "12 Rue Voltaire, 44000 Nantes",
        "24 Quai de la Fosse, 44000 Nantes",
        "2B Boulevard Léon Bureau, 44200 Nantes",
        "8 Rue des Acadiens, 44100 Nantes",
        "8 Rue de l'Hermitage, 44000 Nantes",
        "21 Rue de la Chézine, 44400 Rezé",
        "14 Rue Claude Guillon Verne, 44100 Nantes",
        "105 Quai de la Fosse, 44100",
        "55 Quai de la Fosse, 44000"
        
    ],
    'latitude': [
        47.2192,
        47.21813,
        47.2163,
        47.2118,
        47.2123,
        47.2109,
        47.2065,
        47.2022,
        47.2016,
        47.1915,
        47.2027,
        47.2071,
        47.2097
    ],
    'longitude': [
        -1.5470,
        -1.5594,
        -1.5504,
        -1.5662,
        -1.5646,
        -1.5618,
        -1.5644,
        -1.577,
        -1.577,
        -1.566,
        -1.582,
        -1.571,
        -1.5640
    ]
}

    df = pd.DataFrame(data)
    # geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    liste_coor = []
    m3 = folium.Map(location=[df['latitude'][0], df['longitude'][0]], zoom_start=14)
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],popup = row['name']
        
        # icon=folium.Icon(icon="cloud"),
        ).add_to(m3)
        liste_coor.append([row['latitude'], row['longitude']])

    st.title(":blue[Musées de la région Nantaise.]")
    m3.fit_bounds(liste_coor)
    st_folium(m3, width=725)



    df_rest = pd.read_csv(add/"restaurants.csv")
    liste_coor = [coor.replace("[", "").replace("]", "").split(",") for coor in df_rest.location_latlong]
    liste_nom = [rest for rest in df_rest.nom]
    m4 = folium.Map(zoom_start = 12)
    for coord, nom in zip(liste_coor, liste_nom):   # Ajout des marqueurs pour chaque défibrilateur.
        marker = folium.Marker(coord, popup= nom, icon=folium.Icon(color="green"))
        marker.add_to(m4)
    st.title(":red[Restaurants de la région Nantaise.]")
    m4.fit_bounds(liste_coor)
    st_folium(m4, width=725)


else:
    st.title(":red[Vous devez vous connecter pour accéder à cette page.]")