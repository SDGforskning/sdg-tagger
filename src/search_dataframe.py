import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from typing import Any

tqdm.pandas()

from .consts import LIST_ALL_SDG_NR, COUNTRIES
from .sdg_search import search_all_goals, search_target
from .helpers import get_sdg_phrases


def _format_item(item: str) -> str:
    """Formats a single-digit number (0-9) with a leading zero. Leaves other inputs (letters, multi-digit numbers) as they are.

    Args:
        item: the letter or digit(as a string) to be formatted

    Returns:
        Formatted string
    """
    try:
        if item[0] == '0':
            num = int(item[1:])
            return f'{num:02d}'
        else:
            num = int(item)
            return f'{num:02d}'

    except ValueError:
        return str(item)


def _format_df_value(value: bool, sdg_nr: str, target: str) -> str | float:
    """Format the value to be 'SDG' + the sdg nr in two digits + underscore + the target number in two digits or in one digit if it is a character

    Args:
        value: True or False
        sdg_nr: SDG number to be in the return string
        target: the target number or character for the return string

    Returns
        the formatted string, or np.nan if the result was False
    """
    if value == False:
        return np.nan
    else:
        nr_formatted = f'{int(sdg_nr):02d}'
        return f'SDG{nr_formatted}_{_format_item(target)}'


def _format_results(
    result: dict[str, dict[str, Any]], sdg_list: list[int]
) -> list[str]:
    """Formats the sdg search result json into a list of values

    Args:
        result: the json result from the sdg search 'search_all_goals' function
        sdg_list: A list of SDGs to get the columns for

    Returns:
        a list of formatted values of the search results
    """
    countries = [val for _, val in result['countries'].items()]
    sdgs = []

    for sdg_nr in sdg_list:
        sdg_result = []
        sdg_termlist_results = result[str(sdg_nr)]

        if 'pre_search' in sdg_termlist_results:
            pre_searches = [
                val for _, val in sdg_termlist_results['pre_search'].items()
            ]
            sdg_result.extend(pre_searches)
        sdg_result.extend(
            [
                _format_df_value(any(val.values()), str(sdg_nr), key)
                for key, val in sdg_termlist_results['targets'].items()
            ]
        )

        if 'mentions' in sdg_termlist_results:
            sdg_result.append(sdg_termlist_results['mentions'])
        sdgs.extend(sdg_result)

    return countries + sdgs


def _row_search(text: str, sdg_list: list[int]) -> pd.Series:
    """Performs search for all sdgs for a given text and returns is as a pandas series (aka a row in a pandas dataframe)

    Args:
        text: the text to be labelled
        sdg_list: A list of SDGs to do the search on

    Returns:
        The results of the SDG search as a Pandas series
    """
    sdg_list = [sdg for sdg in sdg_list if int(sdg) in set(LIST_ALL_SDG_NR)]
    results_raw = search_all_goals(text, sdg_list)
    results_formatted = _format_results(results_raw, sdg_list)
    return pd.Series(results_formatted)


def _row_search_one_target(text: str, sdg_nr: int, target: str, countries: dict[str: bool] = False) -> pd.Series:
    """Performs search for all sdgs for a given text and returns is as a pandas series (aka a row in a pandas dataframe)

    Args:
        text: the text to be labelled
        sdg_nr: the SDG to do the search on
        target: the target to search for
        countries: Results of countries search. False by default (optional)

    Returns:
        The results of the SDG search as a Pandas series
    """
    results_raw = search_target(text, sdg_nr, target, countries)
    results_formatted = _format_results(results_raw, [sdg_nr])
    return pd.Series(results_formatted)


def _get_formatted_column_names_export(sdg_list: list[int]) -> list[str]:
    """Based on which sdgs and country searches are implemented, get a list of columns to populate with the search results.

    Args:
        sdg_list: A list of SDGs to get the columns for

    Returns:
        A list of column names based on which SDG searches exist in the json files.
    """
    columns = []
    columns.extend([x['name'] for x in COUNTRIES])

    for sdg_nr in [sdg for sdg in sdg_list if sdg in set(LIST_ALL_SDG_NR)]:
        pre_searches, sdg_all_targets, mentions = get_sdg_phrases(sdg_nr)
        columns.extend([x['name'] for x in pre_searches])
        nr_formatted = f'{sdg_nr:02d}'

        for target in sdg_all_targets:
            target_formatted = _format_item(target['name'])
            columns.append(f'tempsdg{nr_formatted}_{target_formatted}')

        if len(mentions) > 0:
            columns.append(f'tempsdg{nr_formatted}_mentions')

    return columns


def _get_formatted_column_names_one_target(sdg_nr: int, target_to_search: str) -> list[str]:
    """Based on which presearches and country searches are implemented, get a list of column names to populate with the search results. 

    Args:
        sdg: the SDG to get formated column name for
        target: the target to get formated column name for

    Returns:
        A list of column names based on the searches that exist in the json files.
    """
    columns = []
    columns.extend([x['name'] for x in COUNTRIES])

    pre_searches, sdg_all_targets, _ = get_sdg_phrases(sdg_nr)
    columns.extend([x['name'] for x in pre_searches])
    nr_formatted = f'{sdg_nr:02d}'

    for target in sdg_all_targets:
        if target['name'] == target_to_search:
            target_formatted = _format_item(target['name'])
            columns.append(f'tempsdg{nr_formatted}_{target_formatted}')

    return columns


def _to_string_or_empty(value) -> str:
    """Checks whether a value is a string or nan, and converts it to a string. 

    Args:
        value: either a string or a nan value

    Returns:
        A string representation of the value. An empty string if the input was nan.
    """
    if isinstance(value, str):
        return value
    elif pd.isna(value):
        return ''
    else:
        return str(value)


def dataframe_search(
    df: pd.DataFrame,
    sdg_list: list[int] = LIST_ALL_SDG_NR,
    text_column: str = 'result_title',
) -> pd.DataFrame:
    """Replicating the original script that took a dataframe with titles and performed searches for all sdgs for each row

    Args:
        df: a dataframe containing texts to perform SDG search on.
        sdg_list: list of SDGs to perform the search on. Default is all SDGs.
        text_column: the name of the column in the df containing the text to tag. Default is 'result_title'

    Returns:
        a dataframe with the results of all SDG searches
    """
    df_results = df.copy()
    columns = _get_formatted_column_names_export(sdg_list)
    df_results[text_column] = df_results[text_column].apply(_to_string_or_empty)

    df_results[columns] = df_results[text_column].progress_apply(
        lambda x: _row_search(x, sdg_list)
    )

    return df_results


def dataframe_search_target(
    df: pd.DataFrame, 
    sdg_nr: int, 
    target: str, 
    text_column: str,
    countries: dict[str:bool] = False
) -> pd.DataFrame:
    """Takes a dataframe and searches for a sdg target on a text column. Adds the result as a column and returns the dataframe. 

    Args:
        df: a dataframe containing texts to perform SDG search on
        sdg_nr: the SDG to perform the search on
        target: the target to search for
        text_column: the name of the column in the df containing the text to tag. Default is 'result_title'

    Returns:
        a dataframe with the results of the sdg target search and the countries and pre-searches
    """
    df_results = df.copy()
    columns = _get_formatted_column_names_one_target(sdg_nr, target)
    df_results[text_column] = df_results[text_column].apply(_to_string_or_empty)
    
    df_results[columns] = df_results[text_column].progress_apply(
        lambda x: _row_search_one_target(x, sdg_nr, target, countries)
    )

    return df_results