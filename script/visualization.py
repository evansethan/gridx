import pandas as pd
import plotly.express as px
from info import state_abbrev

def show_map():

    df = pd.read_csv("data/areas.csv")
    df['abbrev'] = df['state'].map(state_abbrev)
    fig = px.choropleth(df, locations="abbrev", locationmode="USA-states", color="area (sq. mi)", range_color=(1000, 150000), scope="usa")
    fig.show()

def main():
    show_map()

if __name__ == "__main__":
    main()
