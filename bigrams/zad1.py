import regex as r
from os import listdir
from os.path import isfile, join
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from collections import Counter
import numpy as np
import llr


es = Elasticsearch()

onlyfiles = [f for f in listdir("../ustawy") if isfile(join("../ustawy", f))]
stats = {}

bigrams = dict()
# dirs = [name for name in os.listdir("./ustawy")]
shingles = []
tokens = []
for f in onlyfiles: 
    with open(join("../ustawy", f), encoding='utf-8') as _file:
        text = _file.read()
        doc = es.indices.analyze("my_index", 
                                        {
                                        "tokenizer": "standard",
                                        "filter": ["lowercase", "shingle"],
                                        "text": text
                                        }
        )
        shingles.append([x['token'] for x in doc['tokens'] if x['type'] == 'shingle'])
        tokens.append([x['token'] for x in doc['tokens'] if x['type'] == '<ALPHANUM>'])
        

shingles = [item for sublist in shingles for item in sublist]
tokens =  [item for sublist in tokens for item in sublist]

shingles_counter = Counter([tuple(item.split(' ')) for item in shingles if len(r.findall(r'[\d!@#$%^&*(),.?\":{}|<>]+', item)) == 0])
tokens_counter = Counter([item for item in tokens if len(r.findall(r'[\d!@#$%^&*(),.?\":{}|<>]+', item)) == 0])

print(len(shingles_counter))
def count_pmi(x, y):
    return np.log((shingles_counter[(x, y)] / len(shingles_counter)) / ((tokens_counter[x] / len(tokens_counter)) * (tokens_counter[y] / len(tokens_counter))))

pmi = []
for shingle in shingles_counter.keys():
    pmi.append((shingle, count_pmi(shingle[0], shingle[1])))

pmi = sorted(pmi, key=lambda x: x[1], reverse=True)

print("top 30 pmis", pmi[:30])

with open("results_pmi.txt", "w", encoding='utf-8')as _file:
    for p in pmi:
        _file.write(str(p) + '\n')
def count_lrr(shingle):
    k11 = shingles_counter.get(shingle, 0)
    a = shingle[0]
    b = shingle[1]
    k12 = 0
    k21 = 0
    for s in shingles_counter.items():
        if s[0][0] == a and s[0][1] != b:
            k12 += s[1]
        if s[0][0] != a and s[0][1] == b:
            k21 += s[1]
    k22 = sum(shingles_counter.values()) - k11 - k12 - k21

    return k11, k12, k21, k22

llrs = []
for shingle in shingles_counter.keys():
    k11, k12, k21, k22 = count_lrr(shingle)
    llr_val = llr.llr_2x2(k11, k12, k21, k22)
    llrs.append((shingle, llr_val))

llrs = sorted(llrs, key=lambda x: x[1], reverse=True)

print("-------------------------------")
print("llrs: ", llrs[:30])
with open("results_lrr.txt", "w", encoding='utf-8')as _file:
    for l in lrrs:
        _file.write(str(l) + '\n')

