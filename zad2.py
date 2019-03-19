import regex as r
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("./ustawy") if isfile(join("./ustawy", f))]
stats = {}

# dirs = [name for name in os.listdir("./ustawy")]
for f in onlyfiles: 
    with open(join("./ustawy", f), encoding='utf-8') as fi:
        artust_stats = {}
        art_stats = {}
        text = fi.read()
        # print(text)
        arti = r.findall(r'(Art\.\s\d+.)([\s\S]*?(?=Art\.\s\d+.))|(Art\.\s\d+.)([\s\S]*?)$', text)
        # print(f)
        if len(arti) != 0:
            arti[-1] = (arti[-1][2], arti[-1][3], '', '')
        
        # print(arti)
        for article in arti:
            arti_numbers = []
            art_number = r.findall(r'\d+', article[0])[0]
            # print(article[1])
            # print(article)
            # article_number = int(article[0])
            # print(article_number)
            references = r.findall(r'([aA]rt\.\s*\d{1,4}\s*[uU]st\.\s*[\d\S]+(?![\s\S]{0,10}(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*)\b)|[aA]rt\.[\si,\d]*(?![\s\S]{0,14}(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*)\b)|[uU]st\.\s*[\Si,\d-]*(?![\s\S]{0,10}(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*)\b))', article[1])
            # print(references)
            if len(references) != 0:
                for x in references:
                    for ref in x:
                        if len(ref) > 0:
                            # print(ref)
                            group = r.findall(r'([aA]rt\.\s*[\d i,-]+[uU]st.\s*[\d i,-]+)|([aA]rt\.\s*[\d i,-]+)|([uU]st.\s*[\d i,-]+)', ref)
                            # print(group)
                            if len(group) == 0:
                                break
                            tmp_group = group[0]

                            # print(group)
                            arti_numbers = []
                            ustep_numbers = []
                            if len(tmp_group[0]) > 0:
                                arti = r.findall(r'[\d -,i]+(?=[uU]st)', tmp_group[0])
                                if "-" in arti:
                                    tmp = r.findall(r'\d+', arti)
                                    arti_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    arti_numbers = r.findall(r'\d+', arti[0])
                                ustepy = r.findall(r'(?<=[uU]st\.)\s*[\d \-,i]+', tmp_group[0])
                                if "-" in ustepy:
                                    tmp = r.findall(r'\d+', ustepy)
                                    ustep_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    ustep_numbers = r.findall(r'\d+', ustepy[0])
                                for art_number in arti_numbers:
                                    if art_number not in art_stats:
                                        art_stats[art_number] = 1
                                    else:
                                        art_stats[art_number] += 1
                                    if art_number not in artust_stats:
                                        artust_stats[art_number] = {}
                                    for ust_number in ustep_numbers:
                                        if ust_number not in artust_stats[art_number]:
                                            artust_stats[art_number][ust_number] = 1
                                        else:
                                            artust_stats[art_number][ust_number] += 1
                            if len(tmp_group[1]) > 0:
                                arti = r.findall(r'[\d -,i]+', tmp_group[1])
                                if "-" in arti:
                                    tmp = r.findall(r'\d+', arti)
                                    arti_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    arti_numbers = r.findall(r'\d+', arti[0])
                                for art_number in arti_numbers:
                                    if art_number not in art_stats:
                                        art_stats[art_number] = 1
                                    else:
                                        art_stats[art_number] += 1
                            if len(tmp_group[2]) > 0:
                                ustepy = r.findall(r'[\d \-,i]+', tmp_group[2])
                                if "-" in ustepy:
                                    tmp = r.findall(r'\d+', ustepy)
                                    ustep_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    ustep_numbers = r.findall(r'\d+', ustepy[0])
                                if art_number not in artust_stats:
                                    artust_stats[art_number] = {}
                                if art_number not in art_stats:
                                    art_stats[art_number] = 1
                                else:
                                    art_stats[art_number] += 1
                                for ust_number in ustep_numbers:
                                    if ust_number not in artust_stats[art_number]:
                                        artust_stats[art_number][ust_number] = 1
                                    else:
                                        artust_stats[art_number][ust_number] += 1
                            
        # print(artust_stats)
        tuples_a = []
        tuples_u = []
        for a in art_stats.items():
            a_n = a[0]
            a_v = a[1]
            tuples_a.append((int(a_n), a_v))
        for au in artust_stats.items():
            a_n = au[0]
            # print(au)
            for u in au[1].items():
                # print(u)
                tuples_u.append((int(a_n), u[0], u[1]))
        tuples_a.sort(key=lambda tup: tup[1], reverse=True)
        tuples_u.sort(key=lambda tup: tup[2], reverse=True)

        save_file = open(join("./stats", "stats" + str(f)) ,'w')
        for ta in tuples_a:
            save_file.write("Art. " + str(ta[0]) + " [ " + str(ta[1]) + " ]\n")
        for tu in tuples_u:
            save_file.write("Art. " + str(tu[0]) + " ust. " + str(tu[1]) + " [ " + str(tu[2]) + " ]\n")
        





