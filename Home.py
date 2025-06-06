import streamlit as st
from PIL import Image

# Configurer la page
st.set_page_config(page_title="Optimisation : Localisation & Planification", layout="wide")

# Titre principal
st.title("Problèmes d'Optimisation : Localisation et Planification de Production")
st.write("---")

# Diviser la page en deux colonnes
col1, col2 = st.columns(2)

# Couleurs pour les cadres
pink_bg = "background-color: #FFE4E1; padding: 15px; border-radius: 10px; color: black; min-height: 200px;"
gray_bg = "background-color: #D3D3D3; padding: 15px; border-radius: 10px; color: black; min-height: 200px;"
blue_bg = "background-color: #ADD8E6; padding: 15px; border-radius: 10px; color: black; min-height: 200px;"

# Problème 1 : Localisation des Installations (Colonne 1)
with col1:
    st.markdown("<h2 style='color: #FF69B4;'>Problème de Localisation des Installations</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='{pink_bg}'>"
        "Le problème de localisation des installations est une question d'optimisation largement utilisée dans divers secteurs tels que "
        "la logistique, la gestion de la chaîne d'approvisionnement et la planification des infrastructures. "
        "L'objectif principal est de <strong>trouver les emplacements optimaux</strong> pour construire des installations (usines, entrepôts, etc.), "
        "afin de <strong>minimiser les coûts totaux</strong>, tout en répondant efficacement aux besoins des clients."
        "</div>",
        unsafe_allow_html=True,
    )

    # Ajouter un espace avant l'expander
    st.write("")  # Ligne vide pour espacement
    with st.expander("Afficher les éléments du problème", expanded=False):
        st.markdown(
            f"<div style='{gray_bg}'>"
            "<strong>Clients :</strong>  \n"
            "- Chaque client a une demande spécifique et est situé à un emplacement donné dans un espace bidimensionnel.  \n"
            "- Les clients nécessitent un service efficace depuis une ou plusieurs installations.  \n"
            "\n"
            "<strong>Installations :</strong>  \n"
            "- Plusieurs sites potentiels pour construire des installations (usines, entrepôts, etc.).  \n"
            "- Chaque site a un coût de mise en place associé, qui doit être pris en compte dans les décisions."
            "</div>",
            unsafe_allow_html=True,
        )

    # Ajouter un espace avant l'objectif principal
    st.write("")  # Ligne vide pour espacement
    with st.expander("Afficher l'objectif principal", expanded=False):
        st.markdown(
            f"<div style='{blue_bg}'>"
            "<strong>Quelles installations construire ?</strong>  \n"
            "  Choisir les sites les plus stratégiques parmi les emplacements disponibles.  \n"
            "\n"
            "<strong>Comment affecter les clients ?</strong>  \n"
            "  Minimiser les coûts de transport et les coûts de mise en place des installations."
            "</div>",
            unsafe_allow_html=True,
        )

# Problème 2 : Planification de Production avec Gestion des Ressources (Colonne 2)
with col2:
    st.markdown("<h2 style='color: #87CEEB;'>Problème de Planification de Production</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='{pink_bg}'>"
        "Ce problème est un cas d'optimisation où une usine doit produire différents produits en utilisant un ensemble "
        "de ressources limitées. L'objectif est de <strong>minimiser les coûts totaux</strong> (stockage, production) tout en respectant "
        "les contraintes liées aux ressources, à la maintenance, et à la demande des clients."
        "De plus, il est essentiel d'optimiser l'utilisation des ressources afin d'éviter les gaspillages et de maximiser l'efficacité de la production."
        "</div>",
        unsafe_allow_html=True,
    )

    # Ajouter un espace avant l'expander
    st.write("")  # Ligne vide pour espacement

    with st.expander("Afficher les éléments du problème", expanded=False):
        st.markdown(
            f"<div style='{gray_bg}'>"
            "<strong>Produits :</strong>  \n"
            "- L'usine fabrique des produits différents, chacun ayant une demande spécifique.  \n"
            "- Chaque produit nécessite une quantité définie de temps d'utilisation sur les ressources.  \n"
            "\n"
            "<strong>Ressources :</strong>  \n"
            "- Ressources clés nécessaires pour fabriquer les produits.  \n"
            "- Chaque ressource a une capacité limitée en heures par mois, affectée par des périodes de maintenance."
            "</div>",
            unsafe_allow_html=True,
        )

    # Ajouter un espace avant l'objectif principal
    st.write("")  # Ligne vide pour espacement
    with st.expander("Afficher l'objectif principal", expanded=False):
        st.markdown(
            f"<div style='{blue_bg}'>"
            "<strong>Minimiser les coûts totaux :</strong>  \n"
            "\n"
            "  - Réduire les coûts de stockage inutile tout en garantissant un stock de sécurité.  \n"
            "\n"
            "  - Maximiser l'utilisation efficace des ressources.  \n"
            "\n"
            "  - Éviter les ruptures de stock et répondre à la demande client."
            "</div>",
            unsafe_allow_html=True,
        )

# Ajouter les images côte à côte avec la même taille
col1, col2 = st.columns(2)  # Créer deux colonnes côte à côte pour les images
with col1:
    st.markdown("<h3 style='color: #FF69B4;'>Illustrations</h3>", unsafe_allow_html=True)
    image_location = Image.open("location.png")
    st.image(image_location, caption="Diagramme : Localisation des Installations", use_container_width=True)

with col2:
    st.markdown("<h3 style='color: #87CEEB;'>Illustrations</h3>", unsafe_allow_html=True)
    image_production = Image.open("production.png")
    st.image(image_production, caption="Diagramme : Planification de Production", use_container_width=True)

# Conclusion
st.write("---")
st.success(
    """
    Ces deux problèmes montrent comment l'optimisation mathématique peut être utilisée pour résoudre des défis complexes, 
    allant de la gestion de la logistique à la planification de la production. Avec les bons outils et modèles, 
    il est possible d'améliorer l'efficacité et de réduire les coûts dans divers domaines.
    """
)
