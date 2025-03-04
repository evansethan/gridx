import pandas as pd
import plotly.express as px
from info import state_abbrev
from cleaning import build_outage_dict


def build_data_frame(path, year):

    dic = build_outage_dict(path) # calculate overall outage severity for the year to include in map

    df = pd.DataFrame(list(dic.items()), columns=['state', 'outage severity'])
    df['year'] = year

    return df

def show_map(df):

    # dic = data # calculate overall outage severity for the year to include in map
    # df = pd.DataFrame(list(dic.items()), columns=['state', 'outage severity', 'year'])
    
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", 
                        color="outage severity", range_color=(0, 10), scope="usa", 
                        title="Outage Severity by U.S. State, 2002-2023",
                        animation_frame="year")
    fig.show()


def main():

    appended_data = []
    for year in range(2015, 2024):
        path = f"../data/outages/{year}_Annual_Summary.xls"
        data = build_data_frame(path, year)
        appended_data.append(data)
    appended_data = pd.concat(appended_data)
    print(appended_data)

    show_map(appended_data)
    
    # for i in range(2016, 2024):
    #     path = f"data/outages/{i}_Annual_Summary.xls" # can run data from 2016-2023 (population counts used for percentages are from 2023 only, we will fix this)
    #     show_map(path, i)

    

if __name__ == "__main__":
    main()