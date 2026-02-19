import pytest
import sys
import os 
import mock
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.format_helpers import (
    _check_for_missing_matches,
    _format_list_with_pattern,
    _get_additional_language_terms,
    format_logic_rules,
    prepare_regex_search_termlist
)


################## TESTS FOR _check_for_missing_matches ##################

# Testcase: missing keys
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_dict',
    [
        {
            'Terms1':False,
            'Terms2':False,
            'Terms4':False,
        },
        {
            'Terms1':False,
        },
        {},
    ]
)
def test_check_for_missing_matches_missing_key(input_dict):
    # Arrange
    pattern = r'\[[^\[\]]*\]'
    logic_rule_raw = '([Terms1] and ([Terms2] or [Terms3]))'
    # Act
    with pytest.raises(KeyError):
        _check_for_missing_matches(pattern, logic_rule_raw, input_dict)
    

# Testcase: no missing keys
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_dict',
    [
        {
            'Terms1':False,
            'Terms2':False,
            'Terms3':False,
        },
        {
            'Terms1':False,
            'Terms2':False,
            'Terms3':False,
            'Terms4':False,
            'Terms5':False,
        },
    ]
)
def test_check_for_missing_matches_no_missing_keys(input_dict):
    # Arrange
    pattern = r'\[[^\[\]]*\]'
    logic_rule_raw = '([Terms1] and ([Terms2] or [Terms3]))'
    # Act
    result = _check_for_missing_matches(pattern, logic_rule_raw, input_dict)
    # Assert
    assert result is None

##########################################################################


################### TESTS FOR _format_list_with_pattern ###################
DEFAULT = '(?:{})'
SPECIFIC = '(?:{})\\b'
SPECIFIC_TRUNC = '\\b(?:{})\\b'
NO_LEFT_TRUNC = '\\b(?:{})'

# Testcase: DEFAULT format 
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '(?:one)'),
        (['one', 'two', 'three'], '(?:one|two|three)'),
        (['one two', 'three'], '(?:one two|three)'),
        ([], '(?:)'),
    ]
)
def test_format_list_with_pattern_default(input_terms, output_text):
    # Arrange
    pattern = DEFAULT
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result==output_text


# Testcase: SPECIFIC format
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '(?:one)\\b'),
        (['one', 'two', 'three'], '(?:one|two|three)\\b'),
        (['one two', 'three'], '(?:one two|three)\\b'),
        ([], '(?:)\\b'),
    ]
)
def test_format_list_with_pattern_specific(input_terms, output_text):
    # Arrange
    pattern = SPECIFIC
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result==output_text


# Testcase: SPECIFIC_TRUNC format 
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '\\b(?:one)\\b'),
        (['one', 'two', 'three'], '\\b(?:one|two|three)\\b'),
        (['one two', 'three'], '\\b(?:one two|three)\\b'),
        ([], '\\b(?:)\\b'),
    ]
)
def test_format_list_with_pattern_specific_trunc(input_terms, output_text):
    # Arrange
    pattern = SPECIFIC_TRUNC
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result==output_text


# Testcase: NO_LEFT_TRUNC format 
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (['one'], '\\b(?:one)'),
        (['one', 'two', 'three'], '\\b(?:one|two|three)'),
        (['one two', 'three'], '\\b(?:one two|three)'),
        ([], '\\b(?:)'),
    ]
)
def test_format_list_with_pattern_no_left_trunc(input_terms, output_text):
    # Arrange
    pattern = NO_LEFT_TRUNC
    # Act
    result = _format_list_with_pattern(pattern, input_terms)
    # Assert
    assert result==output_text
##########################################################################


################ TESTS FOR _get_additional_language_terms ################
ADDITIONAL_LANGUAGES = {'no':True}

# Testcase: missing language list
def test_get_additional_language_terms_missing_list(capsys):
    # Arrange
    term_list = {
                'termlist_name': 'Test1',
                'wordlist_en': [],
                'wordlist_fr': []
            }
    # Act
    _get_additional_language_terms(term_list)
    captured = capsys.readouterr()
    # Assert
    assert 'WARNING: The termlist Test1 does not have a list for language no.' in captured.out

# Testcase: add terms for 'no'
@pytest.mark.parametrize(
    'input_terms, output_list',
    [
        (
            {
                'termlist_name': 'Test1',
                'wordlist_en': ['one', 'two'],
                'wordlist_no': ['three', 'four']
            },
            ['three', 'four']
        ),
        (
            {
                'termlist_name': 'Test1',
                'wordlist_en': ['one', 'two'],
                'wordlist_no': []
            },
            []
        )
    ]
)
def test_get_additional_language_terms_with_no(input_terms, output_list):
    # Arrange
    # Act
    with mock.patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True}):
        results = _get_additional_language_terms(input_terms)
    # Assert
    assert set(results) == set(output_list)


# Testcase: add terms for multiple languages
@pytest.mark.parametrize(
    'input_terms, output_list',
    [
        (
            {
                'termlist_name': 'Test1',
                'wordlist_en': ['one', 'two'],
                'wordlist_no': ['three', 'four'],
                'wordlist_fi': ['five'],
            },
            ['three', 'four', 'five']
        ),
        (
            {
                'termlist_name': 'Test1',
                'wordlist_en': ['one', 'two'],
                'wordlist_fi': ['three', 'four'],
                'wordlist_no': [],
            },
            ['three', 'four']
        )
    ]
)
def test_get_additional_language_terms_with_multiple_languages(input_terms, output_list):
    # Arrange
    # Act
    with mock.patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True, 'fi':True}):
        results = _get_additional_language_terms(input_terms)
    # Assert
    assert set(results) == set(output_list)

##########################################################################

###################### TESTS FOR format_logic_rules ######################

# Testcase: format correct, no countries or pre_search
@pytest.mark.parametrize(
    'input_logic_rule, input_termlist_results, output_expected',
    [
        (
            '([Termlist1])',
            {'Termlist1':True},
            '(True)',
        ),
        (
            '([Termlist1])',
            {'Termlist1':True},
            '(True)',
        ),
    ]
)
def test_format_logic_rules(mocker, input_logic_rule, input_termlist_results, output_expected):
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
    ]
)
def test_format_logic_rules_with_countries(mocker, input_logic_rule, output_expected):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1':True, 'Termlist2':False}
    countries = {'Countries1':True, 'Countries2':False}
    # Act
    result = format_logic_rules(input_logic_rule, termlists, countries_results=countries)
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
    ]
)
def test_format_logic_rules_with_presearch(mocker, input_logic_rule, output_expected):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1':True, 'Termlist2':False}
    pre_search = {'Pre1':True, 'Pre2':False}
    # Act
    result = format_logic_rules(input_logic_rule, termlists, pre_search_results=pre_search)
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
    ]
)
def test_format_logic_rules_with_countries_and_presearch(mocker, input_logic_rule, output_expected):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1':True, 'Termlist2':False}
    countries = {'Countries1':True, 'Countries2':False}
    pre_search = {'Pre1':True, 'Pre2':False}
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
    ]
)
def test_format_logic_rules_correct_replacing_logic(mocker, input_logic_rule, output_expected):
    # Arrange
    mocker.patch('src.format_helpers._check_for_missing_matches', return_value=None)
    termlists = {'Termlist1':True, 'Termlist2':True}
    # Act
    result = format_logic_rules(input_logic_rule, termlists)
    # Assert
    assert result == output_expected
##########################################################################

################ TESTS FOR prepare_regex_search_termlist ################
# Testcase: test that it correctly calls _format_list_with_pattern with correct inputs
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers._get_additional_language_terms', return_value=[])
def test_prepare_regex_search_termlist_calls_format(mocker_get_additional_language_terms, mocker_format_list_with_pattern):
    # Arrange
    termlists = {
        'name':'Test1', 
        'wordlist_en':['one','two'], 
        'formatting_rule':'DEFAULT',
        'case':False
    }
    # Act
    with mock.patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True}) and mock.patch('src.format_helpers.REGEX_PATTERNS', {'DEFAULT':'(?:{})'}):
        prepare_regex_search_termlist(termlists, 'text')
    # Assert
    mocker_format_list_with_pattern.assert_called_once_with('(?:{})', ['one','two'])


# Testcase: Lowering the words in the list if case=False
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers._get_additional_language_terms', return_value=[])
def test_prepare_regex_search_termlist_lowercase_list(mocker_get_additional_language_terms, mocker_format_list_with_pattern):
    # Arrange
    termlists = {
        'name':'Test1', 
        'wordlist_en':['ONE','Two'], 
        'formatting_rule':'DEFAULT',
        'case':False
    }
    # Act
    with mock.patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True}) and mock.patch('src.format_helpers.REGEX_PATTERNS', {'DEFAULT':'(?:{})'}):
        prepare_regex_search_termlist(termlists, 'text')
    # Assert
    mocker_format_list_with_pattern.assert_called_once_with('(?:{})', ['one','two'])


# Testcase: Lowering the words in the input text if case=False
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers._get_additional_language_terms', return_value=[])
def test_prepare_regex_search_termlist_lowercase_text(mocker_get_additional_language_terms, mocker_format_list_with_pattern):
    # Arrange
    termlists = {
        'name':'Test1', 
        'wordlist_en':['ONE','Two'], 
        'formatting_rule':'DEFAULT',
        'case':False
    }
    input_text = 'Text with UPPERCASE'
    output_excpected = 'text with uppercase'
    # Act
    with mock.patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True}) and mock.patch('src.format_helpers.REGEX_PATTERNS', {'DEFAULT':'(?:{})'}):
        _, output_text = prepare_regex_search_termlist(termlists, input_text)
    # Assert
    assert output_text == output_excpected


# Testcase: NOT Lowering the words in the list if case=True
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers._get_additional_language_terms', return_value=[])
@patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True})
@patch('src.format_helpers.REGEX_PATTERNS', {'DEFAULT':'(?:{})'})
def test_prepare_regex_search_termlist_do_not_lowercase_list(mocker_get_additional_language_terms, mocker_format_list_with_pattern):
    # Arrange
    termlists = {
        'name':'Test1', 
        'wordlist_en':['ONE','Two'], 
        'formatting_rule':'DEFAULT',
        'case':True
    }
    # Act
    prepare_regex_search_termlist(termlists, 'text')
    # Assert
    mocker_format_list_with_pattern.assert_called_once_with('(?:{})', ['ONE','Two'])


# Testcase: NOT Lowering the words in the input text if case=True
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers._get_additional_language_terms', return_value=[])
@patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':True})
@patch('src.format_helpers.REGEX_PATTERNS', {'DEFAULT':'(?:{})'})
def test_prepare_regex_search_termlist_do_not_lowercase_text(mocker_get_additional_language_terms, mocker_format_list_with_pattern):
    # Arrange
    termlists = {
        'name':'Test1', 
        'wordlist_en':['ONE','Two'], 
        'formatting_rule':'DEFAULT',
        'case':True
    }
    input_text = 'Text with UPPERCASE'
    output_excpected = 'Text with UPPERCASE'
    # Act
    _, output_text = prepare_regex_search_termlist(termlists, input_text)
    # Assert
    assert output_text == output_excpected


# Testcase: no additional languages
@patch('src.format_helpers._format_list_with_pattern')
@patch('src.format_helpers._get_additional_language_terms')
@patch('src.format_helpers.ADDITIONAL_LANGUAGES', {'no':False})
@patch('src.format_helpers.REGEX_PATTERNS', {'DEFAULT':'(?:{})'})
def test_prepare_regex_search_termlist_no_additional_language(mocker_get_additional_language_terms, mocker_format_list_with_pattern):
    # Arrange
    termlists = {
        'name':'Test1', 
        'wordlist_en':['ONE','Two'], 
        'formatting_rule':'DEFAULT',
        'case':False
    }
    # Act
    prepare_regex_search_termlist(termlists, 'text')
    # Assert
    mocker_get_additional_language_terms.assert_not_called()
##########################################################################

