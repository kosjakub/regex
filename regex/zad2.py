import regex as r
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("./ustawy") if isfile(join("./ustawy", f))]
stats = {}

for f in onlyfiles: 
    with open(join("./ustawy", f), encoding='utf-8') as file_:
        artust_stats = {}
        art_stats = {}
        text = file_.read()
        # wyszukujemy Art. \d+ i zawartość pozczególnych artykułów w odpowiednim kontekście
        articles_section = r.findall(r'(Art\.\s\d+.)([\s\S]*?(?=Art\.\s\d+.))|(Art\.\s\d+.)([\s\S]*?)$', text)
        if len(articles_section) != 0:
            articles_section[-1] = (articles_section[-1][2], articles_section[-1][3], '', '')
        
        for article in articles_section:
            articles_numbers = []
            article_number = r.findall(r'\d+', article[0])[0]
            # wyszukujemy art ust w odopowiednim konteksach (przynajmniej się staramy)
            references = r.findall(r'([aA]rt\.\s*\d{1,4}\s*[uU]st\.\s*[\d\S]+(?![\s\S]{0,10}(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*)\b)|[aA]rt\.[\si,\d]*(?![\s\S]{0,14}(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*)\b)|[uU]st\.\s*[\Si,\d-]*(?![\s\S]{0,10}(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*)\b))', article[1])
            if len(references) != 0:
                for x in references:
                    for ref in x:
                        if len(ref) > 0:
                            # sprawdzamy czy :(art ust), (art), (ust)
                            group = r.findall(r'([aA]rt\.\s*[\d i,-]+[uU]st.\s*[\d i,-]+)|([aA]rt\.\s*[\d i,-]+)|([uU]st.\s*[\d i,-]+)', ref)
                            if len(group) == 0:
                                break
                            reference_type = group[0]
                            articles_numbers = []
                            ustep_numbers = []
                            if len(reference_type[0]) > 0:
                                articles_section = r.findall(r'[\d -,i]+(?=[uU]st)', reference_type[0])
                                if "-" in articles_section:
                                    tmp = r.findall(r'\d+', articles_section)
                                    articles_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    articles_numbers = r.findall(r'\d+', articles_section[0])
                                ustepy = r.findall(r'(?<=[uU]st\.)\s*[\d \-,i]+', reference_type[0])
                                if "-" in ustepy:
                                    tmp = r.findall(r'\d+', ustepy)
                                    ustep_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    ustep_numbers = r.findall(r'\d+', ustepy[0])
                                for article_number in articles_numbers:
                                    if article_number not in art_stats:
                                        art_stats[article_number] = 1
                                    else:
                                        art_stats[article_number] += 1
                                    if article_number not in artust_stats:
                                        artust_stats[article_number] = {}
                                    for ust_number in ustep_numbers:
                                        if ust_number not in artust_stats[article_number]:
                                            artust_stats[article_number][ust_number] = 1
                                        else:
                                            artust_stats[article_number][ust_number] += 1
                            if len(reference_type[1]) > 0:
                                articles_section = r.findall(r'[\d -,i]+', reference_type[1])
                                if "-" in articles_section:
                                    tmp = r.findall(r'\d+', articles_section)
                                    articles_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    articles_numbers = r.findall(r'\d+', articles_section[0])
                                for article_number in articles_numbers:
                                    if article_number not in art_stats:
                                        art_stats[article_number] = 1
                                    else:
                                        art_stats[article_number] += 1
                            if len(reference_type[2]) > 0:
                                ustepy = r.findall(r'[\d \-,i]+', reference_type[2])
                                if "-" in ustepy:
                                    tmp = r.findall(r'\d+', ustepy)
                                    ustep_numbers = [i for i in range(tmp[0],tmp[1]+1)]
                                else:
                                    ustep_numbers = r.findall(r'\d+', ustepy[0])
                                if article_number not in artust_stats:
                                    artust_stats[article_number] = {}
                                if article_number not in art_stats:
                                    art_stats[article_number] = 1
                                else:
                                    art_stats[article_number] += 1
                                for ust_number in ustep_numbers:
                                    if ust_number not in artust_stats[article_number]:
                                        artust_stats[article_number][ust_number] = 1
                                    else:
                                        artust_stats[article_number][ust_number] += 1
                            
        tuples_article = []
        tuples_ustep = []
        for a in art_stats.items():
            a_n = a[0]
            a_v = a[1]
            tuples_article.append((int(a_n), a_v))
        for au in artust_stats.items():
            a_n = au[0]
            for u in au[1].items():
                tuples_ustep.append((int(a_n), u[0], u[1]))
        tuples_article.sort(key=lambda tup: tup[1], reverse=True)
        tuples_ustep.sort(key=lambda tup: tup[2], reverse=True)
        # print(tuples_article)
        # print(tuples_ustep)
        save_file = open(join("./stats", "stats" + str(f)) ,'w')
        for ta in tuples_article:
            save_file.write("Art. " + str(ta[0]) + " [ " + str(ta[1]) + " ]\n")
        for tu in tuples_ustep:
            save_file.write("Art. " + str(tu[0]) + " ust. " + str(tu[1]) + " [ " + str(tu[2]) + " ]\n")
        





