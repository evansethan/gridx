from shapely.geometry import Point, Polygon
from typing import NamedTuple
import pathlib
import shapefile
import pandas as pd
import csv
  
class State(NamedTuple):
    id: str
    polygon: Polygon

class Plant(NamedTuple):
    entityid: int
    plantid: int
    entityname: str
    plantname: str
    capacity: int
    latitude: float
    longitude: float
    tech: str


def load_shapefiles(path: pathlib.Path) -> State:
    """
    Extract and parse polygons from NERC shapefiles.
    """
    states = []
    with shapefile.Reader(path) as sf:
        for shape_rec in sf.shapeRecords():
            states.append(
                State(
                    id=shape_rec.record["STUSPS"],
                    polygon=Polygon(shape_rec.shape.points),
                )
            )
    return states

def load_plant_csv(path: pathlib.Path) -> list[Plant]:
    """
    Given a CSV containing plant data, return a list of Plant objects.
    """
    plants = []
    df = pd.read_excel(path, sheet_name="Operating", skiprows=2)
    df = df.reset_index() 
    for index, row in df.iterrows():
            plants.append(
                Plant(
                    entityid=row["Entity ID"],
                    entityname=row["Entity Name"],
                    plantid=row["Plant ID"],
                    plantname=row["Plant Name"],
                    capacity=row["Nameplate Capacity (MW)"],
                    latitude=row["Latitude"],
                    longitude=row["Longitude"],
                    tech=row["Technology"]
                )
            )
    return plants

# We will replace this with a recursive function
def spatial_join(plants: list, states: list) -> list[tuple[str, str]]:

    plant_state = []
    
    for plant in plants: 
        plant_point = Point(plant.longitude, plant.latitude)
        for id, poly in states:
            if poly.contains(plant_point):
                plant_state.append((plant.plantname, id))
                break
            else:
                continue
        
    return plant_state

def main():
    state_path = "data/state_regions/tl_2024_us_state"
    elec_path = "data/Renewables/july_generator2023.xlsx"
    
    states = load_shapefiles(state_path)
    plants = load_plant_csv(elec_path)

    print(len(spatial_join(plants, states)))
    print(spatial_join(plants, states))

    


if __name__ == "__main__":
    main()
