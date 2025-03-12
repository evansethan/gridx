from pathlib import Path
import csv

state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC',
    'Puerto Rico': 'PR'
    }


def build_pop_dict():
    '''
    Creates dict of dictionaries where each dictionary represents a year between
    2016 and 2022. Outer keys are years, inner keys are states, innermost values
    are the state populations for that year.
    '''
    census_file1 = Path("data/state_pops/2010-2020.csv")
    census_file2 = Path("data/state_pops/2020-2024.csv")
    year_dict = {y:{} for y in range(2016, 2023)}

    # census file 2010-2020.csv
    with open(census_file1, 'r') as file:
        for row in csv.DictReader(file): #anyway to skip past the regions>
            state = row["NAME"]
            for i in range(2016, 2020):
                year_dict[i][state] = int(row[f'POPESTIMATE{i}'])

    # census file 2020-2024.csv
    with open(census_file2, 'r') as file:
        for row in csv.DictReader(file):
            state = row["NAME"]
            for i in range(2020, 2023):
                year_dict[i][state] = int(row[f'POPESTIMATE{i}'])

    return year_dict


def load_re(path, year):
    '''
    Load and convert renewables excel files to dict
    '''
    re_df = pd.read_excel(path, "Other renewables", header=2)
    tot_df = pd.read_excel(path, "Total primary energy", header=2)

    re_dict = re_df.set_index("State")[year].to_dict()
    tot_dict = tot_df.set_index("State")[year].to_dict()

    return re_dict, tot_dict