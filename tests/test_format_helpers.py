import pytest
import sys
import os
import mock
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.format_helpers import (
    _check_for_missing_matches,
    _format_list_with_pattern,
    _get_language_termlists,
    format_logic_rules,
    prepare_regex_search_termlist,
)


################## TESTS FOR _check_for_missing_matches ##################
# Testcase: missing keys
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_dict',
    [
        {
            'Terms1': False,
            'Terms2': False,
            'Terms4': False,
        },
        {
            'Terms1': False,
        },
        {},
    ],
)
def test_check_for_missing_matches_missing_key(input_dict):
    # Arrange
    pattern = r'\[[^\[\]]*\]'
    logic_rule_raw = '([Terms1] and ([Terms2] or [Terms3]))'
    # Act
    with pytest.raises(KeyError, match='Terms3'):
        _check_for_missing_matches(pattern, logic_rule_raw, input_dict)


# Testcase: no missing keys
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_dict',
    [
        {
            'Terms1': False,
            'Terms2': False,
            'Terms3': False,
        },
        {
            'Terms1': False,
            'Terms2': False,
            'Terms3': False,
            'Terms4': False,
            'Terms5': False,
        },
    ],
)
def test_check_for_missing_matches_no_missing_keys(input_dict):
    # Arrange
    pattern = r'\[[^\[\]]*\]'
    logic_rule_raw = '([Terms1] and ([Terms2] or [Terms3]))'
    # Act
    result = _check_for_missing_matches(pattern, logic_rule_raw, input_dict)
    # Assert
    assert result is None


################### TESTS FOR _format_list_with_pattern ###################
trunc = '(?:{})'
no_right_trunc = '(?:{})\\b'
no_trunc = '\\b(?:{})\\b'
no_left_trunc = '\\b(?:{})'


# Testcase: trunc format
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '(?:one)'),
        (['one', 'two', 'three'], '(?:one|two|three)'),
        (['one two', 'three'], '(?:one two|three)'),
        ([], '(?:)'),
    ],
)
def test_format_list_with_pattern_trunc(input_terms, output_text):
    # Arrange
    pattern = trunc
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result == output_text


# Testcase: no_right_trunc format
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '(?:one)\\b'),
        (['one', 'two', 'three'], '(?:one|two|three)\\b'),
        (['one two', 'three'], '(?:one two|three)\\b'),
        ([], '(?:)\\b'),
    ],
)
def test_format_list_with_pattern_no_right_trunc(input_terms, output_text):
    # Arrange
    pattern = no_right_trunc
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result == output_text


# Testcase: no_trunc format
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '\\b(?:one)\\b'),
        (['one', 'two', 'three'], '\\b(?:one|two|three)\\b'),
        (['one two', 'three'], '\\b(?:one two|three)\\b'),
        ([], '\\b(?:)\\b'),
    ],
)
def test_format_list_with_pattern_no_trunc(input_terms, output_text):
    # Arrange
    pattern = no_trunc
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result == output_text


# Testcase: no_left_trunc format
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '\\b(?:one)'),
        (['one', 'two', 'three'], '\\b(?:one|two|three)'),
        (['one two', 'three'], '\\b(?:one two|three)'),
        ([], '\\b(?:)'),
    ],
)
def test_format_list_with_pattern_no_left_trunc(input_terms, output_text):
    # Arrange
    pattern = no_left_trunc
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result == output_text


################ TESTS FOR _get_language_termlists ################
# Testcase: get 1/1 language
@pytest.mark.parametrize(
    'input_terms, output_dict',
    [
        (
            {
                'termlist_name': 'Test1',
                'wordlist_no': ['tre', 'fire'],
            },
            {
                'no': ['tre', 'fire']
            },
        ),
    ],
)
def test__get_language_termlists_one_of_one_languages(input_terms, output_dict):
    # Arrange
    # Act
    with mock.patch('src.format_helpers.LANGUAGES', {'no': True}):
        results = _get_language_termlists(input_terms)
    # Assert
    assert set(results) == set(output_dict)


# Testcase: get 2/2 languages
@pytest.mark.parametrize(
    'input_terms, output_dict',
    [
        (
            {
                'termlist_name': 'Test1',
                'wordlist_no': ['tre', 'fire'],
            },
            {
                'no': ['tre', 'fire']
            },
        ),
    ],
)
def test__get_language_termlists_two_of_two_languages(input_terms, output_dict):
    # Arrange
    # Act
    with mock.patch('src.format_helpers.LANGUAGES', {'no': True}):
        results = _get_language_termlists(input_terms)
    # Assert
    assert set(results) == set(output_dict)


# Testcase: get 1/2 languages - e.g. two languages exists but only one is set to true in the constant. 
@pytest.mark.parametrize(
    'input_terms, output_dict',
    [
        (
            {
                'termlist_name': 'Test1',
                'wordlist_en': ['one', 'two'],
                'wordlist_no': ['tre', 'fire'],
            },
            {
                'en': ['one', 'two']
            },
        ),
    ],
)
def test__get_language_termlists_one_of_two_languages(input_terms, output_dict):
    # Arrange
    # Act
    with mock.patch('src.format_helpers.LANGUAGES', {'en':True, 'no': False}):
        results = _get_language_termlists(input_terms)
    # Assert
    assert set(results) == set(output_dict)


#test get 2 languages where one language is not there
# Testcase: get 1/1 language
@pytest.mark.parametrize(
    'input_terms, output_dict',
    [
        (
            {
                'termlist_name': 'Test1',
                'wordlist_no': ['tre', 'fire'],
            },
            {
                'no': ['tre', 'fire']
            },
        ),
    ],
)
def test__get_language_termlists_missing_language_terms(input_terms, output_dict):
    # Arrange
    # Act
    with mock.patch('src.format_helpers.LANGUAGES', {'en':True, 'no': True}):
        results = _get_language_termlists(input_terms)
    # Assert
    assert set(results) == set(output_dict)


###################### TESTS FOR format_logic_rules ######################
# Testcase: format correct, no countries or pre_search
@pytest.mark.parametrize(
    'input_logic_rule, input_termlist_results, output_expected',
    [
        (
            '([Termlist1])',
            {'Termlist1': True},
            '(True)',
        ),
        (
            '([Termlist1])',
            {'Termlist1': True},
            '(True)',
        ),
    ],
)
def test_format_logic_rules(
    mocker, input_logic_rule, input_termlist_results, output_expected
):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    # Act
    result = format_logic_rules(input_logic_rule, input_termlist_results)
    # Assert
    assert result == output_expected


# Testcase: format correct, with countries
@pytest.mark.parametrize(
    'input_logic_rule, output_expected',
    [
        (
            '([Termlist1] and [Countries1])',
            '(True and True)',
        ),
        (
            '([Termlist1] or [Countries2])',
            '(True or False)',
        ),
    ],
)
def test_format_logic_rules_with_countries(mocker, input_logic_rule, output_expected):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1': True, 'Termlist2': False}
    countries = {'Countries1': True, 'Countries2': False}
    # Act
    result = format_logic_rules(
        input_logic_rule, termlists, countries_results=countries
    )
    # Assert
    assert result == output_expected


# Testcase: format correct, with pre_search
@pytest.mark.parametrize(
    'input_logic_rule, output_expected',
    [
        (
            '([Termlist1] and [Pre1])',
            '(True and True)',
        ),
        (
            '([Termlist1] or [Pre2])',
            '(True or False)',
        ),
    ],
)
def test_format_logic_rules_with_presearch(mocker, input_logic_rule, output_expected):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1': True, 'Termlist2': False}
    pre_search = {'Pre1': True, 'Pre2': False}
    # Act
    result = format_logic_rules(
        input_logic_rule, termlists, pre_search_results=pre_search
    )
    # Assert
    assert result == output_expected


# Testcase: format correct, with countries or pre_search
@pytest.mark.parametrize(
    'input_logic_rule, output_expected',
    [
        (
            '(([Termlist1] and [Countries2]) or ([Termlist1] and not [Pre1]))',
            '((True and False) or (True and not True))',
        ),
        (
            '(([Termlist1]) or ([Countries2] and [Pre1]))',
            '((True) or (False and True))',
        ),
        (
            '([Termlist1] and [Countries2] and not [Pre2])',
            '(True and False and not False)',
        ),
        (
            '(([Termlist2] and [Countries2]) or ([Termlist1] and not [Pre2]))',
            '((False and False) or (True and not False))',
        ),
    ],
)
def test_format_logic_rules_with_countries_and_presearch(
    mocker, input_logic_rule, output_expected
):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1': True, 'Termlist2': False}
    countries = {'Countries1': True, 'Countries2': False}
    pre_search = {'Pre1': True, 'Pre2': False}
    # Act
    result = format_logic_rules(input_logic_rule, termlists, countries, pre_search)
    # Assert
    assert result == output_expected


# Testcase: test correct replacing of | and & and extra spaces
@pytest.mark.parametrize(
    'input_logic_rule, output_expected',
    [
        (
            '([Termlist1] & [Termlist2])',
            '(True and True)',
        ),
        (
            '([Termlist1]&[Termlist2])',
            '(True and True)',
        ),
        (
            '([Termlist1] | [Termlist2])',
            '(True or True)',
        ),
        (
            '([Termlist1]|[Termlist2])',
            '(True or True)',
        ),
    ],
)
def test_format_logic_rules_correct_replacing_logic(
    mocker, input_logic_rule, output_expected
):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1': True, 'Termlist2': True}
    # Act
    result = format_logic_rules(input_logic_rule, termlists)
    # Assert
    assert result == output_expected


################ TESTS FOR prepare_regex_search_termlist ################
# Testcase: test that it correctly calls _format_list_with_pattern with correct inputs
@patch('src.format_helpers._format_list_with_pattern')
def test_prepare_regex_search_termlist_calls_format(
    mocker_format_list_with_pattern
):
    # Arrange
    termlist = ['one', 'two']
    formatting_rule = 'trunc'
    case = False

    # Act
    with mock.patch('src.format_helpers.REGEX_PATTERNS', {'trunc': '(?:{})'}):
        prepare_regex_search_termlist(termlist, 'text', formatting_rule, case)
    # Assert
    mocker_format_list_with_pattern.assert_called_once_with('(?:{})', ['one', 'two'])


# Testcase: Lowering the words in the list if case=False
@patch('src.format_helpers._format_list_with_pattern')
def test_prepare_regex_search_termlist_lowercase_list(
    mocker_format_list_with_pattern
):
    # Arrange
    termlist = ['ONE', 'Two']
    formatting_rule = 'trunc'
    case = False

    # Act
    with mock.patch('src.format_helpers.REGEX_PATTERNS', {'trunc': '(?:{})'}):
        prepare_regex_search_termlist(termlist, 'text', formatting_rule, case)
    # Assert
    mocker_format_list_with_pattern.assert_called_once_with('(?:{})', ['one', 'two'])


# Testcase: Lowering the words in the input text if case=False
@patch('src.format_helpers._format_list_with_pattern')
def test_prepare_regex_search_termlist_lowercase_text(
    mocker_format_list_with_pattern
):
    # Arrange
    termlist =['ONE', 'Two']
    formatting_rule = 'trunc'
    case = False

    input_text = 'Text with UPPERCASE'
    output_excpected = 'text with uppercase'
    # Act
    with mock.patch('src.format_helpers.REGEX_PATTERNS', {'trunc': '(?:{})'}):
        _, output_text = prepare_regex_search_termlist(termlist, input_text, formatting_rule, case)

    # Assert
    assert output_text == output_excpected


# Testcase: NOT Lowering the words in the list if case=True
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers.REGEX_PATTERNS', {'trunc': '(?:{})'})
def test_prepare_regex_search_termlist_do_not_lowercase_list(
    mocker_format_list_with_pattern
):
    # Arrange
    termlist = ['ONE', 'Two']
    formatting_rule = 'trunc'
    case = True
 
    # Act
    prepare_regex_search_termlist(termlist, 'text', formatting_rule, case)

    # Assert
    mocker_format_list_with_pattern.assert_called_once_with('(?:{})', ['ONE', 'Two'])


# Testcase: NOT Lowering the words in the input text if case=True
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers.REGEX_PATTERNS', {'trunc': '(?:{})'})
def test_prepare_regex_search_termlist_do_not_lowercase_text(
    mocker_format_list_with_pattern
):
    # Arrange
    termlist = ['ONE', 'Two']
    formatting_rule = 'trunc'
    case = True

    input_text = 'Text with UPPERCASE'
    output_excpected = 'Text with UPPERCASE'
    # Act
    _, output_text = prepare_regex_search_termlist(termlist, input_text, formatting_rule, case)
    # Assert
    assert output_text == output_excpected

