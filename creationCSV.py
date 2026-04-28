import sqlite3
import pandas as pd

chemin = "BaseDeDonnee/base_donnee.db"

def creation_file(base_chemin, requete, fichier, nom_prb):
    connexion = sqlite3.connect(base_chemin)
    # Pandas exécute la requête et crée le DataFrame d'un coup
    df = pd.read_sql_query(requete, connexion)
    # Sauvegarde en CSV très simple
    df.to_csv(fichier, index=False, encoding="utf-8")
    
    print("Fichier CSV pour problématique ",nom_prb," créé")
    connexion.close()

problematique_1 = 1
query_Prob_1 = """
SELECT 
    t.nom_station,
    t.influence AS type_station,
    mp.valeur_poll AS NO2,
    mp.jour,
    mp.mois,
    mp.annee,
    cm.Force_vent_med
FROM STATION AS t
JOIN MESURE_POLLUTION AS mp
    ON t.code_station = mp.code_station
JOIN COMMUNES AS c
    ON t.code_insee_com = c.code_insee_com
JOIN CLIMAT_MENSUEL AS cm
    ON c.code_insee_com = cm.code_insee_com
WHERE mp.nom_poll = 'NO2'
  AND LOWER(c.nom_com) = 'toulouse'
  AND mp.annee = 2022
  AND mp.mois IN (10, 11, 12);
"""

problematique_2 = 2
query_Prob_2 = """
SELECT
    c.code_insee_com,
    c.densite_cat as typologie_territoire,
    c.alti_med,
    c.latitude,
    c.longitude,
    cm.RR_med,
    cm.NBJRR1_med,
    cm.NBJRR5_med,
    cm.NBJRR10_med,
    cm.Tmin_med,
    cm.Tmax_med,
    cm.Insolation_med,
    cm.Rayonnement_med,
    cm.Force_vent_med,
    cm.Tens_vap_med
FROM COMMUNES c
JOIN CLIMAT_MENSUEL cm
    ON c.code_insee_com = cm.code_insee_com;
"""

problematique_3 = 3
query_Prob_3 = """
SELECT
    c.code_insee_com,
    c.nom_com,
    c.densite_cat AS typologie_territoire,
    c.alti_med,
    c.latitude,
    c.longitude,
    cm.RR_med,
    cm.NBJRR1_med,
    cm.NBJRR5_med,
    cm.NBJRR10_med,
    cm.Tmin_med,
    cm.Tmax_med,
    cm.Tens_vap_med,
    cm.Force_vent_med,
    cm.Insolation_med,
    cm.Rayonnement_med
FROM COMMUNES AS c
JOIN CLIMAT_MENSUEL AS cm
    ON c.code_insee_com = cm.code_insee_com;

"""

problematique_4 = 4
query_Prob_4 = """
SELECT
    c.code_insee_com,
    c.densite_cat AS typologie_territoire,
    c.latitude,
    c.longitude,
    c.alti_med,
    mp.nom_poll,
    mp.valeur_poll,
    mp.jour,
    mp.mois,
    mp.annee,
    cm.Force_vent_med,
    cm.Tmin_med,
    cm.Tmax_med,
    cm.RR_med,
    cm.NBJRR1_med,
    cm.NBJRR5_med,
    cm.NBJRR10_med
FROM COMMUNES AS c
JOIN STATION AS s
    ON c.code_insee_com = s.code_insee_com
JOIN MESURE_POLLUTION AS mp
    ON s.code_station = mp.code_station
JOIN CLIMAT_MENSUEL AS cm
    ON c.code_insee_com = cm.code_insee_com;
"""

# Extraction de toutes les problématiques
creation_file(chemin, query_Prob_1, 'FichierProbs/no2_vent_toulouse.csv', problematique_1)
creation_file(chemin, query_Prob_2, 'FichierProbs/climat_territoire.csv', problematique_2)
creation_file(chemin, query_Prob_3, 'FichierProbs/facteurs_distinction.csv', problematique_3)
creation_file(chemin, query_Prob_4, 'FichierProbs/influence_territoire_polluant.csv', problematique_4)