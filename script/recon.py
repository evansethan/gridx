import pandas as pd 
from utils import build_pop_dict, state_abbrev
from clean import clean_outages
import re
import csv
from pathlib import Path


def build_re_dict(path, year):

    """Produces a dictionary of dictionaries for 2016-2022
    mapping each year to the 50 states's renewable energy % of production."""
    final_dict = {} 
    re_df = pd.read_excel(path, "Other renewables", header=2)
    tot_df = pd.read_excel(path, "Total primary energy", header=2)

    re_dict = re_df.set_index("State")[year].to_dict()
    tot_dict = tot_df.set_index("State")[year].to_dict()
    
    for abbrev in state_abbrev.values():

        renews = re_dict[abbrev]
        total = tot_dict[abbrev]
        final_dict[abbrev] = round((renews / total) * 100, 2)
        
    return final_dict


def build_outage_dict(path, year):

    df = clean_outages(path)
    state_pops = build_pop_dict()[year] # repetitive

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

        # this is handling multiple states in same row
        total = 0
        for state in states:
            # calc total population over all states in row
            total += state_pops[state.strip()]
        
        for state in states:
            state = state.strip()

            percent_affected = count*(state_pops[state]/total) # control for differing state pops

            if state not in dic2:
                dic2[state] = percent_affected
            else:
                dic2[state] += percent_affected

            if dic2[state] > state_pops[state]:
                dic2[state] = state_pops[state] # account for sum of total affected customers > state pop

    return {x: round((y/state_pops[x])*100, 2) for x,y in dic2.items()}


def build_storms_dict(path, year):
    
    pop_dict = build_pop_dict()

    dic = {}
    with open(path, "r") as f:
        
        for row in csv.DictReader(f):
            if row["property_damage"] == "0.00K" or row["property_damage"] == '':
                if row["crop_damage"] == "0.00K" or row["crop_damage"] == '':
                    continue

            if "K" in row["property_damage"]:
                damage = float(row["property_damage"][:-1]) * 1000
            if "M" in row["property_damage"]:
                damage = float(row["property_damage"][:-1]) * 1000000
            if "B" in row["property_damage"]:
                damage = float(row["property_damage"][:-1]) * 1000000000
            
            if "K" in row["crop_damage"]:
                damage += float(row["crop_damage"][:-1]) * 1000
            if "M" in row["crop_damage"]:
                damage += float(row["crop_damage"][:-1]) * 1000000
            if "B" in row["crop_damage"]:
                damage += float(row["crop_damage"][:-1]) * 1000000000

            if row["state"] not in dic:
                dic[row["state"]] = damage
            else:
                dic[row["state"]] += damage

    state_damage = {}
    for state, cost in dic.items():
        
        if state in pop_dict[year]:
            state_damage[state] = round(cost/pop_dict[year][state], 2)

    return state_damage


