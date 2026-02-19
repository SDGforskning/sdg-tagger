import pytest
import sys
import os
import pandas as pd
from pandas.testing import assert_series_equal
import numpy as np
from unittest.mock import patch
from unittest.mock import call

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search_dataframe import (
    dataframe_search, 
    _format_item,
    _format_df_value, 
    _format_results,
    _row_search,
    _get_formatted_column_names_export
)
from src.consts import LIST_ALL_SDG_NR


##################################### Testcase: format item correct letters #####################################
@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input, output_expected', 
    [
        ('ab', 'ab'),
        ('b', 'b'),
    ]
)
def test_format_item_letters(input, output_expected):
    # Arrange
    # Act
    output = _format_item(input)

    # Assert
    assert output == output_expected


##################################### Testcase: format item correct digits #####################################
@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input, output_expected', 
    [
        ('1', '01'),
        ('01', '01'),
        ('010', '10'),
        ('15', '15'),
    ]
)
def test_format_item_digits(input, output_expected):
    # Arrange
    # Act
    output = _format_item(input)

    # Assert
    assert output == output_expected


######################## Testcase: check that the string formatting is correct for both single and double digits, and letters ########################
@pytest.mark.dataframe_search
@pytest.mark.dependency()
@pytest.mark.parametrize(
    'input_value, input_sdg_nr, input_target, output_expected', 
    [
        (True, '1', 'b',
         'SDG01_b'
         ),
         (True, '01', '1',
         'SDG01_01'
         ),
         (True, '10', 'b',
         'SDG10_b'
         ),
         (True, '10', '10',
         'SDG10_10'
         ),
         (True, '10', '1',
         'SDG10_01'
         ),
         (True, '11', '02',
         'SDG11_02'
         ),
    ]
)
def test_format_df_value_correct_formatting(input_value, input_sdg_nr, input_target, output_expected):
    # Arrange
    # Act
    output = _format_df_value(input_value, input_sdg_nr, input_target)

    # Assert
    assert output == output_expected


##################################### Testcase: check that nan is returned when the value is false #####################################
@pytest.mark.dataframe_search
@pytest.mark.dependency()
@pytest.mark.parametrize(
    'input_value, input_sdg_nr, input_target', 
    [
        (False, '1', 'b'),
        (False, '5', '1'),
    ]
)
def test_format_df_value_false_value(input_value, input_sdg_nr, input_target):
    # Arrange
    # Act
    output = _format_df_value(input_value, input_sdg_nr, input_target)

    # Assert
    assert np.isnan(output)


######################## Testcases: format results correct (with mocking) ########################
@pytest.mark.dataframe_search
@patch('src.search_dataframe._format_df_value')
@patch('src.search_dataframe.LIST_ALL_SDG_NR', [1])
def test_format_results_basic(mock_format_df_value):
    # Arrange
    input = {
                'countries': {'LDC': True, 'SIDS': False, 'LDS': False, 'LMIC': True},
                '1': {
                    'sdg_number': '1',
                    'pre_search': {},
                    'targets': {
                        '1': {'1': True},
                        'b': {'1': True}
                    },
                    'mentions': False
                }
            }
    sdgs = [1]
    output_expected = [True, False, False, True, 'SDGx_x', 'SDGx_x', False]
    mock_format_df_value.return_value = 'SDGx_x'

    # Act
    output = _format_results(input, sdgs)

    # Assert
    assert output==output_expected
    

@pytest.mark.dataframe_search
@patch('src.search_dataframe.LIST_ALL_SDG_NR', [1])
@patch('src.search_dataframe._format_df_value')
def test_format_results_with_pre_search(mock_format_df_value):
    # Arrange
    input = {
                'countries': {'LDC': True, 'SIDS': False, 'LDS': False, 'LMIC': True},
                '1': {
                    'sdg_number': '1',
                    'pre_search': {'pre': True},
                    'targets': {'1': {'1': True}},
                    'mentions': False
                }
            }
    sdgs = [1]
    output_expected = [True, False, False, True, True, 'SDGx_x', False]
    mock_format_df_value.return_value = 'SDGx_x'

    # Act
    output = _format_results(input, sdgs)

    # Assert
    assert output==output_expected


################### Testcase: check that format_df_values was called with correct values ###################
@pytest.mark.dataframe_search
@patch('src.search_dataframe.LIST_ALL_SDG_NR', [1])
def test_format_results_calls(mocker):
    # Arrange
    input = {
                'countries': {'LDC': True, 'SIDS': False, 'LDS': False, 'LMIC': True},
                '1': {
                    'sdg_number': '1',
                    'targets': {
                        '1': {'1': True, '2': False, '3': True},
                        'b': {'1': False, '2': False, '3': False}
                    }
                }
            }
    sdgs = [1]

    mock_format_df_value = mocker.patch('src.search_dataframe._format_df_value')

    expected_calls = [
        call(True, '1', '1'),
        call(False, '1', 'b')
    ]

    # Act
    _format_results(input, sdgs)

    # Assert
    assert mock_format_df_value.call_count == 2
    assert mock_format_df_value.call_args_list == expected_calls


############################## Testcase: format results correct (while calling format df value)##############################
@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input_dict, input_sdgs, expected_output', 
    [
        (
            {'countries': {'LDC': True, 'SIDS': False, 'LDS': False, 'LMIC': True},
                '1': {
                    'sdg_number': '1',
                    'targets': {
                        '1': {'1': True, '2': False, '3': True},
                        'b': {'1': False, '2': False, '3': False}
                    }
                }
            },
            [1],
            [True, False, False, True, 'SDG01_01', np.nan]
        ),
        (
            {'countries': {'LDC': True},
                '1': {
                    'sdg_number': '1',
                    'targets': {
                        '1': {'1': True},
                        'b': {'1': False, '2': True, '3': False}
                    }
                },
                '15': {
                    'sdg_number': '15',
                    'targets': {
                        '1': {'1': True}
                    }
                }
            },
            [1, 15],
            [True, 'SDG01_01', 'SDG01_b', 'SDG15_01']
        ),
    ]
)
@patch('src.search_dataframe.LIST_ALL_SDG_NR', [1, 15])
def test_format_results_including_df_value_formating(input_dict, input_sdgs, expected_output):
    # Arrange
    # Act
    output = _format_results(input_dict, input_sdgs)

    # Assert
    assert output == expected_output


##################################### Testcase: row search #####################################
@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input_text, input_sdgs, output_expected', 
    [
        ('Some text', [1], pd.Series([True, 'SDG01_01', 'SDG01_b', np.nan]))
    ]
)
@patch('src.search_dataframe.search_all_goals')
@patch('src.search_dataframe._format_results')
def test_row_search(mock_format_results, mock_search_all_goals, input_text, input_sdgs, output_expected):
    # Arrange
    mock_search_all_goals.return_value = 'SDGx_x'
    mock_format_results.return_value = [True, 'SDG01_01', 'SDG01_b', np.nan]
    # Act
    output = _row_search(input_text, input_sdgs)
    print(output)

    # Assert
    assert_series_equal(output, output_expected)


@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input_text, input_sdgs', 
    [('Some text', [1])]
)
def test_row_search_calls_format_results(mocker, input_text, input_sdgs):
    # Arrange
    mock_search_all_goals = mocker.patch('src.search_dataframe.search_all_goals')
    mock_search_all_goals.return_value = 'SDGx_x'
    mock_format_results = mocker.patch('src.search_dataframe._format_results')
    
    # Act
    expected_calls = [call('SDGx_x', [1])]

    # Act
    _row_search(input_text, input_sdgs)

    # Assert
    assert mock_format_results.call_count == 1
    assert mock_format_results.call_args_list == expected_calls


@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input_text, input_sdgs', 
    [('Some text', [1])]
)
def test_row_search_with_mocks(mocker, input_text, input_sdgs):
    # Arrange
    mock_search_all_goals = mocker.patch('src.search_dataframe.search_all_goals')
    mock_format_results = mocker.patch('src.search_dataframe._format_results')
    mock_format_results.return_value = [True, 'SDG01_01', 'SDG01_b', np.nan]
    
    # Act
    expected_calls = [call(input_text, input_sdgs)]

    # Act
    _row_search(input_text, input_sdgs)

    # Assert
    assert mock_search_all_goals.call_count == 1
    assert mock_search_all_goals.call_args_list == expected_calls



# Testcase: get_formatted_column_names_export() #mock the get_countries_phrases and get_sdg_phrases and format_item functions 
##################################### Testcase: format results correct #####################################
@pytest.mark.skip()
@pytest.mark.dataframe_search
@pytest.mark.dependency(depends=[])
@pytest.mark.parametrize(
    '', 
    [

    ]
)
def test_get_formatted_column_names_export():
    # Arrange
    # Act
    output = _get_formatted_column_names_export()

    # Assert
    assert output

############################################################################################################

country_col = ['LDC', 'SIDS', 'LDS', 'LMIC']
sdg_columns = {
    1: ['tempsdg01_01', 'tempsdg01_02', 'tempsdg01_03', 'tempsdg01_04', 'tempsdg01_05', 'tempsdg01_a', 'tempsdg01_b', 'tempmentionsdg01'],
    2: ['tempsdg02_01', 'tempsdg02_02', 'tempsdg02_03', 'tempsdg02_04', 'tempsdg02_05', 'tempsdg02_a', 'tempsdg02_b', 'tempsdg02_c', 'tempmentionsdg02'],
    3: ['tempsdg03_01', 'tempsdg03_02', 'tempsdg03_03', 'tempsdg03_04', 'tempsdg03_05', 'tempsdg03_06', 'tempsdg03_07', 'tempsdg03_08', 'tempsdg03_09', 'tempsdg03_a', 'tempsdg03_b', 'tempsdg03_c', 'tempsdg03_d', 'tempmentionsdg03'],
    4: ['tempsdg04_01', 'tempsdg04_02', 'tempsdg04_03', 'tempsdg04_04', 'tempsdg04_05', 'tempsdg04_06', 'tempsdg04_07', 'tempsdg04_a', 'tempsdg04_b', 'tempsdg04_c', 'tempmentionsdg04'],
    7: ['tempsdg07_01', 'tempsdg07_02', 'tempsdg07_03', 'tempsdg07_a', 'tempsdg07_b', 'tempmentionsdg07'],
    11: ['tempsdg11_01', 'tempsdg11_02', 'tempsdg11_03', 'tempsdg11_04', 'tempsdg11_05', 'tempsdg11_06', 'tempsdg11_07', 'tempsdg11_a', 'tempsdg11_b', 'tempsdg11_c', 'tempmentionsdg11'],
    12: ['scp', 'tempsdg12_01', 'tempsdg12_02', 'tempsdg12_03', 'tempsdg12_04', 'tempsdg12_05', 'tempsdg12_06', 'tempsdg12_07', 'tempsdg12_08', 'tempsdg12_a', 'tempsdg12_b', 'tempsdg12_c', 'tempmentionsdg12'],
    13: ['tempsdg13_01', 'tempsdg13_02', 'tempsdg13_03', 'tempsdg13_a', 'tempsdg13_b', 'tempmentionsdg13'],
    14: ['marine_terms', 'tempsdg14_01', 'tempsdg14_02', 'tempsdg14_03', 'tempsdg14_04', 'tempsdg14_05', 'tempsdg14_06', 'tempsdg14_07', 'tempsdg14_a', 'tempsdg14_b', 'tempsdg14_c', 'tempmentionsdg14'],
    15: ['terr_terms', 'terrestrial_double_NOT', 'tempsdg15_01', 'tempsdg15_02', 'tempsdg15_03', 'tempsdg15_04', 'tempsdg15_05', 'tempsdg15_06', 'tempsdg15_07', 'tempsdg15_08', 'tempsdg15_09', 'tempsdg15_a', 'tempsdg15_b', 'tempsdg15_c', 'tempmentionsdg15']
}

######################### Testcase: Check that the expected columns are present in output #########################
@pytest.mark.dataframe_search
@pytest.mark.parametrize(
    'input_data, input_column', 
    [
        (
            {'text': ['test123', 'test321']},
            'text'
        )
    ]
)
@pytest.mark.skip(reason='Should be added once all the SDG json files are complete.')
def test_dataframe_search(input_data, input_column):
    # Arrange
    input_df = pd.DataFrame(input_data)
    expected_columns = input_df.columns.tolist() + country_col
    for sdg_nr in LIST_ALL_SDG_NR:
        for key, value in sdg_columns[sdg_nr]:
            expected_columns += value

    # Act
    output = dataframe_search(input_df, input_column)

    # Assert
    assert output.columns.tolist() == expected_columns

