import pytest
import sys
import os
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search_dataframe import (
    dataframe_search, 
    format_df_value, 
    format_results,
    format_item,
    row_search,
    get_formatted_column_names_export
)
from src.consts import LIST_ALL_SDG_NR


######################## Testcase: check that the string formatting is correct for both single and double digits, and letters ########################
@pytest.mark.sdg_search
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
    output = format_df_value(input_value, input_sdg_nr, input_target)

    # Act
    assert output == output_expected


##################################### Testcase: check that nan is returned when the value is false #####################################
@pytest.mark.sdg_search
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
    output = format_df_value(input_value, input_sdg_nr, input_target)

    # Act
    assert np.isnan(output)


##################################### Testcase: format results correct #####################################
@pytest.mark.sdg_search
@pytest.mark.dependency(depends=["test_format_df_value_correct_formatting", "test_format_df_value_false_value"])
@pytest.mark.parametrize(
    '', 
    [

    ]
)
def test_format_results():
    # Arrange
    # Act
    output = format_results()

    # Act
    assert output

# TODO Testcase: format_item()

# TODO Testcase: row_search()

# TODO Testcase: get_formatted_column_names_export()


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
@pytest.mark.sdg_search
@pytest.mark.parametrize(
    'input_data, input_column', 
    [
        (
            {'text': ['test123', 'test321']},
            'text'
        )
    ]
)
@pytest.mark.skip(reason="Should be added once all the SDG json files are complete.")
def test_dataframe_search(input_data, input_column):
    # Arrange
    input_df = pd.DataFrame(input_data)
    expected_columns = input_df.columns.tolist() + country_col
    for sdg_nr in LIST_ALL_SDG_NR:
        expected_columns += sdg_columns
    #for key, value in sdg_columns:
    #    expected_columns += value

    # Act
    output = dataframe_search(input_df, input_column)

    # Act
    assert output.columns.tolist() == expected_columns

