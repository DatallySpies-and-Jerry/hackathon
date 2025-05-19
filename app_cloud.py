import streamlit as st
from PIL import Image
import time
import os
import sys
import logging
import warnings
import streamlit.components.v1 as components
import datetime

# Packages Lucile
import pandas as pd
import folium
import math
from streamlit_folium import st_folium

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
page = st.sidebar.radio("Direction :", ["📝 Description de la mission", "🗺️ Exploration", "🔎 Déchiffrage des avis", "🕵️ Localisation des suspects"])

# Page de présentation
if page == "📝 Description de la mission":
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
        left_image_path = "jerry_nicolas.png"
        st.image(left_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="image-item">', unsafe_allow_html=True)
        right_image_path = "totallyspies_manon_lucile_manon.png"
        st.image(right_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Autres onglets
elif page == "🗺️ Exploration":
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
    
elif page == "🕵️ Localisation des suspects":
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


    # ----------------------- Début onglet Lucile ----------------------- #

    st.markdown("# 🕵️ Localisation des suspects")

    @st.cache_data
    def load_data():
        reviews = pd.read_csv("cleaning_data/olist_order_reviews_dataset.csv")
        orders = pd.read_csv("cleaning_data/olist_orders_dataset.csv")
        customers = pd.read_csv("cleaning_data/olist_customers_dataset.csv")
        geoloc = pd.read_csv("cleaning_data/olist_geolocation_dataset.csv")
        return reviews, orders, customers, geoloc

    reviews, orders, customers, geoloc = load_data()

    # Fusion
    data = pd.merge(reviews, orders, on="order_id", how="inner")
    data = pd.merge(data, customers, on="customer_id", how="inner")

    # Notes par État
    note_par_region = (
        data.groupby("customer_state")
        .agg(avis_moyen=("review_score", "mean"), nb_avis=("review_score", "count"))
        .reset_index()
    )

    coord_etats = {
        "AC": (-9.97499, -67.8243), "AL": (-9.5713, -36.782), "AM": (-3.119, -60.0217),
        "AP": (0.0349, -51.0694), "BA": (-12.9714, -38.5014), "CE": (-3.7172, -38.5433),
        "DF": (-15.8267, -47.9218), "ES": (-20.3155, -40.3128), "GO": (-16.6864, -49.2643),
        "MA": (-2.5307, -44.3068), "MG": (-19.9167, -43.9345), "MS": (-20.4486, -54.6295),
        "MT": (-12.6819, -56.9211), "PA": (-1.455, -48.503), "PB": (-7.1151, -34.8641),
        "PE": (-8.0476, -34.877), "PI": (-5.0892, -42.8016), "PR": (-25.4284, -49.2733),
        "RJ": (-22.9068, -43.1729), "RN": (-5.7945, -35.211), "RO": (-11.5057, -63.5806),
        "RR": (2.8238, -60.6753), "RS": (-30.0346, -51.2177), "SC": (-27.5954, -48.548),
        "SE": (-10.9472, -37.0731), "SP": (-23.5505, -46.6333), "TO": (-10.2501, -48.3243)
    }

    note_par_region["lat"] = note_par_region["customer_state"].map(lambda x: coord_etats.get(x, (None, None))[0])
    note_par_region["lng"] = note_par_region["customer_state"].map(lambda x: coord_etats.get(x, (None, None))[1])

    def couleur(score):
        if score < 2:
            return "darkred"
        elif score < 3:
            return "red"
        elif score < 4:
            return "orange"
        else:
            return "green"
        
    def get_closest_state(click_lat, click_lng, coord_dict):
        closest = None
        min_dist = float("inf")
        for state, (lat, lng) in coord_dict.items():
            dist = math.sqrt((click_lat - lat)**2 + (click_lng - lng)**2)
            if dist < min_dist:
                min_dist = dist
                closest = state
        return closest

    def get_closest_city(click_lat, click_lng, df_coords):
                    closest = None
                    min_dist = float("inf")
                    for _, row in df_coords.iterrows():
                        dist = math.sqrt((click_lat - row["geolocation_lat"])**2 + (click_lng - row["geolocation_lng"])**2)
                        if dist < min_dist:
                            min_dist = dist
                            closest = row["customer_city"]
                    return closest


    # Carte principale (États)
    carte_etat = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles="CartoDB positron")

    for _, row in note_par_region.iterrows():
        if pd.notna(row["lat"]) and pd.notna(row["lng"]):
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=7 + row["nb_avis"] / 3000,
                color=couleur(row["avis_moyen"]),
                fill=True,
                fill_opacity=0.8,
                popup=row["customer_state"],
                tooltip=f"{row['customer_state']} - {row['avis_moyen']:.2f} ⭐"
            ).add_to(carte_etat)

    # Affichage côte à côte
    col1, col2 = st.columns(2)


    with col1:
        st.markdown("## 🗺️ Carte des avis par régions")
        st.markdown("### 🇧🇷 Brésil")

        col_legend, col_map1 = st.columns([1, 4])

        with col_legend:

            # Légende des couleurs
            st.markdown("**Légende**")
            legend_items = [
                ("darkred", "< 2 ⭐"),
                ("red", "2-3 ⭐"),
                ("orange", "3-4 ⭐"),
                ("green", "≥ 4 ⭐")
            ]

            st.markdown(" ")
            st.markdown("Notes")

            for color, label in legend_items:
                st.markdown(
                    f'<div style="display: flex; align-items: center; margin-bottom: 6px;">'
                    f'<div style="width: 15px; height: 15px; background-color: {color}; '
                    f'border-radius: 50%; margin-right: 10px;"></div>'
                    f'<span>{label}</span></div>',
                    unsafe_allow_html=True
                )

            # Légende des tailles (remplace le SVG par des divs)
            st.markdown(" ")
            st.markdown("Nombre d’avis")

            st.markdown(
                """
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 10px; height: 10px; background-color: #6A0DAD; border-radius: 50%; margin-right: 10px;"></div>
                        <span> ≤ 100 </span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 20px; height: 20px; background-color: #6A0DAD; border-radius: 50%; margin-right: 10px;"></div>
                        <span> 100 - 1 000</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 30px; height: 30px; background-color: #6A0DAD; border-radius: 50%; margin-right: 10px;"></div>
                        <span> > 1000 </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col_map1 :
            map_etat_data = st_folium(carte_etat, width=600, height=500, key="map_etat")

    with col2:
        st.markdown("## 🏙️ Carte des avis par villes")
        carte_ville = None
        map_ville_data = None
        city_clicked = None
        state_clicked = None
        ville_title_displayed = False

        if map_etat_data["last_object_clicked"] is not None:
            click_lat = map_etat_data["last_object_clicked"]["lat"]
            click_lng = map_etat_data["last_object_clicked"]["lng"]

            state_clicked = get_closest_state(click_lat, click_lng, coord_etats)

            st.markdown(f"### 📍 {state_clicked}")

            df_state = data[data["customer_state"] == state_clicked]

            note_ville = (
                df_state.groupby("customer_city")
                .agg(avis_moyen=("review_score", "mean"), nb_avis=("review_score", "count"))
                .reset_index()
            )

            geoloc_villes = (
                geoloc[geoloc["geolocation_state"] == state_clicked]
                .groupby("geolocation_city")[["geolocation_lat", "geolocation_lng"]]
                .mean()
                .reset_index()
                .rename(columns={"geolocation_city": "customer_city"})
            )

            note_ville_coord = pd.merge(note_ville, geoloc_villes, on="customer_city", how="left")

            col_slider, col_map2 = st.columns([1, 4])

            with col_slider:
                st.markdown("**Filtres**")
                # Slider pour filtrer les villes selon le nombre d'avis
                nb_avis_min, nb_avis_max = int(note_ville_coord["nb_avis"].min()), int(note_ville_coord["nb_avis"].max())
                filtre_nb_avis = st.slider(
                    "Nombre d'avis",
                    min_value=nb_avis_min,
                    max_value=nb_avis_max,
                    value=(nb_avis_min, nb_avis_max),
                    step=1
                )

                # Slider pour filtrer selon la note moyenne
                note_min, note_max = float(note_ville_coord["avis_moyen"].min()), float(note_ville_coord["avis_moyen"].max())
                filtre_note = st.slider(
                    "Note moyenne",
                    min_value=0.0,
                    max_value=5.0,
                    value=(note_min, note_max),
                    step=0.1
                )

            with col_map2:
                # Appliquer les deux filtres
                note_ville_coord = note_ville_coord[
                    (note_ville_coord["nb_avis"] >= filtre_nb_avis[0]) &
                    (note_ville_coord["nb_avis"] <= filtre_nb_avis[1]) &
                    (note_ville_coord["avis_moyen"] >= filtre_note[0]) &
                    (note_ville_coord["avis_moyen"] <= filtre_note[1])
                ]

                lat_center, lng_center = coord_etats[state_clicked]
                carte_ville = folium.Map(location=[lat_center, lng_center], zoom_start=6, tiles="CartoDB positron")

                for _, row in note_ville_coord.iterrows():
                    if pd.notna(row["geolocation_lat"]) and pd.notna(row["geolocation_lng"]):
                        folium.CircleMarker(
                            location=[row["geolocation_lat"], row["geolocation_lng"]],
                            radius=4 + row["nb_avis"] / 500,
                            color=couleur(row["avis_moyen"]),
                            fill=True,
                            fill_opacity=0.7,
                            tooltip=f"{row['customer_city']} - {row['avis_moyen']:.2f} ⭐ ({row['nb_avis']} avis)"
                        ).add_to(carte_ville)

                map_ville_data = st_folium(carte_ville, width=600, height=500, key="map_ville")


            if map_ville_data and map_ville_data["last_object_clicked"] is not None:
                click_lat = map_ville_data["last_object_clicked"]["lat"]
                click_lng = map_ville_data["last_object_clicked"]["lng"]

                city_clicked = get_closest_city(click_lat, click_lng, note_ville_coord)

        # Bloc de texte d’instruction
        if not state_clicked:
            st.info("ℹ️ Veuillez cliquer sur une région dans la carte de gauche pour voir les avis par ville.")

    # Affichage du tableau (sous les deux cartes)
    st.markdown("## 📋 Avis par ville")
    if state_clicked and city_clicked:
        st.markdown(f"### 📍 {city_clicked}, {state_clicked}")

        # Création des colonnes pour l'affichage côte à côte
        col1, col2 = st.columns([0.25, 3.75])  # slider à gauche, tableau à droite

        with col1:
            st.markdown("**Filtre**")
            note_min, note_max = int(data["review_score"].min()), int(data["review_score"].max())
            filtre_note = st.slider(
                "Note",
                min_value=note_min,
                max_value=note_max,
                value=(note_min, note_max),
                step=1
            )

        with col2:
            # Filtrage des avis en fonction de la ville, l'état et la note sélectionnée
            avis_ville = data[
                (data["customer_state"] == state_clicked) &
                (data["customer_city"] == city_clicked) &
                (data["review_score"] >= filtre_note[0]) &
                (data["review_score"] <= filtre_note[1])
            ][["review_comment_title", "review_comment_message", "review_score"]].dropna(subset=["review_comment_message"])

            if avis_ville.empty:
                st.info("Aucun avis client disponible pour cette ville avec la note sélectionnée.")
            else:
                st.dataframe(
                    avis_ville.rename(columns={
                        "review_comment_title": "Titre",
                        "review_comment_message": "Commentaire",
                        "review_score": "Note"
                    }),
                    use_container_width=True
                )

    else:
        st.info("ℹ️ Pour afficher le tableau des commentaires, veuillez d'abord cliquer sur une région, puis une ville.")

    # ------------------------ Fin onglet Lucile ------------------------ #
