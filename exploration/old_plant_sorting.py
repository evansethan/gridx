"""
These functions were written for a previous version of our project that focused more closely
on power plants themselves, but was eventually abandoned due to difficulty with the API. They 
would have co-existed with the shapely file work.
"""
from shapely.geometry import Point, Polygon
from typing import NamedTuple
import pathlib
import shapefile
import pandas as pd
import csv
from typing import NamedTuple
from shapely.geometry import Polygon, box, Point
from shapely.measurement import bounds
from shapely import intersects


def get_plant_total(facility_list):
    """
    Takes our list of Facility objects and creates a dictionary mapping a plant
    to its total capacity
    """
    total_dict = {}
    current_id = facility_list[0].specialid
    for generator in facility_list:
        if generator.specialid == current_id:
            if current_id in total_dict:
                total_dict[current_id] += generator.capacity
            else:
                total_dict[current_id] = generator.capacity
        else:
            current_id = generator.specialid
            if current_id in total_dict:
                total_dict[current_id] += generator.capacity
            else:
                total_dict[current_id] = generator.capacity
    return total_dict

def get_fuel_total(facility_list):
    """
    Takes our list of Facility objects and returns a dictionary of dictionaries
    mapping each plant's energy production to a value.
    """
    end_dict = {}
    current_id = facility_list[0].specialid
    for generator in facility_list:
        if generator.specialid == current_id:
            if generator not in end_dict:
                end_dict[current_id] = {generator.technology: generator.capacity}
            else:
                if generator.technology not in end_dict[current_id]:
                    end_dict[current_id][generator.technology] = generator.capacity
                else:
                    end_dict[current_id][generator.technology] += generator.capacity
        else:
            current_id = generator.specialid
            if generator not in end_dict:
                end_dict[current_id] = {generator.technology: generator.capacity}
            else:
                if generator.technology not in end_dict[current_id]:
                    end_dict[current_id][generator.technology] = generator.capacity
                else:
                    end_dict[current_id][generator.technology] += generator.capacity

    return end_dict

energy_categories = {"Petroleum Liquids": "Fossil Fuels",
"Onshore Wind Turbine": "Green Energy",
"Conventional Hydroelectric": "Green Energy",
"Natural Gas Steam Turbine": "Fossil Fuels",
"Conventional Steam Coal": "Fossil Fuels",
"Natural Gas Fired Combined Cycle": "Fossil Fuels",
"Natural Gas Fired Combustion Turbine": "Fossil Fuels",
"Nuclear": "Nuclear and Other",
"Hydroelectric Pumped Storage": "Green Energy",
"Natural Gas Internal Combustion Engine": "Fossil Fuels",
"Batteries": "Nuclear and Other", #filter out?
"Solar Photovoltaic": "Green Energy",
"Geothermal": "Green Energy",
"Wood/Wood Waste Biomass": "Nuclear and Other",
"Coal Integrated Gasification Combined Cycle": "Fossil Fuels",
"Other Gases": "Fossil Fuels",
"Petroleum Coke": "Fossil Fuels",
"Municipal Solid Waste": "Nuclear and Other", #wut
"Hydrokinetic": "Nuclear and Other",
"Landfill Gas": "Fossil Fuels",
"Natural Gas with Compressed Air Storage": "Fossil Fuels",
"All Other": "Nuclear and Other",
"Other Waste Biomass": "Nuclear and Other",
"Solar Thermal without Energy Storage": "Green Energy",
"Other Natural Gas": "Fossil Fuels",
"Solar Thermal with Energy Storage": "Green Energy",
"Flywheels": "Green Energy",
"Offshore Wind Turbine": "Green Energy",
} #need to list out every unique item in "technology" here and assign it to green, nuclear, or fossil fuels

def get_energy_type_total(tech_dict):
    """Takes a dictionary of dictionaries of each plant's specific technology and returns
    a dictionary of dictionaries for each plant of their energy production"""
    energy_dict = {}
    for plant in tech_dict:
        plant_dict = {}
        for tech, capacity in plant.items:
            energy_type = energy_categories[tech]
            if energy_type not in plant_dict:
                plant_dict[energy_type] = capacity
            else:
                plant_dict[energy_type] += capacity
        energy_dict[plant] = plant_dict #need to check if plant is still ID
    return energy_dict