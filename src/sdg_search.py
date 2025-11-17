import re

from .helpers import (
    format_logic_rules, 
    get_string_formats, 
    get_sdg_phrases,
    search_termlist
)
from .consts import LIST_ALL_SDG_NR


def search_terms_in_sdg_target(input_text:str, sdg_goal_phrases: list[dict], regex_patterns: dict, indexed: bool) -> dict:
    """

    Args:

    Returns:

    """
    conditions = {}

    for phrase in sdg_goal_phrases:
        phrase_results = {}
        number = phrase['number']

        if phrase['sentence_split']=='True':
            sentences = input_text.split(". ")

            for term_lists in phrase['termlists']:
                sentence_results = []
                for sentence in sentences:
                    sentence_results.append(search_termlist(regex_patterns, term_lists, sentence))

                phrase_results[term_lists['termlist_name']] = any(sentence_results)

        for term_lists in phrase['termlists']:
            phrase_results[term_lists['termlist_name']] = search_termlist(regex_patterns, term_lists, input_text, indexed)
        
        conditions[number] = phrase_results

    return conditions


def get_logic_rule_raw(goal_phrases, target_nr):
    """
    """
    for phrase in goal_phrases:
        if phrase["number"] == target_nr:
            return phrase['logic_rule']


def search_all_targets_in_goal(sdg_nr: int, input_text:str, analyze_result:bool=False) -> dict[str:bool]| dict[str:dict] :
    """

    Args:
        sdg_nr: The number of sdg to perform a search for
        input_text: The text to perform the search on
        analyze_text: boolean for whether to run an extra search that returns the indexes of words found for all search terms. 

    Returns:
        The results in boolean for each target of the sdg
        The indexed results for all search terms in each target of the sdg
    """
    regex_patterns = get_string_formats()
    sdg_all_targets = get_sdg_phrases(sdg_nr)

    results = {}
    indexes = {}

    for target in sdg_all_targets:
        goal_phrases = target['phrases']
        
        result_termlist_search = search_terms_in_sdg_target(input_text, goal_phrases, regex_patterns, False)

        phrase_results = {}
        for phrase_nr in result_termlist_search.keys():
            phrase = result_termlist_search[phrase_nr]
            logic_rule_raw = get_logic_rule_raw(goal_phrases, phrase_nr)
            logic_rule_formatted = format_logic_rules(logic_rule_raw, phrase)
            phrase_results[phrase_nr] = eval(logic_rule_formatted) 
        
        results[target['name']] = phrase_results

        if analyze_result:
            index_search = search_terms_in_sdg_target(input_text, goal_phrases, regex_patterns, indexed=True)
            indexes[target['name']] = index_search
    
    return results, indexes



# Replicating the original script that took a dataframe with titles and performed searches for all sdgs for each row
def dataframe_search_all():

    return
