import pytest
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import run_goal_pre_search

######################### Testcase: No presearch #########################
@pytest.mark.pre_search
@pytest.mark.parametrize(
    'search_phrases, input_text',
    [
        ([], "This is a title"),
    ]
)
def test_run_goal_pre_search_empty(search_phrases, input_text):
    # Arrange
    # Act
    _, result = run_goal_pre_search(search_phrases, input_text)
    # Assert
    assert result=={}

 ######################### Testcase: One presearch, found text #########################
@pytest.mark.pre_search
@pytest.mark.pre_search
def test_run_goal_pre_search_one_true():
    # Arrange
    search_phrases = [
        {
            "name": "TEST",
            "logic_rule": "([test1])",
            "sentence_split": False, 
            "termlists": [
                {
                    "termlist_name": "test1",
                    "formatting_rule": "default",
                    "na": False,
                    "case": False,
                    "wordlist_en": ["one", "two"],
                    "wordlist_no": []
                }
            ]
        }
    ]
    input_text = "This is a title"
    output_expected = {"TEST":False}
    # Act
    _, result = run_goal_pre_search(search_phrases, input_text)
    # Assert
    assert result==output_expected

 ######################### Testcase: One presearch, not found text #########################
@pytest.mark.pre_search
def test_run_goal_pre_search_one_false():
    # Arrange
    search_phrases = [
        {
            "name": "TEST",
            "logic_rule": "([test1])",
            "sentence_split": False, 
            "termlists": [
                {
                    "termlist_name": "test1",
                    "formatting_rule": "default",
                    "na": False,
                    "case": False,
                    "wordlist_en": ["one", "two"],
                    "wordlist_no": []
                }
            ]
        }
    ]
    input_text = "This is a title"
    output_expected = {"TEST":False}
    # Act
    _, result = run_goal_pre_search(search_phrases, input_text)
    # Assert
    assert result==output_expected