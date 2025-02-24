Overview:

This project aims to examine power outages and its association with energy generation sources in the United States. By analyzing the frequency and severity of power outages, we aim to explore patterns in grid reliability and generation mix across different regions and time periods. 

Data Sources (in "data" folder)

NERC Regions (data/nerc_regions)
Link: https://atlas.eia.gov/datasets/eia::nerc-regions/explore
Energy Information Administration
Shapefiles representing the different areas of the North American Electric Reliability Corporation (NERC), which are largely power systems split across the US and Canada.

OE-417 (data/outages)
Link: https://doe417.pnnl.gov/instructions
Department of Energy
Outage data (duration, number of customers affected) by U.S. region (NERC region for our purposes)


EIA-860M (data/renewables)
Link: https://www.eia.gov/electricity/data/eia860m/v
Energy Information Administration
July Generator 2023 is a csv of monthly generator inventory collected in a monthly survey from power plants’ Form EIA-860M. The data is broken down into rows of each generator at a facility with its technology type and megawatt capacity. This data can be aggregated to represent the total capacity of a plant, which itself can be broken down into total capacity by technology. 

(Note: In the final project, we will have December Generator 2023 or other csvs for different years to get a better representation of capacity over time while accounting for changes in energy usage and technology.)


We also included data/FEMA, which has weather-related data and shapefiles per census tract. This data is less likely to be included in the final project.



Data Processing:

You can see the output of loading and cleaning of the OE-417 data with the commands

“uv sync”
"uv run python3 script/cleaning.py"

The output shows the number of customers affected by NERC region for 2017 and 2023, respectively.


Additionally, script/load_data.ipynb has several functions, ranging from an initial parse of the data to bucketing the data by energy types. 

Initial classes and data load - We define two classes: NERC and facility. The NERC class simply contains just the ID of a NERC region and its shapefile polygon. The facility object contains significantly more information, including the name and ID of the facility and its parent company, its capacity,  its location in latitude and longitude. Each facility is initially processed by generator, so its technology varies for each row it exists. The special ID is a combination of the ID of the plant and its parent company to unique identify the facility. Load_shapefiles and load_frs_csv are both functions that take the aforementioned NERC and EIA files then convert them into our NERC and facility objects.

There are several functions carried over from PA 5 dealing with the creation of Quadtrees and bounding boxes. 

There are three bucketing functions that return dictionaries mapping the special ID of a planet to its energy output. Get_plant_total provides the total capacity, get_fuel_total is capacity broken down by one of the provided energy sources ranging from oil to nuclear to wind, and get_energy_type_total takes the energy source buckets and aggregates them into three largescale buckets for green energy, fossil fuels, and nuclear power. 


Data Visualization:

“uv sync”
"uv run python3 script/visualization.py"

To run the full program, run the commands above. You should see a heat map of the United States come up. You can hover over each region to see the data in numeric form. Eventually we plan to add the ability to toggle between years, and show heatmaps for both outages and renewables usage.




