from dash import Dash, html, dcc, Input, Output, callback
import webbrowser
import pandas as pd
import plotly.express as px
from utils import state_abbrev
from recon import build_outage_dict, build_storms_dict, build_re_dict
from viz import generate_df, show_outage_map, show_storm_map, show_re_map

app = Dash(__name__)

df = generate_df()

# Define the app layout with dropdowns for selecting map types, 
# graphs for visualization, and a slider for year selection
app.layout = html.Div([
    # Dropdown for selecting the data type for the left map
    html.Div([
        html.Label("Left Map:"),
        dcc.Dropdown(
            ['outage severity', 'cost per resident', 'Renewable Percent'],
            'outage severity',
            id='left-map-dropdown',
        ),
    ], style={'width': '49%', 'display': 'inline-block'}),

    # Dropdown for selecting the data type for the right map
    html.Div([
        html.Label("Right Map:"),
        dcc.Dropdown(
            ['outage severity', 'cost per resident', 'Renewable Percent'],
            'cost per resident',
            id='right-map-dropdown',
        ),
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='left-map', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='right-map', style={'display': 'inline-block', 'width': '49%'}),
    ], style={'display': 'flex'}),

    # Year slider
    html.Div(dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        id='year-slider',
        value=df['year'].max(),
        marks={str(year): str(year) for year in df['year'].unique()}
    ), style={'width': '100%', 'padding': '20px'})
])

def create_map(map_type, df):
    """
    Generates a map based on the selected data type.
    
    Parameters:
        map_type (str): The type of data to visualize 
        df (pd.DataFrame): The dataset filtered by year
    
    Returns:
        A choropleth map based on the selected data type
    """
    df_filtered = df[df['indicator'] == map_type]
    df_filtered = df_filtered.rename(columns={"value": map_type})

    if map_type == 'outage severity':
        return show_outage_map(df_filtered)

    elif map_type == 'cost per resident':
        return show_storm_map(df_filtered)

    elif map_type == 'Renewable Percent':
        return show_re_map(df_filtered)
    
@callback(
    [Output('left-map', 'figure'),
    Output('right-map', 'figure')],
    [Input('left-map-dropdown', 'value'),
    Input('right-map-dropdown', 'value'),
    Input('year-slider', 'value')]
    )        
def update_maps(left_map_type, right_map_type, year_value):
    """
    Updates the maps based on the selected data type and year.
    
    Parameters:
        left_map_type (str): The selected data type for the left map
        right_map_type (str): The selected data type for the right map
        year_value (int): The selected year for visualization
    
    Returns:
        tuple: Two choropleth maps, one for the left side and one for the right side
    """
    df_year = df[df['year'] == year_value]

    left_fig = create_map(left_map_type, df_year)
    right_fig = create_map(right_map_type, df_year)

    left_fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 80, 'r': 10},  
        width=700,
        height=500
    )

    right_fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 80, 'r': 10},  
        width=700,
        height=500
    )

    return left_fig, right_fig


if __name__ == '__main__':
    webbrowser.open_new("http://localhost:8050")
    app.run_server()

