import pandas as pd 
from info import state_abbrev
import re
import csv
from pathlib import Path


def build_re_dict(path, year):

    """Produces a dictionary of dictionaries for 2016-2022
    mapping each year to the 50 states's renewable energy % of production."""
    final_dict = {} 
    renewables_df = pd.read_excel(path, "Other renewables", header=2) # changed to other
    total_energy_df = pd.read_excel(path, "Total primary energy", header=2)

    renewables_dict = renewables_df.set_index("State")[year].to_dict()
    total_energy_dict = total_energy_df.set_index("State")[year].to_dict()
    
    for abbrev in state_abbrev.values():

        renews = renewables_dict[abbrev]
        total = total_energy_dict[abbrev]
        final_dict[abbrev] = round((renews / total) * 100, 2)
        
    return final_dict


def clean_outages(path):

    df = pd.DataFrame(pd.read_excel(path))
  
    df.columns = df.iloc[0]
    df = df.drop(index=0)

    for _, row in df.iterrows():
        #row["Area Affected"] = "".join(re.findall(r"\b\w+:", row["Area Affected"])) # maybe this?
        row["Area Affected"] = re.sub(r":.*", "", row["Area Affected"]) # still some missing states maybe...

        if row["Area Affected"] not in state_abbrev.keys():
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


def build_outage_dict(path, year):

    df = clean_outages(path)
    pop_dict_year = build_pop_dict()[year] # repetitive

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

        # this is handling multiple states in same row
        total = 0
        for state in states:
            # calc total population over all states in row
            total += pop_dict_year[state.strip()]
        
        for state in states:
            state = state.strip()

            percent_affected = count*(pop_dict_year[state]/total) # control for differing state pops

            if state not in dic2:
                dic2[state] = percent_affected
            else:
                dic2[state] += percent_affected

            if dic2[state] > pop_dict_year[state]:
                dic2[state] = pop_dict_year[state] # account for sum of total affected customers > state pop

    return {x: round((y/pop_dict_year[x])*100, 2) for x,y in dic2.items()}



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

    #return dic

    state_damage = {}
    for state, cost in dic.items():
        # state = ' '.join(word.capitalize() for word in text.split())
        
        if state in pop_dict[year]:
            state_damage[state] = round(cost/pop_dict[year][state], 2)


    return state_damage # needs testing

def build_pop_dict():
    '''
    Creates list of dictionaries where each dictionary represents a year between
    2016 and 2022. The keys are states, and the values are population according
    to Census data.
    '''
    #for census data 2016-2020
    census_file1 = Path(__file__).parent.parent / "data/state_pops/2010-2020.csv"
    census_file2 = Path(__file__).parent.parent / "data/state_pops/2020-2024.csv"
    year_dict = {2016: {},
                 2017: {},
                 2018: {},
                 2019: {},
                 2020: {},
                 2021: {},
                 2022: {},
                # 2023: {},
                }
    not_states = {'00', '10'} # 72? get rid of magic numers and assign to variable names

    #a little wonky bc of orientation of csv
    #written to avoid nested loop

    with open(census_file1, 'r') as file:
        reader = csv.DictReader(file)
        
        #years = (2016, 2017, 2018, 2019)
        #pop_est = f'POPESTIMATE{year}'
        for row in reader:
            if row["STATE"] not in not_states:
                state = row["NAME"]
                year_dict[2016][state] = int(row['POPESTIMATE2016'])
                year_dict[2017][state] = int(row['POPESTIMATE2017'])
                year_dict[2018][state] = int(row['POPESTIMATE2018'])
                year_dict[2019][state] = int(row['POPESTIMATE2019'])

    with open(census_file2, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["STATE"] not in not_states:
                state = row["NAME"]
                year_dict[2020][state] = int(row['POPESTIMATE2020'])
                year_dict[2021][state] = int(row['POPESTIMATE2021'])
                year_dict[2022][state] = int(row['POPESTIMATE2022'])
                #year_dict[2023][state] = int(row['POPESTIMATE2023'])

    return year_dict

def main():
    path = "data/outages/2022_Annual_Summary.xls"
    
    dic = build_outage_dict(path, 2022)
    print("")
    print("")
    print("Percent state residents affected by an outage (2022)")
    print("----------------------------------------------------")
    for x,y in dic.items():
        print (x, ":", y, "%")


    # i = 2020
    # path = f"data/Renewables/prod_btu_re_te.xlsx"
    
    # print(build_re_dict(path, i))
    


if __name__ == "__main__":
    main()