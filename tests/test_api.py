from fastapi.testclient import TestClient
import json
import os

# Import de l'API
from src.main import app

# Création d'un faux navigateur pour tester l'API de l'intérieur
client = TestClient(app)

# Test 1 : L'API répond (Vérification de la route /health)
def test_api_repond():
    reponse = client.get("/health")
    assert reponse.status_code == 200 
    assert reponse.json()["status"] == "ok"

# Test 2 : casvalide avec texte de plus de 15 caractères
def test_cas_valide_marche():
    texte_valide = "Ce film d'horreur était vraiment effrayant, j'ai sursauté plusieurs fois."
    reponse = client.post("/predict", json={"texte": texte_valide})
    assert reponse.status_code == 200
    assert "classe" in reponse.json()
    assert "probabilite" in reponse.json()

# Test 3 : cas invalide avec un texte trop court 
def test_cas_invalide_refuse():
    texte_invalide = "Nul"
    reponse = client.post("/predict", json={"texte": texte_invalide})
    assert reponse.status_code == 400
    assert "Le texte est invalide ou trop court" in reponse.json()["detail"]

# Test 4 : Le modèle atteint un score minimum
def test_score_minimum():
    # Lecture fichier JSON généré 
    chemin_metrics = "Model/metrics.json"
    assert os.path.exists(chemin_metrics), "Le fichier metrics.json est introuvable."
    
    with open(chemin_metrics, "r", encoding="utf-8") as f:
        metriques = json.load(f)
        
    score_f1 = metriques.get("f1_score", 0)
    
    # Exigence que le modèle fasse au moins 80% au test final 
    assert score_f1 >= 0.80, f"Le score {score_f1} est trop bas."
    
# Test 5 : Faire vivre votre version
@app.get("/hello")
def hello():
    return {"message": "hello depuis la version deployée sur Azure"}