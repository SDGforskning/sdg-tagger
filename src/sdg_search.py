from .helpers import (
    format_logic_rules, 
    get_string_formats, 
    get_sdg_phrases,
    search_termlist_bool
)

from .country_search import all_country_searches

def search_phrases_in_sdg_target(
        input_text: str, 
        sdg_target_phrases: list[dict], 
        regex_patterns: dict, 
        indexed: bool
    ) -> dict:
    """

    Args:

    Returns:

    """
    target_results = {}

    for phrase in sdg_target_phrases:
        phrase_results = {}
        number = phrase['number']

        if phrase['sentence_split']=='True':
            sentences = input_text.split(". ")

            for term_lists in phrase['termlists']:
                sentence_results = []
                for sentence in sentences:
                    sentence_results.append(search_termlist_bool(
                        regex_patterns=regex_patterns, 
                        term_lists=term_lists, 
                        input_text=sentence,
                    ))
                phrase_results[term_lists['termlist_name']] = any(sentence_results)

        else:
            for term_lists in phrase['termlists']:
                phrase_results[term_lists['termlist_name']] = search_termlist_bool(
                    regex_patterns=regex_patterns, 
                    term_lists=term_lists, 
                    input_text=input_text,
                )
        
        target_results[number] = phrase_results

    return target_results


def get_logic_rule_raw(goal_phrases, target_nr):
    """
    """
    for phrase in goal_phrases:
        if phrase["number"] == target_nr:
            return phrase['logic_rule']

def goal_pre_search(input_text):
    return (None, None)

def search_all_targets_in_goal(sdg_nr: int, input_text:str, analyze_result:bool=False) -> dict[str:bool]| dict[str:dict] :
    """

    Args:
        sdg_nr: The number of sdg to perform a search for
        input_text: The text to perform the search on
        analyze_text: boolean for whether to run an extra search that returns the indexes of words found for all search terms. 

    Returns:
        The results in boolean for each target of the sdg
        The indexed results for all search terms in each target of the sdg. 
        NOTE: The indexed result is per termlist, and will also include terms that are matched in a termlist even if the logic rule gives False as a whole
    """
    regex_patterns = get_string_formats()
    sdg_all_targets = get_sdg_phrases(sdg_nr)

    results = {}
    indexes = {}
    results["sdg_number"] = sdg_nr

    _ , countries = all_country_searches(input_text)
    _ , pre_search = goal_pre_search(input_text)

    for target in sdg_all_targets:
        target_phrases = target['phrases']
        
        result_termlist_search = search_phrases_in_sdg_target(
            input_text=input_text, 
            sdg_target_phrases=target_phrases, 
            regex_patterns=regex_patterns, 
            indexed=False
            )

        phrase_results = {}
        for phrase_nr in result_termlist_search.keys():
            phrase = result_termlist_search[phrase_nr]
            logic_rule_raw = get_logic_rule_raw(target_phrases, phrase_nr)
            logic_rule_formatted = format_logic_rules(
                logic_rule_raw, 
                phrase,
                countries,
                pre_search
                )
            phrase_results[phrase_nr] = eval(logic_rule_formatted) 
        
        results[target['name']] = phrase_results

        if analyze_result:
            index_search = search_phrases_in_sdg_target(input_text, target_phrases, regex_patterns, indexed=True)
            indexes[target['name']] = index_search
    
    return results, indexes



# Replicating the original script that took a dataframe with titles and performed searches for all sdgs for each row
def dataframe_search_all():

    return
