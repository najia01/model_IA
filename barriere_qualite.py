import json
import yaml
import sys
import os

# 1. Chargement de la configuration
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

seuil_f1 = config["min_f1_score"]
seuil_taille = config["min_test_size"]

# 2. Chargement des métriques du modèle
chemin_metrics = "Model/metrics.json"
if not os.path.exists(chemin_metrics):
    print("Erreur : Fichier metrics.json introuvable.")
    sys.exit(1)

with open(chemin_metrics, "r", encoding="utf-8") as f:
    metriques = json.load(f)

# On récupère les valeurs avec les noms exacts de ton fichier
f1_obtenu = metriques.get("f1_score", 0) 
taille_obtenue = metriques.get("taille_test", 0) 

print(f"--- BARRIÈRE QUALITÉ ---")
print(f"F1 Score : {f1_obtenu} (Minimum requis : {seuil_f1})")
print(f"Taille du test : {taille_obtenue} (Minimum requis : {seuil_taille})")

# 3. Le jugement
if f1_obtenu < seuil_f1 or taille_obtenue < seuil_taille:
    print("ÉCHEC : Le modèle est refusé, il ne respecte pas les critères.")
    sys.exit(1) 

print("SUCCÈS : Le modèle est validé !")
sys.exit(0)

# J'ai fixé le seuil F1 à 0.80 et la taille de test minimale à 400 car ces valeurs garantissent un modèle performant et représentatif, 
# tout en tenant compte de la marge de bruit statistique inhérente à notre échantillon."