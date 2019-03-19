import regex as r
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("./ustawy") if isfile(join("./ustawy", f))]
stats = {}

# dirs = [name for name in os.listdir("./ustawy")]
for f in onlyfiles: 
    with open(join("./ustawy", f), encoding='utf-8') as f:
        i = 0
        text = f.read()
        references = r.findall(r'(\(Dz\.\s*U\.\s*[^\)]*\))', text)
        tmp = [x.replace("\n", '') for x in references]
        references_years = []
        for t in tmp:
            reg2 = r.findall(r'(\d{4}\s*r\.[^\)]*?(?=\d{4}\s*r\.))|(\d{4}\s*r\.[^\)]*(?=\)))|(Nr[^\)]*?(?=\d{4}\s*r\.))|(Nr[^\)]*(?=\)))', t)
            for r2 in reg2:
                for c in r2: 
                    if c != '':
                        references_years.append(c)

        references_numbers = []
        reference_positions = []

        for referece_year in references_years:
            year_tmp = r.findall(r'\d+\s*(?=r\.)', referece_year)
            if len(year_tmp) != 0:
                year_number = int(year_tmp[0]) 
            else:
                year_number = -1
            if year_number not in stats:
                stats[year_number] = {}  

            reg3 = r.findall(r'(Nr.*?poz[\s,.\di]*)', referece_year)
            for reference_number in reg3:
                if reference_number != '':
                    references_numbers.append(reference_number)
                    r_tmp = r.findall(r'(?<=Nr)\s*\d+', reference_number)
                    if len(r_tmp) == 0:
                        break
                    number_value = int(r.findall(r'(?<=Nr)\s*\d+', reference_number)[0])
                    if number_value not in stats[year_number]:
                        stats[year_number][number_value] = {}
                    reg4 = r.findall(r'(?<=poz.)[\s\S\d]*', reference_number)
                    reference_positions.append(reg4[0])
                    reg5 = r.findall(r'\d{1,4}', reg4[0])

                    for position in reg5:
                        position_number = int(position)
                        if position_number not in stats[year_number][number_value]:
                            stats[year_number][number_value][position_number] = 1
                        else:
                            stats[year_number][number_value][position_number] +=1
                        i+=1
        print(i)
        
tuples = []
for years in stats.items():
    year = years[0]
    for numbers in years[1].items():
        number = numbers[0]
        for positions in numbers[1].items():
            tuples.append((year, number, positions[0], positions[1]))
tuples.sort(key=lambda tup: tup[3], reverse=True)

save_file = open("stats.txt",'w')

for t in tuples:
    save_file.write(str(t[0]) + " r. Nr " + str(t[1]) + " poz. " + str(t[2]) + " [ " + str(t[3]) + " ] \n") 
