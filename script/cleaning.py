import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
  


def read_and_clean_outages(path) -> dict:
    '''
    Reads outage data and returns dict of total customers affected by NERC region
    '''

    # read an excel file and convert into a dataframe object 
    df = pd.DataFrame(pd.read_excel(path))
    
    df.columns = df.iloc[0]
    df = df.drop(index=0)

    outages = []
    dic = {}
    for _, row in df.iterrows():

        # add datetime (duration) code here

        try: 
            start = row["Date Event Began"] + " " + str(row["Time Event Began"])
            end = row["Date of Restoration"] + " " + str(row["Time of Restoration"])
        except:
            start = "error"
            end = "error"

        if row["Number of Customers Affected"] == "Unknown": # need to handle NaN
            continue
        if row["NERC Region"] not in dic:
            dic[row["NERC Region"]] = int(row["Number of Customers Affected"])
        else:
            dic[row["NERC Region"]] += int(row["Number of Customers Affected"])

        outages.append((row["NERC Region"], start, end))

    return {x:y for x,y in dic.items() if y!=0}



def main():
    path23 = "data/outages/2023_Annual_Summary.xls"
    path17 = "data/outages/2017_Annual_Summary.xls"
    print(read_and_clean_outages(path23))
    print(read_and_clean_outages(path17))


if __name__ == "__main__":
    main()
