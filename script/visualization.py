import pandas as pd
import plotly.express as px
from pathlib import Path
from info import state_abbrev
from cleaning import build_outage_dict, build_storms_dict, build_re_dict


def build_data_frame(path, year, column, build_function):

    if build_function == build_re_dict: 
        dic_all = build_function(path, year)
        dic = dic_all[year]
    else:
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
                        color_continuous_scale="Purples",
                        title="Outage Severity by U.S. State, 2002-2023",
                        animation_frame="year")
    fig.update_traces(marker_line_width=0, marker_opacity=0.8)
    fig.update_layout(legend_title_text='Percent')
    fig.update_layout(title_text='Outage Severity by U.S. State, 2016-2022<br>(As a Percent of State Population Who Experienced an Outage)', title_x=0.5)
    # fig.update_layout(title_text="(As a Percent of Total Electricity Generation)", title_x=0.5)
    fig.update_geos(
    showsubunits=True, subunitcolor="black"
    )
    # fig.show()

    return fig


def show_storm_map(df):

    # dic = build_storms_dict(path) 
    # df = pd.DataFrame(list(dic.items()), columns=['state', 'cost per resident'])
    
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", 
                        color="cost per resident", range_color=(0, 50), 
                        color_continuous_scale="OrRd",
                        scope="usa", 
                        title="Cost of Storms by U.S. State, 2014-2024",
                        animation_frame="year")
    fig.update_traces(marker_line_width=0, marker_opacity=0.8)
    fig.update_layout(legend_title_text='Dollar')
    fig.update_layout(title_text='Cost of Storms by U.S. State, 2016-2022<br>(Damage to Property or Crop Per State Resident)', title_x=0.5)
    # fig.update_layout(title_text="(As a Percent of Total Electricity Generation)", title_x=0.5)
    fig.update_geos(
    showsubunits=True, subunitcolor="black"
    )
    # fig.show()

    return fig


def show_re_map(df):

    # dic = build_storms_dict(path) 
    # df = pd.DataFrame(list(dic.items()), columns=['state', 'cost per resident'])
    
    # df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="state", locationmode="USA-states", 
                        color="Renewable Percent", range_color=(0,100), 
                        color_continuous_scale="GnBu",
                        scope="usa", 
                        animation_frame="year")
    fig.update_traces(marker_line_width=0, marker_opacity=0.8)
    fig.update_layout(legend_title_text='Percent')
    fig.update_layout(title_text='Renewable Generation by U.S. State, 2016-2022<br>(As a Percent of Total Electricity Generation)', title_x=0.5)
    # fig.update_layout(title_text="(As a Percent of Total Electricity Generation)", title_x=0.5)
    fig.update_geos(
    showsubunits=True, subunitcolor="black"
    )
    # fig.show()

    return fig

def main():

    ## outages
    appended_outage_data = []
    for year in range(2016, 2023):
        path = f"data/outages/{year}_Annual_Summary.xls"
        data = build_data_frame(path, year, 'outage severity', build_outage_dict)
        appended_outage_data.append(data)
    appended_outage_data = pd.concat(appended_outage_data)

    outage = show_outage_map(appended_outage_data)
    
    ## storms
    appended_storm_data = []
    for year in range(2016, 2023):
        path = f"data/storms/storms_{year}.csv"
        data = build_data_frame(path, year, 'cost per resident', build_storms_dict)
        appended_storm_data.append(data)
    appended_storm_data = pd.concat(appended_storm_data)

    storm = show_storm_map(appended_storm_data)

    ## renewables
    appended_re_data = []
    path = "data/Renewables/prod_btu_re_te.xlsx"
    for year in range(2016, 2023):
        data = build_data_frame(path, year, "Renewable Percent", build_re_dict)
        appended_re_data.append(data)
    appended_re_data = pd.concat(appended_re_data)
    
    re = show_re_map(appended_re_data)

    with open('..output/maps.html', 'a') as f:
        f.write(outage.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(re.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(storm.to_html(full_html=False, include_plotlyjs='cdn'))
        
    # path = f"../data/Renewables/prod_btu_re_te.xlsx"
    # re_data = build_data_frame(path, year, 'Renewable Percent', get_renewable_production)

    # show_re_map(re_data)







    

if __name__ == "__main__":
    main()