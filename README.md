# Description du projet

Ce projet est un scraper web automatisé développé en Python, utilisant **Selenium** et **Chromium** en mode headless pour rechercher des annonces de logements dans une ville donnée sur le site **Trouver un Logement (lescrous.fr)**. Il permet d'extraire des informations telles que le nom, l'adresse, la surface et le prix des logements disponibles.

## Fonctionnalités principales
- Recherche automatisée des logements en fonction de la ville saisie par l'utilisateur.
- Récupération et affichage des informations sur les logements (nom, adresse, surface, prix).
- Utilisation de **Selenium** pour interagir avec le site web et récupérer les données en toute autonomie.
- Fonctionnement en mode **headless**, sans interface graphique, idéal pour un déploiement en environnement **Docker**.

## Technologies utilisées
- **Python**
- **Selenium** pour l'automatisation du navigateur
- **Chromium** et **Chromedriver** pour l'exécution des tests
- **Docker** pour la conteneurisation de l'application

## Installation
1. Clonez ce repository.
2. Construisez l'image Docker avec :
   ```bash
   docker build -t logement-scraper .

### Before running :  
1. Create a .env file
2. add this line to it : DISCORD_TOKEN = 'your_discord_token_here'  

## Run :
   ```bash
   docker run -it logement-scraper .

