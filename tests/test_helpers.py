import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import _invert_dictionary


###################### TESTS FOR _invert_dictionary ######################
# Testcase: test that output is correct with one inner key
@pytest.mark.parametrize(
    'input_dict, output_dict',
    [
        (
            {
                'Test1': {'en': False},
                'Test2': {'en': False}
            },
            {'en': {'Test1': False, 'Test2': False}}
        ),
        (
            {
                'Test1': {'en': True},
                'Test2': {'en': False}
            },
            {'en': {'Test1': True, 'Test2': False}}
        ),
        (
            {'Outer': {'Inner': True}},
            {'Inner': {'Outer': True}}
        ),
    ],
)
def test__invert_dictionary_one_inner_key(input_dict, output_dict):
    # Arrange
    # Act
    results = _invert_dictionary(input_dict)
    # Assert
    assert set(results) == set(output_dict)


# Testcase: test that output is correct with multiple inner keys
@pytest.mark.parametrize(
    'input_dict, output_dict',
    [
        (
            {
                'Test1': {'en': False, 'no':True},
                'Test2': {'en': False, 'no':False}
            },
            {
                'en': {'Test1': False, 'Test2': False},
                'no': {'Test1': True, 'Test2': False}
            }
        ),
        (
            {
                'Outer1': {'Inner1': False, 'Inner2':True, 'Inner3':False},
                'Outer2': {'Inner1': False, 'Inner2':False, 'Inner3':True}
            },
            {
                'Inner1': {'Outer1': False, 'Outer2': False},
                'Inner2': {'Outer1': True, 'Outer2': False},
                'Inner3': {'Outer1': False, 'Outer2': True}
            }
        ),
    ],
)
def test__invert_dictionary_multiple_inner_keys(input_dict, output_dict):
    # Arrange
    # Act
    results = _invert_dictionary(input_dict)
    # Assert
    assert set(results) == set(output_dict)



