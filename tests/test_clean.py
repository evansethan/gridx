from gridx.clean import clean_outages
from pathlib import Path

def test_clean_outages_path():
    test_path = Path("data/outages/2016_Annual_Summary.xls")
    assert test_path.exists(), "Your file path to clean outages does not exist - please check your folder"


def test_clean_outages_output():
    test_path = Path("data/outages/2016_Annual_Summary.xls")
    output = clean_outages(test_path)
    assert "LUMA Energy" not in output, "Your data has an unconverted name"
    assert "Pacific Gas" not in output, "Your data has an unconverted name"





    

    
