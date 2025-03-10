from script.recon import build_re_dict, build_outage_dict, build_storms_dict
from pathlib import Path
import pandas as pd

def test_build_re_dict():
    actual_path = Path("script/data/renewables/prod_btu_re_te.xlsx")
    assert actual_path.exists(), "Your actual file path to renewables does not exist - please check your folder"
    test_path = "tests/test_files/test_renewables_excel.xlsx"
    renewables_excel = pd.ExcelFile(test_path)
    assert "Other renewables" in renewables_excel.sheet_names, "Check your file's tabs"
    renewables_sheet = pd.read_excel(renewables_excel, "Other renewables", header=2)
    assert "State" in list(renewables_sheet.columns), "Make sure your headers are parsed correctly"
    basic_dict = build_re_dict(test_path, 2017)
    assert len(basic_dict) == 52, "Expected 50 states, Puerto Rico, and DC"
    assert basic_dict["MO"] == round((22/169)*100, 2), "Incorrect renewable calculation"

def test_build_outage_dict():
    actual_path = Path("script/data/outages/2016_Annual_Summary.xls")
    assert actual_path.exists(), "Your actual path to outages does not exist - please check your folder"
    test_dict = build_outage_dict(actual_path, 2016)
    assert len(test_dict) == 42, "Your function is off from the 42 states in the present data"
    assert "Alaska" not in test_dict, "Your function contains a state that shouldn't be there, check your data"
    assert test_dict["Pennsylvania"] == 0.0, "Check your data values"
    assert test_dict["Nevada"] == round((111671/2919555)*100, 2), "Your calculation is wrong, check again"


def test_build_storms_dict():
    test_path = Path("script/data/storms/storms_2020.csv")
    assert test_path.exists(), "Your file path to storm data does not exist, please check your folder"
    test_storms = build_storms_dict(test_path, 2020)
    assert len(test_storms) == 50, "Check that you have all 50 states"
    assert "Hawaii" in test_storms, "Check that your data has all states"
    assert test_storms["Pennsylvania"] == round((13158200/12996143), 2), "Your calculation is wrong, check again"



