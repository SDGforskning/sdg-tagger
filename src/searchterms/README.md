# Instructions: How to work with the json files

<b>Contents:</b>
1. [Getting started](#start)
2. [SDG json file structure](#sdg)
3. [Logic rules format](#logic-rules)
4. [Testing](#testing)


## Getting started <a name="start"></a>
The template files `sdgx_template.json` are created to be a starting point when working on adding the rules to an SDG. All the template files have the correct number of goals for that SDG, and the same number of phrases/logic rules per goal as they had in the original script from the sdg-search repo. 


### To start working on a new sdg: 
- Make a copy of the template file for that SDG
- rename it to `sdgx.json`, where 'x' is the number of the sdg. 


## SDG json file structure <a name="sdg"></a>



## Logic rules format <a name="logic-rules"></a>
- The entire rule must be embraces by one parenthesis ().
- Only the operators 'not', '&', '|' are permitted. 
- All references to termlists or to pre-searches MUST be inside square brackets. Only letters, numbers and underscores are permitted within these brackets. No whitespaces. The text within each bracket MUST correspond to 
    1. the name of a termlist within the same phrase
    2. the name of a pre-search in the same file
    3. the name of a phrase in `countries.json`
- Parentesis can be nested.
- The operators 'not', '&', '|' must have at least one blank space before and after.

### Examples of valid logic rules:
    "([termlist1_ba] | [termlist1_ba_trunc]) & [termlist1_bb] | ([termlist1_bc] & ([termlist1_bd] | [termlist1_bd_trunc]))"
    
    "([termlist14_aa] & [marine])"

### Examples of invalid logic rules: 
    "[termlist1_aa]"                # missing the outer parenthesis
    "([termlist1_aa] & [marine])"   # marine pre-search does not exist in SDG1
    "([a]&[b])",                    # missing spaces around &
    "(not [x])",                    # missing space before 'not'
    "([a] |[b])",                   # missing space before[b]
    "([a]| [b])",                   # missing space after |
    "([A])",                        # capitol letters in []
    "([a b])",                      # whitespace inside []
    "([x] && [y])",                 # '&&' is not permitted
    "([x] | [y]",                   # missing the outside ')'
    "( [x] & )",                    # operator without the right expression
    "( & [x] )",                    # operator without the left expression
    "( [x]|[y] )",                  # missing spaces around |
    "( not[x] )",                   # missing space after 'not'

## Testing <a name="testing"></a>
The json files needs to be validated to ensure the correct format for this project. To do so we have a set of automatic tests written in pytest (https://docs.pytest.org/en/stable/index.html). Before committing changes to the json files, it is important to run the tests to ensure that none of them fail. Use one of the following ways to run the tests:

### Option 1:
First, make sure you have the pytest library by running `pip install pytest==8.2.2`

To run only the tests that validates all the json files, run the command `pytest -v -m 'json-format'` in your terminal. 

If you are working on the <b>logic rules</b> and only want to run the tests that checks their format, you can run `pytest -v -m 'logic_rule_format'` in your terminal.

### Option 2:
Run the file `run_pytest.ipynb`. This will execute all tests in the repository, including the json validation. 