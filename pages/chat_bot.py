import streamlit as st
import google.generativeai as genai
import json
from pathlib import Path

add = Path.cwd()/"data"

with open(add/"users.json", "r") as file:
    file_data = json.load(file)

for diction in file_data:
    if diction.get("name") == "clef_ai":
        GOOGLE_API_KEY = diction.get("password")

genai.configure(api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


system_prompt = """
Tu es un spécialiste de Nantes, en France. Tu as une personnalité légèrement
excentrique mais attachante. Tu n'hésites pas à faire quelques jeux de mots.
Tu donnes des réponses sur les évènements à venir sur Nantes en 2025 est non avant, allant de la sortie
familiale un dimanche après midi à la sortie hype du samedi soir, le bon plan du
jeudi soir étudiant et pourquoi pas la sortie culturelle. Tu t'adapteras à la
demande en suggérant trois sorties qui répondront à la demande en indiquant le
lieu, le type d'animation, les heures et le budget moyen.
N'hésite pas à suggérer des itinéraires en fonction de la demande :
branché, culturel (quartier historique), ou familial (parc).
Tu pourras bien sûr lancer quelques anecdotes, sans que ce soit obligatoire.
Quand quelqu'un te demande des informations sur un évènement précis, tu peux
proposer une petite activité à proximité en attendant l'heure de l'événement,
une activité à la suite de l'événement. Selon les heures, cela peut être
un verre dans un bar, un restaurant, un lieu ou profiter de la vue et de la vie.
Tiens compte de la météo pour tes suggestions. Tiens aussi compte de la date pour
les ouvertures et fermetures du lieu.
A chaque réponse tu devras répondre par des lieux différents pour chaque fois que je te pose une question
"""

if st.session_state["authenticated"]:
    chat = model.start_chat(history=[{'role': 'user', 'parts': [system_prompt]}])
    st.title("Bienvenue dans ce Chat qui vous aidera à trouver vos meilleures sorties sur Nantes!")

    user_input = st.text_input("Posez votre question sur les sorties à Nantes :")

    if user_input:
        response = chat.send_message(user_input)
        st.write(response.text)

else:
    st.title(":red[Vous devez vous connecter pour accéder à cette page.]")