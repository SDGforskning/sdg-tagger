import pytest
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import pattern_search_boolean

DEFAULT = "(?:{})"
SPECIFIC = "(?:{})\\b"
SPECIFIC_TRUNC = "\\b(?:{})\\b"

######################### Testcase: DEFAULT format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["house"], "many houses"),
        (["house"], "this house is pretty"),
        (["house"], "what a lovely courthouse!"),
        (["low-maintenance"], "this is a low-maintenance house."),
        (["low-ball"], "they are low-balling the offer"),
        (["house", "low-maintenance", "low-ball"], "this is a low-maintenance house"),
    ]
)
def test_pattern_search_boolean_default_true(input):
    # Arrange
    pattern = DEFAULT
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert result


######################### Testcase: DEFAULT format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["house"], "many cars"),
        (["houses"], "this house is pretty"),
        (["low-maintenance"], "it has been low maintenance here"),
        (["low-maintenance"], "they are low-balling the offer"),
        (["house", "low-maintenance"], "this is a random sentence"),
    ]
)
def test_pattern_search_boolean_default_false(input):
    # Arrange
    pattern = SPECIFIC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert not result


######################### Testcase: SPECIFIC format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["house"], "this house is nice"),
        (["house"], "courthouse"),
    ]
)
def test_pattern_search_boolean_specific_true(input):
    # Arrange
    pattern = SPECIFIC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert result


######################### Testcase: SPECIFIC format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["house"], "many houses"),
        (["house"], "courthouses"),
        (["low-maintenance"], "it has been low maintenance here"),
        (["house", "low-maintenance"], "this is a random sentence"),
    ]
)
def test_pattern_search_boolean_specific_false(input):
    # Arrange
    pattern = SPECIFIC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert not result


######################### Testcase: SPECIFIC_TRUNC format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["house"], "one house"),
        (["house"], "this house."),
    ]
)
def test_pattern_search_boolean_specific_trunc_true(input):
    # Arrange
    pattern = SPECIFIC_TRUNC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert result


######################### Testcase: SPECIFIC_TRUNC format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["house"], "courthouse"),
        (["house"], "courthouses"),
        (["house"], "houses"),
        (["low-maintenance"], "it has been low maintenance here"),
        (["house", "low-maintenance"], "this is a random sentence"),
    ]
)
def test_pattern_search_boolean_specific_trunc_false(input):
    # Arrange
    pattern = SPECIFIC_TRUNC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert not result

######################### Testcase: STAR icon + SPECIFIC_TRUNC format + TRUE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["economic resource.*"], "economic resources"),
        (["economic resource.*"], "economic resource"),
    ]
)
def test_pattern_search_boolean_specific_trunc_true_with_star(input):
    # Arrange
    pattern = SPECIFIC_TRUNC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert result

######################### Testcase: STAR icon + SPECIFIC_TRUNC format + FALSE output #########################
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (["economic resource.*"], "economic"),
        (["economic resource.*"], "resources"),
        (["house", "low-maintenance"], "this is a random sentence"),
    ]
)
def test_pattern_search_boolean_specific_trunc_false_with_star(input):
    # Arrange
    pattern = SPECIFIC_TRUNC
    # Act
    result = pattern_search_boolean(pattern, search_terms=input[0], text=input[1])
    # Assert
    assert not result


############### Testcase: contains capital letters and TRUE output, various patterns ###############
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (SPECIFIC, ["This"], "This is nice"),
        (SPECIFIC, ["PC"], "One PC"),
        (DEFAULT, ["House"], "Houses"),
    ]
)
def test_pattern_search_boolean_capitol_letters_true(input):
    # Arrange
    pattern=input[0]
    search_terms=input[1]
    text=input[2]
    # Act
    result = pattern_search_boolean(pattern, search_terms, text)
    # Assert
    assert result


############### Testcase: Capital letters FALSE output, various patterns ###############
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (SPECIFIC, ["House"], "Houses are pretty"), 
        (DEFAULT, ["HOUSE"], "this house is pretty"),
    ]
)
def test_pattern_search_boolean_capitol_letters_false(input):
    # Arrange
    pattern=input[0]
    search_terms=input[1]
    text=input[2]
    # Act
    result = pattern_search_boolean(pattern, search_terms, text)
    # Assert
    assert not result


########## Testcase: Norwegian terms (with æøå) NB and NN, TRUE output, various patterns ##########
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (SPECIFIC, ["gård"], "vi bor på en gård."), 
        (SPECIFIC_TRUNC, ["gård"], "vi bor på en gård."), 
        (DEFAULT, ["klær", "klør"], "desse klærne klør."),
    ]
)
def test_pattern_search_boolean_norwegian_terms_true(input):
    # Arrange
    pattern=input[0]
    search_terms=input[1]
    text=input[2]
    # Act
    result = pattern_search_boolean(pattern, search_terms, text)
    # Assert
    assert result


############### Testcase: Norwegian terms (with æøå) NB and NN, FALSE output, various patterns ###############
@pytest.mark.regex_pattern
@pytest.mark.parametrize(
    'input', 
    [
        (SPECIFIC, ["klær", "klør"], "klærne er fine."),
        (SPECIFIC_TRUNC, ["klær"], "treningsklær er nyttig"),
    ]
)
def test_pattern_search_boolean_norwegian_terms_false(input):
    # Arrange
    pattern=input[0]
    search_terms=input[1]
    text=input[2]
    # Act
    result = pattern_search_boolean(pattern, search_terms, text)
    # Assert
    assert not result


