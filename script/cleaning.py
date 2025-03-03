import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
from info import state_pops_23
import re
import csv


def clean_outages(path):

    df = pd.DataFrame(pd.read_excel(path))
  
    df.columns = df.iloc[0]
    df = df.drop(index=0)

    for _, row in df.iterrows():
        #row["Area Affected"] = "".join(re.findall(r"\b\w+:", row["Area Affected"])) # maybe this?
        row["Area Affected"] = re.sub(r":.*", "", row["Area Affected"]) # still some missing states maybe...

        if row["Area Affected"] not in state_pops_23.keys():
            if row["Area Affected"] == "LUMA Energy":
                row["Area Affected"] = "Puerto Rico"
            elif row["Area Affected"] == "ISO New England":
                row["Area Affected"] = "Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont"
            elif row["Area Affected"] == "Otter Tail Power Co":
                row["Area Affected"] = "Minnesota, North Dakota, South Dakota"
            elif "Western Area Power" in row["Area Affected"]:
                row["Area Affected"] = "Montana, North Dakota, South Dakota, Nebraska, Iowa, Minnesota"
            elif row["Area Affected"] == 'Northern and Central California;' or 'Pacific Gas' in row["Area Affected"]:
                row["Area Affected"] = "California"
            elif row["Area Affected"] == 'Central Oklahoma':
                row["Area Affected"] = "Oklahoma"
            elif row["Area Affected"] == 'Pacificorp':  
                row["Area Affected"] = "Oregon, California, Washington, Oregon, Utah, Wyoming, Idaho"
            elif row["Area Affected"] == 'Tampa Electric Company' or row["Area Affected"] == 'Seminole Electric Cooperative Inc':  
                row["Area Affected"] = "Florida"
            elif row["Area Affected"] == 'Tucson Electric Power':
                row["Area Affected"] = "Arizona"
            # if row["Area Affected"] == 'Northern California':  
            #     row["Area Affected"] = "California"
            # if 'Northern/North Eastern' in row["Area Affected"]:
            #     row["Area Affected"] = "Georgia"
            # if 'Fentress County' in row["Area Affected"]:
            #     row["Area Affected"] = "Tennessee"
            else:
                row["Area Affected"] = "Puerto Rico" # fix this .....................
                
    return df


def build_outage_dict(path):

    df = clean_outages(path)

    dic = {}
    for _, row in df.iterrows():

        try:
            num_affected = int(row["Number of Customers Affected"])
        except ValueError:
            continue

        state = row["Area Affected"]
        if row["Area Affected"] not in dic:
            dic[state] = num_affected
        else:
            dic[state] += num_affected

    dic2 = {}
    for lst, count in dic.items():
        states = lst.split(",")
        # if count == 0:
        #     continue
        total = 0
        for state in states:
            total += state_pops_23[state.strip()]
        for state in states:
            state = state.strip()

            percent_affected = count*(state_pops_23[state]/total) # control for differing state pops

            if state not in dic2:
                dic2[state] = percent_affected
            else:
                dic2[state] += percent_affected

            if dic2[state] > state_pops_23[state]: # this could be cleaner
                dic2[state] = state_pops_23[state] # account for sum of total affected customers > state pop

    return {x: round((y/state_pops_23[x])*100, 2) for x,y in dic2.items()}



def build_storms_dict(path):
    
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


    return state_damage # needs testing



def main():
    path = "data/outages/2023_Annual_Summary.xls" # year < 2016 diff format need to handle
    
    dic = build_outage_dict(path)
    print("")
    print("")
    print("Percent state residents affected by an outage (2023)")
    print("----------------------------------------------------")
    for x,y in dic.items():
        print (x, ":", y, "%")
    


if __name__ == "__main__":
    main()
