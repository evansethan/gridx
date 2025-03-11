import csv
import pandas as pd
import re
from gridx.utils import state_abbrev


def clean_storms(path):
    '''
    Cleans and exports shortened versions of large CSV files containing storm
    damage data - only needs to be run once on raw data from NOAA (see
    data/storms/noaa_source_urls.txt)
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

    for _, row in df.iterrows():

        # split text by ':' or ';' and strip spaces, rejoin into single string
        parts = [part.strip() for part in re.split(r'[:;]', row["Area Affected"])]
        row["Area Affected"] = ",".join(parts).rstrip(",")

        # handle energy companies / regions
        if row["Area Affected"] not in state_abbrev.keys():
            if row["Area Affected"] == "LUMA Energy":
                row["Area Affected"] = "Puerto Rico"
            if row["Area Affected"] == "ISO New England":
                row["Area Affected"] = "Connecticut,Maine,Massachusetts,New Hampshire,Rhode Island,Vermont"
            if row["Area Affected"] == "Otter Tail Power Co":
                row["Area Affected"] = "Minnesota,North Dakota,South Dakota"
            if "Western Area Power" in row["Area Affected"]:
                row["Area Affected"] = "Montana,North Dakota,South Dakota,Nebraska,Iowa,Minnesota"
            if (row["Area Affected"] == 'Northern and Central California;'
                or 'Pacific Gas' in row["Area Affected"]):
                row["Area Affected"] = "California"
            if row["Area Affected"] == 'Central Oklahoma':
                row["Area Affected"] = "Oklahoma"
            if row["Area Affected"] == 'Pacificorp':
                row["Area Affected"] = "Oregon,California,Washington,Oregon,Utah,Wyoming,Idaho"
            if (row["Area Affected"] == 'Tampa Electric Company' 
                or row["Area Affected"] == 'Seminole Electric Cooperative Inc'):
                row["Area Affected"] = "Florida"
            if row["Area Affected"] == 'Tucson Electric Power':
                row["Area Affected"] = "Arizona"

    return df


def main():
    '''
    Main function for cleaning, ran once on raw data to shorten csv's
    (see data/storms/noaa_source_urls.txt)
    '''
    for i in range(2014, 2025):
        clean_storms(f"{i}.csv")  # changed default filenames


if __name__ == "__main__":
    main()