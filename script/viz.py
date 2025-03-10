import pandas as pd
import plotly.express as px
from script.utils import state_abbrev
from script.recon import build_outage_dict, build_storms_dict, build_re_dict

def build_data_frame(path, year, column, build_function):

    dic = build_function(path, year)
    df = pd.DataFrame(list(dic.items()), columns=['state', column])
    df['year'] = year

    return df


def show_outage_map(df):

    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="state", locationmode="USA-states", 
                        color="outage severity", range_color=(0, 10), scope="usa", 
                        color_continuous_scale="Purples",
                        title="Outage Severity by U.S. State, 2016-2022",
                        animation_frame="year")
    fig.update_traces(marker_line_width=0.8, marker_line_color="#bcbcbc", marker_opacity=1.0)
    fig.update_layout(legend_title_text='Percent')
    fig.update_layout(title_text='Outage Severity by U.S. State, 2016-2022<br>(As a Percent of State Population Who Experienced an Outage)', title_x=0.1)

    return fig


def show_storm_map(df):
    
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="state", locationmode="USA-states", 
                        color="cost per resident", range_color=(0, 150), 
                        color_continuous_scale="OrRd",
                        scope="usa", 
                        title="Cost of Storms by U.S. State, 2016-2022",
                        animation_frame="year")
    fig.update_traces(marker_line_width=0.8, marker_line_color="#bcbcbc", marker_opacity=1.0)
    fig.update_layout(legend_title_text='Dollar')
    fig.update_layout(title_text='Cost of Storms by U.S. State, 2016-2022<br>(Property/Crop Damage (USD) Per State Resident)', title_x=0.1)
    

    return fig


def show_re_map(df):

    fig = px.choropleth(df, locations="state", locationmode="USA-states", 
                        color="Renewable Percent", range_color=(0,25), 
                        color_continuous_scale="GnBu",
                        scope="usa", 
                        animation_frame="year")
    fig.update_traces(marker_line_width=0.8, marker_line_color="#bcbcbc", marker_opacity=1.0)
    fig.update_layout(legend_title_text='Percent')
    fig.update_layout(title_text='Renewable Generation by U.S. State, 2016-2022<br>(As a Percent of Total Electricity Generation)', title_x=0.1)

    return fig



def generate_df():

    ## outages
    appended_outage_data = []
    for year in range(2016, 2023):
        path = f"data/outages/{year}_Annual_Summary.xls"
        data = build_data_frame(path, year, 'outage severity', build_outage_dict)
        appended_outage_data.append(data)
    outage = pd.concat(appended_outage_data)
    outage['state'] = outage['state'].map(state_abbrev)
    
    ## storms
    appended_storm_data = []
    for year in range(2016, 2023):
        path = f"data/storms/storms_{year}.csv"
        data = build_data_frame(path, year, 'cost per resident', build_storms_dict)
        appended_storm_data.append(data)
    storm = pd.concat(appended_storm_data)
    storm['state'] = storm['state'].map(state_abbrev)

    ## renewables
    appended_re_data = []
    path = "data/renewables/prod_btu_re_te.xlsx"
    for year in range(2016, 2023):
        data = build_data_frame(path, year, "Renewable Percent", build_re_dict)
        appended_re_data.append(data)
    renewable = pd.concat(appended_re_data)
    
    combined = outage.merge(storm, on=['state', 'year'], how='outer')\
                     .merge(renewable, on=['state', 'year'], how='outer')\
    
    df = combined.melt(id_vars=['state', 'year'], var_name='indicator', value_name='value')

    return df


    # with open('output/maps.html', 'a') as f:
    #     f.write(outage.to_html(full_html=False, include_plotlyjs='cdn'))
    #     f.write(re.to_html(full_html=False, include_plotlyjs='cdn'))
    #     f.write(storm.to_html(full_html=False, include_plotlyjs='cdn'))


# if __name__ == "__main__":
    generate_df()