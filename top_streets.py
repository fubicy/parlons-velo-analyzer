#!/bin/python
# -*- coding: UTF-8 -*-

# 2019 - Bruno Adele <brunoadele@gmail.com> #JeSuisUnDesDeux team

import os
import re
import csv
import sys
import shutil
import pprint

from collections import Counter

INSEE_TO_FANTOIR = {
    '13':
     {
         '055': [ 
            '201','202','203','204',
            '205','206','206','208',
            '209','210','211','212',
            '213','214','215','216',
            ]
     },
     
     '69': { 
        '123': [
            '381','382','383','384','385',
            '386','387','388','389',
        ]
     },
     '75': {
         '056': [
             '101','102','103','104','105',
             '106','107','108','109','110',
             '111','112','113','114','115',
             '116','117','118','119','120',
         ]
     }
}


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
    topstreets = Counter()

    for r in responses:
    #    question = questions[156]
        streets = []
        for dmot in dmots:
            if dmot in r['minimal_norm']:
                street = get_streetname(dmot,r['minimal_norm'],r['maximal_norm'])
                if street != '':
                    streets.append(street)

                    nb_responses_with_street += 1
                    if street not in topstreets: 
                        topstreets[street] = 0

                    topstreets[street] += 1

        # oneline = ' / '.join(str(street) for street in streets)

    return (nb_responses_with_street,topstreets)

def get_fantoir_filename_by_code(codedep,codecom):
    
    foldername = ""
    filename = ""

    for file in os.listdir("fantoir/"):
        # Add DOM-TOM identifier
        if codedep=="97":
            cdir = codecom[0:1]
            codedep=f"{codedep}{cdir}"

        if file.startswith(f"{codedep}-"):
            foldername = file
            break

    if foldername == "":
        return filename

    for file in os.listdir(f"fantoir/{foldername}/"):
        if file.startswith(f"{codecom}-"):
            filename = file
            break

    return f"fantoir/{foldername}/{filename}"

def readfantoir_file(fantoirfile):
    # Read FANTOIR file
    fantoirs=dict()
    with open(fantoirfile) as csvfile:
        fantoir = csv.DictReader(csvfile, delimiter=';')
        for line in fantoir:
            dmot = line['dmot']
            lstreet = line['lstreet']
            lstreet_norm = line['lstreet_norm']
            voie = line['voie']
            annulation = line['cann']

            if annulation=="" and len(lstreet_norm)>2:
                if dmot not in fantoirs:
                    fantoirs[dmot] = list()
                
                voiesize = len(voie)
                full_street = "%s %s".strip() % (voie,lstreet)
                full_street_norm = "%s %s".strip() % (voie,lstreet_norm)

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
                }
                fantoirs[dmot].append(datas)

    return fantoirs


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

        if data['full_street'] in text_minimal_norm:
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


            # Compare word distance from mainword (dmot)
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
    max_score_content = ""
    for score in scores:
        if score['percent_found']>50 and score['score']>max_score:
            max_score = score['score']

            if DEBUG:
                max_score_content = "%s (%s%%)" % (score['full_street'],score['percent_found'])
            else:
                max_score_content = "%s" % score['full_street']

    return max_score_content

def write_topstreets(fantoirfile,codedep,codetown,responses, results):
    global nb_responses_with_street

    # Get folder and filename from fantoir filename
    fantoirpath = fantoirfile.replace("fantoir/","")    
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

def write_main_results():
    # Write stats
    shutil.copyfile("README_template.md", "README.md")
    with open("README.md", 'a') as docfile:
        docfile.write("### Résultats par département\n\n")
        docfile.write("Sur l'ensemble du téritoire, il y a eu {} réponses dont {} réponses avec une rue citée ({}%)\n\n".format(stats['total']['nb_responses'],stats['total']['nb_responses_with_street'],stats['total']['nb_responses_with_street_percent']))
        docfile.write("| Departement | Nb réponses | Nb réponses avec rue | Nb points noirs |\n")
        docfile.write("|-------------|-------------|----------------------|-----------------|\n")

        for kd,v in sorted(stats['dep'].items()):
            docfile.write("|<a href='topstreets/{}/README.md'>{}</a>|{}|{}({}%)|{}|\n".format(v['title'],v['title'],v['nb_responses'],v['nb_responses_with_street'],v['nb_responses_with_street_percent'], v['nb_points_noirs']))             

        docfile.write("| **Total** |{}|{}({}%)|{}|\n".format(stats['total']['nb_responses'],stats['total']['nb_responses_with_street'],stats['total']['nb_responses_with_street_percent'], stats['total']['nb_points_noirs']))             


def write_departments_results():
    # Write stats
    for kd,d in sorted(stats['dep'].items()):

        deppath = "topstreets/{}".format(d['title'])
        os.mkdir(deppath)

        filename = f"{deppath}/README.md"

        with open(filename, 'w') as docfile:
            docfile.write("### Résultats pour le département de {}\n\n".format(d['title']))
            docfile.write("Sur l'ensemble du département, il y a eu {} réponses dont {} réponses avec une rue citée ({}%)\n\n".format(d['nb_responses'],d['nb_responses_with_street'],d['nb_responses_with_street_percent']))
            docfile.write("| Ville | Nb réponses | Nb réponses avec rue | Nb points noirs |\n")
            docfile.write("|-------------|-------------|----------------------|-----------------|\n")

            for kt, t in sorted(stats['dep'][kd]['towns'].items()):
                docfile.write("|<a href='{}.md'>{}</a>|{}|{}({}%)|{}|\n".format(t['title'],t['title'],t['nb_responses'],t['nb_responses_with_street'],t['nb_responses_with_street_percent'], t['nb_points_noirs']))             

            docfile.write("| **Total** |{}|{}({}%)|{}|\n".format(d['nb_responses'],d['nb_responses_with_street'],d['nb_responses_with_street_percent'], d['nb_points_noirs']))             


def write_towns_results():
    # Write stats
    for kd,d in sorted(stats['dep'].items()):
        deppath = "topstreets/{}".format(d['title'])
        for kt, t in sorted(stats['dep'][kd]['towns'].items()):
            townname = t['title']
            nb_responses = t['nb_responses']
            nb_responses_with_street = t['nb_responses_with_street']
            nb_responses_with_street_percent = t['nb_responses_with_street_percent']
            nb_points_noirs = t['nb_points_noirs']

            filename = f"{deppath}/{townname}.md"
            with open(filename, 'w') as docfile:
                docfile.write(f"# Résultat pour {townname}\n\n")
                docfile.write(f"Sur l'ensemble de la ville il y a eu {nb_responses} réponses dont {nb_responses_with_street} réponses avec une rue citée ({nb_responses_with_street_percent}%)\n\n")
                docfile.write(f"{nb_points_noirs} points noirs identifiés\n\n")

                docfile.write('| Rue | Vote | % réponses | % Nb rues cités|\n')
                docfile.write("|-----|------|------------|----------------|\n")

                total = 0
                for street,count in t['blackspots'].most_common():
                    total += count

                    striped_street = street.strip()
                    percent_responses = 0
                    percent_with_street = 0

                    if nb_responses > 0:
                        percent_responses = int(count/nb_responses*100.0)

                    if nb_responses_with_street>0:
                        percent_with_street = int(count/nb_responses_with_street*100.0)
                    
                    docfile.write(f"| {striped_street} | {count} | {percent_responses}% | {percent_with_street}%|\n")

                # Total
                if nb_responses > 0:
                    percent_responses = int(total/nb_responses*100.0)

                if nb_responses_with_street>0:
                    percent_with_street = int(total/nb_responses_with_street*100.0)
                docfile.write(f"| **Total** | {total} | {percent_responses}% | {percent_with_street}%|\n")



def analyze_all_responses():
    global stats
    global dmots
    global INSEE_TO_FANTOIR
    global nb_responses_with_street

    files = os.listdir('datas/')
    for filename in files:

        codedep = filename[0:2]
        codecom = filename[2:5]
        codetown = f"{codedep}{codecom}"

        # Convert INSEE code town to FANTOIR code town
        if codedep in INSEE_TO_FANTOIR and codecom in INSEE_TO_FANTOIR[codedep]:
            codecom_list = INSEE_TO_FANTOIR[codedep][codecom]
        else:
            codecom_list = [codecom]

        # Loop for search street in district town       
        for codecom_replaced in codecom_list:

            # Compute topstreet path
            fantoirfullfilename = get_fantoir_filename_by_code(codedep,codecom_replaced)
            firstlash = fantoirfullfilename.find("/")
            lastslash = fantoirfullfilename.rfind("/")
            titledep = fantoirfullfilename[firstlash+1:lastslash]
            topstreetpath = "topstreets/%s" % titledep

            # Compute tpwn top street filename
            townresultfilename = fantoirfullfilename[lastslash+1:].replace('.csv','.md')
            titletown = townresultfilename.replace(".md","")
            topstreets_filename=f"{topstreetpath}/{townresultfilename}"

            print(f"Analyse response for {titledep}/{titletown}")
            try:
                nb_responses_with_street = 0

                dmots = readfantoir_file(fantoirfullfilename)
                responses = load_response(f"datas/{filename}")
                nb_responses_with_street,blackspots = detect_all_streets(dmots,responses)
                top = blackspots.most_common(10)

                # Init department counter
                if codedep not in stats['dep']:
                    stats['dep'][codedep] = {
                        'codecoms': [],
                        'towns': {},
                        'title': titledep,
                        'nb_responses': 0,
                        'nb_responses_with_street': 0,
                        'nb_points_noirs': 0
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
                    'title': titletown,
                    'mustcount': mustcount,
                    'nb_responses': len(responses),
                    'nb_responses_with_street': nb_responses_with_street,
                    'nb_responses_with_street_percent': ratiotown,
                    'nb_points_noirs': len(blackspots),
                    'blackspots':blackspots
                }

                # Update department and total counter
                stats['dep'][codedep]['nb_responses_with_street'] += nb_responses_with_street
                stats['dep'][codedep]['nb_points_noirs'] += len(blackspots)
                stats['total']['nb_responses_with_street'] += nb_responses_with_street
                stats['total']['nb_points_noirs'] += len(blackspots)

                # Update department ratio
                ratiodep = 0
                if len(responses)>0:
                    ratiodep = int(stats['dep'][codedep]['nb_responses_with_street']/stats['dep'][codedep]['nb_responses'] * 100.0)

                stats['dep'][codedep]['nb_responses_with_street_percent'] = ratiodep

                # Update total ratio
                ratiototal = int(stats['total']['nb_responses_with_street']/stats['total']['nb_responses'] * 100.0)
                stats['total']['nb_responses_with_street_percent'] = ratiototal
                
                #write_topstreets(fantoirfullfilename,codedep,codecom,responses,top)

            except KeyboardInterrupt:
                sys.exit()

            except IsADirectoryError:
                pass
                print("IsADirectoryError")
                print(f"#### ERROR for Analyse {codetown} {fantoirfullfilename}".replace("fantoir/",""))

            except FileNotFoundError:
                pass
                print("FileNotFoundError")
                print(f"#### ERROR for Analyse {codetown} {fantoirfullfilename}".replace("fantoir/",""))


DEBUG=False
dmots = dict()
stats = {
    'total': {
        'nb_responses': 0,
        'nb_responses_with_street': 0,
        'nb_points_noirs': 0,
    },
    'dep': {

    }
}

analyze_all_responses()

# Delete previous results
shutil.rmtree('topstreets',ignore_errors=True)
os.mkdir('topstreets')

# Write all datas
write_main_results()
write_departments_results()
write_towns_results()