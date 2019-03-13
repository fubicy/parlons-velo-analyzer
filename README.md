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
### Résultats par département

Sur l'ensemble du téritoire, il y a eu 81005 réponses dont 50075 réponses avec une rue citée (61%)

| Departement | Nb réponses | Nb réponses avec rue | Nb points noirs |
|-------------|-------------|----------------------|-----------------|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/01 - Ain/index.html'>01 - Ain</a>|393|234(59%)|<img src="img/bar_14.gif" />&nbsp;97|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/02 - Aisne/index.html'>02 - Aisne</a>|176|62(35%)|<img src="img/bar_4.gif" />&nbsp;34|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/03 - Allier/index.html'>03 - Allier</a>|127|49(38%)|<img src="img/bar_4.gif" />&nbsp;31|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/04 - Alpes-de-Haute-Provence/index.html'>04 - Alpes-de-Haute-Provence</a>|201|80(39%)|<img src="img/bar_4.gif" />&nbsp;31|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/05 - Hautes-Alpes/index.html'>05 - Hautes-Alpes</a>|368|150(40%)|<img src="img/bar_7.gif" />&nbsp;51|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/06 - Alpes-Maritimes/index.html'>06 - Alpes-Maritimes</a>|1072|460(42%)|<img src="img/bar_23.gif" />&nbsp;161|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/07 - Ardèche/index.html'>07 - Ardèche</a>|229|107(46%)|<img src="img/bar_6.gif" />&nbsp;43|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/08 - Ardennes/index.html'>08 - Ardennes</a>|123|99(80%)|<img src="img/bar_4.gif" />&nbsp;34|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/09 - Ariège/index.html'>09 - Ariège</a>|76|19(25%)|<img src="img/bar_1.gif" />&nbsp;12|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/10 - Aube/index.html'>10 - Aube</a>|277|132(47%)|<img src="img/bar_8.gif" />&nbsp;60|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/11 - Aude/index.html'>11 - Aude</a>|241|38(15%)|<img src="img/bar_3.gif" />&nbsp;23|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/12 - Aveyron/index.html'>12 - Aveyron</a>|194|77(39%)|<img src="img/bar_3.gif" />&nbsp;26|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/13 - Bouches-du-Rhône/index.html'>13 - Bouches-du-Rhône</a>|3547|1605(45%)|<img src="img/bar_47.gif" />&nbsp;329|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/14 - Calvados/index.html'>14 - Calvados</a>|1002|519(51%)|<img src="img/bar_23.gif" />&nbsp;163|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/15 - Cantal/index.html'>15 - Cantal</a>|131|102(77%)|<img src="img/bar_4.gif" />&nbsp;28|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/16 - Charente/index.html'>16 - Charente</a>|194|81(41%)|<img src="img/bar_4.gif" />&nbsp;32|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/17 - Charente-Maritime/index.html'>17 - Charente-Maritime</a>|1106|506(45%)|<img src="img/bar_22.gif" />&nbsp;157|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/18 - Cher/index.html'>18 - Cher</a>|456|233(51%)|<img src="img/bar_10.gif" />&nbsp;74|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/19 - Corrèze/index.html'>19 - Corrèze</a>|124|35(28%)|<img src="img/bar_3.gif" />&nbsp;22|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/21 - Côte-d_Or/index.html'>21 - Côte-d'Or</a>|1053|2062(195%)|<img src="img/bar_23.gif" />&nbsp;165|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/22 - Côtes-d_Armor/index.html'>22 - Côtes-d'Armor</a>|265|89(33%)|<img src="img/bar_8.gif" />&nbsp;59|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/23 - Creuse/index.html'>23 - Creuse</a>|2|0(0%)|<img src="img/bar_0.gif" />&nbsp;0|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/24 - Dordogne/index.html'>24 - Dordogne</a>|60|36(60%)|<img src="img/bar_3.gif" />&nbsp;23|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/25 - Doubs/index.html'>25 - Doubs</a>|695|390(56%)|<img src="img/bar_16.gif" />&nbsp;112|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/26 - Drôme/index.html'>26 - Drôme</a>|1029|1005(97%)|<img src="img/bar_24.gif" />&nbsp;170|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/27 - Eure/index.html'>27 - Eure</a>|110|40(36%)|<img src="img/bar_3.gif" />&nbsp;27|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/28 - Eure-et-Loir/index.html'>28 - Eure-et-Loir</a>|69|37(53%)|<img src="img/bar_3.gif" />&nbsp;24|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/29 - Finistère/index.html'>29 - Finistère</a>|1278|618(48%)|<img src="img/bar_33.gif" />&nbsp;229|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/2A - Corse-du-Sud/index.html'>2A - Corse-du-Sud</a>|222|29(13%)|<img src="img/bar_1.gif" />&nbsp;9|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/2B - Haute-Corse/index.html'>2B - Haute-Corse</a>|28|1(3%)|<img src="img/bar_0.gif" />&nbsp;1|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/30 - Gard/index.html'>30 - Gard</a>|462|220(47%)|<img src="img/bar_9.gif" />&nbsp;67|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/31 - Haute-Garonne/index.html'>31 - Haute-Garonne</a>|4526|2795(61%)|<img src="img/bar_95.gif" />&nbsp;660|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/32 - Gers/index.html'>32 - Gers</a>|70|67(95%)|<img src="img/bar_4.gif" />&nbsp;33|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/33 - Gironde/index.html'>33 - Gironde</a>|2184|1023(46%)|<img src="img/bar_51.gif" />&nbsp;357|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/34 - Hérault/index.html'>34 - Hérault</a>|2262|939(41%)|<img src="img/bar_39.gif" />&nbsp;275|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/35 - Ille-et-Vilaine/index.html'>35 - Ille-et-Vilaine</a>|2126|1473(69%)|<img src="img/bar_43.gif" />&nbsp;298|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/36 - Indre/index.html'>36 - Indre</a>|220|88(40%)|<img src="img/bar_4.gif" />&nbsp;34|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/37 - Indre-et-Loire/index.html'>37 - Indre-et-Loire</a>|1206|1150(95%)|<img src="img/bar_38.gif" />&nbsp;263|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/38 - Isère/index.html'>38 - Isère</a>|3533|2489(70%)|<img src="img/bar_81.gif" />&nbsp;565|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/39 - Jura/index.html'>39 - Jura</a>|280|130(46%)|<img src="img/bar_7.gif" />&nbsp;52|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/40 - Landes/index.html'>40 - Landes</a>|103|24(23%)|<img src="img/bar_2.gif" />&nbsp;17|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/41 - Loir-et-Cher/index.html'>41 - Loir-et-Cher</a>|115|47(40%)|<img src="img/bar_4.gif" />&nbsp;29|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/42 - Loire/index.html'>42 - Loire</a>|954|364(38%)|<img src="img/bar_17.gif" />&nbsp;124|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/43 - Haute-Loire/index.html'>43 - Haute-Loire</a>|212|27(12%)|<img src="img/bar_1.gif" />&nbsp;12|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/44 - Loire-Atlantique/index.html'>44 - Loire-Atlantique</a>|3223|1991(61%)|<img src="img/bar_72.gif" />&nbsp;501|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/45 - Loiret/index.html'>45 - Loiret</a>|1025|466(45%)|<img src="img/bar_22.gif" />&nbsp;158|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/46 - Lot/index.html'>46 - Lot</a>|24|2(8%)|<img src="img/bar_0.gif" />&nbsp;2|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/47 - Lot-et-Garonne/index.html'>47 - Lot-et-Garonne</a>|130|165(126%)|<img src="img/bar_3.gif" />&nbsp;21|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/48 - Lozère/index.html'>48 - Lozère</a>|5|0(0%)|<img src="img/bar_0.gif" />&nbsp;0|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/49 - Maine-et-Loire/index.html'>49 - Maine-et-Loire</a>|1497|957(63%)|<img src="img/bar_33.gif" />&nbsp;232|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/50 - Manche/index.html'>50 - Manche</a>|367|171(46%)|<img src="img/bar_10.gif" />&nbsp;69|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/51 - Marne/index.html'>51 - Marne</a>|709|556(78%)|<img src="img/bar_16.gif" />&nbsp;116|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/52 - Haute-Marne/index.html'>52 - Haute-Marne</a>|147|73(49%)|<img src="img/bar_4.gif" />&nbsp;28|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/53 - Mayenne/index.html'>53 - Mayenne</a>|353|169(47%)|<img src="img/bar_9.gif" />&nbsp;63|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/54 - Meurthe-et-Moselle/index.html'>54 - Meurthe-et-Moselle</a>|837|616(73%)|<img src="img/bar_25.gif" />&nbsp;174|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/55 - Meuse/index.html'>55 - Meuse</a>|10|1(10%)|<img src="img/bar_0.gif" />&nbsp;1|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/56 - Morbihan/index.html'>56 - Morbihan</a>|724|289(39%)|<img src="img/bar_19.gif" />&nbsp;136|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/57 - Moselle/index.html'>57 - Moselle</a>|447|240(53%)|<img src="img/bar_14.gif" />&nbsp;101|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/58 - Nièvre/index.html'>58 - Nièvre</a>|248|111(44%)|<img src="img/bar_6.gif" />&nbsp;44|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/59 - Nord/index.html'>59 - Nord</a>|3199|2076(64%)|<img src="img/bar_79.gif" />&nbsp;550|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/60 - Oise/index.html'>60 - Oise</a>|387|182(47%)|<img src="img/bar_15.gif" />&nbsp;109|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/61 - Orne/index.html'>61 - Orne</a>|167|48(28%)|<img src="img/bar_4.gif" />&nbsp;30|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/62 - Pas-de-Calais/index.html'>62 - Pas-de-Calais</a>|527|589(111%)|<img src="img/bar_12.gif" />&nbsp;89|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/63 - Puy-de-Dôme/index.html'>63 - Puy-de-Dôme</a>|1213|678(55%)|<img src="img/bar_24.gif" />&nbsp;172|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/64 - Pyrénées-Atlantiques/index.html'>64 - Pyrénées-Atlantiques</a>|679|348(51%)|<img src="img/bar_16.gif" />&nbsp;114|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/65 - Hautes-Pyrénées/index.html'>65 - Hautes-Pyrénées</a>|130|35(26%)|<img src="img/bar_3.gif" />&nbsp;23|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/66 - Pyrénées-Orientales/index.html'>66 - Pyrénées-Orientales</a>|339|86(25%)|<img src="img/bar_7.gif" />&nbsp;54|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/67 - Bas-Rhin/index.html'>67 - Bas-Rhin</a>|2702|2317(85%)|<img src="img/bar_54.gif" />&nbsp;378|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/68 - Haut-Rhin/index.html'>68 - Haut-Rhin</a>|498|393(78%)|<img src="img/bar_22.gif" />&nbsp;152|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/69M - Métropole de Lyon/index.html'>69M - Métropole de Lyon</a>|5486|3358(61%)|<img src="img/bar_100.gif" />&nbsp;690|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/70 - Haute-Saône/index.html'>70 - Haute-Saône</a>|16|4(25%)|<img src="img/bar_0.gif" />&nbsp;4|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/71 - Saône-et-Loire/index.html'>71 - Saône-et-Loire</a>|418|173(41%)|<img src="img/bar_12.gif" />&nbsp;84|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/72 - Sarthe/index.html'>72 - Sarthe</a>|802|442(55%)|<img src="img/bar_20.gif" />&nbsp;139|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/73 - Savoie/index.html'>73 - Savoie</a>|773|360(46%)|<img src="img/bar_17.gif" />&nbsp;119|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/74 - Haute-Savoie/index.html'>74 - Haute-Savoie</a>|1175|886(75%)|<img src="img/bar_31.gif" />&nbsp;214|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/75 - Paris/index.html'>75 - Paris</a>|6224|4356(69%)|<img src="img/bar_77.gif" />&nbsp;536|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/76 - Seine-Maritime/index.html'>76 - Seine-Maritime</a>|1222|664(54%)|<img src="img/bar_32.gif" />&nbsp;221|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/77 - Seine-et-Marne/index.html'>77 - Seine-et-Marne</a>|644|309(47%)|<img src="img/bar_20.gif" />&nbsp;141|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/78 - Yvelines/index.html'>78 - Yvelines</a>|1963|1131(57%)|<img src="img/bar_59.gif" />&nbsp;413|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/79 - Deux-Sèvres/index.html'>79 - Deux-Sèvres</a>|281|455(161%)|<img src="img/bar_9.gif" />&nbsp;65|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/80 - Somme/index.html'>80 - Somme</a>|765|526(68%)|<img src="img/bar_16.gif" />&nbsp;115|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/81 - Tarn/index.html'>81 - Tarn</a>|173|89(51%)|<img src="img/bar_7.gif" />&nbsp;54|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/82 - Tarn-et-Garonne/index.html'>82 - Tarn-et-Garonne</a>|48|16(33%)|<img src="img/bar_2.gif" />&nbsp;14|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/83 - Var/index.html'>83 - Var</a>|512|229(44%)|<img src="img/bar_10.gif" />&nbsp;69|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/84 - Vaucluse/index.html'>84 - Vaucluse</a>|402|315(78%)|<img src="img/bar_9.gif" />&nbsp;68|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/85 - Vendée/index.html'>85 - Vendée</a>|291|114(39%)|<img src="img/bar_8.gif" />&nbsp;62|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/86 - Vienne/index.html'>86 - Vienne</a>|328|181(55%)|<img src="img/bar_7.gif" />&nbsp;54|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/87 - Haute-Vienne/index.html'>87 - Haute-Vienne</a>|241|128(53%)|<img src="img/bar_10.gif" />&nbsp;74|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/88 - Vosges/index.html'>88 - Vosges</a>|79|55(69%)|<img src="img/bar_5.gif" />&nbsp;36|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/89 - Yonne/index.html'>89 - Yonne</a>|91|33(36%)|<img src="img/bar_3.gif" />&nbsp;27|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/90 - Territoire-de-Belfort/index.html'>90 - Territoire-de-Belfort</a>|173|110(63%)|<img src="img/bar_6.gif" />&nbsp;47|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/91 - Essonne/index.html'>91 - Essonne</a>|712|383(53%)|<img src="img/bar_30.gif" />&nbsp;210|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/92 - Hauts-de-Seine/index.html'>92 - Hauts-de-Seine</a>|2767|1797(64%)|<img src="img/bar_84.gif" />&nbsp;581|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/93 - Seine-Saint-Denis/index.html'>93 - Seine-Saint-Denis</a>|1061|741(69%)|<img src="img/bar_33.gif" />&nbsp;231|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/94 - Val-de-Marne/index.html'>94 - Val-de-Marne</a>|1302|757(58%)|<img src="img/bar_44.gif" />&nbsp;310|
|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/95 - Val-d_Oise/index.html'>95 - Val-d'Oise</a>|368|173(47%)|<img src="img/bar_13.gif" />&nbsp;90|
| **Total** |81005|50075(61%)|12998|
