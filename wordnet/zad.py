import requests as r
from pprint import pprint
import numpy as np

base = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api"

def ss(word):
    return r.get(base + "/senses/search",{"lemma":word}).json()['content']

def get_synsetid_by_senseId(senseId):
    return r.get(base+ "/senses/{}/synset".format(senseId)).json()['id']

def get_synset_by_id(synsetId):
    return r.get(base+ "/synsets/{}/senses".format(synsetId)).json()

def get_synonyms_by_senseId(senseId):
    return [get_info(x) for x in get_synset_by_id(get_synsetid_by_senseId(senseId))]

def get_info(sense):
    return {
        "word": sense['lemma']['word'],
        "id": sense['id'],
        "description": sense['domain']['description'],
        "partOfSpeech": sense['partOfSpeech']['lmfType'],
        "senseNumber": sense['senseNumber']
    }

# Zadanie 1 
# pprint(ss("szkoda"))
for sense in ss("szkoda"):
    info = get_info(sense)
    if info['partOfSpeech'] == 'noun':
        print("znaczenia złowa szkoda (rzeczownik)")
        pprint(info['description'])
        print("Synonimy: ")
        for synonym in get_synonyms_by_senseId(info['id']):
            print("    " + str(synonym['word']))
        



# Zadanie 2

def synset_relations(synset, rel):
    body = r.get(base + "/synsets/{}/relations".format(synset)).json()
    return [x for x in body if x['relation']['id']==rel and x['synsetFrom']['id']!= synset]

def get_synsetId_from_relation(relation_dict):
    return  relation_dict['synsetFrom']['id']




def find_closure_for_relation(synsetId, relation_id, list_):
    relations = synset_relations(synsetId, relation_id)
    if len(relations) != 0:
        for relation in relations:
            rel_id = get_synsetId_from_relation(relation)
            list_.append(rel_id) 
            return find_closure_for_relation(rel_id, relation_id, list_)
    return list_


hyperonymy_id = 11



wypadek_drogowy_info = get_info(ss('wypadek drogowy')[0])
# pprint(wypadek_drogowy_info)

wypadek_drogowy_synsetId = get_synsetid_by_senseId(wypadek_drogowy_info['id'])

hyperonims_ids = []
hyperonims_ids.append(wypadek_drogowy_synsetId)
print(find_closure_for_relation(wypadek_drogowy_synsetId, hyperonymy_id, hyperonims_ids))

# print(hyperonims_ids)
hyperonims = []
for hyperonim_id in hyperonims_ids:
    synset_ids = get_synset_by_id(hyperonim_id)
    # for id_ in synset_ids:
    info = get_info(synset_ids[0])
    hyperonims.append(info['word'])
    
pprint(hyperonims)



# Zadanie 3


hyponymy_id = 10


wypadek_infos = [get_info(x) for x in ss('wypadek') if get_info(x)['word'] == 'wypadek' and get_info(x)['partOfSpeech'] == 'noun' and get_info(x)['senseNumber'] == 1]
print(len(wypadek_infos))
hyponyms_ids = []
hyponyms_words = []
for wypadek_info in wypadek_infos:
    # pprint(wypadek_info)
    wypadek_id = wypadek_info['id']
    wypadek_synsetId = get_synsetid_by_senseId(wypadek_id)
    
    for synsets_relation_id in synset_relations(wypadek_synsetId, hyponymy_id):
        for hyponim in get_synset_by_id(synsets_relation_id['synsetFrom']['id']):
            hyponym_info = get_info(hyponim)
            hyponyms_words.append(hyponym_info['word'])
            hyponyms_ids.append(hyponym_info['id'])

pprint(hyponyms_words)

# Zadanie 4

hyponymy_id = 10


wypadek_infos = [get_info(x) for x in ss('wypadek') if get_info(x)['word'] == 'wypadek' and get_info(x)['partOfSpeech'] == 'noun' and get_info(x)['senseNumber'] == 1]
print(len(wypadek_infos))
hyponyms_ids = []
hyponyms_words = []
for wypadek_info in wypadek_infos:
    # pprint(wypadek_info)
    wypadek_id = wypadek_info['id']
    wypadek_synsetId = get_synsetid_by_senseId(wypadek_id)
    # print(wypadek_synsetId)
    for synsets_relation_id in synset_relations(wypadek_synsetId, hyponymy_id):
        # pprint(synsets_relation_id)
        for hyponim in get_synset_by_id(synsets_relation_id['synsetFrom']['id']):
            hyponym_info = get_info(hyponim)
            hyponyms_words.append(hyponym_info['word'])
            hyponyms_ids.append(hyponym_info['id'])

second_oreder_hyponyms_words = []
second_oreder_hyponyms_ids = []
for first_order_hyponim_id, first_order_hyponim_word in zip(hyponyms_ids, hyponyms_words):
    print(first_order_hyponim_id)
    print(first_order_hyponim_word)
    first_order_hyponim_synsetid = get_synsetid_by_senseId(first_order_hyponim_id)
    for synsets_relation_id in synset_relations(first_order_hyponim_synsetid, hyponymy_id):
        # print("    " + str(synsets_relation_id))
        for second_oreder_hyponim in get_synset_by_id(synsets_relation_id['synsetFrom']['id']):
            
            hyponym_info = get_info(second_oreder_hyponim)
            print("            " + str(hyponym_info['word']))
            second_oreder_hyponyms_words.append(hyponym_info['word'])
            second_oreder_hyponyms_ids.append(hyponym_info['id'])

pprint(hyponyms_words)
pprint(second_oreder_hyponyms_words)

# Zadanie 5

def create_word(word, id_):
    return{
        'word': word,
        'id': id_
    }

words = [create_word("szkoda", 2), create_word("strata", 1), create_word("uszczerbek", 1),
        create_word("uszczerbek na zdrowiu", 1), create_word("krzywda", 1),
        create_word("niesprawiedliwość", 1), create_word("nieszczęście", 2)]

words_senses = []
for word in words:
    words_senses.append([get_info(x) for x in ss(word['word']) if get_info(x)['senseNumber'] == word['id']][0])

# print(words_senses)
words_synsets_ids = []
word_senses_synsets = []
for word_sense in words_senses:
    synsetId = get_synsetid_by_senseId(word_sense['id'])
    words_synsets_ids.append(synsetId)
    word_senses_synsets.append(tuple((word_sense, synsetId)))
# print(word_senses_synsets)

def find_relations(synsetId):
    body = r.get(base + "/synsets/{}/relations".format(synsetId)).json()
    return [x for x in body]

joint_relations = []

for first_synsetId in words_synsets_ids:
    first_synsetId_realtions = find_relations(first_synsetId)
    for rel in first_synsetId_realtions:
        for second_synsetId in words_synsets_ids:
            if rel['synsetFrom']['id'] == second_synsetId and rel['synsetTo']['id'] == first_synsetId:
                joint_relations.append(tuple(( second_synsetId, first_synsetId, rel['relation']['id'])))
            if rel['synsetFrom']['id'] == first_synsetId and rel['synsetTo']['id'] == second_synsetId:
                joint_relations.append(tuple(( first_synsetId, second_synsetId, rel['relation']['id'])))
            if rel['synsetFrom']['id'] == first_synsetId and rel['synsetTo']['id'] == first_synsetId:
                joint_relations.append(tuple(( first_synsetId, first_synsetId, rel['relation']['id'])))
            if rel['synsetFrom']['id'] == second_synsetId and rel['synsetTo']['id'] == second_synsetId:
                joint_relations.append(tuple(( second_synsetId, second_synsetId, rel['relation']['id'])))
pprint(joint_relations)
y =  np.unique(joint_relations, axis=0)
distinct_relations = [] 
for i in y:
   distinct_relations.append(tuple(i))

# pprint(distinct_relations)
words_pairs = []
for word, synsetId in word_senses_synsets:
    for distinct_relation in distinct_relations:

        if synsetId == distinct_relation[0]:
            for w, sID in word_senses_synsets:
                if sID == distinct_relation[1]:
                    words_pairs.append(tuple((word['word'], w['word'], distinct_relation[2])))

pprint(words_pairs)

# Zadanie 6


words = [create_word("wypadek", 1), create_word("wypadek komunikacyjny", 1), create_word("kolizja", 2),
        create_word("zderzenie", 2), create_word("kolizja drogowa", 1),
        create_word("bezkolizyjny", 2), create_word("katastrofa budowlana", 1), 
        create_word("wypadek drogowy", 1)]

words_senses = []
for word in words:
    pprint(word)
    words_senses.append([get_info(x) for x in ss(word['word']) if get_info(x)['senseNumber'] == word['id']][0])

# print(words_senses)
words_synsets_ids = []
word_senses_synsets = []
for word_sense in words_senses:
    synsetId = get_synsetid_by_senseId(word_sense['id'])
    words_synsets_ids.append(synsetId)
    word_senses_synsets.append(tuple((word_sense, synsetId)))
pprint(word_senses_synsets)

joint_relations = []
# 1284
# 3982
for first_synsetId in words_synsets_ids:
    first_synsetId_realtions = find_relations(first_synsetId)
    for rel in first_synsetId_realtions:
        # print(rel['synsetFrom']['id'], rel['synsetTo']['id'])
        for second_synsetId in words_synsets_ids:
            if rel['synsetFrom']['id'] == second_synsetId and rel['synsetTo']['id'] == first_synsetId:
                joint_relations.append(tuple(( second_synsetId, first_synsetId, rel['relation']['id'])))
            if rel['synsetFrom']['id'] == first_synsetId and rel['synsetTo']['id'] == second_synsetId:
                joint_relations.append(tuple(( first_synsetId, second_synsetId, rel['relation']['id'])))
            if rel['synsetFrom']['id'] == first_synsetId and rel['synsetTo']['id'] == first_synsetId:
                joint_relations.append(tuple(( first_synsetId, first_synsetId, rel['relation']['id'])))
            if rel['synsetFrom']['id'] == second_synsetId and rel['synsetTo']['id'] == second_synsetId:
                joint_relations.append(tuple(( second_synsetId, second_synsetId, rel['relation']['id'])))

# pprint(joint_relations)
y =  np.unique(joint_relations, axis=0)
distinct_relations = [] 
for i in y:
   distinct_relations.append(tuple(i))

pprint(distinct_relations)
words_pairs = []
for distinct_relation in distinct_relations:
    for word, synsetId in word_senses_synsets:
        if synsetId == distinct_relation[0]:
            for w, sID in word_senses_synsets:
                if sID == distinct_relation[1]:
                    words_pairs.append(tuple((word['word'], w['word'], distinct_relation[2])))

pprint(words_pairs)

# Zadanie 7

