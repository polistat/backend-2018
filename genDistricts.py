import json

old_dists = "old_dists.txt"
f = open(old_dists,"r").read().split(',\n')



fixtures = {}

bpis = open("bpis.csv","r").read().split("\n")

final = []

for district, bpis in zip(f, bpis):
    district_dict = json.loads(district)
    temp = district_dict["fields"]
    temp["bpi"] = float(bpis.split(",")[1])
    temp["fundamental"] = float(bpis.split(",")[2])

    district_dict["fields"] = temp
    final.append(str(district_dict))
    
out = open("districts.json","w")

final = ",\n".join(final).replace("'",'"').replace('O"',"O'")

out.write("[\n"+final+"\n]")
out.close()
