# Flavortown

## Abstract

Our group will explore the trends in power outages and electricity generation
sources across U.S. states from 2000 to 2023. One of the questions we are
interested in is whether states that are increasingly integrating weather-dependent
renewable energy (solar, wind) into their grids are experiencing more or fewer
power outages linked to severe weather events. 

To visualize the results, we will create an interactive map (e.g., heat map)
that visualizes the changes in power outages and shifts in electricity generation
sources over time. We will aggregate data by state to account for their outage
history and their energy production and consumption. We also want to integrate
a visual aid indicating each state’s change in its energy profile and its change
in severity of outages. These tools will allow users to easily examine regional
differences in renewable energy adoption and grid reliability in the U.S. 

## Data Sources

### Data Source: OE-417

The DOE OE-417 annual summaries are electric emergency incident and disturbance
reports found on the Department of Energy website. They are mandatory emergency
forms filed by electric power industry actors which alert the DOE to respond to
energy emergencies. There is data from 2000 to 2023, and the 2023 data contains
348 records and 10 unique properties (date, time of start and restoration,
affected area, alert criteria, event type, demand loss, number of customers
affected). The challenge with this data is that it does not provide granular
geographic information beyond the affected county, and sometimes the affected
state (without county-level information). Therefore we plan to aggregate the
outage data by state. This helps standardize our sources in a way that results
in minimal loss of datapoints. We would also need to adjust for state population
when looking at number of homes affected.  Another challenge is finding data
from 2024.


### Data Source: U.S. Energy Information Administration - Energy usage/production by state

- Archival data comes from bulk data on each state’s energy production, including
total energy produced by renewables (2000-2022). Recent data (2023-24) will be scraped
from the state webpages (also from EIA)
- A challenge will be keeping the units (MWh & Btu) consistent, and combining the
scraped data with the archival data
- Will need to remind ourselves to check conversions and implement them correctly
in the code
- Rows: 50 (one for each state)
- Columns: 22 (one for each year)
- We’ll be pulling the total renewable production (Btu) and the overall renewable
production (Btu) in order to get the change in the share of renewables over time,
per state.


### Note 
These two datasets can be connected by year and location (state), resulting in
some potentially interesting insights about each state’s energy profile and its
responsiveness to outages over time.


### Additional Data Source: FEMA National Risk Index Map

- The National Risk Index is a dataset and online tool to help illustrate the United
States communities most at risk for 18 natural hazards. It was designed and built
by FEMA in close collaboration with various stakeholders and partners in academia;
local, state and federal government; and private industry. 
- This data has approx. 200 columns, and 3231 rows. 
- We could use this dataset in the final visualization, aggregating the county
overall risk data by state, and showing each state’s current risk for natural hazards,
using a thresholded heat map to connect it to the other two data sources.
- This is a very large dataset, so extracting the relevant information will be important.
- This would be an additional element to the final product that we may or may not
have time for. 


## Project Plan

- Convert (2000)-2022 archival renewables data to cleaned csv (Ganon, by Milestone #3)
- Clean 2000-2023 outage data, convert to csv/json (Ethan, Callie by Milestone #3)
- Find 2024 outage data (Jinny, by Milestone #3)
- Write code to generate individual state’s trend lines - graph (Ethan, Jinny, begun by Milestone #3)
- Build EIA scraper to get complete dataset for renewables (2024 outage data scraper/API
may be needed too) i.e. last 1-2 years. Make sure units (MWh or Btu) are consistent when
calculating percent total energy production (Ganon, Callie). 
- Final element: Interactive map of U.S. including individual state trend lines 
    Optional: overlay FEMA map
    Optional: include overall U.S. trend lines on side.
    Optional: deeper statistical analysis, additional variables like controlling
    for weather events
    Optional: setup automatic update system as new data is released


## Questions

1) How have projects in the past narrowed their scope? We have a lot of potential
datasets to explore, but we’re also reminding ourselves about the time and size
limitations of this project.

2) Regarding the API/web scraping requirement, how much web-scraping constitutes
“web-scraping” to satisfy the requirements of this project? On the continuum
from using web-scraping to download a file from a webpage to retrieving granular
text information from a multilayer webpage,  what level of intensity do you
envision students engaging in to fulfill a qualifying act of web-scraping for
the scope of this project?