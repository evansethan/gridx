import csv
from script.utils import state_pops_23

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

    # return dic

    state_damage = {}
    for text, cost in dic.items():
        state = ' '.join(word.capitalize() for word in text.split())
        
        if state in state_pops_23:
            state_damage[state] = round(cost/state_pops_23[state], 2)


    return state_damage

def main():
    dic = import_storms("data/storms/2020.csv")

    print(dic['iowa'], dic["louisiana"])

if __name__ == "__main__":
    main()