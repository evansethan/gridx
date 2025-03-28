import pandas as pd 
from gridx.utils import build_pop_dict, get_total_pop, state_abbrev
from gridx.clean import clean_outages
import csv

# build global state population dict
pop_dict = build_pop_dict()


def load_re(path, year):
    '''
    Helper: Loads renewables and total energy data for a given year
    '''
    # read excel
    re_df = pd.read_excel(path, "Other renewables", header=2)
    tot_df = pd.read_excel(path, "Total primary energy", header=2)

    # convert to dict for efficient searching
    re_dict = re_df.set_index("State")[year].to_dict()
    tot_dict = tot_df.set_index("State")[year].to_dict()

    return re_dict, tot_dict


def get_damage(row, header):
    '''
    Helper: Gets storm damage from row and converts to float
    '''
    damage = 0

    # convert shorthand to numeric value
    if "K" in row[header]:
        damage = float(row[header][:-1]) * 1000
    if "M" in row[header]:
        damage = float(row[header][:-1]) * 1000000
    if "B" in row[header]:
        damage = float(row[header][:-1]) * 1000000000

    return damage


def build_re_dict(path, year):
    """
    Produces a dictionary mapping each state to its renewable production
    percentage for a given year
    """
    final_dict = {}

    # load data
    re_dict, tot_dict = load_re(path, year)

    # for each state
    for abbrev in state_abbrev.values():
        if abbrev not in re_dict or abbrev not in tot_dict:
            final_dict[abbrev] = None
        else:
            # calculate percent renewable output
            renews = re_dict[abbrev]
            total = tot_dict[abbrev]
            final_dict[abbrev] = round((renews / total) * 100, 2)

    return final_dict


def build_outage_dict(path, year):
    '''
    Builds a dictionary of outage severity (total outages per 100 residents)
    per U.S. state for a given year
    '''

    df = clean_outages(path)
    state_pops = pop_dict[year]

    dic = {}
    for _, row in df.iterrows():

        try:
            # convert num_affected to int
            num_affected = int(row["Number of Customers Affected"])

        except ValueError:
            # skip "Unknown" rows
            continue

        # handle multiple states per row
        states = row["Area Affected"].split(",")

        # get total population of row
        total = get_total_pop(states, state_pops)

        # for each state in a row,
        for state in states:
            state = state.strip()

            if state in state_pops.keys():

                # distribute affected customers
                num_affected = num_affected*(state_pops[state]/total)

                # add to overall sum
                if state not in dic:
                    dic[state] = num_affected
                else:
                    dic[state] += num_affected

                # sum should not surpass population
                if dic[state] > state_pops[state]:
                    dic[state] = state_pops[state]

    # calculate outages per 100 residents
    return {x: round((y / state_pops[x] * 100), 2) for x,y in dic.items()}


def build_storms_dict(path, year):
    '''
    Builds a dictionary of storm damage (total property/crop cost per resident)
    per U.S. state for a given year
    '''

    dic = {}
    with open(path, "r") as f:

        for row in csv.DictReader(f):

            # skip rows with no damage recorded
            if row["property_damage"] == "0.00K" or row["property_damage"] == '':
                if row["crop_damage"] == "0.00K" or row["crop_damage"] == '':
                    continue

            # get total damage cost
            damage = (get_damage(row, "property_damage") +
                      get_damage(row, "crop_damage"))

            # sum total damage per state
            if row["state"] not in dic:
                dic[row["state"]] = damage
            else:
                dic[row["state"]] += damage

    # compute cost per resident
    state_damage = {}
    for state, cost in dic.items():

        if state in pop_dict[year]:
            state_damage[state] = round(cost/pop_dict[year][state], 2)

    return state_damage
