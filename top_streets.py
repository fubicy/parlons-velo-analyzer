#!/bin/python
# -*- coding: UTF-8 -*-

# 2019 - Bruno Adele <brunoadele@gmail.com> #JeSuisUnDesDeux team

import os
import re
import csv
import sys
import json
import shutil
import branca
import folium
import overpass

from collections import Counter

TOPLIST=[10,30,50,1000]

MAP_WIDTH=700
MAP_HEIGHT=500

# Folium
# LINES_COLOR = [
#     "#00E6CC",
#     "#00CC7F",
#     "#00B300",
#     "#7FCC00",
#     "#CCE600",
#     "#FFFF00",
#     "#FFCC00",
#     "#FF9900",
#     "#FF6600",
#     "#FF0000",
#     "#CC0000",
#     "#cc00ff",
#     "#5500ff",
#     "#000000"
# ]
# LINES_COLOR = [
#     "#5200ff",
#     "#4b00ea",
#     "#4400d4",
#     "#3e00bf",
#     "#3700aa",
#     "#300095",
#     "#290080",
#     "#22006a",
#     "#1b0055",
#     "#150040",
#     "#0e002b",
#     "#070015",
#     "#000000",
# ]

# LINES_COLOR = [
#     "#afd423",
#     "#5dbf30",
#     "#39aa4c",
#     "#3e9576",
#     "#407880",
#     "#3e4f6a",
#     "#3b3955",
#     "#393040",
#     "#2b232a",
#     "#151314",
#     "#000000",
# ]

LINES_COLOR = [
    "#ff4000",
    "#ea3b00",
    "#d43500",
    "#bf3000",
    "#aa2b00",
    "#952500",
    "#802000",
    "#6a1b00",
    "#551500",
    "#401000",
    "#2b0b00",
    "#150500",
    "#000000",
]


MIN_LINE_WIDTH=5
MAX_LINE_WIDTH=5+len(LINES_COLOR)
SRC_RANGE=MAX_LINE_WIDTH-MIN_LINE_WIDTH

# Replace short word
REPLACE_WORDS = {
    'AVENUE ':['AV '],
    'BOULEVARD ':['BD '],
    'SAINT ':['ST '],
    'ROUTE ':['RTE '],
    'DOCTEUR': ['DR '],
    }

# Replace common words
REDUCE_WORDS = {
    ' ':['D ','DE ','LA ','DU '],
    }

# Remove accents
REMOVE_SYMBOLS_ACCENTS = {
    'A':[u'Â',u'À'],
    'C':[u'Ç'],
    'E':[u'È',u'Ê',u'É',u'Ë'],
    'I':[u'Ï',u'Î'],
    'O':[u'Ö',u'Ô'],
    'U':[u'Û',u'Ü'],
    ' ': ['-','\'','"','/','.']
    }


def load_response(filename):
    addrs = list()
    normalized = list()
    with open(filename) as csvfile:
        responses = csv.DictReader(csvfile, delimiter=';',quotechar='"')
        for r in responses:
            addrs.append(r["Points noirs"])


    for addr in addrs:
        minimal_norm = replace_words(REPLACE_WORDS,normalize(addr))
        maximal_norm =  replace_words(REDUCE_WORDS,minimal_norm)

        datas = {
            'minimal_norm': minimal_norm,
            'maximal_norm': maximal_norm,
        }
        
        normalized.append(datas)

    return normalized

def detect_all_streets(dmots, responses):
    nb_responses_with_street = 0
    topstreets = dict()

    for r in responses:
    #    question = questions[156]
        streets = []
        for dmot in dmots:
            if dmot in r['minimal_norm']:
                street = get_streetname(dmot,r['minimal_norm'],r['maximal_norm'])
                if street is not None :
                    streets.append(street)

                    nb_responses_with_street += 1
                    if street['full_street'] not in topstreets: 
                        street['responses_with_this_street'] = 0
                        topstreets[street['full_street']] = street

                    topstreets[street['full_street']]['responses_with_this_street'] += 1

        # oneline = ' / '.join(str(street) for street in streets)

    return (nb_responses_with_street,topstreets)

def get_OSM_filename_by_code(insee,rootdir='osm',level=0):
    
    codedep = insee[0:2]
    for root, directories, filenames in os.walk(rootdir):
        for filename in filenames: 
            if filename.startswith('streets.csv'):
                if insee in root:
                    return os.path.join(root,filename)

        for directory in directories:
            if (level == 1 and directory.startswith(codedep)) or (level == 2 and directory.startswith(insee)):
                folder = os.path.join(root,directory) 
                get_OSM_filename_by_code(insee,folder,level+1)

    return None

def readOSMVilles():
    global villes_info

    filename = 'osm/villes.csv'
    with open(filename) as csvfile:
        OMSlines = csv.DictReader(csvfile, delimiter=';')
        for line in OMSlines:
            villes_info[line['ville_insee']] = line

def readOSMStreetFile(OSMfile):
    # Read FANTOIR file
    osms=dict()
    with open(OSMfile) as csvfile:
        OMSlines = csv.DictReader(csvfile, delimiter=';')
        for line in OMSlines:
            dmot = line['last_word_norm']
            name = line['name']
            name_norm = line['name_norm']
            voie = line['voie']
            ways = line['ways']

            if dmot not in osms:
                osms[dmot] = list()
            
            voiesize = len(voie)
            full_street = f"{name}".strip()
            full_street_norm = f"{voie} {name_norm}".strip()

            full_street_norm_size = len(full_street_norm)
            nb_blocks=len(full_street.split())
            nb_blocks_norm=len(full_street_norm.split())

            pos = 0
            words = []
            for word in full_street_norm.split():
                wordsinfo = {
                    "is_typevoie": voie==word,
                    "word":word,
                    "pos": pos,
                    "size":len(word)
                }
                words.append(wordsinfo)
                pos += len(word)+1 # Add space

            datas = {
                'words': words,
                'full_street': full_street,
                'full_street_norm': full_street_norm,
                'nb_blocks': nb_blocks,
                'nb_blocks_norm': nb_blocks_norm,
                'size': full_street_norm_size,
                'ways': ways
            }
            osms[dmot].append(datas)

    return osms


# Replace dict word
def replace_words(words, text):
    beforesize = len(text)
    for word in iter(words):
        for search in words[word]:
            if text.find(search)==0:
                # Begin word
                text = text.replace(search,word)  
            else:
                search = " %(search)s" % locals()
                text = text.replace(search,word)

    return text

# Normalize texte, remove accents, common words, etc ...
def normalize(text):
    text = text.upper()

    # Remove accent
    for c in iter(REMOVE_SYMBOLS_ACCENTS):
        for r in REMOVE_SYMBOLS_ACCENTS[c]:
            text = text.replace(r,c)    

    # Remove multiple spaces
    text = " ".join(text.split())

    text = re.sub(r'<BR.*?>', ' ', text,flags=re.MULTILINE)
    text = text.replace('PAS DE SAISIE','')

    text = text.strip()

    return text

def get_words_list(word,text):
    pos_list = []

    try:
        tmp_pos_list = [m.start() for m in re.finditer(word, text)]

        for idx in tmp_pos_list:
            wordsize = len(word)
            textsize = len(text)
            
            #Search word
            searchedtext = text[idx-1:idx+wordsize+1].strip().split()
            if word in searchedtext:
                pos_list.append(idx)

    except:
        pass

    return pos_list

# Try detect a street in text content
def get_streetname(dmot,text_minimal_norm,text_maximal_norm):
    global dmots
    
    scores = []
    for street in dmots[dmot]:
        if DEBUG:
            print("TEXT: %s" % text_minimal_norm)
            print ("FULL STREET: %s" % street['full_street'])
            print ("FULL STREET NORM: %s" % street['full_street_norm'])


        words_idxs = []
        data = dict(street)
        data['score'] = 0

        if data['full_street_norm'] in text_minimal_norm:
            # Check if voie tpe is in address
            data['found_voie'] = 0
            data['nb_blocks_found'] = 0
            if data['words'][0]['is_typevoie']:
                data['found_voie'] = 1
                data['nb_blocks_found'] = data['nb_blocks']

            data['percent_found'] = 100
            data['score'] = data['found_voie']*1000000+data['percent_found']*1000+data['nb_blocks_found']
            scores.append(data)
            break
        else:    
            # search all occurences index
            mainword_idx = -1
            idx = 0
            for word in data['words']:
                word['mainword'] = word['word']==dmot
                if word['mainword']:
                    mainword_idx = idx

                word['found_pos'] = get_words_list(word['word'], text_maximal_norm)
                idx +=1 


            for pos in data['words'][mainword_idx]['found_pos']:
                data['nb_blocks_found'] = 0
                data['found_voie'] = 0
                for word in data['words']:
                    postrequested = pos-(data['words'][mainword_idx]['pos']-word['pos'])
                    
                    if postrequested in word['found_pos']:
                        if word['is_typevoie']:
                            data['found_voie']=1

                        data['nb_blocks_found'] += 1

                data['percent_found'] = int((data['nb_blocks_found']/float(data['nb_blocks']))*100)
                if data['percent_found']==100:
                    data['percent_found'] = 99 # set 99% because some words remove ex: DE LA
                data['score'] = data['found_voie']*1000000+data['percent_found']*1000+data['nb_blocks_found']
                
                # DEBUG
                if DEBUG:
                    print ("Found voie(bool): %s" % data['found_voie'])
                    print ("Nb blocks found: %s(%s)" % (data['nb_blocks_found'],data['nb_blocks']))
                    print ("Percent_found: %s" % data['percent_found'])
                    print ("score: %s" % data['score'])
                    print(data)
                    print ("")

                scores.append(data)

    # Get a best street scrore
    max_score = 0
    max_score_content = None
    for score in scores:
        if score['percent_found']>50 and score['score']>max_score:
            max_score = score['score']

            # if DEBUG:
            #     max_score_content = f"{score['full_street']} ({score['percent_found']}%)"
            # else:
            #     max_score_content = score['full_street']
            max_score_content = score
    return max_score_content

def write_topstreets(OSMfile,codedep,insee,responses, results):
    global nb_responses_with_street

    # Get folder and filename from fantoir filename
    fantoirpath = OSMfile.replace("fantoir/","")    
    lastslash = fantoirpath.rfind("/")
    path = "topstreets/%s" % fantoirpath[0:lastslash]
    filename = fantoirpath[lastslash+1:].replace('.csv','.md')
    title = filename.replace(".md","")
    topstreets_filename=f"{path}/{filename}"

    # Create topstreets path
    os.makedirs(path,exist_ok=True)

    with open(topstreets_filename, 'w') as markdown:
        nb_responses = len(responses)
        taux = int(nb_responses_with_street/nb_responses*100.0)
        markdown.write(f"# Résultat pour {title}\n\n")
        markdown.write(f"Sur {nb_responses} réponses dont {nb_responses_with_street} avec une rue cité (taux réussite {taux}%)\n\n")
        
        markdown.write('| Rue | Vote | % réponses | % Nb rues cités|\n')
        markdown.write("|-----|------|------------|----------------|\n")
        for line in results:
            street,count = line
            
            striped_street = street.strip()
            percent_responses = int(count/nb_responses*100.0)
            percent_with_street = int(count/nb_responses_with_street*100.0)
            markdown.write(f"| {striped_street} | {count} | {percent_responses}% | {percent_with_street}%|\n")

def html_percent_bar(root,percent):
    html=f'<img src="{root}/bar_{percent}.gif" />'

    return html

def write_main_readme():
    # Write stats
    shutil.copyfile("README_template.md", "README.md")
    with open("README.md", 'a') as docfile:
        docfile.write("### Résultats par département\n\n")
        docfile.write(f"Sur l'ensemble du téritoire, il y a eu {stats['total']['nb_responses']} réponses dont {stats['total']['nb_responses_with_street']} réponses avec une rue citée ({stats['total']['nb_responses_with_street_percent']}%)\n\n")
        docfile.write("| Departement | Nb réponses | Nb réponses avec rue | Nb points noirs |\n")
        docfile.write("|-------------|-------------|----------------------|-----------------|\n")

        for kd,v in sorted(stats['dep'].items()):
            backspots_percent = int(v['nb_points_noirs']/stats['total']['max_nb_points_noirs']*100.0)
            percent_bar = html_percent_bar('img',backspots_percent)

            path = v['title'].replace("'","_")
            docfile.write(f"|<a href='https://fubicy.github.io/parlons-velo-analyzer/topstreets/{path}/index.html'>{v['title']}</a>|{v['nb_responses']}|{v['nb_responses_with_street']}({v['nb_responses_with_street_percent']}%)|{percent_bar}&nbsp;{v['nb_points_noirs']}|\n")             

        docfile.write(f"| **Total** |{stats['total']['nb_responses']}|{stats['total']['nb_responses_with_street']}({stats['total']['nb_responses_with_street_percent']}%)|{stats['total']['nb_points_noirs']}|\n")             

def write_main_html():

    deps_info = ""
    for kd,v in sorted(stats['dep'].items()):
        backspots_percent = int(v['nb_points_noirs']/stats['total']['max_nb_points_noirs']*100.0)
        percent_bar = html_percent_bar('img',backspots_percent)
        
        path = v['title'].replace("'","_")
        deps_info += f"<tr><td><a href='topstreets/{path}/index.html'>{v['title']}</a></td><td>{v['nb_responses']}</td><td>{v['nb_responses_with_street']}({v['nb_responses_with_street_percent']}%)</td><td>{percent_bar}&nbsp;{v['nb_points_noirs']}</td></tr>\n"


    deps_info += f"<tr><td><strong>Total</strong></td><td>{stats['total']['nb_responses']}</td><td>{stats['total']['nb_responses_with_street']}({stats['total']['nb_responses_with_street_percent']}%)</td><td>{stats['total']['nb_points_noirs']}</td></tr>\n"

    # Write html stats
    with open("index_main_template.html", "r") as templatefile:
        template_content = templatefile.read()

    ## Replace vars template
    htmlcontent = template_content.replace("{{NB_RESPONSES}}",str(stats['total']['nb_responses']))
    htmlcontent = htmlcontent.replace("{{NB_RESPONSES_WITH_STREET}}",str(stats['total']['nb_responses_with_street']))
    htmlcontent = htmlcontent.replace("{{NB_RESPONSES_PERCENT}}",str(stats['total']['nb_responses_with_street_percent']))
    htmlcontent = htmlcontent.replace("{{DEPARTEMENTS_LIST}}",deps_info)

    with open('index.html', 'w') as htmlfile:
        htmlfile.write(htmlcontent)


def write_departments_readme():
    # Write stats
    for kd,d in sorted(stats['dep'].items()):

        path = d['title'].replace("'","_")
        deppath = f"topstreets/{path}"
        os.makedirs(deppath,exist_ok=True)

        filename = f"{deppath}/README.md"

        with open(filename, 'w') as docfile:
            docfile.write(f"### Résultats pour le département de {d['title']}\n\n")
            docfile.write(f"Sur l'ensemble du département, il y a eu {d['nb_responses']} réponses dont {d['nb_responses_with_street']} réponses avec une rue citée ({d['nb_responses_with_street_percent']}%)\n\n")
            docfile.write("| Ville | Nb réponses | Nb réponses avec rue | Nb points noirs |\n")
            docfile.write("|-------------|-------------|----------------------|-----------------|\n")

            for kt, t in sorted(stats['dep'][kd]['towns'].items()):
                backspots_percent = 0
                if stats['dep'][kd]['max_nb_points_noirs'] > 0:
                    backspots_percent = int(t['nb_points_noirs']/stats['dep'][kd]['max_nb_points_noirs']*100.0)
                
                percent_bar = html_percent_bar('../../img',backspots_percent)
                tfile = t['title'].replace("'","_")
                
                if t['nb_points_noirs']>0:
                    links = ""
                    
                    lasttopvalue = 0
                    for top in TOPLIST:
                        mintop = min(top,t['nb_points_noirs'])
                        if mintop != lasttopvalue:
                            links += f"&nbsp;&#124;&nbsp;<a href='{tfile}_top{mintop}.md'>Top {top}</a>"
                            lasttopvalue = mintop
                    
                    docfile.write(f"|{t['title']}{links}|{t['nb_responses']}|{t['nb_responses_with_street']}({t['nb_responses_with_street_percent']}%)|{percent_bar}&nbsp;{t['nb_points_noirs']}|\n")             
                else:
                    docfile.write(f"|{t['title']}|{t['nb_responses']}|{t['nb_responses_with_street']}({t['nb_responses_with_street_percent']}%)|{percent_bar}&nbsp;{t['nb_points_noirs']}|\n")             


            docfile.write(f"| **Total** |{d['nb_responses']}|{d['nb_responses_with_street']}({d['nb_responses_with_street_percent']}%)|{d['nb_points_noirs']}|\n")             

def write_departments_html():
    # Write stats
    for kd,d in sorted(stats['dep'].items()):

        path = d['title'].replace("'","_")
        deppath = f"topstreets/{path}"
        os.makedirs(deppath,exist_ok=True)
        filename = f"{deppath}/index.html"

        cities_info = ""
        for kt, t in sorted(stats['dep'][kd]['towns'].items()):
            backspots_percent = 0
            if stats['dep'][kd]['max_nb_points_noirs'] > 0:
                backspots_percent = int(t['nb_points_noirs']/stats['dep'][kd]['max_nb_points_noirs']*100.0)
            
            percent_bar = html_percent_bar('../../img',backspots_percent)
            tfile = t['title'].replace("'","_")

            if t['nb_points_noirs']>0:
                links = ""
                
                lasttopvalue = 0
                for top in TOPLIST:
                    mintop = min(top,t['nb_points_noirs'])
                    if mintop != lasttopvalue:
                        links += f"&nbsp;|&nbsp;<a href='{tfile}_top{mintop}.html'>Top&nbsp;{mintop}</a>"
                        lasttopvalue = mintop

                nospace_title = t['title'].replace(" ","&nbsp;")
                cities_info += f"<tr><td>{nospace_title}{links}</td><td>{t['nb_responses']}</td><td>{t['nb_responses_with_street']}({t['nb_responses_with_street_percent']}%)</td><td>{percent_bar}&nbsp;{t['nb_points_noirs']}</td></tr>\n"             
            else:
                cities_info += f"<tr><td>{t['title']}</td><td>{t['nb_responses']}</td><td>{t['nb_responses_with_street']}({t['nb_responses_with_street_percent']}%)</td><td>{percent_bar}&nbsp;{t['nb_points_noirs']}</td></tr>\n"             

        cities_info += f"<tr><td> <strong>Total</strong> </td><td>{d['nb_responses']}</td><td>{d['nb_responses_with_street']}({d['nb_responses_with_street_percent']}%)</td><td>{d['nb_points_noirs']}</td></tr>\n"

        # Write html stats
        with open("index_departement_template.html", "r") as templatefile:
            template_content = templatefile.read()

        ## Replace vars template
        htmlcontent = template_content.replace("{{DEPARTEMENT_NAME}}",d['title'])
        htmlcontent = htmlcontent.replace("{{NB_RESPONSES}}",str(d['nb_responses']))
        htmlcontent = htmlcontent.replace("{{NB_RESPONSES_WITH_STREET}}",str(d['nb_responses_with_street']))
        htmlcontent = htmlcontent.replace("{{NB_RESPONSES_PERCENT}}",str(d['nb_responses_with_street_percent']))
        htmlcontent = htmlcontent.replace("{{CITIES_LIST}}",cities_info)

        with open(filename, 'w') as htmlfile:
            htmlfile.write(htmlcontent)


def write_towns_result():
    # Write stats
    for kd,d in sorted(stats['dep'].items()):
        path = d['title'].replace("'","_")
        deppath = f"topstreets/{path}"
        for kt, t in sorted(stats['dep'][kd]['towns'].items()):
            if t['nb_points_noirs']==0:
                continue

            insee = t['insee']
            lat = float(villes_info[insee]['lat'])
            lon = float(villes_info[insee]['lon'])
            lasttopvalue = 0
            for top in TOPLIST:
                m = folium.Map(location=[ lat, lon],height=MAP_HEIGHT,width=MAP_WIDTH,zoom_start=13)


                mintop = min(top,t['nb_points_noirs'])
                if mintop == lasttopvalue:
                    continue

                lasttopvalue = mintop
                tfile = t['title'].replace("'", " ")
                docfilename = f"{deppath}/{tfile}_top{mintop}.md"
                mapfilename = f"{deppath}/{tfile}_top{mintop}.html"
                html_streets_list = ""
                try:
                    with open(docfilename, 'w') as docfile:
                        docfile.write(f"# Résultat pour {t['title']}\n\n")
                        docfile.write(f"Sur l'ensemble de la ville il y a eu {t['nb_responses']} réponses dont {t['nb_responses_with_street']} réponses avec une rue citée ({t['nb_responses_with_street_percent']}%)\n\n")
                        docfile.write(f"{t['nb_points_noirs']} points noirs identifiés\n\n")

                        docfile.write('| Rue | Vote | % / les rues cités|\n')
                        docfile.write("|-----|------|-------------------|\n")

                        # Compute total response with street
                        top_total_response_with_street = 0
                        for full_street,street_info in sorted(t['blackspots'].items(), reverse=True, key=lambda item: (item[1]['responses_with_this_street'], item[0]))[:top]:
                            top_total_response_with_street += street_info['responses_with_this_street']

                        # Compute min/max percent response
                        max_percent = 0
                        for full_street,street_info in sorted(t['blackspots'].items(), reverse=True, key=lambda item: (item[1]['responses_with_this_street'], item[0]))[:top]:
                            if top_total_response_with_street>0:
                                percent_with_street = int(street_info['responses_with_this_street']/top_total_response_with_street*100.0)

                                if percent_with_street > max_percent:
                                    max_percent = percent_with_street

                        # Compute line ratio
                        ratio_line = max_percent/SRC_RANGE

                        idx = 0
                        for full_street,street_info in sorted(t['blackspots'].items(), reverse=True, key=lambda item: (item[1]['responses_with_this_street'], item[0]))[:top]:
                            idx += 1
                            percent_with_street = int(street_info['responses_with_this_street']/top_total_response_with_street*100.0)
                            bar_percent = html_percent_bar('../../img',percent_with_street)
                            docfile.write(f"| {full_street} | {street_info['responses_with_this_street']} | {bar_percent}&nbsp;{percent_with_street}%|\n")
                            html_streets_list += f"<tr><td> {full_street} </td><td> {street_info['responses_with_this_street']} </td><td> {bar_percent}&nbsp;{percent_with_street}%</td></tr>\n"

                            # Get geojson streetfile
                            jways = api.get(f"way(id:{street_info['ways']})",responseformat='geojson',verbosity='geom')
                            idxcolor = round(percent_with_street/ratio_line)
                            linewidth = idxcolor+MIN_LINE_WIDTH
                            for feature in jways['features']:
                                feature['properties']['line_width'] = linewidth
                                feature['properties']['line_color'] = LINES_COLOR[idxcolor-1]

                            gjsonfilename = f"{deppath}/{tfile}_top{mintop}_street_{idx}.geojson"
                            with open(gjsonfilename, 'w') as gjsonfile:
                                gjsonfile.write(json.dumps(jways, indent=4, separators=(',', ': ')))

                            full_street = full_street.strip()
                            style_function = lambda x: {
                                'fillOpacity': 1,
                                'weight': x['properties']['line_width'],
                                'color': x['properties']['line_color']
                            }

                            folium.GeoJson(
                                gjsonfilename,
                                name=f"{idx} - {full_street}",
                                style_function=style_function
                            ).add_to(m)


                        # Total
                        if top_total_response_with_street>0:
                            percent_with_street = int(top_total_response_with_street/top_total_response_with_street*100.0)
                            docfile.write(f"| **Total** | {top_total_response_with_street} | {percent_with_street}%|\n")
                            html_streets_list += f"<tr><td> <strong>Total</strong> </td><td> {top_total_response_with_street} </td><td> {percent_with_street}%</td></tr>\n"

                        # # Generate Map
                        # allways = ','.join(ways)
                    
                    if top_total_response_with_street>0:
                        # Read html ville template
                        with open("index_ville_template.html", "r") as templatefile:
                            template_content = templatefile.read()

                        ## Summaries town
                        htmlcontent = template_content.replace("{{TOWN_NAME}}",t['title'])
                        htmlcontent = htmlcontent.replace("{{TOPVALUE}}",str(mintop))
                        htmlcontent = htmlcontent.replace("{{NB_RESPONSES}}",str(t['nb_responses']))
                        htmlcontent = htmlcontent.replace("{{NB_RESPONSES_WITH_STREET}}",str(t['nb_responses_with_street']))
                        htmlcontent = htmlcontent.replace("{{NB_RESPONSES_PERCENT}}",str(t['nb_responses_with_street_percent']))
                        htmlcontent = htmlcontent.replace("{{NB_POINTS_NOIRS}}",str(t['nb_points_noirs']))

                        # leaflet Map
                        div_width=MAP_WIDTH+200

                        # Color map
                        levels = len(LINES_COLOR)
                        cm     = branca.colormap.LinearColormap(LINES_COLOR, vmin=0, vmax=max_percent).to_step(levels)
                        cm.caption = '% Criticité point noir'
                        m.add_child(cm)

                        # Street name layer control
                        folium.LayerControl().add_to(m)

                        iframe_map = m._repr_html_()
                        htmlcontent = htmlcontent.replace("{{MAP_CONTENT}}",iframe_map)
                        htmlcontent = htmlcontent.replace('<div style="width:100%;"><div style="position:relative;width:100%;',f'<div style="width:{div_width}px;"><div style="position:relative;width:100%;')
                        htmlcontent = htmlcontent.replace("{{STREETS_LIST}}",html_streets_list)

                        #m.save(mapfilename)
                        with open(mapfilename, 'w') as htmlfile:
                            htmlfile.write(htmlcontent)
                except IOError:
                    print (f"##### cannot generate a files for {kt}")


def analyze_all_responses():
    global stats
    global dmots
    global nb_responses_with_street

    files = os.listdir('datas/')
    for filename in files:
        codedep = filename[0:2]
        codecom = filename[2:5]
        insee = f"{codedep}{codecom}"

        codecom_list = [codecom]

        # Loop for search street in district town           
        for codecom_replaced in codecom_list:


            # Compute topstreet path
            OSMfullfilename = get_OSM_filename_by_code(insee)
            if OSMfullfilename is None:
                print(f" ###### {insee} not found")
                break

            firstlash = OSMfullfilename.find("/")
            nextslash = OSMfullfilename.find("/",firstlash+1)
            lastslash = OSMfullfilename.rfind("/")
            titledep = OSMfullfilename[firstlash+1:nextslash]
            titletown = OSMfullfilename[nextslash+1:lastslash]
            topstreetpath = "topstreets/%s" % titledep

            # Compute tpwn top street filename
            topstreets_filename=f"{topstreetpath}/{titletown}.md"

            print(f"Analyse response for {titledep}/{titletown}")
            try:
                nb_responses_with_street = 0

                dmots = readOSMStreetFile(OSMfullfilename)
                responses = load_response(f"datas/{filename}")
                nb_responses_with_street,blackspots = detect_all_streets(dmots,responses)

                # Init department counter
                if codedep not in stats['dep']:
                    stats['dep'][codedep] = {
                        'codecoms': [],
                        'towns': {},
                        'title': titledep,
                        'nb_responses': 0,
                        'nb_responses_with_street': 0,
                        'nb_points_noirs': 0,
                        'max_nb_points_noirs': 0,
                    } 

                topstreets_filename=f"topstreets/{titledep}/{titletown}.md"
                
                # Do not re-count the districts town again
                mustcount = False
                if codecom not in stats['dep'][codedep]['codecoms']:
                    mustcount = True
                    # Department
                    stats['dep'][codedep]['codecoms'].append(codecom)
                    stats['dep'][codedep]['nb_responses'] += len(responses)
                    
                    # Total
                    stats['total']['nb_responses'] += len(responses)

                ratiotown = 0
                if len(responses)>0:
                    ratiotown = int(nb_responses_with_street/len(responses) * 100.0)

                # Set town counter
                stats['dep'][codedep]['towns'][codecom_replaced]= {
                    'insee': insee,
                    'title': titletown,
                    'mustcount': mustcount,
                    'nb_responses': len(responses),
                    'nb_responses_with_street': nb_responses_with_street,
                    'nb_responses_with_street_percent': ratiotown,
                    'nb_points_noirs': len(blackspots),
                    'blackspots':blackspots,
                }

                # Update department and total counter
                stats['dep'][codedep]['nb_responses_with_street'] += nb_responses_with_street
                stats['dep'][codedep]['nb_points_noirs'] += len(blackspots)
                stats['dep'][codedep]['max_nb_points_noirs'] = max(stats['dep'][codedep]['max_nb_points_noirs'],stats['dep'][codedep]['nb_points_noirs'])
                stats['total']['nb_responses_with_street'] += nb_responses_with_street
                stats['total']['nb_points_noirs'] += len(blackspots)
                stats['total']['max_nb_points_noirs'] = max(stats['total']['max_nb_points_noirs'],stats['dep'][codedep]['nb_points_noirs'])

                # Update department ratio
                ratiodep = 0
                if len(responses)>0:
                    ratiodep = int(stats['dep'][codedep]['nb_responses_with_street']/stats['dep'][codedep]['nb_responses'] * 100.0)

                stats['dep'][codedep]['nb_responses_with_street_percent'] = ratiodep

                # Update total ratio
                ratiototal = int(stats['total']['nb_responses_with_street']/stats['total']['nb_responses'] * 100.0)
                stats['total']['nb_responses_with_street_percent'] = ratiototal
                
                #write_topstreets(OSMfullfilename,codedep,codecom,responses,top)

            except KeyboardInterrupt:
                sys.exit()

            except IsADirectoryError:
                pass
                print("IsADirectoryError")
                print(f"#### ERROR for Analyse {insee} {OSMfullfilename}".replace("fantoir/",""))

            except FileNotFoundError:
                pass
                print("FileNotFoundError")
                print(f"#### ERROR for Analyse {insee} {OSMfullfilename}".replace("fantoir/",""))


DEBUG=False
dmots = dict()
villes_info = dict()
stats = {
    'total': {
        'nb_responses': 0,
        'nb_responses_with_street': 0,
        'nb_points_noirs': 0,
        'max_nb_points_noirs': 0,
    },
    'dep': {

    }
}

endpoint = "http://localhost/api/interpreter"
timeout=600
api = overpass.API(endpoint=endpoint,timeout=600,debug=True)


# Read osm-tools villes.csv information
readOSMVilles()

# Analyse FUB responses
analyze_all_responses()

# Delete previous results
shutil.rmtree('topstreets',ignore_errors=True)
os.mkdir('topstreets')

# Write all datas
write_main_readme()
write_main_html()

write_departments_readme()
write_departments_html()

write_towns_result()