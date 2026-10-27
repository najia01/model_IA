from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import keras
import joblib
import json

# Création de l'application API
app = FastAPI(title="Classifieur de résumés de films")

# Chargement du modèle, du vectoriseur et des métriques UNE SEULE FOIS au démarrage
modele = keras.models.load_model("Model/model.keras")
vectoriseur = joblib.load("Model/vectoriseur.joblib")

with open("Model/metrics.json", "r", encoding="utf-8") as f:
    metriques = json.load(f)
version_modele = metriques.get("version", "inconnue")

# Définition du format attendu en entrée
class RequeteTexte(BaseModel):
    texte: str

# Route 1 : Vérification de la santé de l'API
@app.get("/health")
def health():
    return {"status": "ok", "version": version_modele}

# Route 2 : Prédiction
@app.post("/predict")
def predict(requete: RequeteTexte):
    texte_propre = requete.texte.strip()
    
    # Gestion des textes invalides (trop courts ou vides)
    if not texte_propre or len(texte_propre) < 15:
        raise HTTPException(status_code=400, detail="Le texte est invalide ou trop court (minimum 15 caractères).")
    
    # Transformation du texte en nombres avec le TF-IDF
    texte_vectorise = vectoriseur.transform([texte_propre]).toarray()
    
    # Prédiction avec le modèle (renvoie une probabilité)
    probabilite = modele.predict(texte_vectorise, verbose=0)[0][0]
    
    # Déduction de la classe (seuil à 0.5)
    classe = "Horreur" if probabilite > 0.5 else "Comédie"
    
    return {
        "classe": classe,
        "probabilite": float(probabilite),
        "version": version_modele
    }
    
# Route 3: Faire vivre votre version
# @app.get("/hello")
# def hello():
#     return {"message": "hello depuis la version deployée sur Azure"}