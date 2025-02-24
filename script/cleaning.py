import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import re

state_populations_2023 = { # use csv census data instead
    "Alabama": 5074296,
    "Alaska": 733391,
    "Arizona": 7359197,
    "Arkansas": 3045637,
    "California": 39538223,
    "Colorado": 5773714,
    "Connecticut": 3605597,
    "Delaware": 989948,
    "Florida": 21944577,
    "Georgia": 10711908,
    "Hawaii": 1455271,
    "Idaho": 1839106,
    "Illinois": 12812508,
    "Indiana": 6833037,
    "Iowa": 3219171,
    "Kansas": 2937150,
    "Kentucky": 4505836,
    "Louisiana": 4624047,
    "Maine": 1372247,
    "Maryland": 6185278,
    "Massachusetts": 7033469,
    "Michigan": 10077331,
    "Minnesota": 5706494,
    "Mississippi": 2961279,
    "Missouri": 6168187,
    "Montana": 1104271,
    "Nebraska": 1961504,
    "Nevada": 3104614,
    "New Hampshire": 1377529,
    "New Jersey": 9288994,
    "New Mexico": 2117522,
    "New York": 20201249,
    "North Carolina": 10551162,
    "North Dakota": 779094,
    "Ohio": 11780017,
    "Oklahoma": 3990443,
    "Oregon": 4266560,
    "Pennsylvania": 12964056,
    "Rhode Island": 1097379,
    "South Carolina": 5282634,
    "South Dakota": 909824,
    "Tennessee": 7051339,
    "Texas": 31000000,
    "Utah": 3271616,
    "Vermont": 643077,
    "Virginia": 8654542,
    "Washington": 7738692,
    "West Virginia": 1793716,
    "Wisconsin": 5893718,
    "Wyoming": 576851,
    "District of Columbia": 689545,
    "Puerto Rico": 3263584
}


def clean_outages(path):

    df = pd.DataFrame(pd.read_excel("data/outages/2023_Annual_Summary.xls"))
  
    df.columns = df.iloc[0]
    df = df.drop(index=0)

    df = df[df["Number of Customers Affected"] != 0]
    df = df[df["Number of Customers Affected"] != "0"]
    df = df[df["Number of Customers Affected"] != "Unknown"]

    for _, row in df.iterrows():
        row["Area Affected"] = re.sub(r":.*", "", row["Area Affected"]) # need to handle multiple states...

        if row["Area Affected"] not in state_populations_2023.keys():
            if row["Area Affected"] == "LUMA Energy":
                row["Area Affected"] = "Puerto Rico"
            if row["Area Affected"] == "ISO New England":
                row["Area Affected"] = "Connecticut" #, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont"
            if row["Area Affected"] == "Otter Tail Power Co":
                row["Area Affected"] = "Minnesota" #, North Dakota, South Dakota"
            if "Western Area Power" in row["Area Affected"]:
                row["Area Affected"] = "Montana" #, North Dakota, South Dakota, Nebraska, Iowa, Minnesota"

    return df


def build_outage_dict(path):

    df = clean_outages(path)

    dic = {}
    for _, row in df.iterrows():

        state = row["Area Affected"]
        if row["Number of Customers Affected"] == "Unknown":
            continue
        if state not in dic:
            dic[state] = int(row["Number of Customers Affected"])
        else:
            dic[state] += int(row["Number of Customers Affected"])

    del dic["Arkansas, Mississippi"] # get rid of this eventually
    del dic["Wisconsin, Michigan"]

    return {x: round((y/state_populations_2023[x])*100, 2) for x,y in dic.items()} # handle multiple states



def main():
    path = "data/outages/2023_Annual_Summary.xls"
    
    dic = build_outage_dict(path)

    for x,y in dic.items():
        print (x, ":", y)
    


if __name__ == "__main__":
    main()
