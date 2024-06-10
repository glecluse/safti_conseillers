# Récensement des conseillers Safti en France

## Description du projet

Ce projet vise à collecter des informations sur tous les conseillers du réseau Safti en France dans un but éducatif. Les données sont extraites à partir du site web de Safti en utilisant Beautiful Soup pour le scraping et Pandas pour le nettoyage et la manipulation des données.

## Fonctionnalités

- **Extraction des données** : Les informations des conseillers Safti sont récupérées à partir du site web officiel de Safti.
  
- **Nettoyage des données** : Les données extraites sont nettoyées pour garantir leur qualité et leur uniformité.
  
- **Génération d'un fichier CSV** : Un fichier CSV est généré, contenant les informations suivantes pour chaque conseiller :
  - Nom
  - Prénom
  - Numéro de téléphone
  - Ville
  - Département
  - Région
  - Lien de la photo de profil
  - Lien du mini-site

## Comment exécuter le projet

1. Assurez-vous d'avoir Python installé sur votre système.
2. Clonez ce dépôt sur votre machine.
3. Installez les dépendances requises
4. pip install -r requirements.txt
5. Une fois l'exécution terminée, un fichier CSV nommé `conseillers_safti.csv` sera généré, contenant les données collectées.

## Avertissement

Ce projet est à but éducatif uniquement. Assurez-vous de respecter les conditions d'utilisation du site web de Safti lors de l'utilisation de ce script pour le scraping.
