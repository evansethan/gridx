import csv
from info import state_pops_23

def import_storms(path):
    
    dic = {}
    with open(path, "r") as f:
        
        for row in csv.DictReader(f):
            if row["DAMAGE_PROPERTY"] == "0.00K" or row["DAMAGE_PROPERTY"] == '':
                continue

            if "K" in row["DAMAGE_PROPERTY"]:
                damage = float(row["DAMAGE_PROPERTY"][:-1]) * 1000
            if "M" in row["DAMAGE_PROPERTY"]:
                damage = float(row["DAMAGE_PROPERTY"][:-1]) * 1000000
            if "B" in row["DAMAGE_PROPERTY"]:
                damage = float(row["DAMAGE_PROPERTY"][:-1]) * 1000000000

            if row["STATE"].lower() not in dic:
                dic[row["STATE"].lower()] = damage
            else:
                dic[row["STATE"].lower()] += damage

    state_damage = {}
    for state, cost in dic.items():
        
        state_damage

    return dic

def main():
    dic = import_storms("data/storms/2023.csv")

    print(dic)

if __name__ == "__main__":
    main()