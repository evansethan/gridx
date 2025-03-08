from script import recon # import error here... not sure why
import pandas as pd

def test_build_re_dict():
    actual_path = "data/renewables/prod_btu_re_te.xlsx"
    assert actual_path.exists(), "Your actual file path to renewables does not exist - please check your folder"
    test_path = "tests/test_files/test_renewables_excel.xlsx"
    renewables_excel = pd.ExcelFile(test_path)
    assert "Total renewables" in renewables_excel, "Check your file's tabs"
    renewables_sheet = pd.read_excel(renewables_excel, "Total renewables", header=2)
    assert "State" in list(renewables_sheet.columns), "Make sure your headers are parsed correctly"
    basic_dict = recon.build_re_dict(test_path, 2017)
    assert len(basic_dict) == 7, "Expected seven years in the dictionary"
    assert basic_dict[2016]["MO"] == (100/148), "Incorrect renewable calculation"
    for year in basic_dict:
        assert "MS" not in year, "Your file contains the extra non-states from total energy production"

def test_build_outage_dict():
    actual_path = "data/outages/2016_Annual_Summary.xls"
    assert actual_path.exists(), "Your actual path to outages does not exist - please check your folder"
    test_dict = recon.build_outage_dict(actual_path, 2016)
    assert len(test_dict) == 40, "Your function is off from the 40 states in the present data"
    assert "Alaska" not in test_dict, "Your function contains a state that shouldn't be there, check your data"
    assert test_dict["Missouri"] == 0.0, "Check your data values"
    assert test_dict["Nevada"] == round((111671/2919555)*100, 2), "Your calculation is wrong, check again"


def test_build_storms_dict():
    test_path = "data/storms/storms_2020.csv"
    assert test_path.exists(), "Your file path to storm data does not exist, please check your folder"
    test_storms = recon.build_storm_dict(test_path, 2020)
    assert len(test_storms) == 50, "Check that you have all 50 states"
    assert "Hawaii" in test_storms, "Check that your data has all states"
    assert test_storms["Pennsylvania"] == round((13158200/12996143)*100, 2), "Your calculation is wrong, check again"



