from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from os import listdir
from os.path import isfile, join

es = Elasticsearch()
es.indices.delete(index='my_index', ignore=[400, 404])
print(es.indices.create(
    index="my_index",
    body={
        "settings": {
            "analysis": {
                "filter": {
                  "kodeks_synonym" : {
                    "type" : "synonym",
                        "synonyms" : [
                            "kpk => kodeks postępowania karnego",
                            "kpc => kodeks postępowania cywilnego",
                            "kk => kodeks karny",
                            "kc => kodeks cywilny"
                        ]
                    }    
                  },
     
              "analyzer" : {
                    "my_analyzer" : {
                        "tokenizer" : "standard",
                        "filter" : ["kodeks_synonym", "lowercase","morfologik_stem"]
                    }
                }
            }
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "text": {
                        "type": "text",
                        "analyzer": "my_analyzer",
                        "term_vector": "with_positions_offsets_payloads"
                    }
                }
            }
        }
        }
    
)
)


onlyfiles = [f for f in listdir("./ustawy") if isfile(join("./ustawy", f))]

for f in onlyfiles: 
    with open(join("./ustawy", f), encoding='utf-8') as file_:
        text = file_.read()
        es.create(
            index="my_index",
            doc_type="_doc",
            id=f,
            body={"text": text}
        )

