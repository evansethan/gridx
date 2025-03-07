import csv
import pandas as pd
import re
from utils import state_abbrev

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
            if row["DAMAGE_PROPERTY"] == '' or row["DAMAGE_PROPERTY"] == '0.00K':
                if row["DAMAGE_CROPS"] == '' or row["DAMAGE_CROPS"] == '0.00K':
                    continue

            state = ' '.join(word.capitalize() for word in row["STATE"].split()) # normalize state name
            dic["year"] = row["YEAR"]
            dic["state"] = state
            dic["property_damage"] = row["DAMAGE_PROPERTY"]
            dic["crop_damage"] = row["DAMAGE_CROPS"]

            lst.append(dic)

    with open(f"data/storms/storms_{path}", "w") as f:

        fieldnames = lst[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lst)


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
            if row["Area Affected"] == "ISO New England":
                row["Area Affected"] = "Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont"
            if row["Area Affected"] == "Otter Tail Power Co":
                row["Area Affected"] = "Minnesota, North Dakota, South Dakota"
            if "Western Area Power" in row["Area Affected"]:
                row["Area Affected"] = "Montana, North Dakota, South Dakota, Nebraska, Iowa, Minnesota"
            if row["Area Affected"] == 'Northern and Central California;' or 'Pacific Gas' in row["Area Affected"]:
                row["Area Affected"] = "California"
            if row["Area Affected"] == 'Central Oklahoma':
                row["Area Affected"] = "Oklahoma"
            if row["Area Affected"] == 'Pacificorp':  
                row["Area Affected"] = "Oregon, California, Washington, Oregon, Utah, Wyoming, Idaho"
            if row["Area Affected"] == 'Tampa Electric Company' or row["Area Affected"] == 'Seminole Electric Cooperative Inc':  
                row["Area Affected"] = "Florida"
            if row["Area Affected"] == 'Tucson Electric Power':
                row["Area Affected"] = "Arizona"
                
    return df


def main():

    for i in range(2014,2025):
        clean_storms(f"{i}.csv")

if __name__ == "__main__":
    main()