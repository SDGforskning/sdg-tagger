import pytest
import sys
import os 
import mock

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
    pattern = r"\[[^\[\]]*\]"
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
    pattern = r"\[[^\[\]]*\]"
    logic_rule_raw = '([Terms1] and ([Terms2] or [Terms3]))'
    # Act
    result = _check_for_missing_matches(pattern, logic_rule_raw, input_dict)
    # Assert
    assert result is None

##########################################################################


################### TESTS FOR _format_list_with_pattern ###################
DEFAULT = "(?:{})"
SPECIFIC = "(?:{})\\b"
SPECIFIC_TRUNC = "\\b(?:{})\\b"
NO_LEFT_TRUNC = "\\b(?:{})"

# Testcase: DEFAULT format 
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_terms, output_text',
    [
        (["one"], "(?:one)"),
        (["one", "two", "three"], "(?:one|two|three)"),
        (["one two", "three"], "(?:one two|three)"),
        ([], "(?:)"),
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
        (["one"], "(?:one)\\b"),
        (["one", "two", "three"], "(?:one|two|three)\\b"),
        (["one two", "three"], "(?:one two|three)\\b"),
        ([], "(?:)\\b"),
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
        (["one"], "\\b(?:one)\\b"),
        (["one", "two", "three"], "\\b(?:one|two|three)\\b"),
        (["one two", "three"], "\\b(?:one two|three)\\b"),
        ([], "\\b(?:)\\b"),
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
        (["one"], "\\b(?:one)"),
        (["one", "two", "three"], "\\b(?:one|two|three)"),
        (["one two", "three"], "\\b(?:one two|three)"),
        ([], "\\b(?:)"),
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
                "termlist_name": "Test1",
                "wordlist_en": [],
                "wordlist_fr": []
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
                "termlist_name": "Test1",
                "wordlist_en": ["one", "two"],
                "wordlist_no": ["three", "four"]
            },
            ["three", "four"]
        ),
        (
            {
                "termlist_name": "Test1",
                "wordlist_en": ["one", "two"],
                "wordlist_no": []
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
                "termlist_name": "Test1",
                "wordlist_en": ["one", "two"],
                "wordlist_no": ["three", "four"],
                "wordlist_fi": ["five"],
            },
            ["three", "four", "five"]
        ),
        (
            {
                "termlist_name": "Test1",
                "wordlist_en": ["one", "two"],
                "wordlist_fi": ["three", "four"],
                "wordlist_no": [],
            },
            ["three", "four"]
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
#TODO

##########################################################################


################ TESTS FOR prepare_regex_search_termlist ################
#TODO

##########################################################################
