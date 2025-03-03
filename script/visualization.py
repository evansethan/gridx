import pandas as pd
import plotly.express as px
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


def main():

    # path = f"data/outages/2016_Annual_Summary.xls"
    # show_outage_map(path, 2016)

    # for i in range(2016, 2024):
    #     path = f"data/storms/{i}.csv"
    #     show_storm_map(path, i)

    i = 2016
    path = f"data/storms/{i}.csv"
    show_storm_map(path, i)

    

if __name__ == "__main__":
    main()
