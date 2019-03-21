# parlons-velo-analyzer
Analyse des réponses du questionnaire de la FUB

## Installation
Lance l'installation des prérequis, assez long, car lance à la fin le téléchargement et l'import de la map dans le serveur overpass local(docker)
`./setup.sh` 

## Execution
```
# Generation des fichiers Markdown et Html
python top_streets.py
```

Les résultats sont dans le repertoire topstreets

### Dépendances
Ce projets utilise divers contributions libres, notamment :

* [osm-tools](https://github.com/jesuisundesdeux/osm-tools) Permet de generer une base d'adresses sur l'ensemble de la France)
* [docker-overpass-api](https://github.com/jesuisundesdeux/docker-overpass-api]) Exécuter des requête overpass QL sur votre prope instance
* [Folium](https://github.com/python-visualization/folium) Génère des cartes dynamique depuis Python
* [Openstreetmap](https://www.openstreetmap.org) Alternative à Google Map dont les contributions sont effectuées par les bénévoles répartir sur l'ensemble de la planète :)


### Contributeurs
* [Bruno Adelé](https://twitter.com/jesuislibre) - [#JeSuisUnDesDeux](https://twitter.com/search?q=%23JeSuisUnDesDeux)

### Licence
Ce projet est en licence GPL 3