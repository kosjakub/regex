import regex as r
from os import listdir
from os.path import isfile, join
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from collections import Counter
import numpy as np
import http.client as client
import llr
        
onlyfiles = [f for f in listdir("../ustawy") if isfile(join("../ustawy", f))]
con = client.HTTPConnection('localhost', port=9200)
bigrams = Counter()
tokens = Counter()
old_token = ""
i = 0
for f in onlyfiles: 
    old_token = ""
    new_token = ""
    print(i)
    i+=1
    with open(join("../ustawy", f), encoding='utf-8') as _file:
        text = _file.read()
        text = text.lower()
        con.request(method="POST", url="", body=text.encode('utf-8'))
        res = con.getresponse().readlines()
        # print(res)
        for line in res:
            # print("---")
            line_decoded = line.decode("utf-8")
            # print(line_decoded)
            # print(line.decode("utf-8"))
            if "disamb" in line_decoded:
                line_decoded = line_decoded.split("\t")
                word = line_decoded[1]
                t = line_decoded[2].split(":")[0]
                # print("word: ", word)
                # print("t: ", t)
                # print(line)
                new_token = word+":"+t
                if len(r.findall(r'[\d!@#$%^&*\-(),.?\":{}|<>]+', word)) == 0:
                    if old_token != "":
                        bigrams.update([(old_token, new_token)])
                    old_token = new_token
                    tokens.update([new_token])
                else:
                    old_token = ""
                    new_token = ""
        # break

total_count = sum(bigrams.values())
llrs = []
print("ilosc bigramów: ", len(bigrams))
i = 0
for k, v in bigrams.items():
    k11 = v
    k12 = tokens[k[1]] - v
    k21 = tokens[k[0]] - v
    k22 = total_count - tokens[k[1]] - tokens[k[0]]
    llr_value = llr.llr_2x2(k11, k12, k21, k22)
    llrs.append((k,llr_value))

llrs = sorted(llrs, key=lambda x: x[1], reverse=True)
top_llrs = [x for x in llrs if x[0][0].split(":")[1] == "subst" and x[0][1].split(":")[1] in ["adj", "subst"]]

with open("results_lrrs.txt", "w", encoding='utf-8')as _file:
    for l in top_llrs:
        _file.write(str(l) + '\n')
pprint(top_llrs)
print('\n\n\n\n\n\n ----------------------- \n\n\n\n\n')
pprint(top_llrs[:50])



