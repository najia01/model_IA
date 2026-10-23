<h1 align="center" style="color: #D83B01;">🗑️ PLAN DE FIN DE VIE 🛑</h1>

## 1. Stratégie de fin de vie

- **Fin de vie partielle :** On arrête l'application (le conteneur) pour ne plus consommer de ressources de calcul et stopper la facturation immédiate, mais on conserve l'image, les données et le registre pour pouvoir redéployer rapidement si besoin.
- **Fin de vie totale :** On supprime définitivement toutes les ressources Cloud (Azure) générant des coûts. On ne conserve que le code source gratuit sur GitHub et le modèle en local pour l'archivage.

---

## 2. Déroulement du retrait des composants

Voici l'ordre exact et la méthode de suppression pour chaque élément du projet :

| Ordre | Composant                   | Quand et Comment le retirer ?                                                                                                    | Ce qu'on garde                                   | Coût si laissé en place |
| :---: | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------- | :---------------------- |
| **1** | **Application (Conteneur)** | **Quand :** Dès la fin de la démonstration du projet.<br>**Comment :** Arrêt et suppression du conteneur via le portail Azure.   | Rien                                             | ~ 1.56 € / mois         |
| **2** | **Secrets / Mots de passe** | **Quand :** En même temps que l'application.<br>**Comment :** Suppression des variables d'environnement sur Azure.               | Rien                                             | 0 € (inclus)            |
| **3** | **Image Docker & Registre** | **Quand :** Lors de la fin de vie totale.<br>**Comment :** Suppression du registre (Azure Container Registry) depuis le portail. | Rien en ligne (gardé en local)                   | ~ 0.88 € / mois         |
| **4** | **Modèle & Données**        | **Quand :** Lors de la fin de vie totale.<br>**Comment :** Suppression du compte de stockage Azure associé.                      | Le modèle entraîné est archivé sur mon PC local. | ~ 1.17 € / mois         |
| **5** | **Dépôt Git (Code)**        | **Ne sera pas retiré.**<br>Reste en ligne pour le portfolio.                                                                     | Tout l'historique et le code (GitHub).           | 0 € (Gratuit)           |
