import pandas as pd
import plotly.express as px
from info import state_abbrev
from cleaning import build_outage_dict


def show_map(path, year):

    dic = build_outage_dict(path) # calculate overall outage severity for the year to include in map
    df = pd.DataFrame(list(dic.items()), columns=['state', 'outage severity'])
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", color="outage severity", range_color=(0, 10), scope="usa", title=f"{year} Outage Severity by U.S. State")
    fig.show()


def main():

    path = f"data/outages/2023_Annual_Summary.xls"
    show_map(path, 2023)

    # for i in range(2016, 2024):
    #     path = f"data/outages/{i}_Annual_Summary.xls" # can run data from 2016-2023 (population counts used for percentages are from 2023 only, we will fix this)
    #     show_map(path, i)

    

if __name__ == "__main__":
    main()
