import pandas as pd
import numpy as np

from .consts import LIST_ALL_SDG_NR, COUNTRIES
from .sdg_search import search_all_goals
from .helpers import get_sdg_phrases


def format_df_value(value:bool, sdg_nr:str, target:str) -> str:
    """ Format the value to be 'SDG' + the sdg nr in two digits + underscore + the target number in two digits or in one digit if it is a character

    Args:
        value: True or False
        sdg_nr: SDG number to be in the return string
        target: the target number or character for the return string

    Returns
        the formatted string, or nan id the result was False
    """
    if value==False:
        return np.nan
    else:
        nr_formatted = f'{int(sdg_nr):02d}'
        return f'SDG{nr_formatted}_{format_item(target)}'


def format_results(result: dict, sdg_list:list[int]) -> list[str]:
    """ Formats the sdg search result json into a list of values

    Args:
        result: the json result from the sdg search 'search_all_goals' function
        sdg_list: A list of SDGs to get the columns for

    Returns:
        a list of formatted values of the search results
    """
    countries = [val for _,val in result['countries'].items()]
    sdgs = []

    for sdg_nr in [str(sdg) for sdg in sdg_list if sdg in set(LIST_ALL_SDG_NR)]:
        sdg_result = []
        if 'pre_search' in result[sdg_nr]:  
            pre_searches = [val for _,val in result[sdg_nr]['pre_search'].items()]
            sdg_result.extend(pre_searches)
        sdg_result.extend([format_df_value(any(val.values()),sdg_nr, key) for key, val in result[sdg_nr]['targets'].items()])
        if 'mentions' in result[sdg_nr]:  
            sdg_result.append(result[sdg_nr]['mentions'])
        sdgs.extend(sdg_result)

    return countries + sdgs


def format_item(item:str) -> str:
    """Formats a single-digit number (0-9) with a leading zero. Leaves other inputs (letters, multi-digit numbers) as they are.

    Args:
        item: the letter or digit(as a string) to be formatted

    Returns:
        Formatted string
    """
    try:
        if item[0]=='0':
            num = int(item[1:])
            return f"{num:02d}"
        else:
            num = int(item)
            return f"{num:02d}"
    
    except ValueError:
        return str(item)
    

def row_search(text:str, sdg_list:list[int]) -> pd.Series:
    """ Performs search for all sdgs for a given text and returns is as a pandas series (aka a row in a pandas dataframe)

    Args:
        text: the text to be labelled
        sdg_list: A list of SDGs to do the search on

    Returns:
        The results of the SDG search as a Pandas series
    """
    results_raw = search_all_goals(text, sdg_list)
    results_formatted = format_results(results_raw, sdg_list)
    return pd.Series(results_formatted)


def get_formatted_column_names_export(sdg_list:list[int]) -> list[str]:
    """Based on which sdgs and country searches are implemented, get a list of columns to populate with the search results.

    Args:
        sdg_list: A list of SDGs to get the columns for

    Returns:
        A list of column names based on which SDG searches exist in the json files.
    """
    columns = []
    columns.extend([x['name'] for x in COUNTRIES])

    for sdg_nr in [sdg for sdg in sdg_list if sdg in set(LIST_ALL_SDG_NR)]:
        pre_searches, sdg_all_targets = get_sdg_phrases(sdg_nr)
        columns.extend([x['name'] for x in pre_searches])
        nr_formatted = f'{sdg_nr:02d}'

        for target in sdg_all_targets:
            target_formatted = format_item(target['name'])
            columns.append(f'tempsdg{nr_formatted}_{target_formatted}')
        
        #TODO column names for mentions! (for sdgs that got it in the json?)

    return columns


def dataframe_search(df: pd.DataFrame, sdg_list:list[int]=LIST_ALL_SDG_NR, text_column:str='result_title'):
    """Replicating the original script that took a dataframe with titles and performed searches for all sdgs for each row
    
    Args:
        df: a dataframe containing texts to perform SDG search on. 
        sdg_list: list of SDGs to perform the search on. Default is all SDGs.
        text_column: the name of the column in the df containing the text to tag. Default is 'result_title'
    
    Returns:
        a dataframe with the results of all SDG searches
    """
    df_results = df.copy()
    columns = get_formatted_column_names_export(sdg_list)

    df_results[columns] = df_results[text_column].apply(lambda x: row_search(x, sdg_list))

    return df_results

