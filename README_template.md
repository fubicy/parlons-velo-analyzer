# parlons-velo-analyzer
Analyse des réponses du questionnaire de la FUB

```
# Generate Markdown files
python top_streets.py

# Test markdown content
docker run --rm -v $(pwd):/root/docs:ro -p 80:80 -t -i fstab/grip grip /root/docs/README.md 0.0.0.0:80
```

Les résultats sont dans le repertoire topstreets

### Contributeurs
* [Bruno Adelé](https://twitter.com/jesuislibre) - [#JeSuisUnDesDeux](https://twitter.com/search?q=%23JeSuisUnDesDeux)
