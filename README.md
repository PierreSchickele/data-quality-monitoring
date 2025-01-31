# Data quality monitoring

L'objectif de ce projet est de :
- collecter des données d'observation par une API ;
- les nettoyer ;
- faire une visualisation par Streamlit des observations de la journée et des quatre derniers jours.

## Requête sur l'API

Pour lancer l'API en local, saisir la commande suivante sur le terminal :
`uvicorn api.app:app --reload`

Pour faire une requête sur l'API en local, saisir le lien suivant :
http://127.0.0.1:8000/?store_name=Ville&year=YYYY&month=M&day=D
En remplaçant les valeurs des différents champs :
- Ville par le nom de la ville,
- YYYY par l'année,
- M par le numéro du mois,
- D par le jour.
