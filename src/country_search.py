'''
Country category searches for sdg-tagger
'''
from .helpers import (
    get_countries_phrases, 
    get_phrase_boolean_result,
    search_phrase_bool
)


def all_country_searches(input_text:str) -> dict[str:dict[str:bool]] | dict[str: bool]:
    """Triggers all country category searches for a given text

    Args:
        input_text: The text to search in

    Returns:
        A dictionary (json) with the results for each country category and for each termlist in the country categories
    """
    country_search_phrases = get_countries_phrases()

    all_search_results = search_phrase_bool(country_search_phrases, input_text)
    boolean_results = get_phrase_boolean_result(all_search_results, country_search_phrases)

    return all_search_results, boolean_results
