"""
This file contains helper functions for the core functionality of the src. 
This includes text formatting, file reading etc.
Used by both countries_search and sdg_search
"""
import re
import os
import json

from .consts import ADDITIONAL_LANGUAGES

####################### Format helpers #######################
def replacer_function(match_object: re.Match, result_termlist_search: dict) -> str:
    """Replace [] and all the content with {} and the dictionary lookup string for dynamically inserting the results for each term search later on

    Args:
        match_object: 

    Returns:
        the string formatted to be able to take in a dictionary lookup value
    """
    termlist_name = match_object.group()[1:-1]
    return result_termlist_search[termlist_name]


def format_logic_rules(logic_rule_raw:str, result_termlist_search: dict) -> str:
    """ Takes the raw logic rules as is written in the json files and converts them to a python-formatable format. 

    Args: 
        logic_rule_raw: the unformatted logic rule as it is written in the json files

    Returns:
        Logic rule that is ready to be used in the eval function. 
    """
    pattern = r"\[[^\[\]]*\]"
    logic_rule_formatted = re.sub(pattern, lambda x: str(result_termlist_search[x.group()[1:-1]]), logic_rule_raw)
    logic_rule_formatted = logic_rule_formatted.replace('|',' or ').replace('&',' and ')
    logic_rule_formatted = logic_rule_formatted.replace('  ', ' ')

    return logic_rule_formatted


####################### File helpers #######################
def read_json_to_dict(file_path: str) -> dict:
    """ Opens a json file and returns the content as a dictionary

    Args:
        file_path: path to the json file

    Returns:
        A dictionary with the content of the json file
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data


def get_sdg_phrases(sdg_number: int) -> list[dict]:
    """ Get the search phrases for a specific SDG from the json files

    Args:
        sdg_number: the number of the SDG to get the phrases for

    Returns:
        A list with dictionaries containing all the phrases and the logic rule for each of the SDG goals
    """
    file_path = os.path.join(os.path.dirname(__file__), 'phrases/sdg{}.json'.format(str(sdg_number)))
    data = read_json_to_dict(file_path)
    return data["goals"]


def get_countries_phrases() -> list[dict]:
    """ Get the search phrases for the country searches, which are later used in some of the sdg searches
    
    Returns:
        A list with dictionaries containing all the term lists and the logic rule for each country search set
    """
    file_path = os.path.join(os.path.dirname(__file__), 'phrases/countries.json')
    data = read_json_to_dict(file_path)
    return data['phrases']


####################### Search helpers #######################
def get_string_formats() -> dict:
    """ Get the different string formatting patterns that are used for searching in terms lists. 

    Returns:
        a dictionary with the name of the patterns as key and the regex patterns as values
    """
    file_path = os.path.join(os.path.dirname(__file__), 'phrases/formats.json')
    return read_json_to_dict(file_path)


def get_additional_language_terms(term_lists:dict[list[str]]) -> list[str]:
    """ Check which other languages to add and adds terms for those languages. 
    
    Args:
        term_lists: a list of term lists, one for each available language
    
    Returns:
        a list of all terms of the additional languages
    """
    terms = []
    for language in ADDITIONAL_LANGUAGES.keys():
        if ADDITIONAL_LANGUAGES[language] is True:
            terms += term_lists[f'wordlist_{language}']

    return terms


def pattern_search_boolean(pattern:str, search_terms:list[str], text:str) -> bool:
    """ Formats the terms lists into the given reqex pattern and outputs the result of the boolean search.

    Args:
        pattern: regex pattern to use when searching
        search_terms: terms to search for
        text: the text to search in

    Returns:
        boolean for whether the text contained the search terms
    """
    pattern_with_terms = pattern.format('|'.join(search_terms))
    return bool(re.search(rf'{pattern_with_terms}', text))


def pattern_search_indexed(pattern:str, search_terms:list[str], text:str) -> list[dict]:
    """ Finds where in the text the search terms exists so we can use it for evaluation and highlighting later on

    Args:

    Returns:
        a list of all matches contaiting a dict of the matched text along with its start and end index in the text

    """
    pattern_with_terms = pattern.format('|'.join(search_terms))
    matches = re.finditer(rf'{pattern_with_terms}', text)

    matches_with_indices = []
    for match in matches:
        matches_with_indices.append({'matched_text':match.group(0), 'start_index':match.start(), 'end_index':match.end()})

    return matches_with_indices


def search_termlist(regex_patterns:str, term_lists:dict[str, list[str]], input_text:str, indexed:bool=False) -> bool|dict:
    """

    Args:
        regex_patterns: regex pattern to use when searching
        term_lists: terms to search for
        text: the text to search in
        indexed: 

    Returns:

    """
    pattern = str(regex_patterns[term_lists['formatting_rule']])
    terms = term_lists['wordlist_en'] 
    if any(ADDITIONAL_LANGUAGES.values()):
        terms += get_additional_language_terms(term_lists)

    if term_lists['case']=='False':
        text = input_text.lower()
        terms = [term.lower() for term in terms]
    else: text = input_text

    if indexed:
        return pattern_search_indexed(pattern, terms, text)
    return pattern_search_boolean(pattern, terms, text)

