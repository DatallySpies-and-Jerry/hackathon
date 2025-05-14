import streamlit as st
import base64
import time
import pandas as pd
import requests
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import re

# Configuration de la page
st.set_page_config(
    page_title="DatallySpies - E-commerce Brésilien",
    page_icon="🕵️‍♀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URLs des GIFs animés de Totally Spies
gifs = {
    "jerry": "https://tenor.com/bAXPG.gif",
    "spies": "https://tenor.com/XRgg.gif",
    "sam": "https://tenor.com/bG7Yq.gif",
    "clover": "https://tenor.com/bHDpz.gif",
    "alex": "https://tenor.com/bHo6r.gif"
}

# Couleurs des Totally Spies
colors = {
    "sam": "#4CCD00",  # Vert
    "clover": "#FF7070",  # Rose
    "alex": "#FFCF00",  # Jaune
    "jerry": "#3A86FF",  # Bleu
    "bg": "#FFD6EC",  # Fond rose clair
    "title": "#FF1493"  # Rose foncé pour les titres
}

# CSS personnalisé
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');

.main {
    background-color: """ + colors["bg"] + """;
    padding: 20px;
}
.title {
    font-family: 'Bangers', cursive;
    color: """ + colors["title"] + """;
    text-align: center;
    font-size: 3.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    letter-spacing: 2px;
}
.subtitle {
    font-family: 'Comic Neue', cursive;
    color: #333;
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 30px;
}
.speech-bubble {
    position: absolute;
    padding: 15px;
    border-radius: 20px;
    font-family: 'Comic Neue', cursive;
    font-weight: 700;
    color: white;
    max-width: 300px;
    box-shadow: 3px 3px 5px rgba(0,0,0,0.2);
    z-index: 10;
    opacity: 0;
    animation: fadeIn 0.5s forwards;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.jerry-bubble {
    background-color: """ + colors["jerry"] + """;
    left: 250px;
    top: 100px;
}
.jerry-bubble:after {
    content: "";
    position: absolute;
    left: -15px;
    top: 20px;
    border-width: 15px 15px 15px 0;
    border-style: solid;
    border-color: transparent """ + colors["jerry"] + """;
}
.sam-bubble {
    background-color: """ + colors["sam"] + """;
    right: 250px;
    top: 80px;
}
.sam-bubble:after {
    content: "";
    position: absolute;
    right: -15px;
    top: 20px;
    border-width: 15px 0 15px 15px;
    border-style: solid;
    border-color: transparent """ + colors["sam"] + """;
}
.clover-bubble {
    background-color: """ + colors["clover"] + """;
    right: 270px;
    top: 150px;
}
.clover-bubble:after {
    content: "";
    position: absolute;
    right: -15px;
    top: 20px;
    border-width: 15px 0 15px 15px;
    border-style: solid;
    border-color: transparent """ + colors["clover"] + """;
}
.alex-bubble {
    background-color: """ + colors["alex"] + """;
    right: 230px;
    top: 220px;
}
.alex-bubble:after {
    content: "";
    position: absolute;
    right: -15px;
    top: 20px;
    border-width: 15px 0 15px 15px;
    border-style: solid;
    border-color: transparent """ + colors["alex"] + """;
}
.gif-container {
    position: relative;
    margin: 10px;
    display: inline-block;
}
.character-gif {
    border: 5px solid white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
.mission-button {
    font-family: 'Bangers', cursive;
    font-size: 1.5rem;
    background-color: """ + colors["title"] + """;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 30px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: all 0.3s;
    text-align: center;
    display: block;
    margin: 0 auto;
    cursor: pointer;
}
.mission-button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# Titre et sous-titre
st.markdown('<h1 class="title">🕵️‍♀️ DatallySpies 🕵️‍♀️</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">Mission: E-commerce Brésilien</h2>', unsafe_allow_html=True)

# Fonction pour afficher un GIF avec une bulle de dialogue
def show_gif_with_bubble(gif_url, message, bubble_class):
    container = st.empty()
    container.image(gif_url, use_column_width=True)  # Utilise st.image pour afficher le GIF
    container.markdown(f"""
    <div class="speech-bubble {bubble_class}">{message}</div>
    """, unsafe_allow_html=True)
    time.sleep(3)  # Affiche le message pendant 3 secondes
    return container



# Layout principal
col1, col2 = st.columns(2)

# Conteneur pour les GIFs et les bulles
gif_container_jerry = col1.container()
gif_container_spies = col2.container()

# Dialogue animé
dialogue = [
    {"speaker": "jerry", "text": "Bonjour, mesdemoiselles! J'ai une nouvelle mission pour vous.", "gif": gifs["jerry"]},
    {"speaker": "sam", "text": "Quelle est la situation, Jerry?", "gif": gifs["sam"]},
    {"speaker": "jerry", "text": "Nous avons accès à des données d'un site e-commerce brésilien et nous devons analyser les tendances pour améliorer leurs performances.", "gif": gifs["jerry"]},
    {"speaker": "clover", "text": "Des données d'e-commerce? Ça veut dire shopping en ligne, non? Enfin une mission intéressante!", "gif": gifs["clover"]},
    {"speaker": "alex", "text": "Et quelle est la problématique exacte?", "gif": gifs["alex"]},
    {"speaker": "jerry", "text": "Notre principale problématique est: 'Comment optimiser les revenus et la satisfaction client de cette plateforme e-commerce brésilienne?'", "gif": gifs["jerry"]},
    {"speaker": "sam", "text": "Je propose qu'on analyse d'abord les tendances de vente et la saisonnalité pour identifier les périodes clés.", "gif": gifs["sam"]},
    {"speaker": "clover", "text": "Et moi je m'occuperai d'examiner les catégories de produits les plus populaires et leur rentabilité!", "gif": gifs["clover"]},
    {"speaker": "alex", "text": "Je peux me concentrer sur la satisfaction client et les retours d'achats pour voir ce qui pourrait être amélioré.", "gif": gifs["alex"]},
    {"speaker": "jerry", "text": "Excellent plan, mesdemoiselles! N'oubliez pas de créer des visualisations percutantes pour présenter vos résultats.", "gif": gifs["jerry"]},
    {"speaker": "sam", "text": "On va utiliser des graphiques interactifs et des cartes pour montrer les tendances géographiques des ventes!", "gif": gifs["sam"]},
    {"speaker": "jerry", "text": "Parfait! Cette mission est cruciale. Les DatallySpies sont notre meilleure équipe pour résoudre ce mystère des données!", "gif": gifs["jerry"]},
    {"speaker": "clover", "text": "On ne te décevra pas, Jerry! On va transformer ces données en or!", "gif": gifs["clover"]},
    {"speaker": "alex", "text": "À l'attaque des données!", "gif": gifs["alex"]}
]

# Fonction pour afficher le dialogue avec GIFs animés
def display_animated_dialogue():
    # Au début, afficher Jerry d'un côté et les spies de l'autre
    with gif_container_jerry:
        st.markdown(f'<img src="{gifs["jerry"]}" class="character-gif" width="300">', unsafe_allow_html=True)
    
    with gif_container_spies:
        st.markdown(f'<img src="{gifs["spies"]}" class="character-gif" width="400">', unsafe_allow_html=True)
    
    # Attendre un moment avant de commencer le dialogue
    time.sleep(1)
    
    # Conteneur pour le dialogue
    dialogue_container = st.empty()
    
    # Pour chaque message du dialogue
    for i, message in enumerate(dialogue):
        speaker = message["speaker"]
        text = message["text"]
        gif_url = message["gif"]
        
        # Déterminer dans quel conteneur afficher (Jerry à gauche, Spies à droite)
        if speaker == "jerry":
            with gif_container_jerry:
                st.markdown(f"""
                <div class="gif-container">
                    <img src="{gif_url}" class="character-gif" width="300">
                    <div class="speech-bubble jerry-bubble">{text}</div>
                </div>
                """, unsafe_allow_html=True)
            # Effacer l'ancienne image des spies pour éviter l'encombrement
            with gif_container_spies:
                st.empty()
        else:
            # Pour les spies
            with gif_container_spies:
                bubble_class = f"{speaker}-bubble"
                st.markdown(f"""
                <div class="gif-container">
                    <img src="{gif_url}" class="character-gif" width="300">
                    <div class="speech-bubble {bubble_class}">{text}</div>
                </div>
                """, unsafe_allow_html=True)
            # Effacer l'ancien Jerry
            with gif_container_jerry:
                st.empty()
        
        # Pause pour lire le message
        time.sleep(3)

# Bouton pour démarrer l'animation
if st.button("Lancer la mission!", key="mission_button", help="Cliquez pour voir la conversation"):
    with st.spinner("Chargement de la mission..."):
        display_animated_dialogue()

# Bouton pour passer à la page suivante
st.markdown('<br><br>')
if st.button("Continuer vers l'analyse", key="continue_button"):
    st.success("Redirection vers la page d'analyse... (À implémenter)")
    # Ici vous pourriez rediriger vers d'autres pages de votre application

# Footer
st.markdown('---')
st.markdown('<p style="text-align: center; color: gray;">Créé par l\'équipe DatallySpies pour le concours de visualisation de données</p>', unsafe_allow_html=True)