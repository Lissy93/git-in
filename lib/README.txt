The lib directory contains scripts used for repo management, and executed by GitHub Actions

Pre-requisites
--------------
1. Ensure you've got Python (V 3.6+) installed on your system
2. Clone the repository, and cd into it
3. Install the dependencies: `pip install -r lib/requirements.txt`
4. Run a script, with `python lib/[name of script].py`

Scripts
-------
- insert_contributor_content.py - Parses and inserts content from git-in-here.yml into the README.md file

Documentation
-------------
See the header of each script for more information on what it does, requirements and how to use it

Testing
-------
Run `python -m unittest lib/tests/run_all_tests.py`

Parameters
----------
There are some optional environmental variables that can be set before running some scripts
- REPO_OWNER - The username / org where the repository is located (e.g. lissy93)
- REPO_NAME - The name of the repository (e.g. git-into-open-source)
- GH_ACCESS_TOKEN - A GitHub access token, required for higher rate-limit when fetching data
