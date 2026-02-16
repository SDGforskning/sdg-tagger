from .helpers import (
    format_logic_rules,
    get_sdg_phrases,
    search_termlist,
    run_all_termlist_searches_in_phrase_bool,
    get_boolean_result_for_phrase,
)
from .consts import LIST_ALL_SDG_NR, COUNTRIES


def run_goal_pre_search(search_phrases: list[dict], input_text: str) -> dict[str, bool]:
    """Run all the the given pre-searches on a text

    Args:
        search_phrases: all the searches to perform
        input_text: The text to search in

    Returns:
        The boolean result for each pre-search
    """
    all_search_results = run_all_termlist_searches_in_phrase_bool(
        search_phrases, input_text
    )
    boolean_results = get_boolean_result_for_phrase(all_search_results, search_phrases)
    return boolean_results


def run_goal_mentions_search(mentions_search: dict, input_text: str) -> bool:
    """Run the mentions search for an sdg

    Args:
        mentions_search: a dictionary with the logic rule and the termlists to search
        input_text: the text to search in

    Returns:
        A boolean for the mentions search result
    """
    termlists_results = {}
    for term_lists in mentions_search['termlists']:
        termlists_results[term_lists['termlist_name']] = search_termlist(
            term_lists, input_text, indexed=False
        )

    logic_rule_formatted = format_logic_rules(mentions_search['logic_rule'], termlists_results)
    mentions_result = eval(logic_rule_formatted)

    return mentions_result


def run_all_country_searches(
    input_text: str,
) -> dict[str:bool]:
    """Triggers all country category searches for a text

    Args:
        input_text: The text to search in

    Returns:
        A dictionary with the results for each country category and for each termlist in the country categories
    """
    all_search_results = run_all_termlist_searches_in_phrase_bool(COUNTRIES, input_text)
    boolean_results = get_boolean_result_for_phrase(all_search_results, COUNTRIES)

    return boolean_results


def get_logic_rule_raw(goal_phrases: dict[str, dict], phrase_nr: str) -> str:
    """Get the logic rules of an SDG target for one specific phrase

    Args:
        goal_phrases: the whole phrases dict for an sdg target
        phrase_nr: the phrase to get the logic rule for

    Returns:
        the raw logic rule of a search phrase
    """
    for phrase in goal_phrases:
        if phrase["number"] == phrase_nr:
            return phrase['logic_rule']


def search_phrases_in_sdg_target(
    input_text: str, sdg_target_phrases: list[dict], indexed: bool
) -> dict[int, dict]:
    """Search for all phrases in a target for a text

    Args:
        input_text: the text to search in
        sdg_target_phrases: phrases with the logic rules to evaluate
        indexed: wether to include indexed results or not

    Returns:
        the results for all termlist searches in each phrase
    """
    target_results = {}

    for phrase in sdg_target_phrases:
        phrase_results = {}
        number = phrase['number']

        if phrase['sentence_split'] == 'True':
            sentences = input_text.split(". ")

            for term_lists in phrase['termlists']:
                sentence_results = []
                for sentence in sentences:
                    sentence_results.append(
                        search_termlist(term_lists, sentence, indexed)
                    )
                phrase_results[term_lists['termlist_name']] = any(sentence_results)

        else:
            for term_lists in phrase['termlists']:
                phrase_results[term_lists['termlist_name']] = search_termlist(
                    term_lists, input_text, indexed
                )

        target_results[number] = phrase_results

    return target_results


def get_phrase_results(
    result_termlist_search: dict[str, dict[str, dict]],
    target_phrases: dict[str, dict],
    countries: dict[str, bool],
    pre_search: dict[str, bool],
) -> dict[str, bool]:
    """Iterates through the phrases and finds the bool results of the logic rules

    Args:
        result_termlist_search: the results of the termlist searches for all the phrases to evaluate
        target_phrases: phrases with the logic rules to evaluate
        countries: result of country searches
        pre_search: result of pre-searches

    Returns:
        The boolean results of each of the phrases
    """
    phrase_results = {}

    for phrase_nr in result_termlist_search.keys():
        phrase = result_termlist_search[phrase_nr]
        logic_rule_raw = get_logic_rule_raw(target_phrases, phrase_nr)
        logic_rule_formatted = format_logic_rules(
            logic_rule_raw, phrase, countries, pre_search
        )
        phrase_results[phrase_nr] = eval(logic_rule_formatted)

    return phrase_results


def search_all_targets_in_goal(
    sdg_nr: int,
    input_text: str,
    analyze_result: bool = False,
    countries: dict[str, bool] = None,
) -> dict[str, bool] | dict[str, dict]:
    """Perform search on all targets in a goal for a given text

    NOTE: The indexed result is per termlist, and will also include terms that are matched in a termlist even if the logic rule gives False as a whole

    Args:
        sdg_nr: The number of sdg to perform a search for
        input_text: The text to perform the search on
        analyze_text: boolean for whether to run an extra search that returns the indexes of words found for all search terms.
        countries: result of country searches (optional)

    Returns:
        The results in boolean for each target of the sdg
        The indexed results for all search terms in each target of the sdg.
    """
    pre_searches, sdg_all_targets, mentions_search = get_sdg_phrases(sdg_nr)

    results = {}
    indexes = {}
    results["sdg_number"] = sdg_nr
    if not countries:
        countries = run_all_country_searches(input_text)
        results["countries"] = countries
    
    pre_search_result = run_goal_pre_search(pre_searches, input_text)
    results["pre_search"] = pre_search_result

    target_results = {}

    for target in sdg_all_targets:
        target_phrases = target['phrases']

        result_termlist_search = search_phrases_in_sdg_target(
            input_text, target_phrases, indexed=False
        )

        target_results[target['name']] = get_phrase_results(
            result_termlist_search, target_phrases, countries, pre_search_result
        )

        if analyze_result:
            index_search = search_phrases_in_sdg_target(
                input_text, target_phrases, indexed=True
            )
            indexes[target['name']] = index_search

    results["targets"] = target_results

    results["mentions"] = run_goal_mentions_search(mentions_search, input_text)

    return results, indexes


def search_all_goals(text: str, sdg_list: list[int] = LIST_ALL_SDG_NR) -> dict:
    """Search for all the goals in a text

    Args:
        text: The text to perform the search on
        sdg_list: list of sdgs to search for

    Returns:
        a dictionary with the results for country search and the SDG search results
    """
    results = {}

    countries = run_all_country_searches(text)
    results["countries"] = countries

    for sdg in [str(sdg) for sdg in sdg_list if sdg in set(LIST_ALL_SDG_NR)]:
        sdg_result, _ = search_all_targets_in_goal(sdg, text, countries=countries)
        results[sdg] = sdg_result

    return results
