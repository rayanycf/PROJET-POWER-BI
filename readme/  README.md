#  Projet Analyse & Visualisation des Commandes – Power BI & Python

##  Objectif du projet
Ce projet a pour objectif d’analyser les **commandes livrées et non livrées** de la base **Northwind** à l’aide de scripts Python intégrés dans **Power BI**.  
Il permet de produire des **analyses temporelles**, des **classements clients**, des **catégorisations adaptatives** et un **dashboard KPI** afin d’aider à la prise de décision.

---

##  Architecture générale
Le projet repose sur :
- **Power BI** pour la modélisation des données et l’intégration visuelle
- **Scripts Python** pour les calculs avancés et les visualisations personnalisées
- **Dataset Power BI** servant de source d’entrée aux scripts (`dataset`)

Les scripts sont indépendants et peuvent être exécutés séparément selon l’analyse souhaitée.

---

##  Choix techniques et justification

###  Langage
- **Python** : langage adapté à l’analyse de données, très bien intégré à Power BI

###  Bibliothèques utilisées
- `pandas` : manipulation et agrégation des données
- `numpy` : calculs numériques et indicateurs
- `matplotlib` : création de graphiques personnalisés
- `seaborn` (ponctuellement) : amélioration esthétique des visualisations

 Ces bibliothèques sont standards, stables et compatibles avec Power BI.

###  Approche analytique
- Agrégation par dimensions métier (temps, client, employé)
- Sélection dynamique du **Top 10 clients**
- **Catégorisation adaptative** basée sur les percentiles (robuste et générique)
- KPI globaux pour une vision synthétique de la performance

---

##  Scripts disponibles

### 1️⃣ Analyse temporelle
- Analyse des commandes par période (`id_temps`)
- Évolution du taux de livraison dans le temps
- Comparaison livrées / non livrées
- Analyse complémentaire par client et par employé

### 2️⃣ Top 10 clients
- Identification des 10 clients les plus actifs
- Visualisation du volume total et du taux de livraison
- Comparaison performance vs volume

### 3️⃣ Répartition et catégorisation clients
- Calcul automatique des seuils (médiane, 75ᵉ percentile)
- Catégories : Excellence, Haute Performance, Gros Volume, etc.
- Matrice Volume / Performance
- Répartition des catégories

### 4️⃣ Dashboard KPI
- Taux de livraison global
- Volume total de commandes
- Répartition livrées / non livrées
- Indicateur de tendance
- Score global de performance

---

## ▶️ Comment exécuter les scripts

### 🔹 Prérequis
- Power BI Desktop installé
- Python installé sur la machine (version 3.x recommandée)
- Bibliothèques installées :
```bash
pip install pandas numpy matplotlib seaborn
```

### 🔹 Étapes dans Power BI
1. Ouvrir Power BI Desktop
2. Charger les tables nécessaires (fait commandes + dimensions)
3. Vérifier que les champs suivants sont disponibles :
   - `id_seqClient`
   - `nbr_commande_livrees`
   - `nbr_commande_non_livrees`
   - `id_temps` (optionnel)
4. Ajouter un **visuel Python**
5. Glisser les colonnes requises dans le visuel
6. Coller le script Python correspondant
7. Exécuter le script

⚠️ Le dataframe `dataset` est automatiquement fourni par Power BI.

---

## 🔁 Reproduire les résultats
- Utiliser le même modèle de données
- Conserver les mêmes noms de colonnes
- Exécuter les scripts dans le même contexte Power BI
- Les seuils et catégories s’adaptent automatiquement aux données

---

## ✅ Résultats attendus
- Visualisations claires et interprétables
- Identification des clients stratégiques
- Vision globale de la performance logistique
- Outils d’aide à la décision

---

##  Auteur
**Mohamed Rayane Yacef**  
Master Big Data  
Projet académique – Analyse & Visualisation des données NORTWHIND sur POWER BI 

---
