import json

old_dists = "olddistricts.txt"
f = map(lambda s: s.strip(","), open(old_dists,"r").read().split('\n')[1:436])



fixtures = {}

bpis = open("build/district_results.csv","r").read().split("\n")

data = {}
for bpi in bpis[1:436]:
    row = bpi.split(",")
    #print(row)
    data[row[3]] = [row[9], row[7]]

final = []

for district in f:
    district_dict = json.loads(district)
    name = district_dict["pk"]
    temp = district_dict["fields"]
    temp["bpi"] = float(data[name][0])
    temp["fundamental"] = float(data[name][1])

    district_dict["fields"] = temp
    final.append(str(district_dict))
    
out = open("districts.json","w")

final = ",\n".join(final).replace("'",'"').replace('O"',"O'")

out.write("[\n"+final+"\n]")
out.close()
