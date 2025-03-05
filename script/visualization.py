import pandas as pd
import plotly.express as px
from info import state_abbrev
from cleaning import build_outage_dict, build_storms_dict
from renewables_dict import build_re_dict

def build_data_frame(path, year, column, build_function):

    dic = build_function(path) # calculate overall outage severity for the year to include in map
    df = pd.DataFrame(list(dic.items()), columns=['state', column])
    df['year'] = year

    return df


def show_outage_map(df):

    # dic = data # calculate overall outage severity for the year to include in map
    # df = pd.DataFrame(list(dic.items()), columns=['state', 'outage severity', 'year'])
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", 
                        color="outage severity", range_color=(0, 10), scope="usa", 
                        title="Outage Severity by U.S. State, 2002-2023",
                        animation_frame="year")
    fig.show()


def show_storm_map(df):

    # dic = build_storms_dict(path) 
    # df = pd.DataFrame(list(dic.items()), columns=['state', 'cost per resident'])
    
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", 
                        color="cost per resident", range_color=(10, 100), 
                        scope="usa", 
                        title="Cost of Storms by U.S. State, 2014-2024",
                        animation_frame="year")
    fig.show()


def show_re_map(df):

    # dic = build_storms_dict(path) 
    # df = pd.DataFrame(list(dic.items()), columns=['state', 'cost per resident'])
    
    # df['abbrev'] = df['state'].map(state_abbrev)
    print(df)
    fig = px.choropleth(df, locations="state", locationmode="USA-states", 
                        color="Renewable Percent", range_color=(0,1), 
                        color_continuous_scale="GnBu",
                        scope="usa", 
                        animation_frame="year")
    fig.update_traces(marker_line_width=0, marker_opacity=0.8)
    fig.update_layout(title_text="Renewable Generation by U.S. State, 2022", title_x=0.5)
    fig.update_geos(
    showsubunits=True, subunitcolor="black"
    )
    fig.show()

def main():

    ## outages
    appended_outage_data = []
    for year in range(2015, 2024):
        path = f"../data/outages/{year}_Annual_Summary.xls"
        data = build_data_frame(path, year, 'outage severity', build_outage_dict)
        appended_outage_data.append(data)
    appended_outage_data = pd.concat(appended_outage_data)

    show_outage_map(appended_outage_data)
    
    ## storms
    appended_storm_data = []
    for year in range(2014, 2022):
        path = f"../data/storms/storms_{year}.csv"
        data = build_data_frame(path, year, 'cost per resident', build_storms_dict)
        appended_storm_data.append(data)
    appended_storm_data = pd.concat(appended_storm_data)

    show_storm_map(appended_storm_data)

    ## renewables
    re_data = build_data_frame("../data/Renewables/prod_btu_re_te.xlsx", "2022",
                               "Renewable Percent", build_re_dict)
    
    show_re_map(re_data)
    # path = f"../data/Renewables/prod_btu_re_te.xlsx"
    # re_data = build_data_frame(path, year, 'Renewable Percent', get_renewable_production)

    # show_re_map(re_data)







    

if __name__ == "__main__":
    main()