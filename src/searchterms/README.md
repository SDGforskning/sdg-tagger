# sdg-tagger search terms editing - a guide

<b>Contents:</b>
1. Suggested: [Install and set up Visual Studio Code with sdg-tagger](#install)
2. [Files you will need to interact with](#files)
3. [General rules](#rules)
4. [Workflow for editing a SDGX.json file](#workflow)
5. [Building a search in a SDGX.json file - properties and fields](#building)
6. [Functions in demo for testing](#testing)

## Install and set up Visual Studio Code with sdg-tagger <a name="install"></a>

Suggested tools - clone the repository to VScode and work there. 

1. Install Visual Studio Code (perhaps from your university software manager, it is standard software from Microsoft)
2. Install Git for Windows
3. Under "source control" (on the left, symbol that looks like a branch with three circles; see picture) select "Clone repository" (= creates a local copy, which is synchronized with this repository online)

    <img width="150" height="120" alt="bilde" src="https://github.com/user-attachments/assets/9127c90d-a43e-4b31-9ce0-e978a3e2e0b0" />

4. You will be prompted to log in to github, sign in using github - do this and "authorize"
5. If it works, all our repositories should appear in VScode - select _sdg-tagger_
6. Choose where you want to save your local copy (I have been advised not to use Onedrive if possible, rather under C drive > Users > your username, or common > new folder (and call it sdg-tagger or something)
7. If prompted again, you may have to sign in again ("Authorize git ecosystem"). If you get something like "do you trust the authors of these files" (and uncheck the files in the parent folder) = Yes
8. If it works, you will see a copy of sdg-tagger in your VScode. In the file list (see this by clicking on the symbol on the left that looks like papers; see picture above) you will only see readme.md if you are on the main branch, but if you change branch (you do this by clicking at the bottom-left, where it says "main"), you see wull then see more files which are on these branches, which reflect what is available online https://github.com/SDGforskning/sdg-tagger
9. You will also need to make sure python is set up within VScode to actually run the tests and searches. 

## Files you will need to interact with: <a name="files"></a>
For converting old SDGs:
- The **SDGX.json** files (where we construct the searches) are in the folder src > phrases.
- The **run_pytest.ipynb** in the main folder (where we can test that our SDG searches are set up _technichally_ correctly)
- The **demo.ipynb** file (where we run our searches and test how they are working) is in the main folder
- You may need to refer to, but unlikely to edit, **countries.json** and **formats.json** in the folder src > phrases. countries.json are the country searches (LMIC etc.) while formats.json reminds us of the truncation rules available to us (all truncation, right truncation, no truncation, and newly, left truncation)
- You will be unlikely to need consts.py (under src) - this tells the functions which SDGs to search for (to exclude those under construction)

## General rules to remember <a name="rules"></a>
- Always work on your own branch
- Run the **run_pytest** file before trying to use the searches in **demo** or before "finishing" an SDG, to help identify technical problems that need fixing in the SDGXX.json files
- You can edit **demo** as you wish for your own use, but do not push changes github. To do this make sure that demo and run-pytest are not staged when committing, e.g.
  
  <img width="280" height="170" alt="image" src="https://github.com/user-attachments/assets/d0b553ba-17d8-4d34-ae21-da3c51628e8a" />


## Workflow for editing and testing an SDGX.json file <a name="workflow"></a>
1. Check you are on your branch (it is easiest to create a new branch online from the web version of the repository - ask which branch you should use as the source, it is likely _not_ "main" (default)). Then change to your new branch in VScode by clicking on the branch name (a tiny label in the bottom left corner), and choosing your new branch from the "remote" section of the list. As long as your branch name is in the bottom left corner, you are on your branch. 

    <img width="200" height="90" alt="bilde" src="https://github.com/user-attachments/assets/80f85927-c9d7-4d88-a144-974815341b1b" />

2. Create a copy of the "template" file for your SDG (ctrl+c then ctrl+v). Rename it to `sdgx.json`, where 'x' is the number of the SDG. You will edit the new file (sdgx.json) you have just created by copying (not the original template). All the template files have the correct number of goals for that SDG, and 2 empty phrases (you will need to add more termlists withing each phrase (and potentially phrases) by copying and pasting the relevant part of the template).
3. Edit the file. If converting an old SDG, use this file to copy from https://github.com/SDGforskning/sdg-strings/blob/main/SDGs_query_topic_python.md. For instructions on the json fields, see [Building a search in a SDGX.json file - properties and fields](#building)
4. Save often. A black dot next to the file name in the tab heading means it has unsaved changes. ctrl+s saves locally. When you do this you will see an "M" (="modified") appear next to your file name in the files overview, and a (1) appear on the source control symbol - this means git has detected that one local file has saved changes compared to the online version of the branch. At this point your changes are only saved locally. To synchronise them with GitHub, commit and push (under the source control tab). Now you can also see your changes in GitHub. I recommend doing this whenever you are leaving the work for a time. This video shows how to save, commit, synchronise (and staging) in VScode: https://www.youtube.com/watch?v=uuNbZ79SkEo (note: I would just write the commit message in the message box after staging but _before_ you click on the commit button, rather than how he did it, but no worries either way). 
> NB - The first time you try to "commit" from VScode, you may get an error that you lack your username and email (to "sign" the commit with). It wants to know your GitHub user name so it can say who has written the commit. If you get this message, follow this guide to set it up: https://www.youtube.com/watch?v=RT-1Zywrse8
5. The SDG must be complete before you test (if it has empty termlists/phrases, it will (probably?) not work in demo or pass py-tests). Once finished, run the test in **run_pytest.ipynb**. Check that it says SUCCESS for the SDG (no FAILED). Click "open as a scrollable element" at the bottom of the output to see in more detail if there are any errors. Failed means that something is not working with the JSON set up (a technical formatting error, using a termlist that hasn't been defined, etc).
6. Fix any technical errors. Tips:
- Examine the error messages to get clues where the error may lie
- `ctrl+F` will open up a Find window. Search for e.g. `"formatting_rule": ""` or `"sentence_split": false` to find places you may have forgotten to change/add values.
- Selecting a termlist name in the logic rule (left clicking on it once) will also highlight other places it occurs in the script. Look to the very right of the screen, next to the overview
- You can temporarily paste a "logic_rule" into a python script cell to view bracket matching (good for complicated rules)
7. Test your search against real results using the functions in **demo.ipynb**. Here additional errors may also become issues when trying to run a search, such as missing brackets in the SDG.json files, and if so these need to be fixed as before. For how these tests work, see [Functions in demo for testing](#testing)
8. Go back to step 3 if you wish to edit anything, and repeat 3-7 as necessary. You can open a _draft pull request_ at this stage (once you have made the first change on your branch) - and use the pull request to document any substantial changes you make, or changes that will need to be also changed in WOS (see example here: https://github.com/SDGforskning/sdg-tagger/pull/45). When opening the pull request, change the default option (main) so that you compare it with the source branch:
<img width="800" height="150" alt="image" src="https://github.com/user-attachments/assets/e2360184-1eda-47cc-bb82-abaf89c1704e" />
<img width="400" height="50" alt="image" src="https://github.com/user-attachments/assets/10eb21b9-5d52-4446-99f4-42a3fe4de186" />

9. Once finished and happy with your SDG, you can request a review on your pull request.



## Building a search in a SDGX.json file - properties and fields <a name="building"></a>

### General structure
- Each SDG has top matter, where you have _pre-search_ and the _number_ of the SDG, and then come the _targets_. 
- The _targets_ are split into _phrases_ (which correspond to the phrases in our previous python script), and under each phrase you will find the _number_ of the phrase, the _logic_rule_ it uses, the _sentence_split_ switch, and then the _termlists_.
- The _termlists_ correspond to the termlists in our previous python script. Each have a _termlist_name_, a _formatting_rule_, a _case_, and an english and norwegian _wordlist_
- At any of these levels, you can insert a comment, just like the other fields, like so: `"_comment": "This is a comment for this SDG/target/phrase/termlist",`. See SDG1, target 2, phrase 1, termlist 1_2b for an example. Comments should be prefaced by the relevant language code if they are language specific, and terms placed within single quotes, e.g. `"_comment": "NO: The term 'art' is truncated...`. 
- If you need to refer to a country list, see the informatio under _logic_rule_ below.

Example of a phrase with 4 term lists, where one has special truncation rules. **Below it is information about each field**.

<img width="932" height="872" alt="bilde" src="https://github.com/user-attachments/assets/333debd9-227b-4091-b2f4-b094649e410d" />

#### termlist: termlist_name
The name you give to a termlist. It should be unique. 
```
"termlist_name": "termlist3_1b",
```

#### termlist: wordlist_en / wordlist_no
The list of terms that should be searched for, separated by a comma, and enclosed in "". 

```
"wordlist_en": ["pregnan","post partum","postpartum","peripartum","obstetric",
    "premature deliver","preterm deliver","preterm labor","preterm labour","childbirth",
    "maternal","mothers"],
"wordlist_no": ["gravid", "svangerskap", "obstetrikk", "mødre"]
```

#### termlist: formatting_rule
How the termlist should be truncated. **The names for these that should be used can be found in the formats.json** file. This must be filled out or you will get an error. 

Note that we are currently working in two systems (issue https://github.com/SDGforskning/sdg-tagger/issues/28). Those working on old SDGs are using the old names for these rules; those working on new should use the new more intuitive names. **If in doubt, follow the rules on your branch - check the formats.json file on your branch and use the correct name from there**. 

NEW
```
    "trunc": "(?:{})",                #All allowed, e.g. cat will find category and wildcat
    "no_right_trunc": "(?:{})\\b",    #Left hand allowed, e.g. cat will find wildcat but not category
    "no_trunc": "\\b(?:{})\\b"        #None allowed, e.g. cat will find cat
    "no_left_trunc": "\\b(?:{})"      #Left hand allowed, e.g. cat will find category but not wildcat
```

OLD
```
    "default": "(?:{})",                 #All allowed, e.g. cat will find category and wildcat
    "specific": "(?:{})\\b",             #Left hand allowed, e.g. cat will find wildcat but not category
    "specific_trunc": "\\b(?:{})\\b",    #None allowed, e.g. cat will find cat
    "no_left_trunc": "\\b(?:{})"         #Left hand allowed, e.g. cat will find category but not wildcat
```

#### termlist: case
True or false. Should the search be case-sensitive? For example: 
```
{
    "termlist_name": "termlist3_3i",
    "formatting_rule": "default",
    "na": false,
    "case": true,
    "wordlist_en": ["HIV", "AIDS", "MERS", "SARS"],
    "wordlist_no": ["HIV", "AIDS", "MERS", "SARS"]
}
```

#### phrase: logic_rule
The logic_rule is how the termlists are combined in a boolean search. Refer to termlists listed under that phrase by their _termlist_name_. Examples of valid logic_rules:

```
"logic_rule": "(([termlist1_ba] & [termlist1_bb]) | ([termlist1_bc] & ([termlist1_bd] | [termlist1_bd_trunc])))"
"logic_rule": "([termlist14_aa] & [LMIC])"
```

- The entire rule must be embraces by one parenthesis ().
- Only the operators `& not` (NOT), `&` (AND), `|` (OR) are permitted. 
- All references to termlists or to pre-searches MUST be inside square brackets. Only letters, numbers and underscores are permitted within these brackets. No whitespaces. The text within each bracket MUST correspond to 
    1. the name of a termlist **within the same phrase**, (note: if you need to use a termlist from another phrase, see: [pre_search](#presearch)), or
    2. the name of a pre-search in the same file, or
    3. the name of a phrase in `countries.json` (e.g. [LMIC])
- The operators `& not`, `&` and `|` must have at least one blank space before and after.

Examples of invalid logic rules: 
```
    "[termlist1_aa]"                # missing the outer parenthesis
    "([termlist1_aa] & [marine])"   # marine pre-search does not exist in SDG1
    "([a]&[b])",                    # missing spaces around &
    "(& not [x])",                  # missing space before '& not'
    "([a] |[b])",                   # missing space before[b]
    "([a]| [b])",                   # missing space after |
    "([a b])",                      # whitespace inside []
    "([x] && [y])",                 # '&&' is not permitted
    "([x] | [y]",                   # missing the outside ')'
    "( [x] & )",                    # operator without the right expression
    "( & [x] )",                    # operator without the left expression
    "( [x]|[y] )",                  # missing spaces around |
```

#### phrase: sentence_split (true/false)

This determines whether the search (_logic_rule_) should be carried out **within a sentence** (=true), or **within the whole text** (=false). Default = false, but in most cases we likely want to change this to **true** as we want this to work for project descriptions and abstracts.

The following example will only find a result if a term from termlist14_7a and termlist14_7b occur within the same sentence.
```
"logic_rule": "([termlist14_7a] & [termlist14_7b])",
"sentence_split": true,
```

Some more real examples: in SDG1.1, this is set to false - there is only one term list, so it can be anywhere (no AND operator). This could also be the case for AND or especially NOT searches where we don't need the terms to be near each other. But in SDG1.4 phrase 1 it is set to true - we want it to find "access" and "banking" used close to each other to increase the chances of it being about access to banking services. 

Note that sentence_split only affects the termlists, not **presearches** or **country lists** - these are always searched for within the whole text. For example, the following _logic_rule_ will find items where a term from SIDS (a country list) and a term from marine_terms (a pre-search) are in different sentences to the terms from termlist14_7a and termlist14_7b, even though sentence_split = true. The terms from termlist14_7a and termlist14_7b must still occur within the same sentence to get a positive result. 

```
"logic_rule": "(([termlist14_7a] & [termlist14_7b]) & ([LDC] | [SIDS]) & [marine_terms])",
"sentence_split": true,
```

#### pre_search<a name="presearch"></a>
If you want to reuse a termlist across phrases, or in many targets - consider adding it as a _pre_search_. This can be referred to in all _logic_rules_ within that SDG. Example - see SDG 2.

Our "rule": Make a pre-search if a termlist is used in more than two phrases (i.e. has to be copied more than twice). If a term-list is only used in two phrases, copy it. **When re-using a termlist or when making a pre-search, add a comment listing the targets and phrases where it is used.**

However, there is an exception to the above "rule". Pre-searches do not obey _sentence_split_ when used in a target (see information about this under _sentence_split_). Therefore, if you need to combine terms from a termlist with terms from a pre-search WITHIN a sentence, you should duplicate it as a termlist instead so that _sentence_split_ works. 


## Functions for testing in demo.ipynb<a name="testing"></a>

The functions below appear in the order they appear in the file. However, the most useful functions for testing are: 
- Run search on one specific target on an entire dataframe (4) - good for precision
- Search for all targets in a specific goal (1) - good for identifying specific problems or why certain unexpected results are flagged
- An extra bit of code, "Extra function: Compare results before and after changes to a search", can be used to compare results of (4) before and after a change to your search

### 1. Search for all targets in a specific goal (search_all_targets_in_goal)
This function allows you to see whether a specific piece of text (that you paste in manually) would flag as SDG-related for your chosen SDG. 

- Runs against: A single text (a sentence or paragraph)
- Searches for: One SDG at once
- Output: You see for each presearch, target and phrase TRUE or FALSE, where TRUE means the text would be flagged by that phrase.

**Example use case**: You look through the results for one of your searches (e.g. after running (4)), and can't figure out why one of them is flagged target. Paste the relevant text (title/abstract) here, and you can see which target/phrase it is flagged by. You can also delete parts of the abstract and run the function again to help identify which sentence is causing the issues. 

### 2. Search all goals on one text (search_all_goals)
Does the same as _search_all_targets_in_goal_, but for all SDGs. 

- Runs against: A single text (a sentence or paragraph)
- Searches for: All SDGs that are functional and defined in consts.py
- Output: You see for each presearch, target and phrase TRUE or FALSE, where TRUE means the text would be flagged by that phrase.
- Important info: You will need to make sure your SDG is listed in consts.py for it to work on yours (`LIST_ALL_SDG_NR = [1, 2, 3, 4, 7, 13]`)

### 3. Trigger all country category searches (all_country_searches)
Not generally of use, ignore for now. 

### 4. Run search on one specific target on an entire dataframe
You run your SDG search against a dataset of real publications. It will provide a table which shows the publication data you specify, as well as (optionally) whether the item was found by the title, abstract or another specified field.

- Runs against: A dataset (csv or xlsx) of publications, where it will search within the columns you specify in _COLUMNS_. You specify how many rows you want to search (or only rows of a specific language) in box 2. 
- Searches for: One SDG and target at once
- Output: You get a table of results. This table will only contain results found by the search if you keep _INCLUDE_FALSE_VALUES = False_, but will show all publications in the dataset (even those not found by the search) if you change this to _False_. The table will include fields that you define in _EXTRA_COLUMNS_ and _VIEW_. You can save these results to excel for processing - see function nr 6. 
- Important info: The search generally runs rapidly, and can search 10000 results in about a minute. The _DO_NOT_RUN_COUNTRIES_SEARCH_ part is wise to leave as TRUE at the moment - it should be FALSE for testing targets that include a countries search (e.g. LMIC), but at the moment works far too slowly to be useful during rapid testing. 

**Example use case**: 
- Useful for checking **precision**, if you use a general dataset (for example, all Norwegian publications). You can think of this function like running the search in Web of Science and checking the results list.
- Useful for checking **recall**, if you use a SDG-specific dataset (for example, a set you know should be relevant to your SDG). It will easily show you which are found/not found by your search.

### Extra function: Compare results before and after changes to a search
Compare results before and after changes to the search. 

This code is not a neat function, but ad-hoc code that lets you save the results of a search ("4. Run search on one specific target on an entire dataframe"), change your search in the sdg.json file and save it, run (4) again, and then see which results you have gained or lost. 

- Runs against: A search already done by running function (4)
- Output: You get two tables of results - one showing the results in set 1 but not 2 (i.e. what did you have before the change, **lost**), and one showing 2 not 1 (what did you gain from the change, **gain**). 
- Important info: Requires you to follow a small workflow - this is described in the demo file. 

### 5. Run search for all sdgs on an entire dataframe
This function is similar to the previous one, but can search for multiple SDGs and targets. In the background it searches for all targets of the specified SDGs, even if you choose to only show one - it therefore takes a longer time and should not be used on large datasets. In nearly all use cases, **Run search on one specific target on an entire dataframe** should be used instead with specific datasets. 

- Runs against: A dataset (csv or xlsx) of publications, where it will search within the columns you specify in _COLUMNS_. You specify how many rows you want to search, only rows of a specific language, or **only rows previously tagged as an SDG**, in box 2. 
- Searches for: All specified SDGs and targets
- Output: You get a table of results. This table will only contain results found by the search if you keep _INCLUDE_FALSE_VALUES = False_, but will show all publications in the dataset (even those not found by the search) if you change this to _False_. The table will include fields that you define in _EXTRA_COLUMNS_ and _VIEW_.
- Important info: The search is slower, and we suggest testing 100 at once to test speed. 

**Example use case**: Useful for checking **recall** against a set of already labelled publications - this was most relevant for the group converting existing searches, where we were trying to replicate an existing resultset we have. In Box 2 you can specify to only search in publications already labelled as an SDG target by the previous search - you can then check whether your search finds all of them. 

### 6. Saving the styled results to excel
After running **Run search on one specific target on an entire dataframe**, you can run this function and it will export your output to excel. The text after _file_path =_ (by default ´'styled_output.xlsx'´) is the name it will save the excel file as - change this to a new name, if you don't want to overwrite. 
