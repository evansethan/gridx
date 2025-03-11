# Team Name: Flavortown

## Members

- Ethan Evans ethane@uchicago.edu
- Ganon Evans ganon@uchicago.edu
- Jinny Kim ekim1208@uchicago.edu
- Callie Leone clleone@uchicago.edu

Overview:

This project aims to examine power outages and its association with energy generation sources in the United States. By analyzing the frequency and severity of power outages, we aim to explore patterns in grid reliability and generation mix across different regions and time periods. 

To visualize the results, we have created three interactive maps (e.g., heat map)
that visualize the changes in power outages and storm damage as well as the 
shifts in electricity generation sources over time. We have aggregated data by 
state to account for their outage history and their energy production and consumption. 
These tools will allow users to easily examine regional differences in renewable energy 
adoption and grid reliability in the U.S.

Data Sources (in "data" folder)

OE-417 (data/outages)
Link: https://doe417.pnnl.gov/instructions
Department of Energy
Outage data (duration, number of customers affected) by U.S. region (NERC region for our purposes)

State Energy Data System (renewables)
Link: https://www.eia.gov/state/seds/seds-data-complete.php
U.S. Energy Information Administration
Total energy production with renewables broken out by state

U.S. Census State Population Data
Link: 2010-2020: https://www.census.gov/programs-surveys/popest/technical-
documentation/research/evaluation-estimates/2020-evaluation-estimates/2010s-state-total.html
2020-2024: https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html
U.S. Census Bureau
Population by state over each decade.

Storm Bulk Data
Link: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
NOAA
Information on dollar damage amount of storms in given years. 


How To Run:

run "uv sync"
run "uv run python script"

You should have two drop down boxes that will allow you to select from the outage, renewable percentage, and storm damage heat maps
to be displayed on either the right or the left map. From there, a toggle at the bottom of the screen allows you to progress through the years from 2016-2022 and and compare over time.

Our sample API request code can be found in script/API. We will not be using this code in the final project. Similarly, 

script/scratch/load_data.ipynb has several additional functions, which are not yet complete:

Initial classes and data load - We define two classes: NERC and facility. The NERC class simply contains just the ID of a NERC region and its shapefile polygon. The facility object contains significantly more information, including the name and ID of the facility and its parent company, its capacity,  its location in latitude and longitude. Each facility is initially processed by generator, so its technology varies for each row it exists. The special ID is a combination of the ID of the plant and its parent company to unique identify the facility. Load_shapefiles and load_frs_csv are both functions that take the aforementioned NERC and EIA files then convert them into our NERC and facility objects.

There are several functions carried over from PA 5 dealing with the creation of Quadtrees and bounding boxes, and conducting spatial joins.

There are three bucketing functions that return dictionaries mapping the special ID of a planet to its energy output. Get_plant_total provides the total capacity, get_fuel_total is capacity broken down by one of the provided energy sources ranging from oil to nuclear to wind, and get_energy_type_total takes the energy source buckets and aggregates them into three largescale buckets for green energy, fossil fuels, and nuclear power. 







