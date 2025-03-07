from script.scratch import cleaning, visualization #check this
import pytest
from pathlib import Path

#need to add a command to read_me to run the tests
#create dummy data for tests

def test_get_renewable_production():
    test_path = "data/Renewables/prod_btu_re_te.xlsx"
    assert test_path.exists(), "Your file path to renewables does not exist - please check your folder"
    basic_dict = visualization.get_renewable_production()
    assert len(basic_dict) == 8, "Expected seven years in the dictionary"
    assert basic_dict[2017]["AK"] == 0.009181129924485621, "Incorrect renewable calculation"
    
def test_clean_outages():
    test_path = "data/outages/2016_Annual_Summary.xls"
    assert test_path.exists(), "Your file path to clean outages does not exist - please check your folder"
    output = cleaning.clean_outages(test_path)
    assert "LUMA Energy" not in output #need to test by row?
    assert "Pacific Gas" not in output

def test_build_outage_dict():
    test_path = "data/outages/2016_Annual_Summary.xls"
    test_dict = cleaning.build_outage_dict(test_path)
    assert len(test_dict) == 50, "Your function does not have all 50 states"
    assert test_dict["Missouri"] == "insert here", "Check your data values"

def test_build_storms_dict():
    test_path = "data/storms/storms_2020.csv"
    assert test_path.exists(), "Your file path to storm data does not exist, please check your folder"

def test_build_pop_dict():
    cleaning_path = "insert"
    census_one_path = Path(__file__).parent / "data/state_pops/2010-2020.csv"
    census_two_path = Path(__file__).parent / "data/state_pops/2020-2024.csv"
    assert census_one_path.exists(), "Check your census file paths"
    assert census_two_path.exists(), "Check your census file paths"
    test_list = cleaning.build_pop_dict(cleaning_path)
    assert len(test_list) == 7, "Error, check that you have all years and census files"
    

    
