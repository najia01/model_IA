<h1 align="center" style="color: #0078D7;">📖 Première partie

Présentation du projet et mise en production 🚀</h1>

Pour répondre aux exigences de planification et de suivi, ce projet s'appuie sur trois documents principaux qui structurent notre démarche :

- 📝 **[PLAN.md](Plan_Projet/PLAN.md)**
  Ce fichier contient le tableau de bord du projet. Il servira de référence à la fin de l'exercice pour analyser les écarts entre les charges de travail estimées et le temps réellement passé.

- ⚙️ **[PROCEDURE_MISE_EN_PRODUCTION.md](Plan_Projet/PROCEDURE_MISE_EN_PRODUCTION.md)**
  Ce document décrit le cycle de vie du déploiement. Il explique comment la mise en ligne est déclenchée, contrôlée, et comment effectuer un retour en arrière (rollback) manuel en cas de problème. Il intègre également le **journal des versions** qui trace l'historique des mises en ligne.

- 🗑️ **[FIN_DE_VIE.md](Plan_Projet/FIN_DE_VIE.md)**  
  Ce document planifie le nettoyage de l'infrastructure une fois le projet terminé. Il détaille l'ordre de retrait des composants cloud, justifie leur suppression grâce au calcul de leurs coûts d'hébergement, et établit une distinction claire entre une fin de vie partielle et une fin de vie totale.

Partie 2 : de l’enregistrement à la mise en ligne

## Partie A : L'Application (API) et Contrôle Qualité

Cette section regroupe le code permettant de servir le modèle de classification (Horreur ou Comédie) via une API web, ainsi que les scripts de vérification automatisée.

### 1. Démarrer l'API locale

L'API est développée avec **FastAPI**. Elle charge le modèle `model.keras` et le `vectoriseur.joblib` au démarrage, et propose deux routes :

- `GET /health` : Vérifie l'état du serveur et retourne la version du modèle.
- `POST /predict` : Reçoit le résumé d'un film (minimum 15 caractères) et retourne la prédiction avec sa probabilité.

**Commande de lancement :**
uvicorn src.main:app --reload

Une fois le serveur lancé, l'interface de test interactive (Swagger) est accessible à l'adresse : `http://127.0.0.1:8000/docs`

### 2. Tests Automatiques

Les tests valident le bon fonctionnement de l'API (acceptation des cas valides, rejet avec erreur 400 des textes trop courts) et vérifient que les performances du modèle sont satisfaisantes. L'outil utilisé est **Pytest**.

**Commande pour exécuter les tests :**

python -m pytest

### 3. Barrière Qualité

Un script de contrôle (`barriere_qualite.py`) agit comme un filtre strict avant tout déploiement. Il compare les résultats inscrits dans `Model/metrics.json` avec les exigences fixées dans `config.yaml`.

- **Seuil F1 minimum** : 0.80
- **Taille de test minimale** : 400 lignes

_Justification : Le seuil F1 est fixé à 0.80 car il garantit un haut niveau de prédiction tout en absorbant la marge de bruit statistique liée à notre échantillon de test de plus de 400 lignes._

**Commande pour lancer l'audit qualité :**

python barriere_qualite.py

- Note : En cas de non-respect des seuils, le script déclenche une erreur système `exit 1`, ce qui bloquera automatiquement les futures chaînes de déploiement continu.

## Partie B : La boîte (Conteneur Docker)

Cette section explique comment emballer l'API et le modèle dans une image Docker légère et standardisée pour garantir un fonctionnement identique sur n'importe quel serveur.

### 1. Fichiers de configuration

- **`.dockerignore`** : Exclut les fichiers inutiles (données d'entraînement, tests, environnements virtuels, notebooks) pour réduire le poids final de l'image.
- **`requirements.txt`** : Liste les dépendances strictes. Utilisation de `tensorflow-cpu` et d'une image de base `python:3.11-slim` pour optimiser la taille du conteneur.
- **`Dockerfile`** : La recette de construction qui installe les dépendances, copie le code (`src/` et `Model/`) et expose le port 8000.

### 2. Construction de l'image

Pour créer l'image locale nommée `classifieur-films`[cite: 16], exécutez la commande suivante à la racine du projet :

```bash
docker build -t classifieur-films .

* Note : La taille finale de l image optimisée est de **2.19 GB** , respectant la consigne de légèreté.

### 3. Lancement et Tests en local (Conteneur)

Pour démarrer l'application à l'intérieur de son conteneur Docker, exécutez la commande suivante :

docker run -p 8000:8000 classifieur-films
