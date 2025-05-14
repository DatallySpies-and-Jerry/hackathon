import streamlit as st
from PIL import Image
import os

# Configuration de la page
st.set_page_config(
    page_title="Datally Spies & Jerry",
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

# Ajout de CSS personnalisé avec typographie Candice et couleurs violet, rose et jaune
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cabin+Sketch:wght@400;700&display=swap');
    
    * {
        font-family: 'Cabin Sketch', cursive;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cabin Sketch', cursive;
        font-weight: 700;
        color: #6A0DAD; /* Violet */
    }
    
    .stButton button {
        background-color: #FF69B4; /* Rose */
        color: white;
        border: none;
        border-radius: 5px;
    }
    
    .stButton button:hover {
        background-color: #FF1493; /* Rose foncé */
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
    
    /* Stylisation de la barre latérale */
    .sidebar .sidebar-content {
        background-color: #F8F0FF; /* Violet clair */
    }
    
    /* Surcharge des styles Streamlit par défaut */
    .stApp {
        background-color: #FFFACD; /* Jaune pâle */
    }
    
    .stSidebar {
        background-color: #F8F0FF; /* Violet clair */
    }
</style>
""", unsafe_allow_html=True)

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Présentation", "Onglet 1", "Onglet 2", "Onglet 3"])

# Page de présentation
if page == "Présentation":
    # Logo en haut à gauche
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Image principale (les personnages)
    st.markdown('<div class="main-image-container">', unsafe_allow_html=True)
    main_image_path = "totally-spies.png"  # Remplacez par le chemin de votre image
    main_image = load_image(main_image_path)
    if main_image:
        st.image(main_image, width=600)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bulles de dialogue
    st.markdown('<div class="dialogue-container">', unsafe_allow_html=True)
    dialogue1 = "Bienvenue dans notre application Datally Spies & Jerry!"
    dialogue2 = "Explorez les données avec nous et découvrez des informations fascinantes!"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="speech-bubble">{dialogue1}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="speech-bubble">{dialogue2}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Espace pour deux images/GIFs côte à côte
    st.markdown('<div class="side-by-side-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="image-item">', unsafe_allow_html=True)
        left_image_path = "jerry.gif"  # Remplacez par le chemin de votre GIF/image gauche
        st.image(left_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="image-item">', unsafe_allow_html=True)
        right_image_path = "sam-clover-alex.gif"  # Remplacez par le chemin de votre GIF/image droite
        st.image(right_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Autres onglets
elif page == "Onglet 1":
    st.title("Onglet 1")
    st.write("Contenu de l'onglet 1")
    
elif page == "Onglet 2":
    st.title("Onglet 2")
    st.write("Contenu de l'onglet 2")
    
elif page == "Onglet 3":
    st.title("Onglet 3")
    st.write("Contenu de l'onglet 3")