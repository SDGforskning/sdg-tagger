from .helpers import (
    get_sdg_phrases,
    search_for_phrase_unindexed,
    search_phrases_in_sdg_target_indexed,
    run_all_targets_in_goal_search,
)
from .consts import LIST_ALL_SDG_NR, COUNTRIES


def run_goal_mentions_search(mentions_search: dict, input_text: str) -> bool:
    """Run the mentions search for an sdg

    Args:
        mentions_search: a dictionary with the logic rule and the termlists to search
        input_text: the text to search in

    Returns:
        A boolean for the mentions search result
    """
    mentions_result = search_for_phrase_unindexed(
        mentions_search['termlists'], 
        input_text, 
        mentions_search['logic_rule']
    )

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
) -> dict[str:bool]:
    """Triggers all country category searches for a text

    Args:
        input_text: The text to search in

    Returns:
        A dictionary with the results for each country category and for each termlist in the country categories
    """
    results = {}
    for search in pre_searches:
        results[search['name']] = search_for_phrase_unindexed(
                search['termlists'], 
                input_text,
                search['logic_rule'],
                )

    return results


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
        

def search_all_targets_in_goal(
    sdg_nr: int,
    input_text: str,
    countries: dict[str, bool],    
    get_indexes: bool = False,
) -> tuple[dict[str, bool], dict[str, dict]]:
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
    results = {}
    results["sdg_number"] = sdg_nr

    pre_searches, sdg_all_targets, mentions_search = get_sdg_phrases(sdg_nr)
    
    pre_search_result = run_pre_searches(pre_searches, input_text)
    results["pre_search"] = pre_search_result

    results["targets"], indexes = run_all_targets_in_goal_search(sdg_all_targets, input_text, countries, pre_search_result)

    results["mentions"] = run_goal_mentions_search(mentions_search, input_text)

    return results, indexes


def search_in_text_for_one_sdg(
        sdg_nr: int,
        input_text: str,
        get_indexes: bool = False, 
    ) -> tuple[dict[str, bool], dict[str, dict]]:
    """_summary_

    Args:
        sdg_nr: _description_
        input_text: _description_
        get_indexes: _description_. Defaults to False.

    Returns:
        _description_
    """
    countries = run_all_country_searches(input_text)
    results, indexes = search_all_targets_in_goal(
        sdg_nr,
        input_text,
        countries,    
        get_indexes
    )
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

