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

2. Create a copy of the "template" file for your SDG (ctrl+c then ctrl+v). Rename it to `sdgx.json`, where 'x' is the number of the SDG. You will edit the new file (sdgx.json) you have just created by copying (not the original template). All the template files have the correct number of goals for that SDG, and the same number of phrases (but you will need to add more termlists, each phrase only has one in the template).
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
8. Go back to step 3 if you wish to edit anything, and repeat 3-7 as necessary.
9. Once finished and happy with your SDG, open a pull request. You can also open a _draft pull request_ **as soon as** you have made the first change on your branch - the advantage of this is that you can use the pull request to document any substantial changes you make (see example here: https://github.com/SDGforskning/sdg-tagger/pull/45). When opening the pull request, change the default option (main) so that you compare it with the source branch:
<img width="800" height="150" alt="image" src="https://github.com/user-attachments/assets/e2360184-1eda-47cc-bb82-abaf89c1704e" />
<img width="400" height="50" alt="image" src="https://github.com/user-attachments/assets/10eb21b9-5d52-4446-99f4-42a3fe4de186" />



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
How the termlist should be truncated. This recreates how we did it in python (stopping right truncation, all truncation, or allowing all (default)). **The names for these that should be used can be found in the formats.json** file. This must be filled out or you will get an error. 

```
"formatting_rule": "default",
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

This determines whether the search (logic_rule) should be carried out _within a sentence_ (=true), or within the whole text (=false). Default = false, but in most cases we likely want to change this to **true** as we want this to work for project descriptions and abstracts.

For example, in SDG1.1, this is set to false - there is only one term list, so it can be anywhere (no AND operator). This could also be the case for AND or especially NOT searches where we don't need the terms to be near each other. But in SDG1.4 phrase 1 it is set to true - we want it to find "access" and "banking" used close to each other to increase the chances of it being about access to banking services. 

Note: We may come across mixed cases: for example, we want to find results about access to banking in LMICs. Here it might have been optimal to have a solution where we could search for "access" and "banking" within the same sentence, but allow that the LMIC comes in another sentence - however, right now, we do not have this functionality. See https://github.com/SDGforskning/sdg-tagger/issues/18

#### pre_search<a name="presearch"></a>
If you want to reuse a termlist across phrases, or in many targets - consider adding it as a _pre_search_. This can be referred to in all _logic_rules_ within that SDG. Example - see SDG 2.

Our "rule": Make a pre-search if a termlist is used in more than two phrases (i.e. has to be copied more than twice). If a term-list is only used in two phrases, copy it. **When re-using a termlist or when making a pre-search, add a comment listing the targets and phrases where it is used.**


## Functions for testing in demo.ipynb<a name="testing"></a>


