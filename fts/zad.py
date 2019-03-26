from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from pprint import pprint
es = Elasticsearch()


print("Ilość plików w których znaleziono słowo \"ustawa\" (z odmianami) " + str(es.search(
    index="my_index",
    doc_type="_doc",
    body={
        "query": {
            "match": {
                "text": {
                    "query": "ustawa"
                }
            }
        }
    }
)["hits"]["total"]))

print("Ilość \"kpc\" (z odmianami) " + str(es.search(
    index="my_index",
    doc_type="_doc",
    body={
        "query": {
            "match_phrase": {
                "text": {
                    "query": "kodeks postępowania cywilnego"
                }
            }
        }
    }
)["hits"]["total"]))

print("Ilość \"wchodzi w życie\" (z odmianami) " + str(es.search(
    index="my_index",
    doc_type="_doc",
    body={
        "query": {
            "match_phrase": {
                "text": {
                    "query": "wchodzi w życie",
                    "slop":2
                }
            }
        }
    }
)["hits"]["total"]))


result = es.search(
    index="my_index",
    doc_type="_doc",
    body={
        "query": {
            "match": {
                "text": {
                    "query": "konstytucja"
                }
            }
        },
        "highlight": {
            "fields": {
                "text": {}
            },
            "number_of_fragments": 3
        },
        "sort": "_score"
    }
)['hits']['hits']
score = result[:10]
s = [x['_id'] for x in score]
print("10 pierwszych wyników najbardziej znaczących \"konstytucja\" (z odmianami) " + str(s))
pprint([x['highlight'] for x in score])


