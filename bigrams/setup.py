from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


es = Elasticsearch()
es.indices.delete(index='my_index', ignore=[400, 404])

print(es.indices.create(
    index="my_index",
    body={
        "settings": {
            "analysis": {
              "analyzer" : {
                    "my_analyzer" : {
                        "tokenizer" : "standard",
                        "filter" : ["shingle", "lowercase","morfologik_stem"]
                    }
                }
            }
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "text": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    }
                }
            }
        }
        }
    
)
)