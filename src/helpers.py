import re
import os
import json

from .format_helpers import prepare_regex_search_termlist, format_logic_rules


####################### File helpers #######################
def get_sdg_phrases(sdg_number: int) -> tuple[list[dict], list[dict], dict]:
    """Get the search phrases for a specific SDG from the json files

    Args:
        sdg_number: the number of the SDG to get the phrases for

    Returns:
        List of the presearches for the sdg, each a dictionary with the phrases' termlists and logic rule
        A list with dictionaries of all the phrases' termlists and logic rule for each of the SDG targets
        A dict for the mentrions search, containing a logic rule and termlists
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


####################### search helpers for boolean/unindexed search #######################
def _pattern_search_boolean(regex_search: str, text: str) -> bool:
    """search for regex pattern in a text.

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
        countries_results: dict[str:bool] = None,
        pre_search_results: dict[str:bool] = None,
    ) -> bool:
    """Finds the result of a phrases logic rule given all the termlist results

    Args:
        all_search_results: all the boolean results for the searches performed for each phrase
        search_phrases: dictionary containing all data for all the phrases

    Returns:
        the boolean result for the search
    """
    logic_rule_formatted = format_logic_rules(logic_rule_raw, termlist_results, countries_results, pre_search_results)
    boolean_result = eval(logic_rule_formatted)
    return boolean_result


def _are_terms_in_input_text(
        termlists: list[dict], 
        input_text: str, 
    ) -> dict[str, bool]:
    """Search through a list of termlists

    Args:
        termlists: all the term lists used in the logic rule
        input_text: the text to search in
        logic_rule_raw: the logic rule to evaluate on

    Returns:
        The result of the search on the input text for each of the termlists
    """
    termlist_results = {}
    for term_list in termlists:
        regex_term_list, formatted_text = prepare_regex_search_termlist(term_list, input_text)
        termlist_results[term_list['termlist_name']] = _pattern_search_boolean(regex_term_list, formatted_text)
        
    return termlist_results


def search_for_phrase_unindexed(
        termlists: list[dict], 
        input_text: str, 
        logic_rule_raw: str, 
        countries_results: dict[str:bool] = None,
        pre_search_results: dict[str:bool] = None,
    ) -> bool:
    """Search all the termlists in a phrase and checks the logic rule

    Args:
        termlists: all the term lists used in the logic rule
        input_text: the text to search in
        logic_rule_raw: the logic rule to evaluate on

    Returns:
        bool: the result of the search on the input text
    """
    termlist_results = _are_terms_in_input_text(termlists, input_text)
        
    return _is_logic_rule_true(termlist_results, logic_rule_raw, countries_results, pre_search_results)


def run_all_targets_in_goal_search(
        sdg_all_targets: dict,
        input_text: str,
        countries_result: dict,
        pre_search_result: dict,
        get_indexes: bool = False
    ):
    """_summary_

    Args:
        sdg_all_targets: _description_
        input_text: _description_
        countries_result: _description_
        pre_search_result: _description_
        get_indexes: _description_. Defaults to False.

    Returns:
        _description_
    """
    results = {}
    indexes = {}
    for target in sdg_all_targets:
        phrases_results = run_all_termlist_searches_in_phrase_bool(
                    target['phrases'],
                    input_text,
                    'number',
                    countries_results=countries_result,
                    pre_search_results=pre_search_result,
                )

        if get_indexes:
            index_search = search_phrases_in_sdg_target_indexed(
                input_text, target, indexed=True
            )
            indexes[target['name']] = index_search
        
        results[target['name']] = phrases_results 
    return results, indexes


def run_all_termlist_searches_in_phrase_bool(
    search_phrases: list[dict], 
    input_text: str, 
    name_key: str, 
    countries_results: dict[str:bool] = None,
    pre_search_results: dict[str:bool] = None,
) -> dict[str : dict[str:bool]]:
    """Perform a boolean search for all phrases in a dictionary of phrases on a given text

    Args:
        search_phrases: all the searches to perform
        input_text: the text to search in
        name_key: name of the key in a phrase dict indicating the name or number of the phrase
        indexed: whether to include indexed search or not

    Returns:
        the results of all the searches
    """
    all_search_results = {}

    for search_phrase in search_phrases:
        logic_rule_raw = search_phrase['logic_rule']
        name = search_phrase[name_key]
        
        sentence_split = False
        if 'sentence_split' in search_phrase.keys():
            if search_phrase['sentence_split'] == 'True':
                sentence_split = True

        if sentence_split:   
            sentences = input_text.split(". ")
            phrase_sentence_results = []
            for sentence in sentences: 
                sentence_result = search_for_phrase_unindexed(
                    search_phrase['termlists'], 
                    sentence, 
                    logic_rule_raw,
                    countries_results, 
                    pre_search_results
                    )
                phrase_sentence_results.append(sentence_result)
            all_search_results[name] = any(phrase_sentence_results)
        
        else: 
            all_search_results[name] = search_for_phrase_unindexed(
                search_phrase['termlists'], 
                input_text, 
                logic_rule_raw,
                countries_results, 
                pre_search_results
            )

    return all_search_results


################### Search helpers for indexed search ######################################
def _pattern_search_indexed(regex_search: str, text: str) -> list[dict]:
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


def search_phrases_in_sdg_target_indexed(
    input_text: str, 
    sdg_target_phrases: list[dict], 
    key_name: str,
    countries_results: dict[str:bool] = None,
    pre_search_results: dict[str:bool] = None,
) -> dict[int, dict]:
    """Search for all phrases in a target for a text

    Args:
        input_text: the text to search in
        sdg_target_phrases: phrases with the logic rules to evaluate
        indexed: wether to include indexed results or not

    Returns:
        the results for all termlist searches in each phrase
    """
    all_results = {}

    for phrase in sdg_target_phrases:
        logic_rule_raw = phrase['logic_rule']
        phrase_results = {}
        name = phrase[key_name]

        sentence_split = False
        if 'sentence_split' in phrase.keys():
            if phrase['sentence_split'] == 'True':
                sentence_split = True

        if sentence_split:   
            sentences = input_text.split(". ")
            phrase_sentence_results = []
            for sentence in sentences: 
                termlist_results = {}
                #TODO do it indexed!
                sentence_result = search_for_phrase_unindexed(
                    phrase['termlists'], 
                    sentence, 
                    logic_rule_raw,
                    countries_results, 
                    pre_search_results
                    )
                #TODO something like this: (både her og når det ikke er sentence_split)
                for term_list in phrase['term_lists']:
                    regex_term_list, formatted_text = prepare_regex_search_termlist(term_list, input_text)
                    termlist_results[term_list['termlist_name']] = _pattern_search_indexed(regex_term_list, formatted_text)
        
                phrase_sentence_results.append(sentence_result)
            all_results[name] = any(phrase_sentence_results)
        
        else: 
            #TODO do it indexed!
            all_results[name] = search_for_phrase_unindexed(
                phrase['termlists'], 
                input_text, 
                logic_rule_raw,
                countries_results, 
                pre_search_results
            )

        all_results[name] = phrase_results

    return all_results
