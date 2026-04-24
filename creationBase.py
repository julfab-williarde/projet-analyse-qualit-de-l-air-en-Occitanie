import sqlite3
import csv

def colonnes_presentes(reader, colonnes):
    return all(col in reader.fieldnames for col in colonnes)

def creation_base(base_chemin, fichiers, req_create, req_insert, colonnes):
    connexion = sqlite3.connect(base_chemin)
    curs = connexion.cursor()
    curs.execute("PRAGMA foreign_keys = ON")   
    curs.execute(req_create)

    for fichier_csv in fichiers:
        with open(fichier_csv, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if not colonnes_presentes(reader, colonnes):
                continue

            for row in reader:
                curs.execute(req_insert, row)
                
    connexion.commit()
    return connexion, curs

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
conn, cur = creation_base(chemin, fichiers_csv, query_create_MESURE_POLLUTION, query_insert_MESURE_POLLUTION, colonnes_mesure_pollution)

cur.close()
conn.close()