# Team Name: Flavortown

## Members

- Ethan Evans ethane@uchicago.edu
- Ganon Evans ganon@uchicago.edu
- Jinny Kim ekim1208@uchicago.edu
- Callie Leone clleone@uchicago.edu


## Abstract

100-200 words explaining the general idea for your project.  Be sure to read the project requirements and consider how you'll incorporate the various components.  These details can change as much as needed over the next few weeks, but we want to take a look at what's being considered.


Our group will explore the trends in power outages and electricity generation sources across U.S. states from 2000 to 2023. One of the questions we are interested in is whether states that are increasingly integrating weather-dependent renewable energy (solar, wind) into their grids are experiencing more or fewer power outages linked to severe weather events. 

To visualize the results, we will create an interactive map (e.g., heat map) that visualizes the changes in power outages and shifts in electricity generation sources over time. We also want to integrate a visual aid similar to the New York Times’ 2024 election reporting that shows arrows over various parts of the country and whether they’ve become more or less dependent on renewables. These tools will allow users to easily examine regional differences in renewable energy adoption and grid reliability in the U.S. 


## Preliminary Data Sources

### Data Source #1: Power Outage Data (two sources)

- 2014-2022 Outages: https://www.nature.com/articles/s41597-024-03095-5
	- Direct link to 2014-2022 dataset: https://figshare.com/articles/dataset/The_Environment_for_Analysis_of_Geo-Located_Energy_Information_s_Recorded_Electricity_Outages_2014-2022/24237376

- 2000-2023 Outages: https://doe417.pnnl.gov/

- The 2014-2022 data set is bulk data.
- We may need to do some thorough analysis to confirm that the metrics between the 2014-2022 dataset and pre-2014 data are comparable and, if not, adjusted accordingly.

### Data Source #2: EIA Energy Source Data

- All Energy (Mapped): https://atlas.eia.gov/apps/all-energy-infrastructure-and-resources/explore

- Renewable Energy and Resources Dashboard: https://eia.maps.arcgis.com/apps/dashboards/77cde239acfb494b81a00e927574e430

- The data is on a series of webpages, but there’s likely bulk data available for download somewhere on the website.
- The most visible data we’ve found so far seems to be edited maps or tables of other EIA datasets. There hasn’t been one, clear-cut, downloadable CSV or other file with all of the information available on the maps. Some scrapping may be needed to get all of the information in one place like on the maps. 

### Data Source #3: {Name} FEMA - Alternate disaster measure?

- FEMA Risk Map: https://hazards.fema.gov/nri/map

- The bulk data can be downloaded from FEMA’s page.
- Of the three data sources listed, this is the one that would be more of an exploratory addendum than a core part of our project. We need to brainstorm more and see how it could possibly play a larger role in the final version.


## Preliminary Project Plan

A short summary of what components of the project might be needed (e.g. data ingestion, cleaning/preparation, visualization). You might also begin to think about who will work on what. This can be very brief, and will almost certainly change by the next milestone.


The first step is to standardize our datasets  - either around states, counties, census tracts, or some other geographical unit. Then, once the data is downloaded, we’ll clean up the data such that everything is comparable with each other. For the EIA, we’ll likely have to scrape or combine different datasets in order to replicate what their website’s map is producing.

We need to do research of how to visualize the change in green energy over time as arrows - in particular, how to do this in a way that is graphically appealing to and has a manageable (though likely unavoidable) amount of clutter. We also need to think of a way to visually compare green energy development and grid failures, as both are multidimensional issues that we’ll need to find a way to quantify and then represent. 


## Questions

A **numbered** list of questions for us to respond to.

1) What information would you like us to include in project plans going forward? Like what level of specificity, what items should be included?

2) Most previous project examples are data visualizations, but are there other common project formats we should be aware of/consider?


