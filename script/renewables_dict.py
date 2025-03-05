def get_renewable_production():

    """Produces a dictionary of dictionaries for 2016-2022
    mapping each year to the 50 states's renewable energy % of production."""
    start_year = 2016
    end_year = 2022
    years_to_analyze = list(range(start_year, end_year + 1))
    renewable_path = "data/renewables/prod_btu_re_te.xlsx" #for proofing
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