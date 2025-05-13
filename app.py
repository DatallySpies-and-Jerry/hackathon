import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Mon Application Streamlit",
    page_icon="✨",
    layout="wide"
)

# Titre principal
st.title("Mon Application Streamlit")

# Description
st.write("""
Cette application est un exemple simple pour le déploiement.
Vous pourrez la modifier et l'enrichir selon vos besoins.
""")

# Sidebar
with st.sidebar:
    st.header("Options")
    option = st.selectbox(
        "Choisissez une fonctionnalité",
        ["Accueil", "Graphique", "Données"]
    )
    st.write("Sélectionné:", option)

# Contenu principal basé sur l'option choisie
if option == "Accueil":
    st.header("Bienvenue!")
    st.write("Ceci est une application Streamlit de démonstration.")
    
    # Bouton interactif
    if st.button("Cliquez-moi!"):
        st.balloons()
        st.success("Bravo, vous avez cliqué sur le bouton!")

elif option == "Graphique":
    st.header("Démonstration de graphique")
    
    # Création de données aléatoires
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    # Affichage du graphique
    st.line_chart(chart_data)
    
    # Slider pour personnaliser le nombre de lignes
    nb_lignes = st.slider("Nombre de lignes de données à afficher", 5, 20, 10)
    st.write(chart_data.head(nb_lignes))

elif option == "Données":
    st.header("Démonstration de données")
    
    # Création d'un dataframe
    df = pd.DataFrame({
        'Produit': ['A', 'B', 'C', 'D', 'E'],
        'Quantité': [10, 25, 15, 30, 20],
        'Prix': [100, 85, 125, 75, 90]
    })
    
    # Affichage des données
    st.dataframe(df)
    
    # Calcul et affichage de statistiques
    st.subheader("Statistiques")
    st.write(f"Total des produits: {sum(df['Quantité'])}")
    st.write(f"Prix moyen: {df['Prix'].mean():.2f} €")
    
    # Upload de fichier
    st.subheader("Importer vos propres données")
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)
        st.write("Aperçu de vos données:")
        st.dataframe(df_upload.head())

# Footer
st.markdown("---")
st.caption("Créé avec Streamlit • Simple à déployer et à modifier")