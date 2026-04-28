import sqlite3
import pandas as pd

def creation_base(base_chemin, fichiers, req_create, table_name, colonnes):
    connexion = sqlite3.connect(base_chemin)
    # Activer les clés étrangères
    connexion.execute("PRAGMA foreign_keys = ON")   
    # Créer la table si elle n'existe pas
    connexion.execute(req_create)

    for fichier_csv in fichiers:
        try:
            # Lire le header pour vérifier les colonnes sans charger tout le fichier
            df_header = pd.read_csv(fichier_csv, nrows=0)
            if all(col in df_header.columns for col in colonnes):
                # Charger uniquement les colonnes nécessaires
                df = pd.read_csv(fichier_csv, usecols=colonnes)
                # Supprimer les doublons éventuels du DataFrame avant insertion
                df.drop_duplicates(inplace=True)
                # Insérer les données dans SQLite
                # Note: to_sql ne supporte pas nativement "INSERT OR IGNORE". 
                # Si des erreurs de clé primaire surviennent, l'exécution s'arrête ou peut être gérée par bloc.
                df.to_sql(table_name, connexion, if_exists='append', index=False)
                print(f"Données de {fichier_csv} insérées dans {table_name}")
        except Exception as e:
            print(f"Info: {fichier_csv} ignoré ou erreur : {e}")
                
    connexion.close()
    return None, None

chemin = "BaseDeDonnee/base_donnee.db"

DONNEE_GEO = "Donnees/donnees_geo_climatiques.csv"
DONNE_SOCIO = "Donnees/donnees_socio_economiques.csv"
DONNEE_MOJ = "Donnees/mesures_occitanie_journaliere_pollution.csv"

#requetes create et insert

#table region
query_create_region = """
CREATE TABLE IF NOT EXISTS REGIONS (
    reg_code INTEGER PRIMARY KEY,
    reg_nom TEXT
)
"""

query_insert_region = """
INSERT OR IGNORE INTO REGIONS (
    reg_code,reg_nom
) values (:reg_code, :reg_nom)
"""
colonnes_region = ["reg_code","reg_nom"]

#table departement
query_create_departement="""
CREATE TABLE IF NOT EXISTS DEPARTEMENTS (
    dep_code TEXT PRIMARY KEY,
    dep_nom TEXT,
    reg_code INTEGER,
    FOREIGN KEY (reg_code) REFERENCES REGIONS(reg_code)
        ON DELETE CASCADE
)
"""

query_insert_departement = """
INSERT OR IGNORE INTO DEPARTEMENTS (
    dep_code,dep_nom, reg_code
) values (:dep_code, :dep_nom, :reg_code)
"""
colonnes_departement = ["dep_code","dep_nom","reg_code"]

#table commune
query_create_commune="""
CREATE TABLE IF NOT EXISTS COMMUNES (
    code_insee_com TEXT PRIMARY KEY,
    nom_com TEXT,
    dep_code TEXT,
    population INTEGER,
    superficie_km2 REAL,
    densite INTEGER,
    latitude REAL,
    longitude REAL,
    densite_cat TEXT,
    alti_med INTEGER,
    FOREIGN KEY (dep_code) REFERENCES DEPARTEMENTS(dep_code)
        ON DELETE CASCADE
)
"""

query_insert_commune = """
INSERT OR IGNORE INTO COMMUNES (
    code_insee_com, nom_com, dep_code, population, superficie_km2, densite, latitude, longitude, densite_cat, alti_med
) values (:code_insee_com, :nom_com, :dep_code, :population, :superficie_km2, :densite, :latitude, :longitude, :densite_cat, :alti_med)
"""
colonnes_commune = ["code_insee_com", "nom_com", "dep_code", "population", "superficie_km2", "densite", "latitude", "longitude", "densite_cat", "alti_med"]


#table climat_mensuel
query_create_CLIMAT_MENSUEL="""
CREATE TABLE IF NOT EXISTS CLIMAT_MENSUEL (
    code_insee_com TEXT PRIMARY KEY,
    RR_med REAL,
    NBJRR1_med REAL,
    NBJRR5_med REAL,
    NBJRR10_med REAL,
    Tmin_med REAL,
    Tmax_med REAL,
    Tens_vap_med REAL,
    Force_vent_med REAL,
    Insolation_med REAL,
    Rayonnement_med REAL,
    FOREIGN KEY (code_insee_com) REFERENCES COMMUNES(code_insee_com)
        ON DELETE CASCADE
);
"""

query_insert_climat_mensuel = """
INSERT OR IGNORE INTO CLIMAT_MENSUEL (
    code_insee_com,
    RR_med, NBJRR1_med, NBJRR5_med, NBJRR10_med,
    Tmin_med, Tmax_med,
    Tens_vap_med,
    Force_vent_med,
    Insolation_med,
    Rayonnement_med
) VALUES (
    :code_insee_com,
    :RR_med, :NBJRR1_med, :NBJRR5_med, :NBJRR10_med,
    :Tmin_med, :Tmax_med,
    :Tens_vap_med,
    :Force_vent_med,
    :Insolation_med,
    :Rayonnement_med
);

"""
colonnes_climat = [
    "code_insee_com",
    "RR_med", "NBJRR1_med", "NBJRR5_med", "NBJRR10_med",
    "Tmin_med", "Tmax_med",
    "Tens_vap_med",
    "Force_vent_med",
    "Insolation_med",
    "Rayonnement_med"
]

#Table station
query_create_station="""
CREATE TABLE IF NOT EXISTS STATION (
    code_station TEXT PRIMARY KEY,
    nom_station TEXT,
    typologie TEXT,
    influence TEXT,
    code_insee_com TEXT,
    FOREIGN KEY (code_insee_com) REFERENCES COMMUNES(code_insee_com)
        ON DELETE CASCADE
);
"""

query_insert_station="""
INSERT OR IGNORE INTO STATION (
    code_station,
    nom_station,
    typologie,
    influence,
    code_insee_com
) VALUES (
    :code_station,
    :nom_station,
    :typologie,
    :influence,
    :code_insee_com
);


"""
colonnes_station = [
    "code_station",
    "nom_station",
    "typologie",
    "influence",
    "code_insee_com"
]


#Table MESURE_POLLUTION
query_create_MESURE_POLLUTION="""
CREATE TABLE IF NOT EXISTS MESURE_POLLUTION (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    code_station TEXT,
    nom_poll TEXT,
    valeur_poll REAL,
    jour INTEGER,
    mois INTEGER,
    annee INTEGER,
    FOREIGN KEY (code_station) REFERENCES STATION(code_station)
        ON DELETE CASCADE
);
"""

query_insert_MESURE_POLLUTION="""
INSERT INTO MESURE_POLLUTION (
    code_station,
    nom_poll,
    valeur_poll,
    jour,
    mois,
    annee
) VALUES (
    :code_station,
    :nom_poll,
    :valeur_poll,
    :jour,
    :mois,
    :annee
);


"""
colonnes_mesure_pollution = [
    "code_station",
    "nom_poll",
    "valeur_poll",
    "jour",
    "mois",
    "annee"
]


fichiers_csv = [DONNE_SOCIO, DONNEE_GEO, DONNEE_MOJ]

# On crée et remplit toutes les tables
tables_a_creer = [
    (query_create_region, "REGIONS", colonnes_region),
    (query_create_departement, "DEPARTEMENTS", colonnes_departement),
    (query_create_commune, "COMMUNES", colonnes_commune),
    (query_create_CLIMAT_MENSUEL, "CLIMAT_MENSUEL", colonnes_climat),
    (query_create_station, "STATION", colonnes_station),
    (query_create_MESURE_POLLUTION, "MESURE_POLLUTION", colonnes_mesure_pollution)
]

for query, name, cols in tables_a_creer:
    creation_base(chemin, fichiers_csv, query, name, cols)