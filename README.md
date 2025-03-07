# Data quality monitoring

L'objectif de ce projet est de :
- collecter des données d'observation par une API ;
- transformer ces données et les stocker ;
- orchestrer ces étapes de collecte et de transformation ;
- faire une visualisation par Streamlit.

## Structure du projet

```
/api             # Application API
/dags            # DAG pour orchestrer les tâches du pipeline
/data
├── raw          # Données brutes initiales
├── processed    # Données transformées et stockées en format Parquet
/extract_data    # Extraction des données à partir de l'API
/logs            # Logs de l'orchestrateur Airflow
/src             # Définition des classes Sensor et Store
/streamlit       # Dashboard de visualisation des données traitées
/transform_data  # Chargement des données brutes, nettoyage et stockage en format Parquet
/venv            # Environnement virtuel
```

## Activation de l'environnement virtuel

Pour activer l'environnement virtuel :
```
source venv/bin/activate
```

## Requête sur l'API

Pour lancer l'API en local, saisir la commande suivante sur le terminal :
```
uvicorn api.app:app --reload
```

Pour faire une requête sur l'API en local, saisir le lien suivant :
```
http://127.0.0.1:8000/?store_name=Ville&year=YYYY&month=M&day=D&sensor_id=N
```

En remplaçant les valeurs des différents champs :
- Ville par le nom de la ville,
- YYYY par l'année,
- M par le numéro du mois,
- D par le jour,
- N par le numéro du capteur (facultatif).

## Extraction des données

Cette partie consiste à extraire les données brutes à partir de l'API afin de les afficher et de les transformer par la suite.

### Prérequis

- Etablir une connexion avec l'API avec l'étape précédente
- Vérifier que le dossier `data/raw` est bien créé

### Exécution de l'extraction

L'extraction des données brutes à partir de l'API peut être exécutée à partir de la commande suivante (il faut avoir établi la connexion avec l'API) :
```bash
python extract_data/get_api_data.py
```

Les données sont alors enregistrées dans `data/raw`.

## Transformation des données

Cette partie consiste à transformer et analyser des données brutes stockées dans `data/raw`. L'objectif est de nettoyer, agréger et enrichir ces données avant de les stocker dans un format optimisé.

### Étapes de transformation

1. **Lecture des données** : Les fichiers bruts sont chargés depuis `data/raw`.
2. **Agrégation par jour** : La donnée est regroupée afin de faciliter les analyses temporelles.
3. **Nettoyage** : Suppression des valeurs nulles et des entrées inattendues.
4. **Calculs avancés** : Utilisation de window functions pour générer de nouvelles métriques.
5. **Ajout d'une colonne** : Cette colonne permet d'analyser les variations relatives d'une mesure spécifique.
6. **Stockage en Parquet** : Les données finales sont enregistrées dans `data/processed`.

### Pourquoi utiliser Parquet plutôt que CSV ?

Le format Parquet présente plusieurs avantages par rapport au CSV :

- **Optimisation du stockage** : Parquet est un format de stockage en colonnes, ce qui réduit considérablement la taille des fichiers par rapport au CSV.
- **Lecture plus rapide** : Grâce à son stockage en colonnes, Parquet permet de charger uniquement les colonnes nécessaires, améliorant ainsi les performances.
- **Gestion des types** : Contrairement au CSV qui stocke tout sous forme de texte, Parquet conserve les types natifs (entiers, flottants, dates, etc.), évitant ainsi les erreurs de conversion.
- **Compatibilité avec les outils Big Data** : Parquet est largement utilisé avec Apache Spark, Hadoop et d'autres frameworks de traitement de données distribuées.

### Exécution du pipeline

Le pipeline peut être exécuté avec la commande suivante :

```bash
python transform_data/clean_data.py
```

## Automatisation

### Script d'exécution des données passées

Les données passées peuvent être automatiquement extraites par un script Bash :

```bash
./extract_data/script_get_api_data.sh
```

### Orchestration avec Airflow

Les tâches d'extraction et de transformation peuvent être planifiées dans le fichier `dags/extract_transform.py`.

Le DAG contient deux tâches BashOperator exécutées toutes les heures :
- `extract_operator` pour l'extraction ;
- `transform_operator` pour la transformation.

Les paramètres `start_date` et `end_date` (si besoin) permettent de planifier les dates d'exécution du DAG.

Pour démarrer Airflow, exécuter le script Bash suivant :

```bash
./airflow_start.sh
```

## Visualisation sur le dashboard Streamlit

L'application Streamlit peut être lancée avec la commande suivante :

```bash
streamlit run streamlit/app.py
```

Sur le menu à gauche, sélectionner les options :
- le nom du magasin (Lille, Marseille, Toulouse)
- le numéro du capteur
- la période (données de la semaine, données du mois, données de toute l'année)

Le dashboard affichera alors les données traitées et les courbes d'évolution des visites.