from .helpers import (
    get_countries_phrases, 
    get_string_formats, 
    format_logic_rules,
    search_termlist
)

def get_logic_rule_raw(all_phrases:dict, search_name:str) -> str:
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


def all_country_searches(input_text:str) -> dict[str:dict[str:bool]]:
    """Triggers all country category searches for a given text

    Args:
        input_text: The text to search in

    Returns:
        A dictionary (json) with the results for each country category and for each termlist in the country categories
    """
    country_search_phrases = get_countries_phrases()
    regex_patterns = get_string_formats()

    all_search_results = {}

    for search_phrase in country_search_phrases:
        phrase_results = {}
        name = search_phrase['name']

        for term_lists in search_phrase['termlists']:
            phrase_results[term_lists['termlist_name']] = search_termlist(regex_patterns, term_lists, input_text)
        
        all_search_results[name] = phrase_results
    
    boolean_results = {}

    for country_search in all_search_results.keys():
        phrase = all_search_results[country_search]
        logic_rule_raw = get_logic_rule_raw(country_search_phrases, country_search)
        logic_rule_formatted = format_logic_rules(logic_rule_raw, phrase)
        boolean_results[country_search] = eval(logic_rule_formatted) 
            
    return all_search_results, boolean_results