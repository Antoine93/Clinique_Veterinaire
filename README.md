# Clinique Vétérinaire - Application de Gestion

Application permettant de gérer les clients, animaux, vétérinaires, consultations et médicaments d'une clinique vétérinaire.

## Prérequis

- Python 3.13+
- Système de base de données SQLite (inclus dans Python)

## Installation

1. Cloner le dépôt
```
git clone <url-du-repo>
cd clinique-veterinaire
```

2. Installer les dépendances avec uv
```
uv add tkinter sqlite3  (techniquement déjà inclus avec Python)
uv sync
```

## Démarrage de l'application

```
uv run app.py
```

## Fonctionnalités

- Gestion des propriétaires
- Gestion des animaux
- Gestion des vétérinaires
- Gestion des consultations
- Gestion des médicaments
- Gestion des ordonnances

## Structure de la base de données

L'application utilise SQLite avec les tables suivantes:
- Proprietaire
- Animal
- Veterinaire
- Consultation
- Medicament
- Ordonnance (relation N:N entre Consultation et Medicament)

## Notes de développement

La base de données est automatiquement créée au premier lancement de l'application si elle n'existe pas déjà.
