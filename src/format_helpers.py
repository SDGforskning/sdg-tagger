import re

from .consts import ADDITIONAL_LANGUAGES, REGEX_PATTERNS


def _check_for_missing_matches(
    pattern: str, logic_rule_raw: str, all_logic_results: dict[str, bool]
) -> None:
    """Checks if any pattern matches are missing from the list of logic rule results

    This function is used to make sure that a logic rule only references termlists within the same phrase, pre-searches within
    the same file, or country searches. If not it will throw an error, as this is not valid and the search cannot continue

    Args:
        pattern: regex-pattern to locate the names of the termlists in the logic rule
        logic_rule_raw: the unformatted version of a logic rule
        all_logic_results: a lookup for all the results of a search, which are the only valid references for a logic rule

    Raises:
        KeyError: thrown if the logic rule references a result that does not exist
    """
    matches = re.findall(pattern, logic_rule_raw)
    matches = [x[1:-1] for x in matches]
    if not set(matches).issubset(set(all_logic_results)):
        message = f'''WARNING: The logic rule references a search that was not found! Make sure the logic rule only reference 
        termlists within the same phrase, pre-searches within the same file, or country searches.'''
        print(f'\033[1;31m{message}\033[0m')
        raise KeyError


def _format_list_with_pattern(pattern: str, search_terms: list[str]) -> str:
    """Formats the terms lists into the given reqex pattern

    Args:
        pattern: regex pattern to use when searching
        search_terms: terms to search for

    Returns:
        formated regex pattern
    """
    return pattern.format('|'.join(search_terms))


def _get_additional_language_terms(term_list: dict[str, list[str]]) -> list[str]:
    """Check which other languages to add and adds terms for those languages.

    Args:
        term_list: a list of term lists, one for each available language

    Returns:
        a list of all terms of the additional languages
    """
    terms = []
    for language in ADDITIONAL_LANGUAGES.keys():
        if ADDITIONAL_LANGUAGES[language] is True:
            if f'wordlist_{language}' in term_list.keys():
                terms += term_list[f'wordlist_{language}']
            else:
                message = f'''WARNING: The termlist {term_list['termlist_name']} does not have a list for language {language}.'''
                print(f'\033[1;31m{message}\033[0m')

    return terms


def format_logic_rules(
    logic_rule_raw: str,
    result_termlist_search: dict[str, bool],
    countries_results: dict[str, bool] = {},
    pre_search_results: dict[str, bool] = {},
) -> str:
    """Takes the raw logic rules as is written in the json files and inserts the results from the phrases searches which converts
    them to a python-readable format.

    Args:
        logic_rule_raw: the unformatted logic rule as it is written in the json files
        result_termlist_search: results from all termlist searches
        countries_results: results from countries search (optional)
        pre_search_results: results from pre-search (optional)

    Returns:
        Logic rule as a string that is ready to be used in the eval function.
    """
    all_logic_results = result_termlist_search

    if countries_results:
        for key in countries_results.keys():
            all_logic_results[key] = countries_results[key]

    if pre_search_results:
        for key in pre_search_results.keys():
            all_logic_results[key] = pre_search_results[key]

    pattern = r'\[[^\[\]]*\]'

    _check_for_missing_matches(pattern, logic_rule_raw, all_logic_results)

    logic_rule_formatted = re.sub(
        pattern, lambda x: str(all_logic_results[x.group()[1:-1]]), logic_rule_raw
    )
    logic_rule_formatted = logic_rule_formatted.replace('|', ' or ').replace(
        '&', ' and '
    )
    logic_rule_formatted = logic_rule_formatted.replace('  ', ' ')

    return logic_rule_formatted


def prepare_regex_search_termlist(
    term_lists: dict[str, list[str]],
    input_text: str,
) -> tuple[str, str]:
    """Formats the regex search for a termlist given its formatting rules, and lowers the input text if required in the termlist rules.

    Args:
        term_lists: lists of terms and the rules to use when searching
        text: the text to search in

    Returns:
        the formated regex search for the termlist, and the formated text to search in
    """
    pattern = str(REGEX_PATTERNS[term_lists['formatting_rule']])
    terms = term_lists['wordlist_en']
    if any(ADDITIONAL_LANGUAGES.values()):
        terms += _get_additional_language_terms(term_lists)

    if not term_lists['case']:
        text = input_text.lower()
        terms = [term.lower() for term in terms]
    else:
        text = input_text

    regex_term_list = _format_list_with_pattern(pattern, terms)
    return regex_term_list, text
