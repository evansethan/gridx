from script import clean

#the functions we're testing could be abstracted further to make testing easier


def test_clean_outages():
    test_path = "data/outages/2016_Annual_Summary.xls"
    assert test_path.exists(), "Your file path to clean outages does not exist - please check your folder"
    output = clean.clean_outages(test_path)
    assert "LUMA Energy" not in output #need to test by row?
    assert "Pacific Gas" not in output





    

    
