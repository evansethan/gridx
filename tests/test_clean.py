from script.clean import clean_outages
from pathlib import Path

#the functions we're testing could be abstracted further to make testing easier


def test_clean_outages():
    test_path = Path("script/data/outages/2016_Annual_Summary.xls")
    assert test_path.exists(), "Your file path to clean outages does not exist - please check your folder"
    output = clean_outages(test_path)
    assert "LUMA Energy" not in output, "Your data has an unconverted name"
    assert "Pacific Gas" not in output, "Your data has an unconverted name"





    

    
