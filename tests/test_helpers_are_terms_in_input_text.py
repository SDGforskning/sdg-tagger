import pytest
import sys
import os
import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import _are_terms_in_input_text

termlists = [
    {
        'termlist_name': 'Test1',
        'wordlist_en': ['ONE', 'Two'],
        'formatting_rule': 'DEFAULT',
        'case': True,
    },
    {
        'termlist_name': 'Test2',
        'wordlist_en': ['Three', 'FOUR'],
        'formatting_rule': 'DEFAULT',
        'case': False,
    },
]
input_text = 'Text with UPPERCASE'


# Testcase: test that output is correct
@mock.patch('src.helpers.prepare_regex_search_termlist')
@mock.patch('src.helpers._pattern_search_boolean')
def test_are_terms_in_input_text(
    mocker_pattern_search_boolean, mocker_prepare_regex_search_termlist
):
    # Arrange
    mocker_prepare_regex_search_termlist.side_effect = [
        ('(?:ONE|Two)', 'Text with UPPERCASE'),
        ('(?:three|four)', 'text with uppercase'),
    ]
    mocker_pattern_search_boolean.side_effect = [False, False]

    output_excpected = {'Test1': False, 'Test2': False}

    # Act
    output = _are_terms_in_input_text(termlists, input_text)

    # Assert
    assert output == output_excpected


# Testcase: test that it calls _pattern_search_boolean with correct values
@mock.patch('src.helpers.prepare_regex_search_termlist')
@mock.patch('src.helpers._pattern_search_boolean')
def test_are_terms_in_input_text_calls_pattern_search_boolean(
    mocker_pattern_search_boolean, mocker_prepare_regex_search_termlist
):
    # Arrange
    mocker_prepare_regex_search_termlist.side_effect = [
        ('(?:ONE|Two)', 'Text with UPPERCASE'),
        ('(?:three|four)', 'text with uppercase'),
    ]
    mocker_pattern_search_boolean.side_effect = [False, False]

    expected_calls_pattern_search_boolean = [
        mock.call('(?:ONE|Two)', 'Text with UPPERCASE'),
        mock.call('(?:three|four)', 'text with uppercase'),
    ]

    # Act
    _are_terms_in_input_text(termlists, input_text)

    # Assert
    mocker_pattern_search_boolean.assert_has_calls(
        expected_calls_pattern_search_boolean
    )
    assert mocker_pattern_search_boolean.call_count == 2


# Testcase: test that it calls prepare_regex_search_termlist with correct values
@mock.patch('src.helpers.prepare_regex_search_termlist')
@mock.patch('src.helpers._pattern_search_boolean')
def test_are_terms_in_input_text_calls_prepare_regex_search_termlist(
    mocker_pattern_search_boolean, mocker_prepare_regex_search_termlist
):
    mocker_prepare_regex_search_termlist.side_effect = [
        ('(?:ONE|Two)', 'Text with UPPERCASE'),
        ('(?:three|four)', 'text with uppercase'),
    ]
    mocker_pattern_search_boolean.side_effect = [False, False]

    expected_calls_prepare_regex_search_termlist = [
        mock.call(termlists[0], 'Text with UPPERCASE'),
        mock.call(termlists[1], 'Text with UPPERCASE'),
    ]

    # Act
    _are_terms_in_input_text(termlists, input_text)

    # Assert
    mocker_prepare_regex_search_termlist.assert_has_calls(
        expected_calls_prepare_regex_search_termlist
    )
    assert mocker_prepare_regex_search_termlist.call_count == 2
