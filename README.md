# Clinique Vétérinaire - Application de Gestion

Application permettant de gérer les clients, animaux, vétérinaires, consultations et médicaments d'une clinique vétérinaire.

## Prérequis

- Python 3.13+
- Système de base de données SQLite (inclus dans Python)

## Installation

1. Cloner le dépôt
```
git clone https://github.com/Antoine93/Clinique_Veterinaire
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

### Table Proprietaire
- `id_proprietaire` INTEGER PRIMARY KEY AUTOINCREMENT
- `nom` TEXT NOT NULL
- `prenom` TEXT NOT NULL
- `telephone` TEXT UNIQUE NOT NULL
- `email` TEXT UNIQUE NOT NULL
- `adresse` TEXT

### Table Animal
- `id_animal` INTEGER PRIMARY KEY AUTOINCREMENT
- `nom` TEXT NOT NULL
- `espece` TEXT NOT NULL
- `race` TEXT
- `age` INTEGER CHECK (age >= 0)
- `poids` REAL
- `id_proprietaire` INTEGER (clé étrangère vers Proprietaire)

### Table Veterinaire
- `id_veterinaire` INTEGER PRIMARY KEY AUTOINCREMENT
- `nom` TEXT NOT NULL
- `specialisation` TEXT
- `telephone` TEXT UNIQUE NOT NULL
- `email` TEXT UNIQUE NOT NULL

### Table Consultation
- `id_consultation` INTEGER PRIMARY KEY AUTOINCREMENT
- `date` TEXT NOT NULL
- `diagnostic` TEXT NOT NULL
- `traitement` TEXT
- `id_animal` INTEGER NOT NULL (clé étrangère vers Animal)
- `id_veterinaire` INTEGER NOT NULL (clé étrangère vers Veterinaire)
- Index sur `id_veterinaire` pour optimiser les recherches

### Table Medicament
- `id_medicament` INTEGER PRIMARY KEY AUTOINCREMENT
- `nom` TEXT NOT NULL
- `description` TEXT
- `posologie` TEXT

### Table Ordonnance
- `id_consultation` INTEGER (clé étrangère vers Consultation)
- `id_medicament` INTEGER (clé étrangère vers Medicament)
- `quantite` INTEGER CHECK (quantite > 0)
- Clé primaire composée de (`id_consultation`, `id_medicament`)

## Particularités SQLite vs MySQL

- `AUTO_INCREMENT` (MySQL) est remplacé par `AUTOINCREMENT` (SQLite)
- Types de données:
  - `VARCHAR` (MySQL) → `TEXT` (SQLite)
  - `DECIMAL(5,2)` (MySQL) → `REAL` (SQLite)
  - `DATE` (MySQL) → `TEXT` (SQLite) au format "YYYY-MM-DD"
- SQLite utilise la syntaxe de contraintes légèrement différente
- Le support des clés étrangères doit être explicitement activé dans SQLite

## Notes de développement

- La base de données est automatiquement créée au premier lancement de l'application si elle n'existe pas déjà
- L'application implémente des transactions avec COMMIT et ROLLBACK pour garantir l'intégrité des données
- Les relations CASCADE sont préservées pour maintenir la cohérence des données (par exemple, supprimer un propriétaire supprime aussi ses animaux)
