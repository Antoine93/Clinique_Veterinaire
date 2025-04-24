# Clinique Vétérinaire - Application de Gestion

Application permettant de gérer les clients, animaux, vétérinaires, consultations et médicaments d'une clinique vétérinaire.

## Prérequis

- uv ou pip (gestionnaire de dépendance)
- terminal comme powershell 7.5 pour les cli

*Nous utiliserons uv car plus performant

### Installation de uv

> **Note**: Ouvrir PowerShell en mode administrateur pour Windows ou un terminal pour macOS/Linux.

#### Windows
```bash
# Télécharger et installer uv avec PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux
```bash
# Télécharger et installer uv avec curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Mise en place du projet

> **Note**: Les commandes suivantes doivent être exécutées dans un terminal PowerShell (Windows) ou Bash (macOS/Linux).

1. Cloner le dépôt
```bash
# Naviguer vers un dossier où vous souhaitez créer le projet (ex: Documents)
cd C:\Users\VotreNom\Documents  # Exemple pour Windows
# ou
cd ~/Documents  # Exemple pour macOS/Linux

# Cloner le dépôt dans un dossier nommé "Clinique_Veterinaire"
git clone https://github.com/Antoine93/Clinique_Veterinaire Clinique_Veterinaire
cd Clinique_Veterinaire # Ne pas oublier
```

La commande `git clone https://github.com/Antoine93/Clinique_Veterinaire Clinique_Veterinaire` créera spécifiquement un dossier nommé "Clinique_Veterinaire" contenant le projet, au lieu d'utiliser le nom du dépôt par défaut.

2. Création et activation de l'environnement virtuel
```bash
# S'assurer d'être dans le dossier du projet
# Créer un environnement virtuel (exécuter dans le dossier du projet)
uv venv --python 3.13.1

# Activer l'environnement virtuel
# Sur Windows (PowerShell):
.venv\Scripts\activate
# Sur macOS/Linux (Bash/Zsh):
source .venv/bin/activate

# Vérifier que l'environnement est activé
# Le nom de l'environnement (.venv) devrait apparaître en préfixe du prompt de commande
```

3. Installer les dépendances avec uv
```bash
# S'assurer que l'environnement virtuel est activé (vous devriez voir (.venv) en préfixe)
uv add tkinter sqlite3  # déjà inclus avec Python, juste pour l'exemple
uv sync
```

## Démarrage de l'application
```bash
# S'assurer que l'environnement virtuel est activé
# Se placer dans le répertoire du projet si ce n'est pas déjà fait
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

## Schéma MySQL original

```sql
-- Supprime la base de données si elle existe déjà
DROP DATABASE IF EXISTS projetsessiongr05;
CREATE DATABASE projetsessiongr05;
USE projetsessiongr05;
-- Table Propriétaire
DROP TABLE IF EXISTS Proprietaire;
CREATE TABLE Proprietaire (
    id_proprietaire INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    adresse VARCHAR(255)
);
-- Table Animal
DROP TABLE IF EXISTS Animal;
CREATE TABLE Animal (
    id_animal INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    espece VARCHAR(50) NOT NULL,
    race VARCHAR(50),
    age INT CHECK (age >= 0),
    poids DECIMAL(5,2),
    id_proprietaire INT,
    FOREIGN KEY (id_proprietaire) REFERENCES Proprietaire(id_proprietaire) ON DELETE CASCADE
);
-- Table Vétérinaire
DROP TABLE IF EXISTS Veterinaire;
CREATE TABLE Veterinaire (
    id_veterinaire INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    specialisation VARCHAR(100),
    telephone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
-- Table Consultation
DROP TABLE IF EXISTS Consultation;
CREATE TABLE Consultation (
    id_consultation INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    diagnostic VARCHAR(500) NOT NULL,
    traitement VARCHAR(500),
    id_animal INT NOT NULL,
    id_veterinaire INT NOT NULL,
    FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    FOREIGN KEY (id_veterinaire) REFERENCES Veterinaire(id_veterinaire)
);
-- Table Médicament
DROP TABLE IF EXISTS Medicament;
CREATE TABLE Medicament (
    id_medicament INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    posologie VARCHAR(255)
);
-- Table Ordonnance (relation N:N entre Consultation et Médicament)
DROP TABLE IF EXISTS Ordonnance;
CREATE TABLE Ordonnance (
    id_consultation INT,
    id_medicament INT,
    quantite INT CHECK (quantite > 0),
    PRIMARY KEY (id_consultation, id_medicament),
    FOREIGN KEY (id_consultation) REFERENCES Consultation(id_consultation) ON DELETE CASCADE,
    FOREIGN KEY (id_medicament) REFERENCES Medicament(id_medicament) ON DELETE CASCADE
);
-- Création d'un index pour accélérer la recherche des consultations d'un vétérinaire
CREATE INDEX idx_consultation_veterinaire ON Consultation(id_veterinaire);
```

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
