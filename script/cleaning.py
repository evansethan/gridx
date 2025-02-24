import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
from info import state_pops_23
import re


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
            if row["Area Affected"] == "ISO New England":
                row["Area Affected"] = "Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont"
            if row["Area Affected"] == "Otter Tail Power Co":
                row["Area Affected"] = "Minnesota, North Dakota, South Dakota"
            if "Western Area Power" in row["Area Affected"]:
                row["Area Affected"] = "Montana, North Dakota, South Dakota, Nebraska, Iowa, Minnesota"
            if row["Area Affected"] == 'Northern and Central California;':
                row["Area Affected"] = "California"
            if row["Area Affected"] == 'Central Oklahoma':
                row["Area Affected"] = "Oklahoma"
            # if row["Area Affected"] == 'Northern California':  
            #     row["Area Affected"] = "California"
            # if 'Northern/North Eastern' in row["Area Affected"]:
            #     row["Area Affected"] = "Georgia"
            # if 'Fentress County' in row["Area Affected"]:
            #     row["Area Affected"] = "Tennessee"
                
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
        if count == 0:
            continue
        total = 0
        for state in states:
            total += state_pops_23[state.strip()]
        for state in states:
            state = state.strip()
            if state not in dic2:
                dic2[state.strip()] = count*(state_pops_23[state]/total) # handle differing state populations
            else:
                dic2[state.strip()] += count*(state_pops_23[state]/total) # pytest this

    return {x: round((y/state_pops_23[x])*100, 2) for x,y in dic2.items()}


def main():
    path = "data/outages/2023_Annual_Summary.xls" # year <= 2015 diff format need to handle
    
    dic = build_outage_dict(path)
    print("")
    print("")
    print("Percent state residents affected by an outage (2023)")
    print("----------------------------------------------------")
    for x,y in dic.items():
        print (x, ":", y, "%")
    


if __name__ == "__main__":
    main()
