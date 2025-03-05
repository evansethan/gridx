import pandas as pd
from pathlib import Path

#Note: this notebook needs to be in the project directory and not "scratch" to work

#renewable_path = Path(__file__).parent / "data" / "Renewables" / "prod_btu_re_te.xlsx"
def build_re_dict(path):

    state_dict = {}
    final_dict = {} #needs to be dict of dict for each year then each state to renewables
    #limit range of 2016 to 2023, can allow subsets
    # renewable_path = "data/renewables/prod_btu_re_te.xlsx"
    renewable_path = path
    renewables_excel = pd.ExcelFile(renewable_path)
    total_renewables_sheet = pd.read_excel(renewables_excel, "Total renewables", header=2)
    total_energy_production_sheet = pd.read_excel(renewables_excel, "Total primary energy", header=2)

    for index, row in total_renewables_sheet.iterrows():
        state = row["State"]
        state_dict[state] = {"Total renewables": row[2022]}

    for index, row in total_energy_production_sheet.iterrows():
        state = row["State"]
        if state in state_dict:
            state_dict[state]["Total energy production"] = row[2022]

    for us_state, energy_dict in state_dict.items():
        # energy_dict["Renewable Percent"] = energy_dict["Total renewables"]/energy_dict["Total energy production"]
        final_dict[us_state] = energy_dict["Total renewables"]/energy_dict["Total energy production"]

    return final_dict