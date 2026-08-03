import pytest
import sys
import os
import mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.helpers import _are_terms_in_input_text

termlists_en = [
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

termlists_empty = [
    #all languages are empty
    {
        'termlist_name': 'Test5',
        'wordlist_en': [],
        'wordlist_no': [],
        'formatting_rule': 'DEFAULT',
        'case': True,
    },
    {
        'termlist_name': 'Test6',
        'wordlist_en': [],
        'wordlist_no': [],
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

    output_expected = {
        'en': {'Test1': False, 'Test2': False}
    }

    # Act
    output = _are_terms_in_input_text(termlists_en, input_text)

    # Assert
    assert output == output_expected


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
    _are_terms_in_input_text(termlists_en, input_text)

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
        mock.call(
                terms=termlists_en[0]['wordlist_en'], 
                input_text='Text with UPPERCASE', 
                formatting_rule=termlists_en[0]['formatting_rule'], 
                case=termlists_en[0]['case']
        ),
        mock.call(
                terms=termlists_en[1]['wordlist_en'], 
                input_text='Text with UPPERCASE', 
                formatting_rule=termlists_en[1]['formatting_rule'], 
                case=termlists_en[1]['case']
        )
    ]

    # Act
    _are_terms_in_input_text(termlists_en, input_text)

    # Assert
    mocker_prepare_regex_search_termlist.assert_has_calls(
        expected_calls_prepare_regex_search_termlist
    )
    assert mocker_prepare_regex_search_termlist.call_count == 2


# Testcase: test that it calls prepare_regex_search_termlist with correct values when having a multilanguage search
@mock.patch('src.helpers.prepare_regex_search_termlist')
@mock.patch('src.helpers._pattern_search_boolean')
@mock.patch('src.helpers._get_language_termlists')
def test_are_terms_in_input_text_calls_prepare_regex_search_termlist_multilanguage(
    mocker_get_language_termlists, mocker_pattern_search_boolean, mocker_prepare_regex_search_termlist
):
    #Arrange:
    termlists_multilanguage = [
        {
            'termlist_name': 'Test3',
            'wordlist_en': ['one', 'Two'],
            'wordlist_no': ['EN', 'To'],
            'formatting_rule': 'DEFAULT',
            'case': True,
        },
        {
            'termlist_name': 'Test4',
            'wordlist_en': ['Three', 'four'],
            'wordlist_no': ['Tre', 'FIRE'],
            'formatting_rule': 'DEFAULT',
            'case': False,
        },
    ]

    mocker_get_language_termlists.side_effect = [
        {'en': ['one', 'Two'], 'no': ['EN', 'To']}, 
        {'en': ['Three', 'four'], 'no': ['Tre', 'FIRE']},

    ]

    mocker_prepare_regex_search_termlist.side_effect = [
        ('(?:one|Two)', 'Text with UPPERCASE'),
        ('(?:EN|To)', 'Text with UPPERCASE'),
        ('(?:three|four)', 'text with uppercase'),
        ('(?:tre|fire)', 'text with uppercase'),
    ]
    mocker_pattern_search_boolean.side_effect = [False, False, False, False]

    expected_calls_prepare_regex_search_termlist = [
        mock.call(
                terms=termlists_multilanguage[0]['wordlist_en'], 
                input_text='Text with UPPERCASE', 
                formatting_rule=termlists_multilanguage[0]['formatting_rule'], 
                case=termlists_multilanguage[0]['case']
        ),
        mock.call(
                terms=termlists_multilanguage[0]['wordlist_no'], 
                input_text='Text with UPPERCASE', 
                formatting_rule=termlists_multilanguage[0]['formatting_rule'], 
                case=termlists_multilanguage[0]['case']
        ),
        mock.call(
                terms=termlists_multilanguage[1]['wordlist_en'], 
                input_text='Text with UPPERCASE', 
                formatting_rule=termlists_multilanguage[1]['formatting_rule'], 
                case=termlists_multilanguage[1]['case']
        ),
        mock.call(
                terms=termlists_multilanguage[1]['wordlist_no'], 
                input_text='Text with UPPERCASE', 
                formatting_rule=termlists_multilanguage[1]['formatting_rule'], 
                case=termlists_multilanguage[1]['case']
        )
    ]

    # Act
    _are_terms_in_input_text(termlists_multilanguage, input_text)

    # Assert
    mocker_prepare_regex_search_termlist.assert_has_calls(
        expected_calls_prepare_regex_search_termlist
    )
    assert mocker_prepare_regex_search_termlist.call_count == 4


# Testcase: test if we successfully search separately between languages
@pytest.mark.parametrize(
    'input_termlists, input_text, output_expected',
    [
        (
            [
                {
                    'termlist_name': 'Termlist1',
                    'wordlist_en': ['one', 'two', 'three'],
                    'wordlist_no': ['en', 'to', 'tre'],
                    'formatting_rule': 'default',
                    'case': False,
                },
                {
                    'termlist_name': 'Termlist2',
                    'wordlist_en': ['Three', 'four'],
                    'wordlist_no': ['Tre', 'FIRE'],
                    'formatting_rule': 'default',
                    'case': False,
                },
            ],
            'en to four five',
            {
                'en': {'Termlist1':False, 'Termlist2':True},
                'no': {'Termlist1':True, 'Termlist2':False},
            }
        ),
    ],
)
def test_multilingual_search_without_mocking(input_termlists, input_text, output_expected):
    # Arrange
    # Act
    actual_output = _are_terms_in_input_text(input_termlists, input_text)

    # Assert
    assert actual_output == output_expected


