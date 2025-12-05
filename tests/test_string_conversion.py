import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import format_logic_rules

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
