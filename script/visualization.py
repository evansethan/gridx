import pandas as pd
import plotly.express as px
import pandas as pd
from pathlib import Path
from info import state_abbrev
from cleaning import build_outage_dict, build_storms_dict


def show_outage_map(path, year):

    dic = build_outage_dict(path) # calculate overall outage severity for the year to include in map
    df = pd.DataFrame(list(dic.items()), columns=['state', 'outage severity'])
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", color="outage severity", range_color=(0, 10), scope="usa", title=f"{year} Outage Severity by U.S. State")
    fig.show()


def show_storm_map(path, year):

    dic = build_storms_dict(path) 
    df = pd.DataFrame(list(dic.items()), columns=['state', 'cost per resident'])
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", color="cost per resident", range_color=(10, 100), scope="usa", title=f"{year} Outage Severity by U.S. State")
    fig.show()

def get_renewable_production(start_year:int=2016, end_year:int=2022):

    """Takes a range of years and produces a dictionary of dictionaries
    mapping each year to the 50 states's renewable energy % of production."""
    if start_year < 2016 or start_year > 2022:
        raise KeyError("Please enter a valid start year from 2016-2022.")
    if end_year < 2016 or end_year > 2022:
        raise KeyError("Please enter a valid end year from 2016-2022.")
    if start_year > end_year:
        raise KeyError("Please make sure your start and end years are in the correct order.")
    years_to_analyze = list(range(start_year, end_year + 1))
    renewable_path = "data/renewables/prod_btu_re_te.xlsx"
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
            renewable_dict[us_state] = energy_dict["Total renewables"]/energy_dict["Total energy production"]
        final_dict[year] = renewable_dict
    return final_dict


def main():

    i = 2016
    #path = f"data/outages/{i}_Annual_Summary.xls"
    #show_outage_map(path, i)
    #path = f"data/storms/storms_{i}.csv"
    #show_storm_map(path, i)
    x = get_renewable_production(2017, 2022)
    print(x)

    # for i in range(2016, 2024):
    #     path = f"data/storms/{i}.csv"
    #     show_storm_map(path, i)



    

if __name__ == "__main__":
    main()