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

| Date        | Identifiant du commit | Changement                           | Résultat    |
| :---------- | :-------------------- | :----------------------------------- | :---------- |
| [À remplir] | [À remplir]           | Déploiement initial de l'application | [À remplir] |
|             |                       |                                      |             |
