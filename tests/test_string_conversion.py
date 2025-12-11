import pytest

from src.helpers import format_logic_rules


############### Testcases: Basic logic rule tests without country searches and pre-search ###############
# Reason for testing without country and presearch
# This function is used by the presearch and the country search (not only sdg search), and for these cases it is of course not 
# required to include country search and presearch results when calling the function.
@pytest.mark.format_logic_rules
@pytest.mark.parametrize(
    'input, output_text', 
    [
        (
            "([termlist1_ba] | [termlist1_ba_trunc]) & [termlist1_bb] | ([termlist1_bc] & ([termlist1_bd] | [termlist1_bd_trunc]))", 
            "(True or True) and True or (True and (True or True))"
         ),
    ]
)
def test_format_logic_rules_all_true(input, output_text):
    # Arrange
    dict = {
        "termlist1_ba": True,
        "termlist1_ba_trunc": True,
        "termlist1_bb": True,
        "termlist1_bc": True,
        "termlist1_bd": True,
        "termlist1_bd_trunc": True,
    }
    # Act
    result = format_logic_rules(input, dict)
    # Assert
    assert result == output_text

@pytest.mark.format_logic_rules
@pytest.mark.parametrize(
    'input, output_text', 
    [
        (
            "([termlist1_ba] | [termlist1_ba_trunc]) & [termlist1_bb] | ([termlist1_bc] & ([termlist1_bd] | [termlist1_bd_trunc]))", 
            "(False or False) and False or (False and (False or False))"
         ),
    ]
)
def test_format_logic_rules_all_false(input, output_text):
    # Arrange
    dict = {
        "termlist1_ba": False,
        "termlist1_ba_trunc": False,
        "termlist1_bb": False,
        "termlist1_bc": False,
        "termlist1_bd": False,
        "termlist1_bd_trunc": False,
    }
    # Act
    result = format_logic_rules(input, dict)
    # Assert
    assert result == output_text


@pytest.mark.format_logic_rules
@pytest.mark.parametrize(
    'input, output_text', 
    [
        (
            "([termlist1_ba] | [termlist1_ba_trunc]) & [termlist1_bb] | ([termlist1_bc] & ([termlist1_bd] | [termlist1_bd_trunc]))", 
            "(True or False) and True or (True and (False or True))"
         ),
    ]
)
def test_format_logic_rules_combined_true_false(input, output_text):
    # Arrange
    dict = {
        "termlist1_ba": True,
        "termlist1_ba_trunc": False,
        "termlist1_bb": True,
        "termlist1_bc": True,
        "termlist1_bd": False,
        "termlist1_bd_trunc": True,
    }
    # Act
    result = format_logic_rules(input, dict)
    # Assert
    assert result == output_text
#####################################################################################################################



##################################### Testcase: include country search #####################################
@pytest.mark.format_logic_rules
@pytest.mark.parametrize(
    'input_logic_rule, output_text', 
    [
        (
            "([termlist1_ba] | [termlist1_ba_trunc]) & [termlist1_bb] | ([termlist1_bc] & ([termlist1_bd] | [termlist1_bd_trunc]))", 
            "(True or True) and True or (True and (True or True))"
         ),
    ]
)
def test_format_logic_rules_countries(input_logic_rule, output_text):
    # Arrange
    termlist_results = {
        "termlist1_ba": True,
        "termlist1_ba_trunc": True,
        "termlist1_bb": True,
        "termlist1_bc": True,
        "termlist1_bd": True,
        "termlist1_bd_trunc": True,
    }
    country_results = {
        "LDC": True,
        "SIDS": False,
        "LDS": False,
        "LMIC": False,
    }

    # Act
    result = format_logic_rules(
        logic_rule_raw=input_logic_rule, 
        result_termlist_search=termlist_results,
        countries=country_results
    )

    # Assert
    assert result == output_text


##################################### TODO Testcase: include pre-search #####################################


################################## TODO Testcase: include both country- and pre-search ##################################


################################## TODO Testcase: missing a referenced termlist result ##################################


################################## TODO Testcase: missing a referenced countries result ##################################


################################## TODO Testcase: missing a referenced pre-search result ##################################


