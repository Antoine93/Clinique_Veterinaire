import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

class ClinicVeterinaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Clinique Vétérinaire")
        self.root.geometry("1000x600")

        # Vérifier si la base de données existe, sinon la créer
        if not os.path.exists('clinique_veterinaire.db'):
            self.creer_base_de_donnees()

        # Créer l'interface
        self.create_widgets()

    def creer_base_de_donnees(self):
        # Connexion à la base de données (la crée si elle n'existe pas)
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()

        # Supprimer les tables si elles existent
        cursor.execute('DROP TABLE IF EXISTS Ordonnance')
        cursor.execute('DROP TABLE IF EXISTS Medicament')
        cursor.execute('DROP TABLE IF EXISTS Consultation')
        cursor.execute('DROP TABLE IF EXISTS Veterinaire')
        cursor.execute('DROP TABLE IF EXISTS Animal')
        cursor.execute('DROP TABLE IF EXISTS Proprietaire')

        # Créer les tables
        cursor.execute('''
        CREATE TABLE Proprietaire (
            id_proprietaire INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            adresse TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE Animal (
            id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            espece TEXT NOT NULL,
            race TEXT,
            age INTEGER CHECK (age >= 0),
            poids REAL,
            id_proprietaire INTEGER,
            FOREIGN KEY (id_proprietaire) REFERENCES Proprietaire (id_proprietaire) ON DELETE CASCADE
        )
        ''')

        cursor.execute('''
        CREATE TABLE Veterinaire (
            id_veterinaire INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            specialisation TEXT,
            telephone TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE Consultation (
            id_consultation INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            diagnostic TEXT NOT NULL,
            traitement TEXT,
            id_animal INTEGER NOT NULL,
            id_veterinaire INTEGER NOT NULL,
            FOREIGN KEY (id_animal) REFERENCES Animal (id_animal),
            FOREIGN KEY (id_veterinaire) REFERENCES Veterinaire (id_veterinaire)
        )
        ''')

        cursor.execute('''
        CREATE TABLE Medicament (
            id_medicament INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            posologie TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE Ordonnance (
            id_consultation INTEGER,
            id_medicament INTEGER,
            quantite INTEGER CHECK (quantite > 0),
            PRIMARY KEY (id_consultation, id_medicament),
            FOREIGN KEY (id_consultation) REFERENCES Consultation (id_consultation) ON DELETE CASCADE,
            FOREIGN KEY (id_medicament) REFERENCES Medicament (id_medicament) ON DELETE CASCADE
        )
        ''')

        # Création d'un index
        cursor.execute('CREATE INDEX idx_consultation_veterinaire ON Consultation(id_veterinaire)')

        # Valider les changements
        conn.commit()
        conn.close()

        print("Base de données créée avec succès!")

    def create_widgets(self):
        # Créer le notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Créer les onglets
        self.tab_proprietaires = ttk.Frame(self.notebook)
        self.tab_animaux = ttk.Frame(self.notebook)
        self.tab_veterinaires = ttk.Frame(self.notebook)
        self.tab_consultations = ttk.Frame(self.notebook)
        self.tab_medicaments = ttk.Frame(self.notebook)
        self.tab_ordonnances = ttk.Frame(self.notebook)

        # Ajouter les onglets au notebook
        self.notebook.add(self.tab_proprietaires, text="Propriétaires")
        self.notebook.add(self.tab_animaux, text="Animaux")
        self.notebook.add(self.tab_veterinaires, text="Vétérinaires")
        self.notebook.add(self.tab_consultations, text="Consultations")
        self.notebook.add(self.tab_medicaments, text="Médicaments")
        self.notebook.add(self.tab_ordonnances, text="Ordonnances")

        # Configurer les onglets
        self.setup_proprietaires_tab()
        self.setup_animaux_tab()
        self.setup_veterinaires_tab()
        self.setup_consultations_tab()
        self.setup_medicaments_tab()
        self.setup_ordonnances_tab()

    def setup_proprietaires_tab(self):
        # Frame pour les entrées
        frame_inputs = ttk.LabelFrame(self.tab_proprietaires, text="Ajouter/Modifier un propriétaire")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # Champs de saisie
        ttk.Label(frame_inputs, text="Nom:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.prop_nom = ttk.Entry(frame_inputs, width=30)
        self.prop_nom.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Prénom:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.prop_prenom = ttk.Entry(frame_inputs, width=30)
        self.prop_prenom.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Téléphone:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.prop_telephone = ttk.Entry(frame_inputs, width=30)
        self.prop_telephone.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Email:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.prop_email = ttk.Entry(frame_inputs, width=30)
        self.prop_email.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Adresse:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.prop_adresse = ttk.Entry(frame_inputs, width=70)
        self.prop_adresse.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        # Variable pour stocker l'ID du propriétaire sélectionné
        self.current_prop_id = None

        # Boutons
        frame_buttons = ttk.Frame(self.tab_proprietaires)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_buttons, text="Ajouter", command=self.add_proprietaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Modifier", command=self.update_proprietaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_proprietaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Effacer champs", command=self.clear_proprietaire_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Rafraîchir", command=self.refresh_proprietaires).pack(side=tk.LEFT, padx=5)

        # Tableau des propriétaires
        frame_table = ttk.LabelFrame(self.tab_proprietaires, text="Liste des propriétaires")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Tableau avec scrollbar
        scroll = ttk.Scrollbar(frame_table)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.proprietaires_table = ttk.Treeview(frame_table, yscrollcommand=scroll.set,
                                                columns=("ID", "Nom", "Prénom", "Téléphone", "Email", "Adresse"),
                                                show="headings")
        self.proprietaires_table.pack(fill="both", expand=True)

        scroll.config(command=self.proprietaires_table.yview)

        # Définir les en-têtes
        self.proprietaires_table.heading("ID", text="ID")
        self.proprietaires_table.heading("Nom", text="Nom")
        self.proprietaires_table.heading("Prénom", text="Prénom")
        self.proprietaires_table.heading("Téléphone", text="Téléphone")
        self.proprietaires_table.heading("Email", text="Email")
        self.proprietaires_table.heading("Adresse", text="Adresse")

        # Définir la largeur des colonnes
        self.proprietaires_table.column("ID", width=50)
        self.proprietaires_table.column("Nom", width=150)
        self.proprietaires_table.column("Prénom", width=150)
        self.proprietaires_table.column("Téléphone", width=150)
        self.proprietaires_table.column("Email", width=200)
        self.proprietaires_table.column("Adresse", width=300)

        # Bind pour la sélection d'une ligne
        self.proprietaires_table.bind("<ButtonRelease-1>", self.select_proprietaire)

        # Charger les données
        self.refresh_proprietaires()

    def setup_animaux_tab(self):
        # Frame pour les entrées
        frame_inputs = ttk.LabelFrame(self.tab_animaux, text="Ajouter/Modifier un animal")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # Champs de saisie
        ttk.Label(frame_inputs, text="Nom:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ani_nom = ttk.Entry(frame_inputs, width=30)
        self.ani_nom.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Espèce:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.ani_espece = ttk.Entry(frame_inputs, width=30)
        self.ani_espece.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Race:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ani_race = ttk.Entry(frame_inputs, width=30)
        self.ani_race.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Âge:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.ani_age = ttk.Entry(frame_inputs, width=30)
        self.ani_age.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Poids (kg):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.ani_poids = ttk.Entry(frame_inputs, width=30)
        self.ani_poids.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Propriétaire:").grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # Combobox pour sélectionner le propriétaire
        self.ani_proprietaire = ttk.Combobox(frame_inputs, width=28)
        self.ani_proprietaire.grid(row=2, column=3, padx=5, pady=5)
        self.update_proprietaires_combobox()

        # Variable pour stocker l'ID de l'animal sélectionné
        self.current_ani_id = None

        # Boutons
        frame_buttons = ttk.Frame(self.tab_animaux)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_buttons, text="Ajouter", command=self.add_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Modifier", command=self.update_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Effacer champs", command=self.clear_animal_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Rafraîchir", command=self.refresh_animaux).pack(side=tk.LEFT, padx=5)

        # Tableau des animaux
        frame_table = ttk.LabelFrame(self.tab_animaux, text="Liste des animaux")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Tableau avec scrollbar
        scroll = ttk.Scrollbar(frame_table)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.animaux_table = ttk.Treeview(frame_table, yscrollcommand=scroll.set,
                                          columns=("ID", "Nom", "Espèce", "Race", "Âge", "Poids", "Propriétaire"),
                                          show="headings")
        self.animaux_table.pack(fill="both", expand=True)

        scroll.config(command=self.animaux_table.yview)

        # Définir les en-têtes
        self.animaux_table.heading("ID", text="ID")
        self.animaux_table.heading("Nom", text="Nom")
        self.animaux_table.heading("Espèce", text="Espèce")
        self.animaux_table.heading("Race", text="Race")
        self.animaux_table.heading("Âge", text="Âge")
        self.animaux_table.heading("Poids", text="Poids (kg)")
        self.animaux_table.heading("Propriétaire", text="Propriétaire")

        # Définir la largeur des colonnes
        self.animaux_table.column("ID", width=50)
        self.animaux_table.column("Nom", width=150)
        self.animaux_table.column("Espèce", width=150)
        self.animaux_table.column("Race", width=150)
        self.animaux_table.column("Âge", width=80)
        self.animaux_table.column("Poids", width=100)
        self.animaux_table.column("Propriétaire", width=200)

        # Bind pour la sélection d'une ligne
        self.animaux_table.bind("<ButtonRelease-1>", self.select_animal)

        # Charger les données
        self.refresh_animaux()

    def setup_veterinaires_tab(self):
        # Frame pour les entrées
        frame_inputs = ttk.LabelFrame(self.tab_veterinaires, text="Ajouter/Modifier un vétérinaire")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # Champs de saisie
        ttk.Label(frame_inputs, text="Nom:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vet_nom = ttk.Entry(frame_inputs, width=30)
        self.vet_nom.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Spécialisation:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.vet_specialisation = ttk.Entry(frame_inputs, width=30)
        self.vet_specialisation.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Téléphone:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.vet_telephone = ttk.Entry(frame_inputs, width=30)
        self.vet_telephone.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Email:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.vet_email = ttk.Entry(frame_inputs, width=30)
        self.vet_email.grid(row=1, column=3, padx=5, pady=5)

        # Variable pour stocker l'ID du vétérinaire sélectionné
        self.current_vet_id = None

        # Boutons
        frame_buttons = ttk.Frame(self.tab_veterinaires)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_buttons, text="Ajouter", command=self.add_veterinaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Modifier", command=self.update_veterinaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_veterinaire).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Effacer champs", command=self.clear_veterinaire_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Rafraîchir", command=self.refresh_veterinaires).pack(side=tk.LEFT, padx=5)

        # Tableau des vétérinaires
        frame_table = ttk.LabelFrame(self.tab_veterinaires, text="Liste des vétérinaires")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Tableau avec scrollbar
        scroll = ttk.Scrollbar(frame_table)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.veterinaires_table = ttk.Treeview(frame_table, yscrollcommand=scroll.set,
                                               columns=("ID", "Nom", "Spécialisation", "Téléphone", "Email"),
                                               show="headings")
        self.veterinaires_table.pack(fill="both", expand=True)

        scroll.config(command=self.veterinaires_table.yview)

        # Définir les en-têtes
        self.veterinaires_table.heading("ID", text="ID")
        self.veterinaires_table.heading("Nom", text="Nom")
        self.veterinaires_table.heading("Spécialisation", text="Spécialisation")
        self.veterinaires_table.heading("Téléphone", text="Téléphone")
        self.veterinaires_table.heading("Email", text="Email")

        # Définir la largeur des colonnes
        self.veterinaires_table.column("ID", width=50)
        self.veterinaires_table.column("Nom", width=200)
        self.veterinaires_table.column("Spécialisation", width=200)
        self.veterinaires_table.column("Téléphone", width=150)
        self.veterinaires_table.column("Email", width=200)

        # Bind pour la sélection d'une ligne
        self.veterinaires_table.bind("<ButtonRelease-1>", self.select_veterinaire)

        # Charger les données
        self.refresh_veterinaires()

    def setup_consultations_tab(self):
        # Frame pour les entrées
        frame_inputs = ttk.LabelFrame(self.tab_consultations, text="Ajouter/Modifier une consultation")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # Champs de saisie
        ttk.Label(frame_inputs, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cons_date = ttk.Entry(frame_inputs, width=30)
        self.cons_date.grid(row=0, column=1, padx=5, pady=5)
        # Date par défaut
        self.cons_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(frame_inputs, text="Animal:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        # Combobox pour sélectionner l'animal
        self.cons_animal = ttk.Combobox(frame_inputs, width=28)
        self.cons_animal.grid(row=0, column=3, padx=5, pady=5)
        self.update_animaux_combobox()

        ttk.Label(frame_inputs, text="Vétérinaire:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        # Combobox pour sélectionner le vétérinaire
        self.cons_veterinaire = ttk.Combobox(frame_inputs, width=28)
        self.cons_veterinaire.grid(row=1, column=1, padx=5, pady=5)
        self.update_veterinaires_combobox()

        ttk.Label(frame_inputs, text="Diagnostic:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.cons_diagnostic = tk.Text(frame_inputs, width=50, height=4)
        self.cons_diagnostic.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Traitement:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.cons_traitement = tk.Text(frame_inputs, width=50, height=4)
        self.cons_traitement.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        # Variable pour stocker l'ID de la consultation sélectionnée
        self.current_cons_id = None

        # Boutons
        frame_buttons = ttk.Frame(self.tab_consultations)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_buttons, text="Ajouter", command=self.add_consultation).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Modifier", command=self.update_consultation).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_consultation).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Effacer champs", command=self.clear_consultation_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Rafraîchir", command=self.refresh_consultations).pack(side=tk.LEFT, padx=5)

        # Tableau des consultations
        frame_table = ttk.LabelFrame(self.tab_consultations, text="Liste des consultations")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Tableau avec scrollbar
        scroll = ttk.Scrollbar(frame_table)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.consultations_table = ttk.Treeview(frame_table, yscrollcommand=scroll.set,
                                               columns=("ID", "Date", "Animal", "Vétérinaire", "Diagnostic", "Traitement"),
                                               show="headings")
        self.consultations_table.pack(fill="both", expand=True)

        scroll.config(command=self.consultations_table.yview)

        # Définir les en-têtes
        self.consultations_table.heading("ID", text="ID")
        self.consultations_table.heading("Date", text="Date")
        self.consultations_table.heading("Animal", text="Animal")
        self.consultations_table.heading("Vétérinaire", text="Vétérinaire")
        self.consultations_table.heading("Diagnostic", text="Diagnostic")
        self.consultations_table.heading("Traitement", text="Traitement")

        # Définir la largeur des colonnes
        self.consultations_table.column("ID", width=50)
        self.consultations_table.column("Date", width=100)
        self.consultations_table.column("Animal", width=150)
        self.consultations_table.column("Vétérinaire", width=150)
        self.consultations_table.column("Diagnostic", width=250)
        self.consultations_table.column("Traitement", width=250)

        # Bind pour la sélection d'une ligne
        self.consultations_table.bind("<ButtonRelease-1>", self.select_consultation)

        # Charger les données
        self.refresh_consultations()

    def setup_medicaments_tab(self):
        # Frame pour les entrées
        frame_inputs = ttk.LabelFrame(self.tab_medicaments, text="Ajouter/Modifier un médicament")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # Champs de saisie
        ttk.Label(frame_inputs, text="Nom:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.med_nom = ttk.Entry(frame_inputs, width=30)
        self.med_nom.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Description:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.med_description = tk.Text(frame_inputs, width=50, height=4)
        self.med_description.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Posologie:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.med_posologie = tk.Text(frame_inputs, width=50, height=4)
        self.med_posologie.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        # Variable pour stocker l'ID du médicament sélectionné
        self.current_med_id = None

        # Boutons
        frame_buttons = ttk.Frame(self.tab_medicaments)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_buttons, text="Ajouter", command=self.add_medicament).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Modifier", command=self.update_medicament).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_medicament).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Effacer champs", command=self.clear_medicament_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Rafraîchir", command=self.refresh_medicaments).pack(side=tk.LEFT, padx=5)

        # Tableau des médicaments
        frame_table = ttk.LabelFrame(self.tab_medicaments, text="Liste des médicaments")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Tableau avec scrollbar
        scroll = ttk.Scrollbar(frame_table)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.medicaments_table = ttk.Treeview(frame_table, yscrollcommand=scroll.set,
                                             columns=("ID", "Nom", "Description", "Posologie"),
                                             show="headings")
        self.medicaments_table.pack(fill="both", expand=True)

        scroll.config(command=self.medicaments_table.yview)

        # Définir les en-têtes
        self.medicaments_table.heading("ID", text="ID")
        self.medicaments_table.heading("Nom", text="Nom")
        self.medicaments_table.heading("Description", text="Description")
        self.medicaments_table.heading("Posologie", text="Posologie")

        # Définir la largeur des colonnes
        self.medicaments_table.column("ID", width=50)
        self.medicaments_table.column("Nom", width=200)
        self.medicaments_table.column("Description", width=300)
        self.medicaments_table.column("Posologie", width=300)

        # Bind pour la sélection d'une ligne
        self.medicaments_table.bind("<ButtonRelease-1>", self.select_medicament)

        # Charger les données
        self.refresh_medicaments()

    def setup_ordonnances_tab(self):
        # Frame pour les entrées
        frame_inputs = ttk.LabelFrame(self.tab_ordonnances, text="Ajouter/Modifier une ordonnance")
        frame_inputs.pack(fill="x", padx=10, pady=10)

        # Champs de saisie
        ttk.Label(frame_inputs, text="Consultation:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Combobox pour sélectionner la consultation
        self.ord_consultation = ttk.Combobox(frame_inputs, width=28)
        self.ord_consultation.grid(row=0, column=1, padx=5, pady=5)
        self.update_consultations_combobox()

        ttk.Label(frame_inputs, text="Médicament:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        # Combobox pour sélectionner le médicament
        self.ord_medicament = ttk.Combobox(frame_inputs, width=28)
        self.ord_medicament.grid(row=0, column=3, padx=5, pady=5)
        self.update_medicaments_combobox()

        ttk.Label(frame_inputs, text="Quantité:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ord_quantite = ttk.Entry(frame_inputs, width=30)
        self.ord_quantite.grid(row=1, column=1, padx=5, pady=5)

        # Variables pour stocker la consultation et le médicament sélectionnés
        self.current_ord_cons_id = None
        self.current_ord_med_id = None

        # Boutons
        frame_buttons = ttk.Frame(self.tab_ordonnances)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_buttons, text="Ajouter", command=self.add_ordonnance).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Modifier", command=self.update_ordonnance).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Supprimer", command=self.delete_ordonnance).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Effacer champs", command=self.clear_ordonnance_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="Rafraîchir", command=self.refresh_ordonnances).pack(side=tk.LEFT, padx=5)

        # Tableau des ordonnances
        frame_table = ttk.LabelFrame(self.tab_ordonnances, text="Liste des ordonnances")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Tableau avec scrollbar
        scroll = ttk.Scrollbar(frame_table)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.ordonnances_table = ttk.Treeview(frame_table, yscrollcommand=scroll.set,
                                             columns=("Consultation", "Date", "Animal", "Médicament", "Quantité"),
                                             show="headings")
        self.ordonnances_table.pack(fill="both", expand=True)

        scroll.config(command=self.ordonnances_table.yview)

        # Définir les en-têtes
        self.ordonnances_table.heading("Consultation", text="ID Consultation")
        self.ordonnances_table.heading("Date", text="Date")
        self.ordonnances_table.heading("Animal", text="Animal")
        self.ordonnances_table.heading("Médicament", text="Médicament")
        self.ordonnances_table.heading("Quantité", text="Quantité")

        # Définir la largeur des colonnes
        self.ordonnances_table.column("Consultation", width=100)
        self.ordonnances_table.column("Date", width=100)
        self.ordonnances_table.column("Animal", width=200)
        self.ordonnances_table.column("Médicament", width=200)
        self.ordonnances_table.column("Quantité", width=100)

        # Bind pour la sélection d'une ligne
        self.ordonnances_table.bind("<ButtonRelease-1>", self.select_ordonnance)

        # Charger les données
        self.refresh_ordonnances()

    # Méthodes pour les propriétaires
    def refresh_proprietaires(self):
        # Effacer le tableau
        for i in self.proprietaires_table.get_children():
            self.proprietaires_table.delete(i)

        # Charger les données
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Proprietaire")
        proprietaires = cursor.fetchall()
        conn.close()

        # Remplir le tableau
        for proprietaire in proprietaires:
            self.proprietaires_table.insert("", "end", values=proprietaire)

    def add_proprietaire(self):
        # Récupérer les valeurs
        nom = self.prop_nom.get()
        prenom = self.prop_prenom.get()
        telephone = self.prop_telephone.get()
        email = self.prop_email.get()
        adresse = self.prop_adresse.get()

        # Vérifier que les champs obligatoires sont remplis
        if not nom or not prenom or not telephone or not email:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Enregistrer dans la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Proprietaire (nom, prenom, telephone, email, adresse)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, prenom, telephone, email, adresse))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Propriétaire ajouté avec succès")

            # Effacer les champs
            self.clear_proprietaire_fields()

            # Rafraîchir le tableau
            self.refresh_proprietaires()

            # Mettre à jour les combobox
            self.update_proprietaires_combobox()

        except sqlite3.IntegrityError:
            # Gestion des erreurs d'intégrité (téléphone ou email déjà existant)
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", "Le téléphone ou l'email existe déjà")
        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def update_proprietaire(self):
        # Vérifier qu'un propriétaire est sélectionné
        if self.current_prop_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un propriétaire à modifier")
            return

        # Récupérer les valeurs
        nom = self.prop_nom.get()
        prenom = self.prop_prenom.get()
        telephone = self.prop_telephone.get()
        email = self.prop_email.get()
        adresse = self.prop_adresse.get()

        # Vérifier que les champs obligatoires sont remplis
        if not nom or not prenom or not telephone or not email:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Mettre à jour la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Proprietaire
                SET nom = ?, prenom = ?, telephone = ?, email = ?, adresse = ?
                WHERE id_proprietaire = ?
            """, (nom, prenom, telephone, email, adresse, self.current_prop_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Propriétaire modifié avec succès")

            # Effacer les champs
            self.clear_proprietaire_fields()

            # Rafraîchir le tableau
            self.refresh_proprietaires()

            # Mettre à jour les combobox
            self.update_proprietaires_combobox()

        except sqlite3.IntegrityError:
            # Gestion des erreurs d'intégrité (téléphone ou email déjà existant)
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", "Le téléphone ou l'email existe déjà")
        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def delete_proprietaire(self):
        # Vérifier qu'un propriétaire est sélectionné
        if self.current_prop_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un propriétaire à supprimer")
            return

        # Demander confirmation
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce propriétaire et tous ses animaux associés?"):
            return

        # Supprimer de la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Proprietaire WHERE id_proprietaire = ?", (self.current_prop_id,))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Propriétaire supprimé avec succès")

            # Effacer les champs
            self.clear_proprietaire_fields()

            # Rafraîchir le tableau
            self.refresh_proprietaires()

            # Mettre à jour les combobox
            self.update_proprietaires_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def select_proprietaire(self, event):
        # Récupérer l'item sélectionné
        selection = self.proprietaires_table.selection()
        if not selection:
            return

        # Récupérer les valeurs
        item = self.proprietaires_table.item(selection[0])
        values = item['values']

        # Stocker l'ID
        self.current_prop_id = values[0]

        # Remplir les champs
        self.prop_nom.delete(0, tk.END)
        self.prop_nom.insert(0, values[1])

        self.prop_prenom.delete(0, tk.END)
        self.prop_prenom.insert(0, values[2])

        self.prop_telephone.delete(0, tk.END)
        self.prop_telephone.insert(0, values[3])

        self.prop_email.delete(0, tk.END)
        self.prop_email.insert(0, values[4])

        self.prop_adresse.delete(0, tk.END)
        if values[5]:
            self.prop_adresse.insert(0, values[5])

    def clear_proprietaire_fields(self):
        # Effacer les champs
        self.prop_nom.delete(0, tk.END)
        self.prop_prenom.delete(0, tk.END)
        self.prop_telephone.delete(0, tk.END)
        self.prop_email.delete(0, tk.END)
        self.prop_adresse.delete(0, tk.END)

        # Réinitialiser l'ID sélectionné
        self.current_prop_id = None

    def update_proprietaires_combobox(self):
        # Charger les propriétaires pour les combobox
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_proprietaire, nom, prenom FROM Proprietaire")
        proprietaires = cursor.fetchall()
        conn.close()

        # Format: "ID - Nom Prénom"
        proprietaires_values = [f"{p[0]} - {p[1]} {p[2]}" for p in proprietaires]

        # Mettre à jour la combobox des propriétaires dans l'onglet Animaux
        self.ani_proprietaire['values'] = proprietaires_values

    # Méthodes pour les animaux
    def refresh_animaux(self):
        # Effacer le tableau
        for i in self.animaux_table.get_children():
            self.animaux_table.delete(i)

        # Charger les données
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id_animal, a.nom, a.espece, a.race, a.age, a.poids,
                   p.nom || ' ' || p.prenom as proprietaire
            FROM Animal a
            LEFT JOIN Proprietaire p ON a.id_proprietaire = p.id_proprietaire
        """)
        animaux = cursor.fetchall()
        conn.close()

        # Remplir le tableau
        for animal in animaux:
            self.animaux_table.insert("", "end", values=animal)

    def add_animal(self):
        # Récupérer les valeurs
        nom = self.ani_nom.get()
        espece = self.ani_espece.get()
        race = self.ani_race.get()
        age = self.ani_age.get()
        poids = self.ani_poids.get()
        proprietaire = self.ani_proprietaire.get()

        # Vérifier que les champs obligatoires sont remplis
        if not nom or not espece:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Extraire l'ID du propriétaire (format: "ID - Nom Prénom")
        id_proprietaire = None
        if proprietaire:
            try:
                id_proprietaire = int(proprietaire.split(' - ')[0])
            except:
                messagebox.showerror("Erreur", "Format de propriétaire invalide")
                return

        # Convertir les types
        try:
            if age:
                age = int(age)
            else:
                age = None

            if poids:
                poids = float(poids)
            else:
                poids = None
        except:
            messagebox.showerror("Erreur", "Format de l'âge ou du poids invalide")
            return

        # Enregistrer dans la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Animal (nom, espece, race, age, poids, id_proprietaire)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, espece, race, age, poids, id_proprietaire))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Animal ajouté avec succès")

            # Effacer les champs
            self.clear_animal_fields()

            # Rafraîchir le tableau
            self.refresh_animaux()

            # Mettre à jour les combobox
            self.update_animaux_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def update_animal(self):
        # Vérifier qu'un animal est sélectionné
        if self.current_ani_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un animal à modifier")
            return

        # Récupérer les valeurs
        nom = self.ani_nom.get()
        espece = self.ani_espece.get()
        race = self.ani_race.get()
        age = self.ani_age.get()
        poids = self.ani_poids.get()
        proprietaire = self.ani_proprietaire.get()

        # Vérifier que les champs obligatoires sont remplis
        if not nom or not espece:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Extraire l'ID du propriétaire (format: "ID - Nom Prénom")
        id_proprietaire = None
        if proprietaire:
            try:
                id_proprietaire = int(proprietaire.split(' - ')[0])
            except:
                messagebox.showerror("Erreur", "Format de propriétaire invalide")
                return

        # Convertir les types
        try:
            if age:
                age = int(age)
            else:
                age = None

            if poids:
                poids = float(poids)
            else:
                poids = None
        except:
            messagebox.showerror("Erreur", "Format de l'âge ou du poids invalide")
            return

        # Mettre à jour la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Animal
                SET nom = ?, espece = ?, race = ?, age = ?, poids = ?, id_proprietaire = ?
                WHERE id_animal = ?
            """, (nom, espece, race, age, poids, id_proprietaire, self.current_ani_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Animal modifié avec succès")

            # Effacer les champs
            self.clear_animal_fields()

            # Rafraîchir le tableau
            self.refresh_animaux()

            # Mettre à jour les combobox
            self.update_animaux_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def delete_animal(self):
        # Vérifier qu'un animal est sélectionné
        if self.current_ani_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un animal à supprimer")
            return

        # Demander confirmation
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet animal et toutes ses consultations associées?"):
            return

        # Supprimer de la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Animal WHERE id_animal = ?", (self.current_ani_id,))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Animal supprimé avec succès")

            # Effacer les champs
            self.clear_animal_fields()

            # Rafraîchir le tableau
            self.refresh_animaux()

            # Mettre à jour les combobox
            self.update_animaux_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def select_animal(self, event):
        # Récupérer l'item sélectionné
        selection = self.animaux_table.selection()
        if not selection:
            return

        # Récupérer les valeurs
        item = self.animaux_table.item(selection[0])
        values = item['values']

        # Stocker l'ID
        self.current_ani_id = values[0]

        # Remplir les champs
        self.ani_nom.delete(0, tk.END)
        self.ani_nom.insert(0, values[1])

        self.ani_espece.delete(0, tk.END)
        self.ani_espece.insert(0, values[2])

        self.ani_race.delete(0, tk.END)
        if values[3]:
            self.ani_race.insert(0, values[3])

        self.ani_age.delete(0, tk.END)
        if values[4]:
            self.ani_age.insert(0, values[4])

        self.ani_poids.delete(0, tk.END)
        if values[5]:
            self.ani_poids.insert(0, values[5])

        # Sélectionner le propriétaire dans la combobox
        if values[6]:
            # Récupérer l'ID du propriétaire
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id_proprietaire FROM Animal WHERE id_animal = ?", (self.current_ani_id,))
            id_proprietaire = cursor.fetchone()[0]
            conn.close()

            # Trouver l'entrée correspondante dans la combobox
            for i, prop in enumerate(self.ani_proprietaire['values']):
                if prop.startswith(f"{id_proprietaire} - "):
                    self.ani_proprietaire.current(i)
                    break

    def clear_animal_fields(self):
        # Effacer les champs
        self.ani_nom.delete(0, tk.END)
        self.ani_espece.delete(0, tk.END)
        self.ani_race.delete(0, tk.END)
        self.ani_age.delete(0, tk.END)
        self.ani_poids.delete(0, tk.END)
        self.ani_proprietaire.set('')

        # Réinitialiser l'ID sélectionné
        self.current_ani_id = None

    def update_animaux_combobox(self):
        # Charger les animaux pour les combobox
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_animal, nom, espece FROM Animal")
        animaux = cursor.fetchall()
        conn.close()

        # Format: "ID - Nom (Espèce)"
        animaux_values = [f"{a[0]} - {a[1]} ({a[2]})" for a in animaux]

        # Mettre à jour la combobox des animaux dans l'onglet Consultations
        self.cons_animal['values'] = animaux_values

    # Méthodes pour les vétérinaires
    def refresh_veterinaires(self):
        # Effacer le tableau
        for i in self.veterinaires_table.get_children():
            self.veterinaires_table.delete(i)

        # Charger les données
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Veterinaire")
        veterinaires = cursor.fetchall()
        conn.close()

        # Remplir le tableau
        for veterinaire in veterinaires:
            self.veterinaires_table.insert("", "end", values=veterinaire)

    def add_veterinaire(self):
        # Récupérer les valeurs
        nom = self.vet_nom.get()
        specialisation = self.vet_specialisation.get()
        telephone = self.vet_telephone.get()
        email = self.vet_email.get()

        # Vérifier que les champs obligatoires sont remplis
        if not nom or not telephone or not email:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Enregistrer dans la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Veterinaire (nom, specialisation, telephone, email)
                VALUES (?, ?, ?, ?)
            """, (nom, specialisation, telephone, email))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Vétérinaire ajouté avec succès")

            # Effacer les champs
            self.clear_veterinaire_fields()

            # Rafraîchir le tableau
            self.refresh_veterinaires()

            # Mettre à jour les combobox
            self.update_veterinaires_combobox()

        except sqlite3.IntegrityError:
            # Gestion des erreurs d'intégrité (téléphone ou email déjà existant)
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", "Le téléphone ou l'email existe déjà")
        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def update_veterinaire(self):
        # Vérifier qu'un vétérinaire est sélectionné
        if self.current_vet_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un vétérinaire à modifier")
            return

        # Récupérer les valeurs
        nom = self.vet_nom.get()
        specialisation = self.vet_specialisation.get()
        telephone = self.vet_telephone.get()
        email = self.vet_email.get()

        # Vérifier que les champs obligatoires sont remplis
        if not nom or not telephone or not email:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Mettre à jour la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Veterinaire
                SET nom = ?, specialisation = ?, telephone = ?, email = ?
                WHERE id_veterinaire = ?
            """, (nom, specialisation, telephone, email, self.current_vet_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Vétérinaire modifié avec succès")

            # Effacer les champs
            self.clear_veterinaire_fields()

            # Rafraîchir le tableau
            self.refresh_veterinaires()

            # Mettre à jour les combobox
            self.update_veterinaires_combobox()

        except sqlite3.IntegrityError:
            # Gestion des erreurs d'intégrité (téléphone ou email déjà existant)
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", "Le téléphone ou l'email existe déjà")
        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def delete_veterinaire(self):
        # Vérifier qu'un vétérinaire est sélectionné
        if self.current_vet_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un vétérinaire à supprimer")
            return

        # Demander confirmation
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce vétérinaire et toutes ses consultations associées?"):
            return

        # Supprimer de la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            # Vérifier s'il y a des consultations associées
            cursor.execute("SELECT COUNT(*) FROM Consultation WHERE id_veterinaire = ?", (self.current_vet_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Il y a des consultations, demander confirmation
                if not messagebox.askyesno("Confirmation", f"Ce vétérinaire a {count} consultation(s) associée(s). Voulez-vous vraiment le supprimer?"):
                    conn.close()
                    return

                # Supprimer les consultations associées
                cursor.execute("DELETE FROM Consultation WHERE id_veterinaire = ?", (self.current_vet_id,))

            # Supprimer le vétérinaire
            cursor.execute("DELETE FROM Veterinaire WHERE id_veterinaire = ?", (self.current_vet_id,))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Vétérinaire supprimé avec succès")

            # Effacer les champs
            self.clear_veterinaire_fields()

            # Rafraîchir les tableaux
            self.refresh_veterinaires()
            self.refresh_consultations()

            # Mettre à jour les combobox
            self.update_veterinaires_combobox()
            self.update_consultations_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def select_veterinaire(self, event):
        # Récupérer l'item sélectionné
        selection = self.veterinaires_table.selection()
        if not selection:
            return

        # Récupérer les valeurs
        item = self.veterinaires_table.item(selection[0])
        values = item['values']

        # Stocker l'ID
        self.current_vet_id = values[0]

        # Remplir les champs
        self.vet_nom.delete(0, tk.END)
        self.vet_nom.insert(0, values[1])

        self.vet_specialisation.delete(0, tk.END)
        if values[2]:
            self.vet_specialisation.insert(0, values[2])

        self.vet_telephone.delete(0, tk.END)
        self.vet_telephone.insert(0, values[3])

        self.vet_email.delete(0, tk.END)
        self.vet_email.insert(0, values[4])

    def clear_veterinaire_fields(self):
        # Effacer les champs
        self.vet_nom.delete(0, tk.END)
        self.vet_specialisation.delete(0, tk.END)
        self.vet_telephone.delete(0, tk.END)
        self.vet_email.delete(0, tk.END)

        # Réinitialiser l'ID sélectionné
        self.current_vet_id = None

    def update_veterinaires_combobox(self):
        # Charger les vétérinaires pour les combobox
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_veterinaire, nom, specialisation FROM Veterinaire")
        veterinaires = cursor.fetchall()
        conn.close()

        # Format: "ID - Nom (Spécialisation)"
        veterinaires_values = []
        for v in veterinaires:
            if v[2]:
                veterinaires_values.append(f"{v[0]} - {v[1]} ({v[2]})")
            else:
                veterinaires_values.append(f"{v[0]} - {v[1]}")

        # Mettre à jour la combobox des vétérinaires dans l'onglet Consultations
        self.cons_veterinaire['values'] = veterinaires_values

    # Méthodes pour les consultations
    def refresh_consultations(self):
        # Effacer le tableau
        for i in self.consultations_table.get_children():
            self.consultations_table.delete(i)

        # Charger les données
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_consultation, c.date,
                   a.nom || ' (' || a.espece || ')' as animal,
                   v.nom as veterinaire,
                   c.diagnostic, c.traitement
            FROM Consultation c
            JOIN Animal a ON c.id_animal = a.id_animal
            JOIN Veterinaire v ON c.id_veterinaire = v.id_veterinaire
            ORDER BY c.date DESC
        """)
        consultations = cursor.fetchall()
        conn.close()

        # Remplir le tableau
        for consultation in consultations:
            self.consultations_table.insert("", "end", values=consultation)

    def add_consultation(self):
        # Récupérer les valeurs
        date = self.cons_date.get()
        animal = self.cons_animal.get()
        veterinaire = self.cons_veterinaire.get()
        diagnostic = self.cons_diagnostic.get("1.0", tk.END).strip()
        traitement = self.cons_traitement.get("1.0", tk.END).strip()

        # Vérifier que les champs obligatoires sont remplis
        if not date or not animal or not veterinaire or not diagnostic:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Extraire les IDs
        try:
            id_animal = int(animal.split(' - ')[0])
            id_veterinaire = int(veterinaire.split(' - ')[0])
        except:
            messagebox.showerror("Erreur", "Format d'animal ou de vétérinaire invalide")
            return

        # Enregistrer dans la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Consultation (date, diagnostic, traitement, id_animal, id_veterinaire)
                VALUES (?, ?, ?, ?, ?)
            """, (date, diagnostic, traitement, id_animal, id_veterinaire))

            # Récupérer l'ID de la consultation ajoutée
            id_consultation = cursor.lastrowid

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Consultation ajoutée avec succès")

            # Effacer les champs
            self.clear_consultation_fields()

            # Rafraîchir le tableau
            self.refresh_consultations()

            # Mettre à jour les combobox
            self.update_consultations_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def update_consultation(self):
        # Vérifier qu'une consultation est sélectionnée
        if self.current_cons_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner une consultation à modifier")
            return

        # Récupérer les valeurs
        date = self.cons_date.get()
        animal = self.cons_animal.get()
        veterinaire = self.cons_veterinaire.get()
        diagnostic = self.cons_diagnostic.get("1.0", tk.END).strip()
        traitement = self.cons_traitement.get("1.0", tk.END).strip()

        # Vérifier que les champs obligatoires sont remplis
        if not date or not animal or not veterinaire or not diagnostic:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        # Extraire les IDs
        try:
            id_animal = int(animal.split(' - ')[0])
            id_veterinaire = int(veterinaire.split(' - ')[0])
        except:
            messagebox.showerror("Erreur", "Format d'animal ou de vétérinaire invalide")
            return

        # Mettre à jour la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Consultation
                SET date = ?, diagnostic = ?, traitement = ?, id_animal = ?, id_veterinaire = ?
                WHERE id_consultation = ?
            """, (date, diagnostic, traitement, id_animal, id_veterinaire, self.current_cons_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Consultation modifiée avec succès")

            # Effacer les champs
            self.clear_consultation_fields()

            # Rafraîchir le tableau
            self.refresh_consultations()

            # Mettre à jour les combobox
            self.update_consultations_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def delete_consultation(self):
        # Vérifier qu'une consultation est sélectionnée
        if self.current_cons_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner une consultation à supprimer")
            return

        # Demander confirmation
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette consultation et toutes ses ordonnances associées?"):
            return

        # Supprimer de la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Consultation WHERE id_consultation = ?", (self.current_cons_id,))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Consultation supprimée avec succès")

            # Effacer les champs
            self.clear_consultation_fields()

            # Rafraîchir les tableaux
            self.refresh_consultations()
            self.refresh_ordonnances()

            # Mettre à jour les combobox
            self.update_consultations_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def select_consultation(self, event):
        # Récupérer l'item sélectionné
        selection = self.consultations_table.selection()
        if not selection:
            return

        # Récupérer les valeurs
        item = self.consultations_table.item(selection[0])
        values = item['values']

        # Stocker l'ID
        self.current_cons_id = values[0]

        # Remplir les champs
        self.cons_date.delete(0, tk.END)
        self.cons_date.insert(0, values[1])

        # Récupérer les IDs pour les combobox
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_animal, id_veterinaire FROM Consultation WHERE id_consultation = ?", (self.current_cons_id,))
        id_animal, id_veterinaire = cursor.fetchone()
        conn.close()

        # Sélectionner l'animal dans la combobox
        for i, ani in enumerate(self.cons_animal['values']):
            if ani.startswith(f"{id_animal} - "):
                self.cons_animal.current(i)
                break

        # Sélectionner le vétérinaire dans la combobox
        for i, vet in enumerate(self.cons_veterinaire['values']):
            if vet.startswith(f"{id_veterinaire} - "):
                self.cons_veterinaire.current(i)
                break

        # Remplir les champs de texte
        self.cons_diagnostic.delete("1.0", tk.END)
        self.cons_diagnostic.insert("1.0", values[4])

        self.cons_traitement.delete("1.0", tk.END)
        if values[5]:
            self.cons_traitement.insert("1.0", values[5])

    def clear_consultation_fields(self):
        # Réinitialiser la date à aujourd'hui
        self.cons_date.delete(0, tk.END)
        self.cons_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Effacer les combobox
        self.cons_animal.set('')
        self.cons_veterinaire.set('')

        # Effacer les champs de texte
        self.cons_diagnostic.delete("1.0", tk.END)
        self.cons_traitement.delete("1.0", tk.END)

        # Réinitialiser l'ID sélectionné
        self.current_cons_id = None

    def update_consultations_combobox(self):
        # Charger les consultations pour les combobox
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_consultation, c.date, a.nom, a.espece
            FROM Consultation c
            JOIN Animal a ON c.id_animal = a.id_animal
            ORDER BY c.date DESC
        """)
        consultations = cursor.fetchall()
        conn.close()

        # Format: "ID - Date - Animal (Espèce)"
        consultations_values = [f"{c[0]} - {c[1]} - {c[2]} ({c[3]})" for c in consultations]

        # Mettre à jour la combobox des consultations dans l'onglet Ordonnances
        self.ord_consultation['values'] = consultations_values

    # Méthodes pour les médicaments
    def refresh_medicaments(self):
        # Effacer le tableau
        for i in self.medicaments_table.get_children():
            self.medicaments_table.delete(i)

        # Charger les données
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicament")
        medicaments = cursor.fetchall()
        conn.close()

        # Remplir le tableau
        for medicament in medicaments:
            self.medicaments_table.insert("", "end", values=medicament)

    def add_medicament(self):
        # Récupérer les valeurs
        nom = self.med_nom.get()
        description = self.med_description.get("1.0", tk.END).strip()
        posologie = self.med_posologie.get("1.0", tk.END).strip()

        # Vérifier que les champs obligatoires sont remplis
        if not nom:
            messagebox.showerror("Erreur", "Veuillez remplir le nom du médicament")
            return

        # Enregistrer dans la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Medicament (nom, description, posologie)
                VALUES (?, ?, ?)
            """, (nom, description, posologie))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Médicament ajouté avec succès")

            # Effacer les champs
            self.clear_medicament_fields()

            # Rafraîchir le tableau
            self.refresh_medicaments()

            # Mettre à jour les combobox
            self.update_medicaments_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def update_medicament(self):
        # Vérifier qu'un médicament est sélectionné
        if self.current_med_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médicament à modifier")
            return

        # Récupérer les valeurs
        nom = self.med_nom.get()
        description = self.med_description.get("1.0", tk.END).strip()
        posologie = self.med_posologie.get("1.0", tk.END).strip()

        # Vérifier que les champs obligatoires sont remplis
        if not nom:
            messagebox.showerror("Erreur", "Veuillez remplir le nom du médicament")
            return

        # Mettre à jour la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Medicament
                SET nom = ?, description = ?, posologie = ?
                WHERE id_medicament = ?
            """, (nom, description, posologie, self.current_med_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Médicament modifié avec succès")

            # Effacer les champs
            self.clear_medicament_fields()

            # Rafraîchir le tableau
            self.refresh_medicaments()

            # Mettre à jour les combobox
            self.update_medicaments_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def delete_medicament(self):
        # Vérifier qu'un médicament est sélectionné
        if self.current_med_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médicament à supprimer")
            return

        # Demander confirmation
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce médicament et toutes ses ordonnances associées?"):
            return

        # Supprimer de la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            # Vérifier s'il y a des ordonnances associées
            cursor.execute("SELECT COUNT(*) FROM Ordonnance WHERE id_medicament = ?", (self.current_med_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Il y a des ordonnances, demander confirmation
                if not messagebox.askyesno("Confirmation", f"Ce médicament est présent dans {count} ordonnance(s). Voulez-vous vraiment le supprimer?"):
                    conn.close()
                    return

            # Supprimer le médicament
            cursor.execute("DELETE FROM Medicament WHERE id_medicament = ?", (self.current_med_id,))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Médicament supprimé avec succès")

            # Effacer les champs
            self.clear_medicament_fields()

            # Rafraîchir les tableaux
            self.refresh_medicaments()
            self.refresh_ordonnances()

            # Mettre à jour les combobox
            self.update_medicaments_combobox()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def select_medicament(self, event):
        # Récupérer l'item sélectionné
        selection = self.medicaments_table.selection()
        if not selection:
            return

        # Récupérer les valeurs
        item = self.medicaments_table.item(selection[0])
        values = item['values']

        # Stocker l'ID
        self.current_med_id = values[0]

        # Remplir les champs
        self.med_nom.delete(0, tk.END)
        self.med_nom.insert(0, values[1])

        self.med_description.delete("1.0", tk.END)
        if values[2]:
            self.med_description.insert("1.0", values[2])

        self.med_posologie.delete("1.0", tk.END)
        if values[3]:
            self.med_posologie.insert("1.0", values[3])

    def clear_medicament_fields(self):
        # Effacer les champs
        self.med_nom.delete(0, tk.END)
        self.med_description.delete("1.0", tk.END)
        self.med_posologie.delete("1.0", tk.END)

        # Réinitialiser l'ID sélectionné
        self.current_med_id = None

    def update_medicaments_combobox(self):
        # Charger les médicaments pour les combobox
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_medicament, nom FROM Medicament")
        medicaments = cursor.fetchall()
        conn.close()

        # Format: "ID - Nom"
        medicaments_values = [f"{m[0]} - {m[1]}" for m in medicaments]

        # Mettre à jour la combobox des médicaments dans l'onglet Ordonnances
        self.ord_medicament['values'] = medicaments_values

    # Méthodes pour les ordonnances
    def refresh_ordonnances(self):
        # Effacer le tableau
        for i in self.ordonnances_table.get_children():
            self.ordonnances_table.delete(i)

        # Charger les données
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.id_consultation, c.date, a.nom, m.nom, o.quantite
            FROM Ordonnance o
            JOIN Consultation c ON o.id_consultation = c.id_consultation
            JOIN Animal a ON c.id_animal = a.id_animal
            JOIN Medicament m ON o.id_medicament = m.id_medicament
            ORDER BY c.date DESC
        """)
        ordonnances = cursor.fetchall()
        conn.close()

        # Remplir le tableau
        for ordonnance in ordonnances:
            self.ordonnances_table.insert("", "end", values=ordonnance)

    def add_ordonnance(self):
        # Récupérer les valeurs
        consultation = self.ord_consultation.get()
        medicament = self.ord_medicament.get()
        quantite = self.ord_quantite.get()

        # Vérifier que les champs obligatoires sont remplis
        if not consultation or not medicament or not quantite:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        # Extraire les IDs
        try:
            id_consultation = int(consultation.split(' - ')[0])
            id_medicament = int(medicament.split(' - ')[0])
            quantite = int(quantite)

            if quantite <= 0:
                messagebox.showerror("Erreur", "La quantité doit être supérieure à 0")
                return
        except:
            messagebox.showerror("Erreur", "Format de consultation, de médicament ou de quantité invalide")
            return

        # Enregistrer dans la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()

            # Vérifier si l'ordonnance existe déjà
            cursor.execute("""
                SELECT COUNT(*) FROM Ordonnance
                WHERE id_consultation = ? AND id_medicament = ?
            """, (id_consultation, id_medicament))
            count = cursor.fetchone()[0]

            if count > 0:
                # L'ordonnance existe déjà, demander confirmation pour la mise à jour
                if not messagebox.askyesno("Confirmation", "Cette ordonnance existe déjà. Voulez-vous mettre à jour la quantité?"):
                    conn.close()
                    return

                # Mettre à jour l'ordonnance
                cursor.execute("""
                    UPDATE Ordonnance
                    SET quantite = ?
                    WHERE id_consultation = ? AND id_medicament = ?
                """, (quantite, id_consultation, id_medicament))
            else:
                # Ajouter une nouvelle ordonnance
                cursor.execute("""
                    INSERT INTO Ordonnance (id_consultation, id_medicament, quantite)
                    VALUES (?, ?, ?)
                """, (id_consultation, id_medicament, quantite))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Ordonnance ajoutée avec succès")

            # Effacer les champs
            self.clear_ordonnance_fields()

            # Rafraîchir le tableau
            self.refresh_ordonnances()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def update_ordonnance(self):
        # Vérifier qu'une ordonnance est sélectionnée
        if self.current_ord_cons_id is None or self.current_ord_med_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner une ordonnance à modifier")
            return

        # Récupérer les valeurs
        quantite = self.ord_quantite.get()

        # Vérifier que les champs obligatoires sont remplis
        if not quantite:
            messagebox.showerror("Erreur", "Veuillez remplir la quantité")
            return

        # Convertir la quantité
        try:
            quantite = int(quantite)

            if quantite <= 0:
                messagebox.showerror("Erreur", "La quantité doit être supérieure à 0")
                return
        except:
            messagebox.showerror("Erreur", "Format de quantité invalide")
            return

        # Mettre à jour la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Ordonnance
                SET quantite = ?
                WHERE id_consultation = ? AND id_medicament = ?
            """, (quantite, self.current_ord_cons_id, self.current_ord_med_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Ordonnance modifiée avec succès")

            # Effacer les champs
            self.clear_ordonnance_fields()

            # Rafraîchir le tableau
            self.refresh_ordonnances()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def delete_ordonnance(self):
        # Vérifier qu'une ordonnance est sélectionnée
        if self.current_ord_cons_id is None or self.current_ord_med_id is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner une ordonnance à supprimer")
            return

        # Demander confirmation
        if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette ordonnance?"):
            return

        # Supprimer de la base de données
        try:
            conn = sqlite3.connect('clinique_veterinaire.db')
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Ordonnance
                WHERE id_consultation = ? AND id_medicament = ?
            """, (self.current_ord_cons_id, self.current_ord_med_id))

            # Utilisation d'instruction TCL pour valider la transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Succès", "Ordonnance supprimée avec succès")

            # Effacer les champs
            self.clear_ordonnance_fields()

            # Rafraîchir le tableau
            self.refresh_ordonnances()

        except Exception as e:
            conn.rollback()  # Utilisation d'instruction TCL pour annuler la transaction
            conn.close()
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

    def select_ordonnance(self, event):
        # Récupérer l'item sélectionné
        selection = self.ordonnances_table.selection()
        if not selection:
            return

        # Récupérer les valeurs
        item = self.ordonnances_table.item(selection[0])
        values = item['values']

        # Stocker les IDs
        self.current_ord_cons_id = values[0]

        # Récupérer l'ID du médicament
        conn = sqlite3.connect('clinique_veterinaire.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_medicament
            FROM Ordonnance
            WHERE id_consultation = ? AND id_medicament IN (
                SELECT id_medicament FROM Medicament WHERE nom = ?
            )
        """, (self.current_ord_cons_id, values[3]))
        self.current_ord_med_id = cursor.fetchone()[0]
        conn.close()

        # Sélectionner la consultation dans la combobox
        for i, cons in enumerate(self.ord_consultation['values']):
            if cons.startswith(f"{self.current_ord_cons_id} - "):
                self.ord_consultation.current(i)
                break

        # Sélectionner le médicament dans la combobox
        for i, med in enumerate(self.ord_medicament['values']):
            if med.startswith(f"{self.current_ord_med_id} - "):
                self.ord_medicament.current(i)
                break

        # Remplir le champ quantité
        self.ord_quantite.delete(0, tk.END)
        self.ord_quantite.insert(0, values[4])

    def clear_ordonnance_fields(self):
        # Effacer les champs
        self.ord_consultation.set('')
        self.ord_medicament.set('')
        self.ord_quantite.delete(0, tk.END)

        # Réinitialiser les IDs sélectionnés
        self.current_ord_cons_id = None
        self.current_ord_med_id = None


# Code principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicVeterinaireApp(root)
    root.mainloop()
