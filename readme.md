# 📖 Première partie : Présentation du projet et mise en production 🚀

Pour répondre aux exigences de planification et de suivi, ce projet s'appuie sur trois documents principaux qui structurent ma démarche :

- **[PLAN.md](Plan_Projet/PLAN.md)** : Ce fichier contient le tableau de bord du projet. Il servira de référence à la fin de l'exercice pour analyser les écarts entre les charges de travail estimées et le temps réellement passé.
- **[PROCEDURE_MISE_EN_PRODUCTION.md](Plan_Projet/PROCEDURE_MISE_EN_PRODUCTION.md)** : Ce document décrit le cycle de vie du déploiement. Il explique comment la mise en ligne est déclenchée, contrôlée, et comment effectuer un retour en arrière (rollback) manuel en cas de problème. Il intègre également le **journal des versions** qui trace l'historique des mises en ligne.
- **[FIN_DE_VIE.md](Plan_Projet/FIN_DE_VIE.md)** : Ce document planifie le nettoyage de l'infrastructure une fois le projet terminé. Il détaille l'ordre de retrait des composants cloud, justifie leur suppression grâce au calcul de leurs coûts d'hébergement, et établit une distinction claire entre une fin de vie partielle et une fin de vie totale.

# 🚀 Partie 2 : De l’enregistrement à la mise en ligne

## Partie A : L'API et le contrôle qualité

Cette section regroupe le code permettant de servir le modèle de classification (Horreur ou Comédie) via une API web, ainsi que les scripts de vérification automatisée.

### 1. Démarrer l'API locale

L'API est développée avec **FastAPI**. Elle charge le modèle `model.keras` et le `vectoriseur.joblib` au démarrage, et propose deux routes :

- `GET /health` : Vérifie l'état du serveur et retourne la version du modèle.
- `POST /predict` : Reçoit le résumé d'un film (minimum 15 caractères) et retourne la prédiction avec sa probabilité.

**Commande de lancement :**

```bash
uvicorn src.main:app --reload
```

Une fois le serveur lancé, l'interface de test interactive (Swagger) est accessible à l'adresse : `http://127.0.0.1:8000/docs`

### 2. Tests Automatiques

Les tests valident le bon fonctionnement de l'API (acceptation des cas valides, rejet avec erreur 400 des textes trop courts) et vérifient que les performances du modèle sont satisfaisantes. L'outil utilisé est **Pytest**.

**Commande pour exécuter les tests :**

```bash
python -m pytest
```

### 3. Barrière Qualité

Un script de contrôle (`barriere_qualite.py`) agit comme un filtre strict avant tout déploiement. Il compare les résultats inscrits dans `Model/metrics.json` avec les exigences fixées dans `config.yaml`.

- **Seuil F1 minimum** : 0.80
- **Taille de test minimale** : 400 lignes

> _Justification : Le seuil F1 est fixé à 0.80 car il garantit un haut niveau de prédiction tout en absorbant la marge de bruit statistique liée à notre échantillon de test de plus de 400 lignes._

**Commande pour lancer l'audit qualité :**

```bash
python barriere_qualite.py
```

Note : En cas de non-respect des seuils, le script déclenche une erreur système , ce qui bloquera automatiquement les futures chaînes de déploiement continu.

## Partie B : La boîte (Conteneur Docker)

Cette section explique comment emballer l'API et le modèle dans une image Docker légère et standardisée pour garantir un fonctionnement identique sur n'importe quel serveur.

### 1. Fichiers de configuration

- **`.dockerignore`** : Exclut les fichiers inutiles (données d'entraînement, tests, environnements virtuels, notebooks) pour réduire le poids final de l'image.
- **`requirements.txt`** : Liste les dépendances strictes. Utilisation de `tensorflow-cpu` et d'une image de base `python:3.11-slim` pour optimiser la taille du conteneur.
- **`Dockerfile`** : La recette de construction qui installe les dépendances, copie le code (`src/` et `Model/`) et expose le port 8000.

### 2. Construction de l'image

Pour créer l'image locale nommée `classifieur-films`, exécutez la commande suivante à la racine du projet :

```bash
docker build -t classifieur-films .
```

Note : La taille finale de l'image optimisée est de **2.19 GB**, respectant la consigne de légèreté.

### 3. Lancement et tests en local (Conteneur)

Pour démarrer l'application à l'intérieur de son conteneur Docker, exécutez la commande suivante :

```bash
docker run -p 8000:8000 classifieur-films
```

## Partie C : Le pipeline CI/CD (GitHub Actions)

L'automatisation des vérifications, de la construction et de la publication de l'image est gérée par **GitHub Actions**. Le fichier de configuration se trouve dans `.github/workflows/pipeline.yml` et s'exécute automatiquement à chaque envoi de code (`git push`).

### 1. Structure du Workflow

Le pipeline est divisé en trois travaux (jobs) exécutés séquentiellement sur un environnement Ubuntu (`ubuntu-latest`) :

- **Job 1 : `test`**
  - Configure l'environnement Python 3.11 et installe les dépendances via `requirements.txt`.
  - Exécute la **barrière qualité**. Si les seuils ne sont pas respectés, le processus s'arrête en erreur.
  - Exécute les **tests automatiques** de l'API avec Pytest.

- **Job 2 : `image`**
  - Sécurisé par une condition de dépendance (`needs: test`).
  - Construit l'image Docker.
  - Démarre le conteneur en arrière-plan et effectue une requête automatisée sur la route de santé (`/health`) pour certifier que l'API est fonctionnelle.

- **Job 3 : `publier`**
  - Sécurisé par une condition de dépendance (`needs: image`).
  - Se connecte au registre **Azure Container Registry (ACR)** en utilisant les identifiants stockés dans les secrets GitHub (`AZURE_REGISTRY`, `AZURE_USERNAME`, `AZURE_PASSWORD`).
  - Construit et pousse l'image finale sur Azure en utilisant l'identifiant unique du commit (`${{ github.sha }}`) comme balise (tag) d'image pour garantir la traçabilité.

### 2. Validation de la barrière qualité

Le système de blocage a été audité en conditions réelles : une modification volontaire du fichier de configuration, exigeant un score F1 inatteignable (0.99), a correctement provoqué un échec critique du job `test`. Ce rejet a automatiquement annulé les jobs suivants, prouvant qu'aucun modèle sous-performant ne peut être conteneurisé et envoyé en production.

## Partie D : Le déploiement Cloud (Azure Container Apps)

Une fois l'image validée et poussée dans le registre Azure par GitHub Actions, le déploiement et la gestion des versions s'effectuent sur **Azure Container Apps**.

### 1. Stratégie de versionnage

Grâce à l'utilisation de `${{ github.sha }}` dans notre workflow, chaque modification du code génère une image avec une balise unique (ex: `0c1f6e0`). L'image n'est donc pas écrasée sous un tag générique `latest`, ce qui permet de conserver un historique propre des différentes versions dans le registre.

### 2. Déploiement et rollback (Retour en arrière)

La gestion des versions en ligne se fait manuellement depuis le portail Azure, offrant un contrôle total sur ce qui est exposé au public :

1. Dans l'application de conteneur, naviguer vers **Conteneurs**.
2. Cliquer sur **Modifier et déployer** puis sélectionner le conteneur.
3. Dans le champ **Balise d'image**, saisir l'identifiant du commit souhaité.
4. Enregistrer et déployer la nouvelle révision.

Cette architecture permet de déployer de nouvelles fonctionnalités (comme l'ajout d'une route `/hello`) ou de réaliser un **rollback immédiat** vers une version stable en cas d'anomalie détectée en production.

## Partie E : Nettoyage des ressources (Cost Management)

Afin d'éviter une facturation inutile (un registre de conteneurs étant facturé tant qu'il existe, même inutilisé), les ressources spécifiques au projet ont été supprimées à la fin de l'exercice.

⚠️ _Conformément aux directives de sécurité, le groupe de ressources partagé de l'environnement de formation n'a pas été supprimé._

**Ressources ciblées et supprimées individuellement :**

- L'application de conteneur (Container App)
- L'environnement Container Apps
- L'espace de travail Log Analytics (généré automatiquement)
- Le registre de conteneurs (ACR)
