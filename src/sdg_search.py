from .helpers import (
    format_logic_rules, 
    get_sdg_phrases,
    search_termlist, 
    run_goal_pre_search,
)
from .consts import LIST_ALL_SDG_NR
from .country_search import all_country_searches



def get_logic_rule_raw(goal_phrases, target_nr):
    """ Get all the logic rules of an SDG for one specific target

    Args:

    Returns: 

    """
    for phrase in goal_phrases:
        if phrase["number"] == target_nr:
            return phrase['logic_rule']
        

def search_phrases_in_sdg_target(
        input_text: str, 
        sdg_target_phrases: list[dict], 
        indexed: bool
    ) -> dict:
    """_summary_

    Args:
        input_text: _description_
        sdg_target_phrases: _description_
        indexed: _description_

    Returns:
        dict: _description_
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
                    sentence_results.append(search_termlist(term_lists, sentence, indexed))
                phrase_results[term_lists['termlist_name']] = any(sentence_results)

        else:
            for term_lists in phrase['termlists']:
                phrase_results[term_lists['termlist_name']] = search_termlist(term_lists, input_text, indexed)
        
        target_results[number] = phrase_results

    return target_results


def search_all_targets_in_goal(sdg_nr: int, input_text:str, analyze_result:bool=False, countries:dict=None) -> dict[str:bool]| dict[str:dict] :
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
    pre_searches, sdg_all_targets = get_sdg_phrases(sdg_nr)

    results = {}
    indexes = {}
    results["sdg_number"] = sdg_nr
    if not countries:
        _ , countries = all_country_searches(input_text)
        results["countries"] = countries
    _ , pre_search = run_goal_pre_search(pre_searches, input_text)

    results["pre_search"] = pre_search

    target_results = {}

    for target in sdg_all_targets:
        target_phrases = target['phrases']
        
        result_termlist_search = search_phrases_in_sdg_target(
            input_text, 
            target_phrases, 
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
        
        target_results[target['name']] = phrase_results

        if analyze_result:
            index_search = search_phrases_in_sdg_target(input_text, target_phrases, indexed=True)
            indexes[target['name']] = index_search
    
    results["targets"] = target_results
    
    return results, indexes


def search_all_goals(text:str, sdg_list:list[int]=LIST_ALL_SDG_NR) -> dict:
    """ Search all the goals. 

    Args:
        text: The text to perform the search on
    
    Returns:
        a dictionary with the results for country search and all the SDGs
    """
    results = {}

    _ , countries = all_country_searches(text)
    results["countries"] = countries

    for sdg in [str(sdg) for sdg in sdg_list if sdg in set(LIST_ALL_SDG_NR)]:
        sdg_result, _ = search_all_targets_in_goal(sdg, text, countries=countries)
        results[sdg] = sdg_result

    return results

