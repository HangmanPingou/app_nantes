import streamlit as st
import pandas as pd
import folium
import joblib
from datetime import datetime, timedelta
from streamlit_folium import st_folium
from pathlib import Path
from random import randint

def couleur(mark):
    if len(mark) == 1:
        return colors.get(mark[0])
    else:
        return "beige"

colors = {"Audiovisuel": "orange", "Divers": "gray", "Economie circulaire": "darkblue", "Evasion": "green", "Exposition": "red",
            "Fête": "purple", "Jeux": "lightgreen", "Littérature": "black", "Musique": "cadetblue", "Rencontre": "pink",
            "Spectacle": "beige", "Sport": "blue", "Théatre": "lightred"}

colors_legende = {"Audiovisuel": "orange", "Divers": "gray", "Economie circulaire": "darkblue", "Evasion": "green", "Exposition": "red",
            "Fête": "purple", "Jeux": "lightgreen", "Littérature": "black", "Musique": "cadetblue", "Rencontre": "#e8addf",
            "Spectacle": "", "Sport": "blue", "Théatre": "#FF7F7F"}

aujourdhui = datetime.now()
add = Path.cwd()/"data"

df = joblib.load(add/"df_final.flemm")
# df = pd.read_parquet(add/"df_ac.parquet")
df = df.dropna(subset="location_latlong")
# df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
# df["date"] = df["date"].dt.to_pydatetime()
df = df[df["date"] >= aujourdhui].reset_index(drop= True)

if "affichage" not in st.session_state:  # Dataframe de la session.
    st.session_state.affichage = df.sort_values("date").head(15)

if st.session_state["authenticated"]:  # Test si la personne est connectée.
    with st.sidebar:
        
        liste_categories = []  # Filtre catégories.
        for cat in df["Catégories"]:
            for cats in cat.split(", "):
                liste_categories.append(cats)
        liste_categories = (list(set(liste_categories)))
        liste_categories.sort()
        categories = st.multiselect("Catégories.", liste_categories)
        st.write("Légende.")
        colored_text = " ".join([f"<span style='background-color:{colors_legende[opt]}; padding: 5px; border-radius: 5px;'>{opt}</span>" for opt in liste_categories])
        st.markdown(colored_text, unsafe_allow_html=True)
        
        liste_themes = []   # Filtre thèmes.
        for them in df['themes_libe'].unique():
            for thems in them.split(" - "):
                liste_themes.append(thems)
        liste_themes = (list(set(liste_themes)))
        liste_themes.sort()
        liste_themes.remove("None")
        themes = st.multiselect("Thèmes.", liste_themes)

        deb_date = df["date"].min().to_pydatetime() # Filtre temps. Cette ligne force la date pandas en format python.
        fin_date = df["date"].max().to_pydatetime() 
        selected_date = st.slider("Sélectionnez une plage de dates.", min_value= deb_date, max_value= fin_date, value= (deb_date, fin_date), format="DD-MM-YYYY")
        
        liste_cp = []  # Filtre code postal.
        for code in df["code_postal"]:
            liste_cp.append(code)
        liste_cp = (list(set(liste_cp)))
        liste_cp.sort()
        cp = st.multiselect("Code postal.", liste_cp)

        gratuit = st.checkbox("Gratuit.")
        if gratuit:
            st.session_state.affichage = df[(df["tarif_à_partir_de"] == 0.00) & (df["date"] >= selected_date[0]) & (df["date"] <= selected_date[1])]
        # else:
        #     st.session_state.affichage = df[(df["date"] >= selected_date[0]) & (df["date"] <= selected_date[1])].head(15) #df.sort_values("date").head(15)
    st.title(":rainbow[Evénements de la région Nantaise.]")
    m1 = folium.Map(zoom_start = 12)
    if (themes != []) or (categories != []) or (cp != []):
        if gratuit:
            st.session_state.affichage = df[(df['themes_libe'].str.contains('|'.join(themes))) & (df['Catégories'].str.contains('|'.join(categories))) & (df["code_postal"].str.contains('|'.join(cp))) & (df["date"] >= selected_date[0]) & (df["date"] <= selected_date[1])].sort_values("date").head(15)
            st.session_state.affichage = st.session_state.affichage[st.session_state.affichage["tarif_à_partir_de"] == 0.00]
        else:
            st.session_state.affichage = df[(df['themes_libe'].str.contains('|'.join(themes))) & (df['Catégories'].str.contains('|'.join(categories))) & (df["code_postal"].str.contains('|'.join(cp))) & (df["date"] >= selected_date[0]) & (df["date"] <= selected_date[1])].sort_values("date").head(15)

    liste_index = st.session_state.affichage.index
    coordonnees = []
    for indice in liste_index:
        popup_html = f"""
    <style>
    .leaflet-popup-content-wrapper {{
        background: transparent !important;  /* Fond totalement transparent */
        border: none !important;  /* Supprime les bordures */
        box-shadow: none !important;  /* Supprime toute ombre */
    }}
    .leaflet-popup-tip {{
        display: none !important;  /* Supprime la flèche du popup */
    }}
    </style>
    <div style="width: 1px; height: 1px; opacity: 0;">{indice}</div>
    """ # Pour cacher le popup.
        marqueur = folium.Marker(df['location_latlong'].iloc[indice], popup= folium.Popup(popup_html, max_width=0), tooltip= df["nom"][indice], icon=folium.Icon(color= couleur((df["Catégories"].iloc[indice]).split(", "))))
        marqueur.add_to(m1)
        coordonnees.append(list(df['location_latlong'].iloc[indice]))

    m1.fit_bounds(coordonnees)
    map_data = st_folium(m1, width=725)

    st.session_state.affichage = df[(df["date"] >= selected_date[0]) & (df["date"] <= selected_date[1])].sort_values("date").head(15)

    if map_data is not None and "last_clicked" in map_data and map_data["last_clicked"]:
        st.write(df['nom'].iloc[int(map_data.get("last_object_clicked_popup"))])
        st.write(df['lieu'].iloc[int(map_data.get("last_object_clicked_popup"))])
        st.write(df["description_evt"].iloc[int(map_data.get("last_object_clicked_popup"))])
        st.write(f"Heure de début : {df['heure_debut'].iloc[int(map_data.get("last_object_clicked_popup"))]}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Heure de fin : {df['heure_fin'].iloc[int(map_data.get("last_object_clicked_popup"))]}")
        st.write(f"Tarif à partir de : {df['tarif_à_partir_de'].iloc[int(map_data.get("last_object_clicked_popup"))]} € &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Jusqu'à : {df['tarif_jusqua'].iloc[int(map_data.get("last_object_clicked_popup"))]} €")
        st.write(df['url_site'].iloc[int(map_data.get("last_object_clicked_popup"))])


else:
    st.title(":red[Vous devez vous connecter pour accéder à cette page.]")