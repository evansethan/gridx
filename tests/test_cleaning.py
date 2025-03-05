from script.scratch import cleaning, visualization #check this
import pytest

def test_get_renewable_production():
    basic_dict = visualization.get_renewable_production() #what to do if just one year entered?
    assert len(basic_dict) == 7, "Expected seven years in the dictionary"
    assert basic_dict[2017]["AK"] == 0.009181129924485621, "Incorrect renewable calculation"
    with pytest.raises(KeyError):
        bad_year_one = visualization.get_renewable_production(2015, 2022)
        bad_year_two = visualization.get_renewable_production(2016, 2024)
        bad_year_three = visualization.get_renewable_production(2022, 2016)
    
def test_clean_outages():
    path = "placeholder"
    output = cleaning.clean_outages(path)
    assert "LUMA Energy" not in output #need to test by row?
    assert "Pacific Gas" not in output
    
