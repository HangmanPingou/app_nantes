import streamlit as st
import hashlib
import json
import re
from datetime import date
from pathlib import Path

def hash_password(password): # Fonction pour le hachage du mot de passe avant de l'enregistrer dans le fichier json.
    return hashlib.sha256(password.encode()).hexdigest()

st.title("INSCRIPTION", )
new_username = st.text_input("Choisir un nom d'utilisateur.")
new_password = st.text_input("Choisir un mot de passe : \n\nDoit comporter au moins 8 caractères, une majuscule, une minuscule, un caractère spécial et un chiffre.", type="password")
confirm_password = st.text_input("Confirmer le mot de passe.", type="password")
new_age = st.date_input("Entrer votre date de naissance : \n\nInformation non enregistrée. Vous devez être majeure.", format="YYYY/MM/DD", min_value=date(year=1900, month=1, day=1), max_value=date(year=2025, month=2, day=28)) # Vérifie la majorité.

add = Path.cwd()/"data"

with open(add/"users.json", "r") as file: # Lecture du fichier des utilisateurs et mot de passe.
    file_data = json.load(file)

liste_users = [user.get("name") for user in file_data]  # Liste des utilisateurs.

if st.button("S'inscrire"):  # Test des différentes conditions pour réussir une inscription.
    if new_username in liste_users:
        st.error("Ce nom d'utilisateur existe déjà.")
    elif new_password != confirm_password:
        st.error("Les mots de passe ne correspondent pas.")
    elif len(new_password) < 8:
        st.error("Le mot de passe ne contient pas au moins 8 caractères.")
    elif new_password == new_password.lower():
        st.error("Le mot de passe ne contient pas de lettres majuscules.")
    elif new_password == new_password.upper():
        st.error("Le mot de passe ne contient pas de lettres minuscules.")
    elif re.findall("\d", new_password) == []:
        st.error("Le mot de passe ne contient pas de chiffres.")
    elif re.findall("\W", new_password) == []:
        st.error("Le mot de passe ne contient pas de caractères spéciaux.")
    elif (date.today().year - new_age.year) < 18:
        st.error("Vous n'avez pas 18 ans.")
    else:
        users = {"name" : new_username, "password": hash_password(new_password)}  # Créer le dictionnaire correspondant à un utilisateur unique.
        with open(add/"users.json", "r") as file:
            file_data = json.load(file)
            file_data.append(users)
        with open(add/"users.json", "w") as file:
            json.dump(file_data, file, indent= 4)  # Ajoute dans le fichier json le nouveau membre.

