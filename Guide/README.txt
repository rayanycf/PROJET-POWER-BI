Projet Analyse & Visualisation des Commandes – Power BI & Python

OBJECTIF DU PROJET
Ce projet a pour objectif d’analyser les commandes livrées et non livrées de la base Northwind à l’aide de scripts Python intégrés dans Power BI.
Il permet de produire des analyses temporelles, des classements clients, des catégorisations adaptatives et un dashboard KPI afin d’aider à la prise de décision.

ARCHITECTURE GÉNÉRALE
Le projet repose sur :
- Power BI pour la modélisation des données et l’intégration visuelle
- Scripts Python pour les calculs avancés et les visualisations personnalisées
- Dataset Power BI servant de source d’entrée aux scripts (dataset)

CHOIX TECHNIQUES ET JUSTIFICATION

Langage
Python est utilisé pour sa puissance en analyse de données et sa compatibilité native avec Power BI.

Bibliothèques utilisées
- pandas : agrégation et manipulation des données
- numpy : calculs numériques et indicateurs
- matplotlib : création de graphiques personnalisés
- seaborn : amélioration esthétique des visualisations

Ces bibliothèques sont standards, stables et adaptées à un projet académique.

APPROCHE ANALYTIQUE
- Agrégation par dimensions métier (temps, client, employé)
- Sélection dynamique du Top 10 clients
- Catégorisation adaptative basée sur les percentiles
- Calcul de KPI globaux pour une vision synthétique

SCRIPTS DISPONIBLES

1. Analyse temporelle
Analyse des commandes par période (id_temps), évolution du taux de livraison, comparaison livrées / non livrées, analyses complémentaires par client et employé.

2. Top 10 clients
Identification des 10 clients les plus actifs, visualisation du volume total et du taux de livraison.

3. Répartition et catégorisation des clients
Catégorisation automatique (Excellence, Haute Performance, Gros Volume, etc.) basée sur les données réelles.

4. Dashboard KPI
Calcul et visualisation du taux de livraison global, volumes, tendances et score de performance.

COMMENT EXÉCUTER LES SCRIPTS

Prérequis
- Power BI Desktop installé
- Python 3.x installé
- Bibliothèques Python :
pip install pandas numpy matplotlib seaborn

Étapes dans Power BI
1. Ouvrir Power BI Desktop
2. Charger les tables nécessaires (fait + dimensions)
3. Vérifier la présence des colonnes :
   id_seqClient
   nbr_commande_livrees
   nbr_commande_non_livrees
   id_temps (optionnel)
4. Ajouter un visuel Python
5. Glisser les champs nécessaires dans le visuel
6. Coller le script Python
7. Exécuter le script

Le dataframe dataset est automatiquement généré par Power BI.

REPRODUIRE LES RÉSULTATS
- Utiliser le même modèle de données
- Conserver les mêmes noms de colonnes
- Exécuter les scripts dans le même contexte Power BI
- Les seuils et catégories s’adaptent automatiquement aux données

RÉSULTATS ATTENDUS
- Visualisations claires et interprétables
- Identification des clients stratégiques
- Vision globale de la performance logistique

AUTEUR
Mohamed Rayane Yacef
Master Big Data
Projet académique
