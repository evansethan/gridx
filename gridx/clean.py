import csv
import pandas as pd
import re
from gridx.utils import state_abbrev


def clean_storms(path):
    '''
    Cleans and exports shortened versions of large CSV files containing storm
    damage data - only needs to be run once on raw data from NOAA (see
    data/storms/noaa_source_urls.txt). Preexisting CSV files in data/storms are
    output of this function. 
    '''

    lst = []
    fullpath = "data/storms/" + path

    with open(fullpath, "r") as f:

        for row in csv.DictReader(f):
            dic = {}

            # skip rows with no damage recorded
            if row["DAMAGE_PROPERTY"] == '' or row["DAMAGE_PROPERTY"] == '0.00K':
                if row["DAMAGE_CROPS"] == '' or row["DAMAGE_CROPS"] == '0.00K':
                    continue

            # standardize state name, build dictionary of relevant columns
            state = ' '.join(word.capitalize() for word in row["STATE"].split())
            dic["year"] = row["YEAR"]
            dic["state"] = state
            dic["property_damage"] = row["DAMAGE_PROPERTY"]
            dic["crop_damage"] = row["DAMAGE_CROPS"]

            lst.append(dic)

    # export to csv
    with open(f"data/storms/storms_{path}", "w") as f:

        fieldnames = lst[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lst)


def clean_outages(path):
    '''
    Takes in a path to a DOE-outage excel file and converts it to a cleaned
    pandas dataframe
    '''

    df = pd.DataFrame(pd.read_excel(path))

    df.columns = df.iloc[0]
    df = df.drop(index=0)

    area = "Area Affected"

    for _, row in df.iterrows():

        # split text by ':' or ';' and strip spaces, rejoin into single string
        parts = [part.strip() for part in re.split(r'[:;]', row[area])]
        row[area] = ",".join(parts).rstrip(",")

        # handle energy companies / regions
        if row[area] not in state_abbrev.keys():
            region = row[area]
            if region == "LUMA Energy":
                row[area] = "Puerto Rico"
            elif region == "ISO New England":
                row[area] = "Connecticut,Maine,Massachusetts,New Hampshire,Rhode Island,Vermont"
            elif region == "Otter Tail Power Co":
                row[area] = "Minnesota,North Dakota,South Dakota"
            elif "Western Area Power" in region:
                row[area] = "Montana,North Dakota,South Dakota,Nebraska,Iowa,Minnesota"
            elif (region == 'Northern and Central California;' or 'Pacific Gas' in region):
                row[area] = "California"
            elif region == 'Central Oklahoma':
                row[area] = "Oklahoma"
            elif region == 'Pacificorp':
                row[area] = "Oregon,California,Washington,Oregon,Utah,Wyoming,Idaho"
            elif (region == 'Tampa Electric Company' or region == 'Seminole Electric Cooperative Inc'):
                row[area] = "Florida"
            elif region == 'Tucson Electric Power':
                row[area] = "Arizona"

    return df


def main():
    '''
    Main function for cleaning storm data, ran once and stored output in data/storms
    (see data/storms/noaa_source_urls.txt for raw data)
    '''
    for i in range(2014, 2025):
        clean_storms(f"{i}.csv")  # shortened default filenames


if __name__ == "__main__":
    main()