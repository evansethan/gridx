from script import recon # import error here... not sure why

def test_build_re_dict():
    test_path = "data/renewables/prod_btu_re_te.xlsx"
    assert test_path.exists(), "Your file path to renewables does not exist - please check your folder"
    # basic_dict = recon.build_re_dict(test_path, 2017)
    # #assert len(basic_dict) == 8, "Expected seven years in the dictionary"
    # assert basic_dict["AK"] == 0.009181129924485621, "Incorrect renewable calculation"
    
# edited this one a bit ^^^ rest still need updating




def test_build_outage_dict():
    test_path = "data/outages/2016_Annual_Summary.xls"
    test_dict = cleaning.build_outage_dict(test_path)
    assert len(test_dict) == 50, "Your function does not have all 50 states"
    assert test_dict["Missouri"] == "insert here", "Check your data values"


def test_build_outage_dict_populations():
    """ Tests to ensure the correct population data is used for outages"""
    # TODO
    pass


def test_build_storms_dict():
    test_path = "data/storms/storms_2020.csv"
    assert test_path.exists(), "Your file path to storm data does not exist, please check your folder"


def test_build_storms_dict_populations():
    """ Tests to ensure the correct population data is used for storms"""
    # TODO
    pass

