from script import utils
from pathlib import Path

def test_build_pop_dict():
    census_one_path = Path(__file__).parent / "data/state_pops/2010-2020.csv"
    census_two_path = Path(__file__).parent / "data/state_pops/2020-2024.csv"
    assert census_one_path.exists(), "Check your census file paths"
    assert census_two_path.exists(), "Check your census file paths"
    test_dict = utils.build_pop_dict()
    assert len(test_dict) == 7, "Error, check that you have the correct years and census files"
    assert "Iowa" in test_dict["2016"], "Check that you are parsing all states"
    assert "Virginia" in test_dict["2023"], "Check that you are parsing all states"
    assert test_dict["2020"]["Utah"] == 3284077, "Check that you are parsing the correct population column"
    assert test_dict["2017"]["Florida"] == 20977089, "Check that you are parsing the correct population column"