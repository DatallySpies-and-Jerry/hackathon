import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import datetime
import pandas as pd
# Packages exploration
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Packages déchiffrage des avis 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import re
from collections import Counter
import plotly.express as px
# Packages localisation des suspects
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
    
    @import url('https://fonts.googleapis.com/css2?family=Chewy&display=swap');

    /* Appliquer partout */
    div[class^="stMarkdown"] * {
        font-family: 'Caveat', cursive;
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
page = st.sidebar.radio("", ["📝 Description de la mission", "🗺️ Exploration", "🔎 Déchiffrage des avis", "🕵️ Localisation des suspects"])

# Page de présentation
if page == "📝 Description de la mission":
    # Logo en haut à gauche
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>Mission e-commerce Brésilien</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "images/DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
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
        left_image_path = "images/jerry_nicolas.png"
        st.image(left_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="image-item">', unsafe_allow_html=True)
        right_image_path = "images/totallyspies_manon_lucile_manon.png"
        st.image(right_image_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Autres onglets
elif page == "🗺️ Exploration":
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>🗺️ Exploration</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "images/DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    ########### nombre de clients totaux à avoir commander sur le site
    df_customers = pd.read_csv("cleaning_data/olist_customers_dataset.csv")
    df_orders = pd.read_csv("cleaning_data/olist_orders_dataset.csv")
    df_orders_items = pd.read_csv("cleaning_data/olist_order_items_dataset.csv")
    df_products = pd.read_csv("cleaning_data/olist_products_dataset.csv")
    df_name = pd.read_csv("cleaning_data/product_category_name_translation.csv")
    df_avis = pd.read_csv("cleaning_data/olist_order_reviews_dataset.csv")

    df_merged_orders = pd.merge(df_orders_items,
                        df_orders,
                        on='order_id',
                        how='left')

    df_final1 = pd.merge(df_merged_orders,
                        df_products,
                        on='product_id',
                        how='left')
    df_final1["product_category_name"] = df_final1["product_category_name"].fillna("other")

    df_final2 = pd.merge(df_final1,
                        df_name,
                        on='product_category_name',
                        how='left')
    df_final2["product_category_name_english"] = df_final2["product_category_name_english"].fillna("other")

    df_final3 = pd.merge(df_final2,
                        df_customers,
                        on='customer_id',
                        how='left')

    df_final3['order_purchase_timestamp'] = pd.to_datetime(df_final3['order_purchase_timestamp'])
    df_final3['year'] = df_final3['order_purchase_timestamp'].dt.year
    # calcul kpi
    nb_commandes = df_final3["order_id"].nunique()
    nb_clients_uniques = df_final3["customer_unique_id"].nunique()
    nb_products = df_final3["product_id"].nunique()
    ca = df_final3['price'].sum()
    ca_formatted = f"{round(ca):,}".replace(",", " ")

    m1, m2, m3, m4, m5, m6 = st.columns((0.5,1,1,1,1,0.5))
    m1.write('')
    m2.metric(label ='Nombre total de clients',value = nb_clients_uniques)
    m3.metric(label ='Nombre total de commandes',value = nb_commandes)
    m4.metric(label = 'Produits disponibles',value = nb_products)
    m5.metric(label = 'Recettes totales R($)',value = str(ca_formatted)+" (R$)")
    m1.write('')

    # # Évolution des ventes mensuelles
    ventes_annuelles = df_final3.groupby("year").agg({"price": "sum"}).reset_index()
    command_annuel = df_final3.groupby("year", as_index=False)["order_id"].nunique()

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # Barres = nombre de commandes (axe Y principal)
    fig1.add_trace(
            go.Bar(
                x=command_annuel["year"],
                y=command_annuel["order_id"],
                name="Nombre de commandes",
                marker_color="#FFD700",            # jaune
                opacity=0.8
            ),
            secondary_y=False,
        )

    # Courbe = chiffre d'affaires (axe Y secondaire)
    fig1.add_trace(
            go.Scatter(
                x=ventes_annuelles["year"],
                y=ventes_annuelles["price"],
                name="Recette (R$)",
                mode="lines+markers",
                line=dict(color="#FF69B4", width=4),
                marker=dict(size=10, color="#FF69B4")
            ),
            secondary_y=True,
        )

    # --- 3. Mise en forme cohérente avec ta charte -------------
    fig1.update_layout(
            title="Tendances du chiffre d'affaire  et nombre de commandes vendues par an",
            plot_bgcolor="#FFFACD",
            paper_bgcolor="#FFFACD",
            font=dict(color="#4B0082", size=16),
            title_font=dict(size=22, color="#4B0082"),
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
            xaxis=dict(
                title="Année",
                linecolor="#4B0082",
                tickfont=dict(color="#4B0082"),
                tickvals=[2016, 2017, 2018],
                ticktext=["2016", "2017", "2018"],
                showgrid=False
            ),
        )

    # Axe Y principal (barres)
    fig1.update_yaxes(
            title_text="Nombre de commandes",
            linecolor="#4B0082",
            tickfont=dict(color="#4B0082"),
            gridcolor="#A9A9A9",
            secondary_y=False
        )

    # Axe Y secondaire (courbe CA)
    fig1.update_yaxes(
            title_text="Chiffres d'affaires (R$)",
            linecolor="#4B0082",
            tickfont=dict(color="#4B0082"),
            showgrid=False,
            secondary_y=True
        )

    # --- 4. Affichage ------------------------------------------
    st.plotly_chart(fig1, use_container_width=True)

    g1, g2 = st.columns((1,1))

    with g1:
        top_cat_revenue = (df_final3.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(10).reset_index())
        fig2 = px.bar(
                top_cat_revenue,
                x='product_category_name_english',
                y='price',
                hover_data={'price': ':.2f'},
                title="Top 10 des catégories en fonction du chiffre d'affaires",
                labels={'price': "Chiffre d'affaire (R$)", 'product_category_name_english': 'Catégorie'},
                color_discrete_sequence=["#FF69B4"])
        fig2.update_traces(text=None)
        fig2.update_layout(title="Top 10 des catégories en fonction du chiffre d'affaires",plot_bgcolor='#FFFACD',paper_bgcolor='#FFFACD',font=dict(color="#4B0082", size=16),
            title_font=dict(size=22, color="#4B0082"),
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),yaxis=dict(tickformat=".2s",gridcolor='lightgray'),xaxis=dict(showgrid=False))
        st.plotly_chart(fig2, use_container_width=True)
    with g2:
        top_cat_quantity = (df_final3.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).head(10).reset_index())
        fig3 = px.bar(
                top_cat_quantity,
                x='product_category_name_english',
                y='order_id', 
                hover_data={'order_id': ':.2f'},
                title="Top 10 des catégories par quantité vendue",
                labels={'order_id': 'Nombre de commandes par catégorie', 'product_category_name_english': 'Catégorie'},
                color_discrete_sequence=["#FF69B4"])
        fig3.update_traces(text=None)
        fig3.update_layout(title="Top 10 des catégories par quantité vendue",plot_bgcolor='#FFFACD',paper_bgcolor='#FFFACD',font=dict(color="#4B0082", size=16),
            title_font=dict(size=22, color="#4B0082"),
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),yaxis=dict(tickformat=".2s",gridcolor='lightgray'),xaxis=dict(showgrid=False))
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
    "<h3 style='color:#4B0082; font-size:22px; font-weight:bold;'>Nombre de clients distincts par région</h3>",
    unsafe_allow_html=True)
    g3, g4 = st.columns((1,2))
    region_summary = df_final3.groupby('customer_state').agg(
    n_commandes=('order_id', 'nunique'),
    n_clients=('customer_unique_id', 'nunique')
    ).reset_index()
    with g3:
        # Affichage du tableau trié par nombre de commandes décroissant
        st.dataframe(region_summary.sort_values(by='n_commandes', ascending=False).style
                    .format({'n_commandes': '{:,}', 'n_clients': '{:,}'}))
    with g4:
        fig = px.bar(region_summary.sort_values(by='n_clients'),
                x='n_clients', y='customer_state',
                orientation='h',
                title=None,
                color='n_clients',
                color_continuous_scale=["#f7c6f7", "#d98bdb", "#a64ac9", "#6a0dad"])
        fig.update_layout(plot_bgcolor='#FFFACD',paper_bgcolor='#FFFACD',font=dict(color="#4B0082", size=16))
        fig.update_yaxes(tickmode='linear')
        st.plotly_chart(fig, use_container_width=True)

    df_avis['review_creation_date'] = pd.to_datetime(df_avis['review_creation_date'])
    df_avis['review_year'] = df_avis['review_creation_date'].dt.year
    score_moyen_par_année = (df_avis.groupby('review_year')['review_score'].mean().reset_index().sort_values(by='review_year', ascending=False))

    score_moyen = df_avis['review_score'].mean()
    score_top3_annees = score_moyen_par_année.head(3)
    st.markdown(
    "<h3 style='color:#4B0082; font-size:22px; font-weight:bold;'>Score moyen global vs Score moyen par année</h3>",
    unsafe_allow_html=True)
    c1,c2,c3,c9,c10 = st.columns([1, 1.5, 1.5, 1.5, 1])
    with c3:
        st.metric(label = 'Score Moyen',value = f"{round(score_moyen,2):.2f} ★")

    c4,c5,c6,c7,c8 = st.columns([1, 1.5, 1.5, 1.5, 1])
    for col, (_, row) in zip([c5,c6,c7], score_top3_annees.iterrows()):
        annee = int(row["review_year"])
        score = row["review_score"]
        delta = score - score_moyen
        col.metric(
            label=f"{annee}",
            value=f"{score:.2f} ★",
            delta=f"{delta:+.2f}",
            delta_color="normal"  # rouge si au-dessus, vert si en-dessous du global
        )
    counts_review = df_avis['review_score'].value_counts().reset_index()
    counts_review.columns = ['review_score', 'count']
    counts_review['percentage'] = counts_review['count'] / counts_review['count'].sum()
    star_labels = {1: '1★', 2: '2★', 3: '3★', 4: '4★', 5: '5★'}
    fig5 = px.bar(
        counts_review,
        x='review_score',
        y='percentage',
        hover_data={'percentage': ':.2f'},
        labels={'percentage': "Pourcentage d'avis", 'review_score': "Note de la commande"},
        title='Distribution des notes attribuées aux commandes',
        color_discrete_sequence=["#FF69B4"])
    fig5.update_traces(text=None)
    fig5.update_layout(title='Distribution des notes attribuées aux commandes',plot_bgcolor='#FFFACD',paper_bgcolor='#FFFACD',font=dict(color="#4B0082", size=16),
            title_font=dict(size=22, color="#4B0082"),yaxis=dict(tickformat=".1f",dtick=0.2,gridcolor='lightgray'),xaxis=dict(
            tickvals=[1, 2, 3, 4, 5],  # valeurs existantes
            ticktext=[star_labels[i] for i in [1, 2, 3, 4, 5]],showgrid=False))
    st.plotly_chart(fig5, use_container_width=True)

    df_final3["order_delivered_customer_date"] = pd.to_datetime(df_final3["order_delivered_customer_date"])
    df_final3["order_estimated_delivery_date"] = pd.to_datetime(df_final3["order_estimated_delivery_date"])
    df_orders_group = df_final3.groupby("order_id", as_index=False).agg({
    "order_delivered_customer_date": "max",  # ou "first", selon cohérence
    "order_estimated_delivery_date": "max"
    })
    df_orders_group["delivery_delay"] = (df_orders_group["order_delivered_customer_date"] - df_orders_group["order_estimated_delivery_date"]).dt.days
    taux_retard = (df_orders_group["delivery_delay"] > 0).mean()
    taux_avance = (df_orders_group["delivery_delay"] < 0).mean()
    taux_normal = (df_orders_group["delivery_delay"] == 0).mean()
    # delai_moyen = df_final3["delivery_delay"].mean()
    # delai_median = df_final3["delivery_delay"].median()

    st.markdown(
    "<h3 style='color:#4B0082; font-size:22px; font-weight:bold;'>Performance logistiques des livraisons</h3>",
    unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Livraison en retard", f"{taux_retard:.1%}")
    col2.metric("Livraison en avance", f"{taux_avance:.1%}")
    col3.metric("Livraison à l'heure", f"{taux_normal:.1%}")

    bins = [-200, -30, -10, -1, 0, 1, 10, 30, 200]
    labels = [
        "Avance >30j",        # (-200, -30]
        "Avance 10-30j",      # (-30, -10]
        "Avance 1-10j",       # (-10, -1]
        "Avance <1j",         # (-1, 0]
        "Retard <1j",         # (0, 1]
        "Retard 1-10j",       # (1, 10]
        "Retard 10-30j",      # (10, 30]
        "Retard >30j"         # (30, 200]
    ]
    df_orders_group["delay_group"] = pd.cut(df_orders_group["delivery_delay"], bins=bins, labels=labels)
    fig = px.bar(df_orders_group["delay_group"].value_counts().sort_index(),
             orientation='h',
             title="Répartition des livraisons selon l'écart d'attentes",
             labels={"value": "Nombre de livraisons", "delay_group": "Délais de livraison"},
             color_discrete_sequence=["#AB63FA"])
    fig.update_layout(title="Répartition des livraisons selon l'écart d'attentes",plot_bgcolor='#FFFACD',paper_bgcolor='#FFFACD',font=dict(color="#4B0082", size=16),
            title_font=dict(size=22, color="#4B0082"))
    st.plotly_chart(fig, use_container_width=True)
    
elif page == "🔎 Déchiffrage des avis":
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>🔎 Déchiffrage des avis</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "images/DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)


    # Palette de couleurs personnalisée violet, rose et jaune
    custom_color_scale = ["#6A0DAD", "#8A2BE2", "#9370DB", "#BA55D3", "#DA70D6", "#EE82EE", "#FF69B4", "#FFB6C1", "#FFD700", "#FFFF00"]

    # Télécharger les ressources NLTK nécessaires
    @st.cache_resource
    def download_nltk_resources():
        nltk.download('stopwords')
        nltk.download('punkt')

    download_nltk_resources()

    # Fonction pour charger les données
    @st.cache_data
    def load_data():
        # Charger les différents fichiers CSV
        orders = pd.read_csv('cleaning_data/olist_orders_dataset.csv')
        order_reviews = pd.read_csv('cleaning_data/olist_order_reviews_dataset.csv')
        order_items = pd.read_csv('cleaning_data/olist_order_items_dataset.csv')
        products = pd.read_csv('cleaning_data/olist_products_dataset.csv')
        customers = pd.read_csv('cleaning_data/olist_customers_dataset.csv')
        sellers = pd.read_csv('cleaning_data/olist_sellers_dataset.csv')
        product_category_translation = pd.read_csv('cleaning_data/product_category_name_translation.csv')
        
        # Fusionner pour avoir toutes les informations nécessaires
        # Joindre les commandes avec les avis
        df = order_reviews.merge(orders, on='order_id', how='left')
        
        # Joindre avec les items pour avoir les produits
        df = df.merge(order_items, on='order_id', how='left')
        
        # Joindre avec les produits pour avoir les catégories
        df = df.merge(products, on='product_id', how='left')
        
        # Joindre avec les clients pour avoir les informations sur les clients
        df = df.merge(customers, on='customer_id', how='left')
        
        # Joindre avec les vendeurs pour avoir les informations sur les vendeurs
        df = df.merge(sellers, on='seller_id', how='left')
        
        # Joindre avec les traductions des catégories
        df = df.merge(product_category_translation, on='product_category_name', how='left')
        
        return df

    # Fonction pour nettoyer le texte
    @st.cache_data
    def clean_text(text):
        if isinstance(text, str):
            # Convertir en minuscules
            text = text.lower()
            # Supprimer les caractères spéciaux et les chiffres
            text = re.sub(r'[^\w\s]', '', text)
            text = re.sub(r'\d+', '', text)
            # Supprimer les espaces supplémentaires
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        return ""

    # Fonction pour obtenir les mots-clés les plus fréquents
    @st.cache_data
    def get_top_words(texts, n=50, min_length=3):
        # Combine all texts
        all_text = ' '.join(texts)
        
        # Tokenize
        words = nltk.word_tokenize(all_text)
        
        # Remove stopwords and short words
        stop_words = set(stopwords.words('portuguese'))
        words = [word for word in words if word.lower() not in stop_words and len(word) >= min_length]
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Return top n words
        return dict(word_freq.most_common(n))

    # Fonction pour créer un nuage de mots
    def create_wordcloud(text_data, title="", colormap='magma', background_color='white'):
        if not text_data:
            return None
        
        combined_text = ' '.join(text_data)
        if not combined_text.strip():
            return None
        
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color=background_color,
            colormap=colormap,
            max_words=100,
            stopwords=set(stopwords.words('portuguese')),
            collocations=True,
            normalize_plurals=False,
            contour_width=3,
            contour_color='#6A0DAD',  # Contour violet
            random_state=42
        ).generate(combined_text)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(title, fontsize=20)
        ax.axis('off')
        
        return fig

    # Fonction pour créer un nuage de mots de n-grammes
    @st.cache_data
    def create_ngram_wordcloud(text_data, n=2, title="", colormap='magma', background_color='white'):
        if not text_data:
            return None
        
        # Tokenize
        tokenized_texts = [nltk.word_tokenize(text) for text in text_data if isinstance(text, str) and text.strip()]
        
        # Flatten the list of tokens
        all_tokens = []
        for tokens in tokenized_texts:
            all_tokens.extend(tokens)
        
        # Create n-grams
        ngrams = list(nltk.ngrams(all_tokens, n))
        ngram_phrases = [' '.join(gram) for gram in ngrams]
        
        # Count n-gram frequencies
        ngram_freq = Counter(ngram_phrases)
        
        # Create a text for WordCloud
        ngram_text = ' '.join([f"{ngram} " * freq for ngram, freq in ngram_freq.items()])
        
        if not ngram_text.strip():
            return None
        
        # Create WordCloud
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color=background_color,
            colormap=colormap,
            max_words=100,
            stopwords=set(),  # We already filtered stopwords when creating n-grams
            collocations=False,  # Already creating our own collocations
            normalize_plurals=False,
            contour_width=3,
            contour_color='#6A0DAD',  # Contour violet
            random_state=42
        ).generate(ngram_text)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(title, fontsize=20)
        ax.axis('off')
        
        return fig

    # Fonction pour catégoriser les scores d'avis
    def categorize_review_score(score):
        if score <= 2:
            return "Négatif"
        elif score == 3:
            return "Neutre"
        else:
            return "Positif"

    # Simuler le chargement des données
    with st.spinner("Chargement des données en cours..."):
        # Charger les données
        df = load_data()
        
        # Préparation des données
        df['sentiment'] = df['review_score'].apply(categorize_review_score)
        df['clean_comment'] = df['review_comment_message'].fillna('').apply(clean_text)
        
        # Extraire l'année et le mois pour le filtrage
        if 'review_creation_date' in df.columns:
            df['review_date'] = pd.to_datetime(df['review_creation_date'])
            df['review_year'] = df['review_date'].dt.year
            df['review_month'] = df['review_date'].dt.month
        else:
            # Colonnes factices si la date n'est pas disponible
            df['review_year'] = 2021
            df['review_month'] = 1

    # Section des filtres
    st.sidebar.title("📋 Filtres d'analyse")

    # Filtres pour le profil utilisateur
    st.sidebar.subheader("Filtres démographiques")

    # Filtres pour les États (limiter à 10 pour éviter la surcharge)
    if 'customer_state' in df.columns:
        available_states = sorted(df['customer_state'].unique())
        selected_states = st.sidebar.multiselect(
            "États",
            options=available_states,
            default=available_states[:5] if len(available_states) > 5 else available_states
        )
        if selected_states:
            df_filtered = df[df['customer_state'].isin(selected_states)]
        else:
            df_filtered = df
    else:
        df_filtered = df

    # Filtres pour les catégories de produits
    if 'product_category_name_english' in df.columns:
        product_categories = sorted(df_filtered['product_category_name_english'].dropna().unique())
        selected_categories = st.sidebar.multiselect(
            "Catégories de produits",
            options=product_categories,
            default=[]
        )
        if selected_categories:
            df_filtered = df_filtered[df_filtered['product_category_name_english'].isin(selected_categories)]

    # Filtres de temps
    st.sidebar.subheader("Filtres temporels")

    # Années
    if 'review_year' in df.columns:
        years = sorted(df_filtered['review_year'].unique())
        selected_years = st.sidebar.multiselect(
            "Années",
            options=years,
            default=years
        )
        if selected_years:
            df_filtered = df_filtered[df_filtered['review_year'].isin(selected_years)]

    # Mois
    if 'review_month' in df.columns:
        months = sorted(df_filtered['review_month'].unique())
        month_names = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
            7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        month_options = [(m, month_names[m]) for m in months]
        selected_months = st.sidebar.multiselect(
            "Mois",
            options=months,
            format_func=lambda x: month_names[x],
            default=months
        )
        if selected_months:
            df_filtered = df_filtered[df_filtered['review_month'].isin(selected_months)]

    # Filtres de sentiment
    st.sidebar.subheader("Filtres de sentiment")
    sentiments = sorted(df_filtered['sentiment'].unique())
    selected_sentiments = st.sidebar.multiselect(
        "Sentiments",
        options=sentiments,
        default=sentiments
    )
    if selected_sentiments:
        df_filtered = df_filtered[df_filtered['sentiment'].isin(selected_sentiments)]

    # Paramètres des nuages de mots
    st.sidebar.subheader("Paramètres des nuages de mots")
    wordcloud_type = st.sidebar.selectbox(
        "Type de nuage de mots",
        options=["Mots simples", "Bigrammes (groupes de 2 mots)", "Trigrammes (groupes de 3 mots)"],
        index=0
    )

    min_word_length = st.sidebar.slider(
        "Longueur minimale des mots",
        min_value=2,
        max_value=10,
        value=3
    )

    # Traduction des commentaires si nécessaire
    comments_to_use = df_filtered['clean_comment'].fillna('')

    # Analyse des données filtrées
    st.markdown("## 📊 Analyse des commentaires")

    # Créer les onglets pour les différentes visualisations
    tab1, tab2, tab3 = st.tabs(["📊 Distribution des sentiments", "☁️ Nuages de mots", "📈 Analyse comparative"])

    with tab1:
        st.markdown("### Distribution des sentiments par catégorie")
        
        # Distribution des sentiments
        sentiment_counts = df_filtered['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Nombre']
        
        # Mapping des couleurs pour les sentiments
        sentiment_colors = {
            "Positif": "#6A0DAD",  # Violet
            "Neutre": "#FF69B4",   # Rose
            "Négatif": "#FFD700"   # Jaune doré
        }
        
        fig = px.pie(sentiment_counts, values='Nombre', names='Sentiment', 
                    title='Distribution des sentiments dans les commentaires',
                    color='Sentiment',
                    color_discrete_map=sentiment_colors,
                    hole=0.4)
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title_text='Répartition des sentiments')
        fig.update_traces(hovertemplate='Sentiment: %{label}<br>Nb commentaires: %{value}<extra></extra>')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution des scores
        score_counts = df_filtered['review_score'].value_counts().sort_index().reset_index()
        score_counts.columns = ['Score', 'Nombre']
        
        fig = px.bar(score_counts, x='Score', y='Nombre', 
                    title='Distribution des scores des avis',
                    color='Score', color_continuous_scale=custom_color_scale)
        fig.update_layout(xaxis_title='Score', yaxis_title='Nombre de commentaires')
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig.update_traces(textfont_size=12)
        fig.update_traces(hovertemplate='Score: %{x}<br>Nb commentaires: %{y}<extra></extra>')
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Nuages de mots par sentiment")
        
        # Filtrer les commentaires par sentiment
        positive_comments = comments_to_use[df_filtered['sentiment'] == 'Positif'].tolist()
        neutral_comments = comments_to_use[df_filtered['sentiment'] == 'Neutre'].tolist()
        negative_comments = comments_to_use[df_filtered['sentiment'] == 'Négatif'].tolist()
        
        # Créer les colonnes pour afficher les nuages de mots
        col1, col2 = st.columns(2)
        
        # Mappings des colormap par sentiment
        positive_colormap = "magma"         # Violets et roses
        negative_colormap = "plasma"        # Violets et jaunes
        neutral_colormap = "RdPu"           # Rouge à violet
        
        with col1:
            st.markdown("#### 💚 Commentaires positifs")
            if positive_comments:
                if wordcloud_type == "Mots simples":
                    fig_positive = create_wordcloud(positive_comments, 
                                                title="Mots les plus fréquents - Avis positifs",
                                                colormap=positive_colormap)
                elif wordcloud_type == "Bigrammes (groupes de 2 mots)":
                    fig_positive = create_ngram_wordcloud(positive_comments, n=2,
                                                        title="Bigrammes les plus fréquents - Avis positifs",
                                                        colormap=positive_colormap)
                else:  # Trigrammes
                    fig_positive = create_ngram_wordcloud(positive_comments, n=3,
                                                        title="Trigrammes les plus fréquents - Avis positifs",
                                                        colormap=positive_colormap)
                
                if fig_positive:
                    st.pyplot(fig_positive)
                else:
                    st.info("Pas assez de données pour générer un nuage de mots.")
            else:
                st.info("Aucun commentaire positif trouvé avec les filtres actuels.")
        
        with col2:
            st.markdown("#### ❤️ Commentaires négatifs")
            if negative_comments:
                if wordcloud_type == "Mots simples":
                    fig_negative = create_wordcloud(negative_comments, 
                                                title="Mots les plus fréquents - Avis négatifs",
                                                colormap=negative_colormap)
                elif wordcloud_type == "Bigrammes (groupes de 2 mots)":
                    fig_negative = create_ngram_wordcloud(negative_comments, n=2,
                                                        title="Bigrammes les plus fréquents - Avis négatifs",
                                                        colormap=negative_colormap)
                else:  # Trigrammes
                    fig_negative = create_ngram_wordcloud(negative_comments, n=3,
                                                        title="Trigrammes les plus fréquents - Avis négatifs",
                                                        colormap=negative_colormap)
                
                if fig_negative:
                    st.pyplot(fig_negative)
                else:
                    st.info("Pas assez de données pour générer un nuage de mots.")
            else:
                st.info("Aucun commentaire négatif trouvé avec les filtres actuels.")
        
        # Afficher les commentaires neutres si disponibles
        if neutral_comments:
            st.markdown("#### 🔵 Commentaires neutres")
            if wordcloud_type == "Mots simples":
                fig_neutral = create_wordcloud(neutral_comments, 
                                            title="Mots les plus fréquents - Avis neutres",
                                            colormap=neutral_colormap)
            elif wordcloud_type == "Bigrammes (groupes de 2 mots)":
                fig_neutral = create_ngram_wordcloud(neutral_comments, n=2,
                                                    title="Bigrammes les plus fréquents - Avis neutres",
                                                    colormap=neutral_colormap)
            else:  # Trigrammes
                fig_neutral = create_ngram_wordcloud(neutral_comments, n=3,
                                                    title="Trigrammes les plus fréquents - Avis neutres",
                                                    colormap=neutral_colormap)
            if fig_neutral:
                st.pyplot(fig_neutral)
            else:
                st.info("Pas assez de données pour générer un nuage de mots neutres.")

    with tab3:
        st.markdown("### Analyse comparative des profils clients")
        
        # Créer une analyse par régions/états
        if 'customer_state' in df_filtered.columns:
            st.write("### Sentiment par État/Région")
            sentiment_by_state = df_filtered.groupby(['customer_state', 'sentiment']).size().reset_index(name='count')
            
            fig = px.bar(sentiment_by_state, x='customer_state', y='count', color='sentiment', 
                        barmode='group', title='Distribution des sentiments par État/Région',
                        color_discrete_sequence=custom_color_scale)
            fig.update_layout(xaxis_title='État/Région', yaxis_title='Nombre de commentaires')
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            fig.update_traces(textfont_size=12)
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            fig.update_traces(hovertemplate='État: %{x}<br>Nb commentaires: %{y}<extra></extra>')
            st.plotly_chart(fig, use_container_width=True)
        
        # Créer une analyse par catégories de produits
        if 'product_category_name_english' in df_filtered.columns:
            st.write("### Sentiment par Catégorie de Produit")
            # Prendre les 10 catégories les plus fréquentes
            top_categories = df_filtered['product_category_name_english'].value_counts().index.tolist()
            df_top_categories = df_filtered[df_filtered['product_category_name_english'].isin(top_categories)]
            
            sentiment_by_category = df_top_categories.groupby(['product_category_name_english', 'sentiment']).size().reset_index(name='count')
            
            fig = px.bar(sentiment_by_category, x='product_category_name_english', y='count', color='sentiment', 
                        barmode='group', title='Distribution des sentiments par catégorie de produit',
                        color_discrete_sequence=custom_color_scale)
            fig.update_layout(xaxis_title='Catégorie de produit', yaxis_title='Nombre de commentaires')
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            fig.update_traces(textfont_size=12)
            fig.update_traces(hovertemplate='Catégorie: %{x}<br>Nb commentaires: %{y}<extra></extra>')
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Score moyen par catégorie
        if 'product_category_name_english' in df_filtered.columns:
            avg_score_by_category = df_filtered.groupby('product_category_name_english')['review_score'].mean().reset_index()
            avg_score_by_category.columns = ['Catégorie', 'Score moyen']
            avg_score_by_category = avg_score_by_category.sort_values('Score moyen', ascending=False)
            
            fig = px.bar(avg_score_by_category, x='Catégorie', y='Score moyen', 
                        title='Score moyen par catégorie de produit',
                        color='Score moyen', color_continuous_scale=custom_color_scale)
            fig.update_layout(xaxis_title='Catégorie de produit', yaxis_title='Score moyen')
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            fig.update_traces(textfont_size=12)
            fig.update_traces(hovertemplate='Catégorie: %{x}<br>Score moyen: %{y}<extra></extra>')
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig, use_container_width=True)


    # Section pour afficher quelques exemples de commentaires
    st.markdown("## 📝 Exemples de commentaires")

    # Sélectionner le sentiment pour voir les exemples
    sentiment_selection = st.selectbox(
        "Sélectionnez le type de commentaires à afficher",
        options=["Positifs", "Neutres", "Négatifs"],
        index=0
    )

    mapping = {"Positifs": "Positif", "Neutres": "Neutre", "Négatifs": "Négatif"}
    filtered_sentiment = df_filtered[df_filtered['sentiment'] == mapping[sentiment_selection]]

    # Sélectionner les colonnes pertinentes pour l'affichage
    if 'translated_comment' in filtered_sentiment.columns:
        comments_to_display = filtered_sentiment[['review_score', 'clean_comment', 'translated_comment']].copy()
        comments_to_display.columns = ['Score', 'Commentaire original', 'Commentaire traduit']
    else:
        comments_to_display = filtered_sentiment[['review_score', 'clean_comment']].copy()
        comments_to_display.columns = ['Score', 'Commentaire']

    # Afficher les premiers commentaires non vides
    non_empty_comments = comments_to_display[comments_to_display.iloc[:, -1].str.len() > 0].head(5)
    if not non_empty_comments.empty:
        st.dataframe(non_empty_comments, use_container_width=True)
    else:
        st.info(f"Aucun commentaire {sentiment_selection.lower()} trouvé avec les filtres actuels.")

    # Footer avec des informations sur l'application
    st.markdown("---")
    st.markdown("""
    Développé avec Streamlit et Python, par Lucile Saillant, Manon Léonardi et Manon Cousin.
    """) 
elif page == "🕵️ Localisation des suspects":
    col1, col2 = st.columns([12, 1])
    with col1:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<h1>🕵️ Localisation des suspects</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_path = "images/DatallySpies_Logo.png"  # Remplacez par le chemin de votre logo
        logo = load_image(logo_path)
        if logo:
            st.image(logo, width=150)
        st.markdown('</div>', unsafe_allow_html=True)

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