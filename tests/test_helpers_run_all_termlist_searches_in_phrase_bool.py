import pytest
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import run_all_termlist_searches_in_list_of_phrases_bool


######################### Testcase: sentence splitting #########################
@pytest.mark.pre_search
@pytest.mark.countries
@pytest.mark.sentence_split
@pytest.mark.parametrize(
    'input_text, output_expected',
    [
        (
            'Sentence one. Sentence two. Sentence three.',
            {'TEST': False}
        ),
        (
            'Sentence one. Sentence two three.',
            {'TEST': True}
        ),
        (
            'Sentence one! Sentence three.',
            {'TEST': False}
        ),
        (
            'Sentence one? Sentence three.',
            {'TEST': False}
        ),
    ]
)
def test_run_all_termlist_searches_in_list_of_phrases_bool_sentence_split(input_text, output_expected):
    # Arrange
    search_phrases = [
        {
            'name': 'TEST',
            'logic_rule': '([test1] and [test2])',
            'sentence_split': True, 
            'termlists': [
                {
                    'termlist_name': 'test1',
                    'formatting_rule': 'default',
                    'na': False,
                    'case': False,
                    'wordlist_en': ['one', 'two'],
                    'wordlist_no': []
                },
                {
                    'termlist_name': 'test2',
                    'formatting_rule': 'default',
                    'na': False,
                    'case': False,
                    'wordlist_en': ['three', 'four'],
                    'wordlist_no': []
                }
            ]
        }
    ]
    # Act
    result = run_all_termlist_searches_in_list_of_phrases_bool(search_phrases, input_text, 'name')
    # Assert
    assert result==output_expected