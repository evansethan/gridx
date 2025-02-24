from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px


def show_map():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)


    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                    dtype={"fips": str})


    fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            scope="usa",
                            labels={'unemp':'mock data'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()


def main():
    show_map()

if __name__ == "__main__":
    main()
