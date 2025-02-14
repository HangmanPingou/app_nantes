import streamlit as st
import json
import hashlib
from pathlib import Path

def cacher_menu():  # Permet de cacher le menu par défaut.
    if "sidebar_state" not in st.session_state:
        st.session_state.sidebar_state = False  # Caché par défaut

    if st.button("Afficher/Masquer le menu"):
        st.session_state.sidebar_state = not st.session_state.sidebar_state

    if st.session_state.sidebar_state:
        st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: block !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    else:
        st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def hash_password(password): # Fonction pour le hachage du mot de passe.
    return hashlib.sha256(password.encode()).hexdigest()

add = Path.cwd()/"data"

with open(add/"users.json", "r") as file: # Lecture du fichier des utilisateurs et mot de passe.
    file_data = json.load(file)

liste_users = [user.get("name") for user in file_data]  # Liste des utilisateurs.
liste_passwords = [user.get("password") for user in file_data]  # Liste des mot de passe hachurés.

st.title("Bienvenue chez :rainbow[DATA FLEMM]")

if "authenticated" not in st.session_state: # Gère la variable d'authentification.
    st.session_state["authenticated"] = False

username = st.text_input(":orange[Nom d'utilisateur]")
password = st.text_input(":orange[Mot de passe]", type="password")

if st.button(":blue[Se connecter]"): # Test la connection après avoir appuyer sur le bouton "Se connecter".
    if username in liste_users:
        good_pass = liste_passwords[liste_users.index(username)]
        if good_pass == hash_password(password):
            st.session_state["authenticated"] = True
            st.success("Connexion réussie !")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")
    
if st.button(":blue[Se déconnecter]"):
    st.session_state["authenticated"] = False

cacher_menu()
