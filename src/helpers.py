'''
Helper functions for the core functionality of sdg-tagger. 
This includes text formatting, file reading etc.
Used by both countries_search and sdg_search
'''
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


def get_logic_rule_raw_countries_and_presearch(all_phrases:dict, search_name:str) -> str:
    """Looks throug all phrases until it finds the one matching the search_name, then returns the logic rule for that phrase

    Args:
        all_phrases: Dictionary containing all data for all the phrases
        search_name: The name of the phrase to find the logic rule for

    Returns:
        A string with the logic rule for the phrase matching the given search name
    """
    for phrase in all_phrases:
        if phrase['name'] == search_name:
            return phrase['logic_rule']
        

def format_logic_rules(
        logic_rule_raw:str, 
        result_termlist_search: dict[str: bool], 
        countries: dict[str: bool] = None, 
        pre_search: dict[str: bool] = None
    ) -> str:
    """ Takes the raw logic rules as is written in the json files and converts them to a python-formatable format. 

    Args: 
        logic_rule_raw: the unformatted logic rule as it is written in the json files

    Returns:
        Logic rule that is ready to be used in the eval function. 
    """
    all_logic_results = result_termlist_search

    if countries:
        for key in countries.keys():
            all_logic_results[key] = countries[key]

    if pre_search:
        for key in pre_search.keys():
            all_logic_results[key] = pre_search[key]

    def replacer_function(x):
        try:
            boolean_result = str(all_logic_results[x.group()[1:-1]])
            return boolean_result
        except KeyError:
            message = f'''WARNING: The search result for {x.group()[1:-1]} was not found. Make sure the logic rule only reference termlists within the same phrase, pre-searches withing the same file, or coutry searches.'''
            print(f'\033[1;31m{message}\033[0m')
            raise

    pattern = r"\[[^\[\]]*\]"
    logic_rule_formatted = re.sub(pattern, lambda x: replacer_function(x), logic_rule_raw)
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


def get_sdg_phrases(sdg_number: int) -> list[dict] | list[dict]:
    """ Get the search phrases for a specific SDG from the json files

    Args:
        sdg_number: the number of the SDG to get the phrases for

    Returns:
        A list with dictionaries containing all the phrases and the logic rule for each of the SDG goals
    """
    file_path = os.path.join(os.path.dirname(__file__), 'searchterms/sdg{}.json'.format(str(sdg_number)))
    data = read_json_to_dict(file_path)
    targets = data['targets']

    if 'pre-search' in data:
        return data['pre-search'], targets
    else: 
        return [], targets
    
    #TODO this has to also return mentions! 


def get_countries_phrases() -> list[dict]:
    """ Get the search phrases for the country searches, which are later used in some of the sdg searches
    
    Returns:
        A list with dictionaries containing all the term lists and the logic rule for each country search set
    """
    file_path = os.path.join(os.path.dirname(__file__), 'searchterms/countries.json')
    data = read_json_to_dict(file_path)
    return data['phrases']


####################### Search helpers #######################
def get_string_formats() -> dict:
    """ Get the different string formatting patterns that are used for searching in terms lists. 

    Returns:
        a dictionary with the name of the patterns as key and the regex patterns as values
    """
    file_path = os.path.join(os.path.dirname(__file__), 'searchterms/formats.json')
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

def search_phrase_bool(search_phrases, input_text):
    """
    """
    regex_patterns = get_string_formats()
    all_search_results = {}

    for search_phrase in search_phrases:
        phrase_results = {}
        name = search_phrase['name']

        for term_lists in search_phrase['termlists']:
            phrase_results[term_lists['termlist_name']] = search_termlist_bool(
                regex_patterns, 
                term_lists, 
                input_text
                )
        
        all_search_results[name] = phrase_results

    return all_search_results

def get_phrase_boolean_result(all_search_results, search_phrases):
    boolean_results = {}

    for search in all_search_results.keys():
        phrase = all_search_results[search]
        logic_rule_raw = get_logic_rule_raw_countries_and_presearch(search_phrases, search)
        logic_rule_formatted = format_logic_rules(logic_rule_raw, phrase)
        boolean_results[search] = eval(logic_rule_formatted) 

    return boolean_results
    

def run_goal_pre_search(search_phrases: list[dict], input_text:str) -> dict[str, bool]:
    """    
    """
    all_search_results = search_phrase_bool(search_phrases, input_text)
    boolean_results = get_phrase_boolean_result(all_search_results, search_phrases)
    return all_search_results, boolean_results


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


def search_termlist_bool(
        regex_patterns:str, 
        term_lists:dict[str, list[str]], 
        input_text:str
    ) -> bool|dict:
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

    return pattern_search_boolean(pattern, terms, text)


def search_termlist_indexed(
        regex_patterns:str, 
        term_lists:dict[str, list[str]], 
        input_text:str
    ) -> bool|dict:
    """

    Args:
        regex_patterns: regex pattern to use when searching
        term_lists: terms to search for
        text: the text to search in

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

    return pattern_search_indexed(pattern, terms, text)
