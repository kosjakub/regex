import regex as r
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("./ustawy") if isfile(join("./ustawy", f))]
stats = {}

# dirs = [name for name in os.listdir("./ustawy")]
i = 0
for f in onlyfiles: 

    with open(join("./ustawy", f), encoding='utf-8') as f:

        text = f.read()
        ustaw = r.findall(r'(\bu[\s-]*s[\s-]*t[\s-]*a[\s-]*w[\s-]*(([-ayęąo]+)|(i[\s-]*e)|(o[\s-]*m)|(a[\s-]*m[\s-]*i)|(a[\s-]*c[\s-]*h))*\b)', text, flags=r.IGNORECASE)
        for u in ustaw:
            i+=1
print(i)