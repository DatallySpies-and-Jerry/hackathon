import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import datetime
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Hackathon Data Visualisation Avisia",
    page_icon="🕵️",
    layout="wide"
)

# Fonction pour charger une image si elle existe
def load_image(image_path):
    try:
        return Image.open(image_path)
    except:
        st.warning(f"Image non trouvée: {image_path}")
        return None

# CSS pour le header fixe et autres styles - méthode plus robuste
st.markdown("""
<style>
    
    /* Typographie et couleurs */
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    
    div[class^="stMarkdown"] h1 {
        font-size: 3em;
        text-align: center;
        margin-bottom: 20px;
        font-family: 'Luckiest Guy', cursive;
        color: transparent;
        -webkit-text-stroke: 2px #4B0082; /* contour violet */
        text-stroke: 2px #4B0082; /* pour compatibilité */
    }
    
    .stButton button {
        background-color: #FF69B4; /* Rose */
        color: white;
        border: none;
        border-radius: 5px;
    }
    
    .stButton button:hover {
        background-color: #FF1493; /* Rose foncé */
        color: white;
    }
    
    .stTextInput input, .stSelectbox, .stMultiselect {
        border: 2px solid #FFD700; /* Jaune */
    }
    
    .logo-container {
        text-align: left;
        padding: 10px;
    }
    
    .main-image-container {
        text-align: center;
        margin: 20px 0;
    }
    
    .dialogue-container {
        background-color: #F8F0FF; /* Violet clair */
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        border: 2px solid #6A0DAD; /* Violet */
    }
    
    .side-by-side-container {
        display: flex;
        justify-content: space-between;
    }
    
    .image-item {
        flex: 1;
        margin: 10px;
        text-align: center;
    }
    
    .speech-bubble {
        position: relative;
        background: #FF69B4; /* Rose */
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        border: 2px solid #6A0DAD; /* Violet */
        color: white;
        font-size: 18px;
    }
    
    .speech-bubble:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 0;
        border: 15px solid transparent;
        border-top-color: #FF69B4; /* Rose */
        border-bottom: 0;
        margin-left: -15px;
        margin-bottom: -15px;
    }

    
    /* Surcharge des styles Streamlit par défaut */
    .stApp {
        background-color: #FFFACD; /* Jaune pâle */
    }
    
    /* Fond de la sidebar */
    .stSidebar {
        background-color: #6A0DAD; /* Violet clair */
        color: white;
    }

    /* Couleur des titres de la sidebar */
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: white;
    }
    .stSidebar text {
        color: white;
    }
    /* Couleur des textes de la sidebar */
    .stSidebar p {
        color: white;
    }
    /* Couleur des liens de la sidebar */
    .stSidebar a {
        color: white;
    }
    /* Couleur des boutons de la sidebar */
    .stSidebar button {
        background-color: #FF69B4; /* Rose */
        color: white;
        border: none;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Présentation", "Chiffres clés", "Réponse à notre problématique"])

# Page de présentation
if page == "Présentation":
    # Logo en haut à gauche
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>Mission e-commerce Brésilien</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialisation des variables de session
    if "dialogue_index" not in st.session_state:
        st.session_state.dialogue_index = 0
        st.session_state.last_update_time = datetime.datetime.now()

    # Liste des dialogues
    dialogues_1 = [
        "Salut Jerry !",
        "Mais comment tu sais ça Jerry ?",
        "Ok Jerry, peut-on se rendre au Brésil pour enquêter ?",
        "Wouhouuuuuh nous allons au Brésil ! A plus Jerry !",
    ]

    dialogues_2 = [
        "Salut les filles, ici Jerry, j'ai une mission pour vous !",
        "Clover, je suis sûr que tes chaussures viennent du site e-commerce Modally Spies, nouveau site à la mode brésilien !",
        "J'ai vu un de tes avis. De nombreux clients se plaignent de ce nouveau site, j'ai besoin de vous pour comprendre qui ose mettre des avis négatifs !",
        "Vos billets vous sont envoyés, vous partez dans 2 heures, n'oubliez pas votre ordinateur, je veux les plus beaux graphiques possibles qui expliquent ce phénomène !",
    ]

    col1, col2, col3 = st.columns([6, 6, 1])

    # Afficher les dialogues jusqu'à l'étape actuelle
    if st.session_state.dialogue_index < len(dialogues_1):
        with col1:
            st.markdown(f'<div class="speech-bubble">{dialogues_2[st.session_state.dialogue_index]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="speech-bubble">{dialogues_1[st.session_state.dialogue_index]}</div>', unsafe_allow_html=True)
        with col3:
            if st.button("➡️", help="Passer au dialogue suivant"):
                st.session_state.dialogue_index += 1
                st.rerun()
    else:
        with col1:
            st.markdown(f'<div class="speech-bubble"></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="speech-bubble"></div>', unsafe_allow_html=True)
        with col3:
            if st.button("🔄", help="Recommencer"):
                st.session_state.dialogue_index = 0
                st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="image-item">', unsafe_allow_html=True)
        left_image_path = "image (2).png"
        st.image(left_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="image-item">', unsafe_allow_html=True)
        right_image_path = "image (1).png"
        st.image(right_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Autres onglets
elif page == "Chiffres clés":
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>Chiffres clés</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    
elif page == "Réponse à notre problématique":
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>Réponse à notre problématique</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    # Ajoutez ici le contenu de la page "Réponse à notre problématique"
    # Import des données :
    payments = pd.read_csv("cleaning_data/olist_order_payments_dataset.csv")
    reviews = pd.read_csv("cleaning_data/olist_order_reviews_dataset.csv")
    orders = pd.read_csv("cleaning_data/olist_orders_dataset.csv")
    items = pd.read_csv("cleaning_data/olist_order_items_dataset.csv")
    geolocations = pd.read_csv("cleaning_data/olist_geolocation_dataset.csv")
    customers = pd.read_csv("cleaning_data/olist_customers_dataset.csv")
    products = pd.read_csv("cleaning_data/olist_products_dataset.csv")
    sellers = pd.read_csv("cleaning_data/olist_sellers_dataset.csv")
    products_categories = pd.read_csv("cleaning_data/olist_product_category_name_translation.csv")
    # Nuage de mots