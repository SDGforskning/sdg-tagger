from typing import Any

from .helpers import (
    get_sdg_phrases,
    search_for_phrase_unindexed,
    run_all_targets_in_goal_search,
)
from .consts import LIST_ALL_SDG_NR, COUNTRIES


def run_goal_mentions_search(mentions_search: dict, input_text: str) -> bool:
    """Run the mentions search for an sdg on a text

    Args:
        mentions_search: a dictionary with the logic rule and the termlists to search
        input_text: the text to search in

    Returns:
        A boolean for the mentions search result
    """
    mentions_result = search_for_phrase_unindexed(
        mentions_search['termlists'], input_text, mentions_search['logic_rule']
    )

    return mentions_result


def run_all_country_searches(
    input_text: str,
) -> dict[str, bool]:
    """Triggers all country category searches for a text

    Args:
        input_text: The text to search in

    Returns:
        A dictionary with the results for each country category
    """
    results = {}
    for country_search in COUNTRIES:
        results[country_search['name']] = search_for_phrase_unindexed(
            country_search['termlists'],
            input_text,
            country_search['logic_rule'],
        )

    return results


def run_pre_searches(
    pre_searches: list[dict],
    input_text: str,
) -> dict[str, bool]:
    """Triggers all country category searches for a text

    Args:
        pre_searches: the phrases for all the presearches to run
        input_text: The text to search in

    Returns:
        A dictionary with the results for each pre search
    """
    results = {}
    for search in pre_searches:
        results[search['name']] = search_for_phrase_unindexed(
            search['termlists'],
            input_text,
            search['logic_rule'],
        )

    return results


def search_all_targets_in_goal(
    sdg_nr: int,
    input_text: str,
    countries: dict[str, bool],
    target: str = '',
) -> dict[str, Any]:
    """Perform search on all targets in a goal for a given text

    NOTE: The indexed result is per termlist, and will also include terms that are matched in a termlist even if the logic rule gives False as a whole

    Args:
        sdg_nr: The number of sdg to perform a search for
        input_text: The text to perform the search on
        countries: result of country searches (optional)

    Returns:
        The results in boolean for each target of the sdg
    """
    results: dict[str, Any] = {}
    results['sdg_number'] = sdg_nr

    pre_searches, sdg_all_targets, mentions_search = get_sdg_phrases(sdg_nr)

    pre_search_result = run_pre_searches(pre_searches, input_text)
    results['pre_search'] = pre_search_result

    if target.strip():
        for t in sdg_all_targets:
            if t['name'] == target.strip():
                targets_to_search = [t]
    else:
        targets_to_search = sdg_all_targets

    results['targets'] = run_all_targets_in_goal_search(
        targets_to_search, input_text, countries, pre_search_result
    )

    if not target.strip():
        results['mentions'] = run_goal_mentions_search(mentions_search, input_text)

    return results


def search_in_text_for_one_sdg(
    sdg_nr: int,
    input_text: str,
) -> dict[str, Any]:
    """performs the search for one sdg on one text

    Args:
        sdg_nr: the SDG to search for
        input_text: the text to search in

    Returns:
        the results for the sdg search, pre-search, targets and mentions
    """
    countries = run_all_country_searches(input_text)
    results = search_all_targets_in_goal(sdg_nr, input_text, countries)
    return results


def search_all_goals(
    text: str, sdg_list: list[int] = LIST_ALL_SDG_NR
) -> dict[str, dict[str, Any]]:
    """Search for all the goals in a text

    Args:
        text: the text to perform the search on
        sdg_list: list of sdgs to search for, defaults to the const list of all SDGs

    Returns:
        the results for country search and the SDG search results
    """
    results: dict[str, Any] = {}

    countries = run_all_country_searches(text)
    results['countries'] = countries

    for sdg in [sdg for sdg in sdg_list if sdg in set(LIST_ALL_SDG_NR)]:
        sdg_result = search_all_targets_in_goal(sdg, text, countries=countries)
        results[str(sdg)] = sdg_result

    return results


def search_target(
    text: str, sdg_nr: int, target: str, countries_results: dict[str: bool] = False
) -> dict[str, dict[str, Any]]:
    """Search for all the goals in a text

    Args:
        text: the text to perform the search on
        sdg_list: list of sdgs to search for, defaults to the const list of all SDGs
        target:
        countries_results: 

    Returns:
        the results for country search and the SDG search results
    """
    results: dict[str, Any] = {}

    if not countries_results: 
        countries = run_all_country_searches(text)
    else: 
        countries = countries_results
    
    results['countries'] = countries

    sdg_result = search_all_targets_in_goal(sdg_nr, text, countries=countries, target=target)
    results[str(sdg_nr)] = sdg_result

    return results

