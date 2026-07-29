
# Snowflake Retail Analytics

## Présentation

Ce projet met en place une plateforme analytique dans Snowflake pour une entreprise de retail présente en France, en Allemagne et au Maroc.

L’objectif est de centraliser les données de ventes, de les transformer selon une architecture Bronze, Silver et Gold, puis de les exposer dans un dashboard Streamlit.

## Architecture

Le projet suit l’architecture suivante :

Bronze → Silver → Gold → Streamlit

## Technologies

- Snowflake
- SQL
- Streamlit
- Git
- GitHub

## Fonctionnalités

- Ingestion et nettoyage des données
- Création de tables analytiques Gold
- Row Access Policy par pays
- Masquage des données sensibles
- Automatisation avec Streams et Tasks
- Dashboard Streamlit

## Structure du projet

```text
snowflake-retail-analytics/
├── sql/
├── streamlit/
├── images/
├── README.md
└── .gitignore


