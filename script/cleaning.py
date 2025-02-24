import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
from info import state_pops_23
import re


def clean_outages(path):

    df = pd.DataFrame(pd.read_excel(path))
  
    df.columns = df.iloc[0]
    df = df.drop(index=0)

    df = df[df["Number of Customers Affected"] != 0]
    df = df[df["Number of Customers Affected"] != "0"]
    df = df[df["Number of Customers Affected"] != "Unknown"]

    for _, row in df.iterrows():
        row["Area Affected"] = re.sub(r":.*", "", row["Area Affected"]) # need to handle multiple states

        if row["Area Affected"] not in state_pops_23.keys():
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

        num_affected = row["Number of Customers Affected"]

        state = row["Area Affected"]
        if row["Area Affected"] not in dic:
            dic[state] = int(num_affected)
        else:
            dic[state] += int(num_affected)

    del dic["Arkansas, Mississippi"] # get rid of this eventually
    del dic["Wisconsin, Michigan"]

    return {x: round((y/state_pops_23[x])*100, 2) for x,y in dic.items()} # handle multiple states



def main():
    path = "data/outages/2023_Annual_Summary.xls"
    
    dic = build_outage_dict(path)
    print("")
    print("")
    print("Percent state residents affected by an outage (2023)")
    print("----------------------------------------------------")
    for x,y in dic.items():
        print (x, ":", y, "%")
    


if __name__ == "__main__":
    main()
