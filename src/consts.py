import os
import json

COUNTRIES_FILE_PATH = 'searchterms/countries.json'
FORMATS_FILE_PATH = 'searchterms/formats.json'

def _read_file(file_path: str) -> dict:
    """Opens a json file and returns the content as a dictionary"""
    file_path_absolute = os.path.join(os.path.dirname(__file__), file_path)
    with open(file_path_absolute, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

COUNTRIES = _read_file(COUNTRIES_FILE_PATH)['phrases']
REGEX_PATTERNS = _read_file(FORMATS_FILE_PATH)

LIST_ALL_SDG_NR = [1, 2, 3, 4, 7, 10, 11, 12, 13, 14, 15]
ADDITIONAL_LANGUAGES = {
    'no':True
}
