# Helper functions for the core functionality of sdg-tagger.
# This includes text formatting, file reading etc.
# Used by both countries_search and sdg_search

import re
import os
import json

from .consts import ADDITIONAL_LANGUAGES, REGEX_PATTERNS


####################### Format helpers #######################
def get_logic_rule_raw_countries_and_presearch(
    all_phrases: dict, search_name: str
) -> str:
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


def _check_for_missing_matches(
    pattern: str, logic_rule_raw: str, all_logic_results: dict[str:bool]
) -> None:
    """Checks if any pattern matches are missing from the list of logic rule results

    This function is used to make sure that a logic rule only references termlists within the same phrase, pre-searches withing
    the same file, or country searches. If not it will throw an error, as this is not valid and the search cannot continue

    Args:
        pattern: regex-pattern to locate the names of the termlists in the logic rule
        logic_rule_raw: the unformatted version of a logic rule
        all_logic_results: a lookup for all the results of a search, which are the only valid references for a logic rule

    Raises:
        KeyError: thrown if the logic rule references a result that does not exist
    """
    matches = re.findall(pattern, logic_rule_raw)
    matches = [x[1:-1] for x in matches]
    if not set(matches) <= set(all_logic_results):

        if len(set(matches) - set(all_logic_results)) > 0:
            message = f'''WARNING: The logic rule references a seaarch that was not found! Make sure the logic rule only reference 
            termlists within the same phrase, pre-searches withing the same file, or country searches.'''
            print(f'\033[1;31m{message}\033[0m')
            raise KeyError


def format_logic_rules(
    logic_rule_raw: str,
    result_termlist_search: dict[str:bool],
    countries_results: dict[str:bool] = None,
    pre_search_results: dict[str:bool] = None,
) -> str:
    """Takes the raw logic rules as is written in the json files and inserts the results from the phrases searches which converts 
    them to a python-readable format.

    Args:
        logic_rule_raw: the unformatted logic rule as it is written in the json files
        result_termlist_search: results from all termlist searches
        countries_results: results from countries_search (optional)
        pre_search_results: results from pre-search (optional)

    Returns:
        Logic rule as a string that is ready to be used in the eval function.
    """
    all_logic_results = result_termlist_search

    if countries_results:
        for key in countries_results.keys():
            all_logic_results[key] = countries_results[key]

    if pre_search_results:
        for key in pre_search_results.keys():
            all_logic_results[key] = pre_search_results[key]

    pattern = r"\[[^\[\]]*\]"

    _check_for_missing_matches(pattern, logic_rule_raw, all_logic_results)

    logic_rule_formatted = re.sub(
        pattern, lambda x: str(all_logic_results[x.group()[1:-1]]), logic_rule_raw
    )
    logic_rule_formatted = logic_rule_formatted.replace('|', ' or ').replace(
        '&', ' and '
    )
    logic_rule_formatted = logic_rule_formatted.replace('  ', ' ')

    return logic_rule_formatted


def format_list_with_pattern(pattern: str, search_terms: list[str]):
    """Formats the terms lists into the given reqex pattern

    Args:
        pattern: regex pattern to use when searching
        search_terms: terms to search for

    Returns:
        formated regex pattern
    """
    return pattern.format('|'.join(search_terms))


####################### File helpers #######################
def get_sdg_phrases(sdg_number: int) -> list[dict] | list[dict]:
    """Get the search phrases for a specific SDG from the json files

    Args:
        sdg_number: the number of the SDG to get the phrases for

    Returns:
        A list with dictionaries containing all the phrases and the logic rule for each of the SDG goals
    """
    file_path_absolute = os.path.join(
        os.path.dirname(__file__), 'searchterms/sdg{}.json'.format(str(sdg_number))
    )
    with open(file_path_absolute, 'r') as file:
        data = json.load(file)

    targets = data['targets']

    if 'pre-search' in data:
        return data['pre-search'], targets
    else:
        return [], targets
    # TODO this has to also return mentions!


####################### Country search and pre-search helpers #######################
def run_all_termlist_searches_in_phrase_bool(
    search_phrases: dict, input_text: str
) -> dict[str : dict[str:bool]]:
    """Perform a boolean search for all phrases in a dictionary of phrases on a given text

    Args:
        search_phrases: all the searches to perform
        input_text: the text to search in

    Returns:
        the results of all the searches
    """
    all_search_results = {}

    for search_phrase in search_phrases:
        phrase_results = {}
        name = search_phrase['name']

        for term_lists in search_phrase['termlists']:

            phrase_results[term_lists['termlist_name']] = search_termlist(
                term_lists, input_text, indexed=False
            )

        all_search_results[name] = phrase_results

    return all_search_results


def get_boolean_result_for_phrase(all_search_results, search_phrases) -> dict[str:bool]:
    """Finds the result of a phrases logic rule given all the search results

    Only to be used for pre-search and countries search (since they are not dependent on other searches)

    Args:
        all_search_results: all the boolean results for the searches performed for each phrase
        search_phrases: dictionary containing all data for all the phrases

    Returns:
        the boolean results for all the searcges
    """
    boolean_results = {}

    for search in all_search_results.keys():
        phrase = all_search_results[search]
        logic_rule_raw = get_logic_rule_raw_countries_and_presearch(
            search_phrases, search
        )
        logic_rule_formatted = format_logic_rules(logic_rule_raw, phrase)
        boolean_results[search] = eval(logic_rule_formatted)

    return boolean_results


####################### Search helpers #######################
def get_additional_language_terms(term_lists: dict[list[str]]) -> list[str]:
    """Check which other languages to add and adds terms for those languages.

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


def pattern_search_boolean(regex_search: str, text: str) -> bool:
    """search for regex pattern in a text.

    Args:
        regex_search: formated regex pattern
        text: the text to search in

    Returns:
        boolean for whether the text contained the search terms
    """
    return bool(re.search(rf'{regex_search}', text))


def pattern_search_indexed(regex_search: str, text: str) -> list[dict]:
    """Find instances of words from a list in a text, including where in the text the search terms were

    Args:
        regex_search: formated regex pattern
        text: the text to search in

    Returns:
        a list of all matches contaiting a dict of the matched text along with its start and end index in the text
    """
    matches = re.finditer(rf'{regex_search}', text)

    matches_with_indices = []
    for match in matches:
        matches_with_indices.append(
            {
                'matched_text': match.group(0),
                'start_index': match.start(),
                'end_index': match.end(),
            }
        )

    return matches_with_indices


def search_termlist(
    term_lists: dict[str, list[str]],
    input_text: str,
    indexed: bool,
) -> bool | dict:
    """Check if any of a list of words exists in a text. Can also include indexes for where in the text each match is found.

    Args:
        term_lists: lists of terms to search for, in a dict with one list for each language
        text: the text to search in
        indexed: whether to include indexes of the words that are found in the texts

    Returns:
        a boolean for the search result if indexed is false, or a dictionary with boolean and a list of indexes if indexed is true
    """
    pattern = str(REGEX_PATTERNS[term_lists['formatting_rule']])
    terms = term_lists['wordlist_en']
    if any(ADDITIONAL_LANGUAGES.values()):
        terms += get_additional_language_terms(term_lists)

    if term_lists['case'] == 'False':
        text = input_text.lower()
        terms = [term.lower() for term in terms]
    else:
        text = input_text

    regex_term_list = format_list_with_pattern(pattern, terms)
    if indexed:
        return pattern_search_indexed(regex_term_list, text)
    else:
        return pattern_search_boolean(regex_term_list, text)
