import re
import os
import json
from typing import Any

from .format_helpers import prepare_regex_search_termlist, format_logic_rules


####################### File helpers #######################
def get_sdg_phrases(sdg_number: int) -> tuple[list[dict], list[dict], dict]:
    """Get the search phrases for a specific SDG from the json files

    Args:
        sdg_number: the number of the SDG to get the phrases for

    Returns:
        List of the presearches for the sdg, each a dictionary with the phrases' termlists and logic rule
        A list with dictionaries of all the phrases' termlists and logic rule for each of the SDG targets
        A dict for the mentions search, containing a logic rule and termlists
    """
    file_path_absolute = os.path.join(
        os.path.dirname(__file__), 'searchterms/sdg{}.json'.format(str(sdg_number))
    )
    with open(file_path_absolute, 'r') as file:
        data = json.load(file)

    targets = data['targets']

    if 'pre-search' in data:
        return data['pre-search'], targets, data['mentions']
    else:
        return [], targets, data['mentions']


#################### Search helpers for boolean/unindexed search ####################
def _pattern_search_boolean(regex_search: str, text: str) -> bool:
    """Search for regex pattern in a text.

    Args:
        regex_search: formated regex pattern
        text: the text to search in

    Returns:
        boolean for whether the text contained the search terms
    """
    return bool(re.search(rf'{regex_search}', text))


def _is_logic_rule_true(
    termlist_results,
    logic_rule_raw,
    countries_results: dict[str, bool] = {},
    pre_search_results: dict[str, bool] = {},
) -> bool:
    """Finds the result of a phrases logic rule given all the termlist results

    Args:
        termlist_results: all the boolean results for each termlist
        logic_rule_raw: the logic rule to be evaluated
        countries_results: a dict with bool results for each countries search
        pre_search_results: a dict with bool results for each presearch (that might be) referenced in the search_phrase

    Returns:
        the boolean result for the search
    """
    logic_rule_formatted = format_logic_rules(
        logic_rule_raw, termlist_results, countries_results, pre_search_results
    )
    boolean_result = eval(logic_rule_formatted)
    return boolean_result


def _are_terms_in_input_text(
    termlists: list[dict],
    input_text: str,
) -> dict[str, bool]:
    """Search in a text for terms in a list of termlists

    Args:
        termlists: all the term lists used in the logic rule
        input_text: the text to search in

    Returns:
        The result of the search on the input text for each of the termlists
    """
    termlist_results = {}
    for term_list in termlists:
        regex_term_list, formatted_text = prepare_regex_search_termlist(
            term_list, input_text
        )
        if regex_term_list:
            termlist_results[term_list['termlist_name']] = _pattern_search_boolean(
                regex_term_list, formatted_text
            )
        else: termlist_results[term_list['termlist_name']] = False

    return termlist_results


def search_for_phrase_unindexed(
    termlists: list[dict],
    input_text: str,
    logic_rule_raw: str,
    countries_results: dict[str, bool] = {},
    pre_search_results: dict[str, bool] = {},
) -> bool:
    """Search all the termlists in a phrase and checks the logic rule

    Args:
        termlists: all the term lists used in the logic rule
        input_text: the text to search in
        logic_rule_raw: the logic rule to evaluate on
        countries_results: a dict with bool results for each countries search
        pre_search_results: a dict with bool results for each presearch (that might be) referenced in the search_phrase

    Returns:
        bool: the result of the search on the input text
    """
    termlist_results = _are_terms_in_input_text(termlists, input_text)

    return _is_logic_rule_true(
        termlist_results, logic_rule_raw, countries_results, pre_search_results
    )


def run_all_termlist_searches_in_list_of_phrases_bool(
    search_phrases: list[dict],
    input_text: str,
    name_key: str,
    countries_results: dict[str, bool] = {},
    pre_search_results: dict[str, bool] = {},
) -> dict[Any, bool]:
    """Perform a boolean search for all phrases in a list of phrases on a given text

    Args:
        search_phrases: all the searches to perform
        input_text: the text to search in
        name_key: name of the key in a phrase dict indicating the name or number of the phrase
        countries_results: a dict with bool results for each countries search
        pre_search_results: a dict with bool results for each presearch (that might be) referenced in the search_phrase

    Returns:
        the results of all the searches
    """
    all_search_results = {}

    for search_phrase in search_phrases:
        logic_rule_raw = search_phrase['logic_rule']
        name = str(search_phrase[name_key])

        sentence_split = False
        if 'sentence_split' in search_phrase.keys():
            if search_phrase['sentence_split'] == True:
                sentence_split = True
        
        if sentence_split:
            sentences = re.split(r'[?!.]', input_text)
            phrase_sentence_results = []
            for sentence in sentences:
                sentence_result = search_for_phrase_unindexed(
                    search_phrase['termlists'],
                    sentence,
                    logic_rule_raw,
                    countries_results,
                    pre_search_results,
                )
                phrase_sentence_results.append(sentence_result)
            all_search_results[name] = any(phrase_sentence_results)

        else:
            all_search_results[name] = search_for_phrase_unindexed(
                search_phrase['termlists'],
                input_text,
                logic_rule_raw,
                countries_results,
                pre_search_results,
            )

    return all_search_results


def run_all_targets_in_goal_search(
    sdg_all_targets: list[dict],
    input_text: str,
    countries_result: dict[str, bool],
    pre_search_result: dict[str, bool],
) -> dict[str, dict[str, bool]]:
    """Run all the phrases searches for all targets in a list

    Args:
        sdg_all_targets: all the searches to performfor each target
        input_text: the text to search in
        countries_result: a dict with bool results for each countries search
        pre_search_result: a dict with bool results for each presearch (that might be) referenced in the search_phrase

    Returns:
        the results of all the searches for each target
    """
    results = {}

    for target in sdg_all_targets:
        phrases_results = run_all_termlist_searches_in_list_of_phrases_bool(
            target['phrases'],
            input_text,
            'number',
            countries_results=countries_result,
            pre_search_results=pre_search_result,
        )
        results[target['name']] = phrases_results

    return results
