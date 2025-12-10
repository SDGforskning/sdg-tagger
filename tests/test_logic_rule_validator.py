"""
Test the logic rule validator code, which is used to validate the format of the logic rules in the json files.
"""
import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_helpers.logic_rule_validation import validate_boolean_expression


@pytest.mark.logic_rule_validation
@pytest.mark.parametrize(
    'input_valid', 
    [
        "( [a] & [b] )",
        "( not [foo] | ( [bar_1] & not ( [baz] | [b2] ) ) )",
        "( ( [termlist1_ba] | [termlist1_ba_trunc] ) & [termlist1_bb] | ( [termlist1_bc] & ( [termlist1_bd] | [termlist1_bd_trunc] ) ) )",
        "( ( [x] ) )",  # ekstra whitespace/paranteser er ok
        "( not not [x] )",  # dobbel 'not' med mellomrom
        "()"
    ]
)
def test_logic_rule_validator_valid(input_valid):
    # Arrange    
    # Act
    result = validate_boolean_expression(input_valid)
    # Assert
    assert result


@pytest.mark.logic_rule_validation
@pytest.mark.parametrize(
    'input_invalid', 
    [
        "([a]&[b])",           # mangler mellomrom rundt &
        "(not [x])",           # mangler mellomrom før 'not'
        "([a] |[b])",          # mangler mellomrom før [b]
        "([a]| [b])",          # mangler mellomrom etter |
        "([A])",               # store bokstaver i []
        "([foo bar])",         # whitespace inne i []
        "([x] && [y])",        # '&&' ikke tillatt
        "([x] | [y]",          # mangler ytre ')'
        "( [x] & )",           # operator uten høyre operand
        "( & [x] )",           # operator uten venstre operand
        "( [x]|[y] )",         # mangler mellomrom rundt |
        "( not[x] )",          # ikke lov med 'not' uten mellomrom etter
    ]
)
def test_logic_rule_validator_invalid(input_invalid):
    # Arrange    
    # Act
    result = validate_boolean_expression(input_invalid)
    # Assert
    assert not result
