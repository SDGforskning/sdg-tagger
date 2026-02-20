import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import _pattern_search_boolean

DEFAULT = '(?:{})'
SPECIFIC = '(?:{})\\b'
SPECIFIC_TRUNC = '\\b(?:{})\\b'
NO_LEFT_TRUNC = '\\b(?:{})'


######################### Testcase: DEFAULT format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:house)', 'many houses'),
        ('(?:house)', 'this house is pretty'),
        ('(?:house)', 'what a lovely courthouse!'),
        ('(?:low-maintenance)', 'this is a low-maintenance house.'),
        ('(?:low-ball)', 'they are low-balling the offer'),
        ('(?:house|low-maintenance|low-ball)', 'this is a low-maintenance house'),
    ],
)
def test_pattern_search_boolean_default_true(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert result


######################### Testcase: DEFAULT format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:house)', 'many cars'),
        ('(?:houses)', 'this house is pretty'),
        ('(?:low-maintenance)', 'it has been low maintenance here'),
        ('(?:low-maintenance)', 'they are low-balling the offer'),
        ('(?:house|low-maintenance)', 'this is a random sentence'),
    ],
)
def test_pattern_search_boolean_default_false(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert not result


######################### Testcase: SPECIFIC format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:house)\\b', 'this house is nice'),
        ('(?:house)\\b', 'courthouse'),
    ],
)
def test_pattern_search_boolean_specific_true(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert result


######################### Testcase: SPECIFIC format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:house)\\b', 'many houses'),
        ('(?:house)\\b', 'courthouses'),
        ('(?:low-maintenance)\\b', 'it has been low maintenance here'),
        ('(?:house|low-maintenance)\\b', 'this is a random sentence'),
    ],
)
def test_pattern_search_boolean_specific_false(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert not result


######################### Testcase: SPECIFIC_TRUNC format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('\\b(?:house)\\b', 'one house'),
        ('\\b(?:house)\\b', 'this house.'),
    ],
)
def test_pattern_search_boolean_specific_trunc_true(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert result


######################### Testcase: SPECIFIC_TRUNC format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('\\b(?:house)\\b', 'courthouse'),
        ('\\b(?:house)\\b', 'courthouses'),
        ('\\b(?:house)\\b', 'houses'),
        ('\\b(?:low-maintenance)\\b', 'it has been low maintenance here'),
        ('\\b(?:house|low-maintenance)\\b', 'this is a random sentence'),
    ],
)
def test_pattern_search_boolean_specific_trunc_false(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert not result


######################### Testcase: STAR icon + SPECIFIC_TRUNC format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('\\b(?:economic resource.*)\\b', 'economic resources'),
        ('\\b(?:economic resource.*)\\b', 'economic resource'),
    ],
)
def test_pattern_search_boolean_specific_trunc_true_with_star(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert result


######################### Testcase: STAR icon + SPECIFIC_TRUNC format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('\\b(?:economic resource.*)\\b', 'economic'),
        ('\\b(?:economic resource.*)\\b', 'resources'),
        ('\\b(?:house|low-maintenance)\\b', 'this is a random sentence'),
    ],
)
def test_pattern_search_boolean_specific_trunc_false_with_star(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert not result


############### Testcase: contains capital letters and TRUE output, various patterns ###############
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:This)\\b', 'This is nice'),
        ('(?:PC)\\b', 'One PC'),
        ('(?:House)', 'Houses'),
    ],
)
def test_pattern_search_boolean_capitol_letters_true(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert result


############### Testcase: Capital letters FALSE output, various patterns ###############
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:House)\\b', 'Houses are pretty'),
        ('(?:HOUSE)', 'this house is pretty'),
    ],
)
def test_pattern_search_boolean_capitol_letters_false(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert not result


########## Testcase: Norwegian terms (with æøå) NB and NN, TRUE output, various patterns ##########
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:gård)\\b', 'vi bor på en bondegård.'),
        ('\\b(?:gård)\\b', 'vi bor på en gård.'),
        ('(?:klær|klør)', 'desse klærne klør.'),
    ],
)
def test_pattern_search_boolean_norwegian_terms_true(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert result


############### Testcase: Norwegian terms (with æøå) NB and NN, FALSE output, various patterns ###############
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input_regex, input_text',
    [
        ('(?:klær|klør)\\b', 'klærne er fine.'),
        ('\\b(?:gård)\\b', 'vi bor på en bondegård.'),
        ('\\b(?:klær)\\b', 'treningsklær er nyttig'),
    ],
)
def test_pattern_search_boolean_norwegian_terms_false(input_regex, input_text):
    # Arrange
    # Act
    result = _pattern_search_boolean(input_regex, input_text)
    # Assert
    assert not result
