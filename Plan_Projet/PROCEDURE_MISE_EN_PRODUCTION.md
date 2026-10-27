<h1 align="center">🚀 PROCÉDURE DE MISE EN PRODUCTION ⚙️</h1>

## 1. Cycle de déploiement

- **Déclencheur :** Envoi du code (git push) sur la branche principale du dépôt GitHub.
- **Vérifications automatiques (CI - GitHub Actions) :**
  - Lancement des tests unitaires avec `pytest` pour vérifier le bon fonctionnement de l'API.
  - Validation de la **Barrière Qualité** : le script vérifie que le F1-score dans `metrics.json` est supérieur au seuil défini dans `config.yaml`.
  - Construction de l'image Docker et vérification de son démarrage.
- **Déploiement (CD - Manuel) :** Le robot GitHub pousse l'image validée dans le registre Azure (ACR) avec l'identifiant du commit. Le déploiement se fait **à la main** sur le portail Azure (Container Apps) en spécifiant cet identifiant de commit, car le compte de formation ne possède pas les droits nécessaires pour un déploiement automatique.
- **Contrôle :** Test manuel des routes `/health` et `/predict` sur l'adresse publique fournie par Azure.
- **Conditions et mode de retour arrière (Rollback) :** En cas d'anomalie en production, on redéploie manuellement l'image précédente depuis le portail Azure, en indiquant l'ancien identifiant de commit validé.
- **Rôles :**
  - Qui décide : Najia
  - Qui exécute : Najia (Déploiement manuel) / GitHub Actions (Tests et Build)

---

## 2. Journal des versions

| Date | Identifiant du commit | Changement | Résultat

| **Partie 1 : Développement local et Modélisation** | | | |
| 23/10/2026 | `b871389` | mon premier commit (Initialisation du projet). | OK |
| 24/10/2026 | `84c2245` | partie1 (Création API, tests, et Dockerfile). | OK |
| **Partie 2 : Intégration et Déploiement Continu (CI/CD)** | | | |
| 25/10/2026 | `9a43c16` | partie 2 API et conteneur Docker. | OK |
| 25/10/2026 | `438cde8` | Ajout du workflow GitHub Actions. | OK |
| 26/10/2026 | `b645d83` | Déplacement du fichier pipeline dans le dossier workflows. | OK |
| 26/10/2026 | `e5badda` | Correction majuscule du dossier Model dans les tests. | OK |
| 26/10/2026 | `441dfe8` | Test de la barriere qualite (crash test). | OK |
| 26/10/2026 | `c607a7f` | Restauration du seuil F1. | OK |
| 26/10/2026 | `fe20fae` | Ajout du job de publication vers Azure. | OK |
| 26/10/2026 | `794b319` | Ajout du job de publication vers Azure (Correction/Ajustement). | OK |
| **Partie 3 : Déploiement et Rollback sur Azure** | | | |
| 27/10/2026 | `f43b586` | Ajout de la route hello. | OK |
| 27/10/2026 | `0c1f6e0` | Déplacement route hello dans l'API. | OK |
| 26/10/2026 | `937e495` | Correction tag image docker avec github.sha. | OK |
| 27/10/2026 | `dd2acc9` | Rollback : retour a la version precedente. | OK |
