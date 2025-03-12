# Team Name: Grid Expectations

## Members

- Ethan Evans ethane@uchicago.edu
- Ganon Evans ganon@uchicago.edu
- Jinny Kim ekim1208@uchicago.edu
- Callie Leone clleone@uchicago.edu

Overview:

This project aims to examine power outages and its association with energy generation
sources in the United States. By analyzing the frequency and severity of power outages,
we aim to explore patterns in grid reliability and generation mix across different
regions and time periods. 

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
Outage data (duration, number of customers affected) by U.S. region

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
National Oceanic and Atmospheric Administration
Information on dollar damage amount of storms in given years. 

How To Run:

"uv sync" (install uv if necessary)
"uv run gridx"

To run pytests:
"uv run pytest"

A new tab will open in your browser with the program. You should have two drop-down boxes that will allow you to select from the outage, renewable percentage, and storm damage heat maps. From there, a toggle at the bottom of the screen allows you to progress through the years and compare over time. Hovering over a state reveals specific information for that map in the selected year.







