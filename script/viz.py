import pandas as pd
import plotly.express as px
from utils import state_abbrev
from recon import build_outage_dict, build_storms_dict, build_re_dict

def build_data_frame(path, year, column, build_function):
    """
    Builds a dataframe from a given data source and function for specific dataset.
    
    Parameters:
        path (str): File path to the dataset
        year (int): Year of the dataset
        column (str): Name of the column for the processed data
        build_function (function): Function to process the dataset into a dictionary

    Returns:
        pd.DataFrame: Processed dataframe with state, year, and the specified column.
    """

    dic = build_function(path, year)
    df = pd.DataFrame(list(dic.items()), columns=['state', column])
    df['year'] = year

    return df

def show_map(df, color_column, title, color_scale, range_color, colorbar_title):
    """
    Generates a choropleth map visualization for the given dataset.
    
    Parameters:
        df (pd.DataFrame): Dataframe containing state, year, and the specified data column.
        color_column (str): Column to be used for colour
        title (str): Title of the map
        color_scale (str): Colour scale for visualization
        range_color (tuple): Range of colour values
        colorbar_title (str): Title for the colourbar legend

    Returns:
        Choropleth maps
    """
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(
        df, locations="state", locationmode="USA-states",
        color=color_column, range_color=range_color,
        color_continuous_scale=color_scale, scope="usa",
        animation_frame="year"
    )
    fig.update_traces(marker_line_width=0.8, marker_line_color="#bcbcbc", marker_opacity=1.0)
    fig.update_layout(
        title_text=title, title_x=0.1,
        coloraxis_colorbar=dict(title=dict(text=colorbar_title))
    )
    return fig


def show_outage_map(df):
    """
    Visualizes power outage severity across states on a choropleth map.
    """
    return show_map(df, "outage severity", 
                    "Annual Average Power Outage (2016-2022)", 
                    "Purples", (0, 10), "Event<br>Per Capita")


def show_storm_map(df):
    """
    Visualizes severe weather damage cost per resident across states on a choropleth map.
    """
    return show_map(df, "cost per resident", 
                    "Annual Average Severe Weather (2016-2022)", 
                    "OrRd", (0, 150), "Damage<br>Per Capita<br>(USD)")


def show_re_map(df):
    """
    Visualizes share of renewable energy generation across states on a choropleth map.
    """
    return show_map(df, "Renewable Percent", 
                    "Annual Share of Renewable Generation in Power Mix (2016-2022)", 
                    "GnBu", (0, 25), "%")


def generate_df():
    """
    Generates a consolidated Dataframe containing outage, storm, and renewable 
    energy data from 2016 to 2022.
    
    Returns:
        pd.DataFrame: DataFrame with state, year, indicator type, and corresponding values
    """

    years = range(2016, 2023)
    
    outage_data = [build_data_frame(f"data/outages/{year}_Annual_Summary.xls", year, 
                                    "outage severity", build_outage_dict) for year in years]
    storm_data = [build_data_frame(f"data/storms/storms_{year}.csv", year, 
                                   "cost per resident", build_storms_dict) for year in years]
    renewable_data = [build_data_frame("data/renewables/prod_btu_re_te.xlsx", year, 
                                       "Renewable Percent", build_re_dict) for year in years]
    
    outage = pd.concat(outage_data)
    storm = pd.concat(storm_data)
    renewable = pd.concat(renewable_data)
    
    combined = outage.merge(storm, on=['state', 'year'], how='outer')\
                     .merge(renewable, on=['state', 'year'], how='outer')
    
    return combined.melt(id_vars=['state', 'year'], var_name='indicator', value_name='value')
