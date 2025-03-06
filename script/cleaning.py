import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
from info import state_pops_23
import re
import csv
from pathlib import Path

def build_re_dict(path, year):

    """Produces a dictionary of dictionaries for 2016-2022
    mapping each year to the 50 states's renewable energy % of production."""
    start_year = 2016
    end_year = 2022
    years_to_analyze = list(range(start_year, end_year + 1))
    renewable_path = path #for proofing
    #renewable_path = Path(__file__).parent / "data" / "Renewables" / "prod_btu_re_te.xlsx"
    final_dict = {} 
    renewables_excel = pd.ExcelFile(renewable_path)
    total_renewables_sheet = pd.read_excel(renewables_excel, "Total renewables", header=2)
    total_energy_production_sheet = pd.read_excel(renewables_excel, "Total primary energy", header=2)
    for year in years_to_analyze:
        all_state_dict = {}
        renewable_dict = {}
        for index, row in total_renewables_sheet.iterrows():
            state = row["State"]
            all_state_dict[state] = {"Total renewables": row[year]}
        for index, row in total_energy_production_sheet.iterrows():
            state = row["State"]
            if state in all_state_dict:
                all_state_dict[state]["Total energy production"] = row[year]
        for us_state, energy_dict in all_state_dict.items():
            renewable_dict[us_state] = round((energy_dict["Total renewables"]/energy_dict["Total energy production"])*100, 1)
        final_dict[year] = renewable_dict

    return final_dict


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
            elif row["Area Affected"] == 'Northern and Central California;' or 'Pacific Gas' in row["Area Affected"]: #Why not change this to "row["Area Affected"] == "Pacific Gas"?" - Ganon
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
            if row["property_damage"] == "0.00K" or row["property_damage"] == '': # crop damage too?
                continue

            if "K" in row["property_damage"]:
                damage = float(row["property_damage"][:-1]) * 1000
            if "M" in row["property_damage"]:
                damage = float(row["property_damage"][:-1]) * 1000000
            if "B" in row["property_damage"]:
                damage = float(row["property_damage"][:-1]) * 1000000000

            if row["state"].lower() not in dic:
                dic[row["state"].lower()] = damage
            else:
                dic[row["state"].lower()] += damage

    # return dic

    state_damage = {}
    for text, cost in dic.items():
        state = ' '.join(word.capitalize() for word in text.split())
        
        if state in state_pops_23:
            state_damage[state] = round(cost/state_pops_23[state], 2)


    return state_damage # needs testing

def build_pop_dict(path):
    '''
    Creates list of dictionaries where each dictionary represents a year between
    2016 and 2022. The keys are states, and the values are population according
    to Census data.
    '''
    #for census data 2016-2020
    census_file1 = Path(__file__).parent / "data/state_pops/2010-2020.csv"
    census_file2 = Path(__file__).parent / "data/state_pops/2020-2024.csv"
    year_lst = [{}] *7
    not_states = {'00', '10', '72'}

    #a little wonky bc of orientation of csv
    #written to avoid nested loop

    with open(census_file1, 'r') as file:
        reader = csv.DictReader(file)
        
        #years = (2016, 2017, 2018, 2019)
        #pop_est = f'POPESTIMATE{year}'
        for row in reader:
            if row["STATE"] not in not_states:
                state = row["NAME"]
                year_lst[0][state] = row['POPESTIMATE2016']
                year_lst[1][state] = row['POPESTIMATE2017']
                year_lst[2][state] = row['POPESTIMATE2018']
                year_lst[3][state] = row['POPESTIMATE2019']

    with open(census_file2, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["STATE"] not in not_states:
                state = row["NAME"]
                year_lst[4][state] = row['POPESTIMATE2020']
                year_lst[5][state] = row['POPESTIMATE2021']
                year_lst[6][state] = row['POPESTIMATE2022']

    return year_lst

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