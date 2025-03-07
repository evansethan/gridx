from script import utils
# but may not need this one

def test_build_pop_dict():
    cleaning_path = "insert"
    census_one_path = Path(__file__).parent / "data/state_pops/2010-2020.csv"
    census_two_path = Path(__file__).parent / "data/state_pops/2020-2024.csv"
    assert census_one_path.exists(), "Check your census file paths"
    assert census_two_path.exists(), "Check your census file paths"
    test_list = cleaning.build_pop_dict(cleaning_path)
    assert len(test_list) == 7, "Error, check that you have all years and census files"