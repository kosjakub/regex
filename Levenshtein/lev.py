from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
from pathlib import Path
import Levenshtein
import regex as re
from pprint import pprint
from collections import Counter
import matplotlib.pyplot as plt
import csv

es = Elasticsearch()

ids = indices = [h["_id"] for h in es.search(
    index="my_index",
    doc_type="_doc",
    body={
        "query": {
            "match_all": {}
            }
        },
        size=1500
)["hits"]["hits"]]
global_counter = Counter()
i = 0
for _id in ids:
    term_vectors = es.termvectors(index="my_index", doc_type="_doc", id=_id, body={"term_statistics" : "true"})["term_vectors"]["text"]["terms"]
    single_counter = Counter(dict([(key, value["term_freq"]) for key, value in term_vectors.items()]))
    global_counter.update(single_counter)

global_counter = Counter(dict([(key.replace('\xad',''), value) for key, value in global_counter.items() if len(key) >= 2 and not re.findall(r'\d+', key)]))
x = [i for i in range(len(global_counter))]
y = [v[1] for v in global_counter.most_common()]

plt.plot(x, y)
plt.xscale('log')
plt.yscale('log')
plt.show()
forms_set = set()
with open('polimorfologik-2.1\\polimorfologik-2.1.txt', 'r', encoding='utf-8') as csvFile:
    reader = csv.reader(csvFile)
    print(reader)
    for row in reader:
        splited_row = row[0].split(';')
        forms_set.add(splited_row[1].lower())    

not_existing_words = []
for word in global_counter.most_common():
        if word[0] not in forms_set:

            not_existing_words.append(word)

pprint(not_existing_words[:30])

triple_missing = [x for x in not_existing_words if x[1] == 3]

pprint(triple_missing[:30])

for word in triple_missing[:30]:
    corect = []
    for form in forms_set:
        lev_dist = Levenshtein.distance(word[0], form)
        if lev_dist < 4:
            corect.append((form, lev_dist))

    corect.sort(key=lambda x: x[1])
    print(word)
    pprint(corect[:3])


# print(df)