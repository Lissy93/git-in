"""
Assortment of checks run against new PRs, when git-in-here.yml is appended to
The script formats results into markdown, and posts as a comment on the PR
It checks:
- The YAML is still valid and parsable
- The users username matches submission
- A valid question was selected
- The response was appended to the end of the list
- The length of the response is within recommended bounds
- PR template has not been deleted
- PR type has been filled in
- PR checklist has been completed
- The user has starred the repo
"""

# Dependency imports
import os
import yaml
import json
import requests
import logging
from typing import Dict, List, Union, Optional
from requests.exceptions import RequestException

# Constants
""" The username / org where the repository is located """
REPO_OWNER = os.environ.get("REPO_OWNER", "lissy93")
""" The name of the repository """
REPO_NAME = os.environ.get("REPO_NAME", "git-into-open-source")
""" A GitHub access token, required for higher rate-limit when fetching data """
GH_ACCESS_TOKEN = os.environ.get("GH_ACCESS_TOKEN", None)
""" The directory where this script is located """
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
""" The relative path to the YAML file containing the user-contributed content """
CONTRIBUTORS_FILE_PATH = os.path.join(SCRIPT_DIR, "..", "git-in-here.yml")

# Configure Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def read_yaml_data(file_path: str) -> Union[Dict, List]:
    """
    Reads and returns the content of a YAML file.
    :param file_path: The path to the YAML file.
    :return: Parsed content of the YAML file.
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        logger.error(f"Error reading or parsing {file_path}.")
        return {}

def check_valid_yaml() -> bool:
    """
    Checks if a given file contains valid YAML.
    :param file_path: The path to the file to check.
    :return: Boolean indicating whether the file contains valid YAML.
    """
    try:
        logger.info(f"Checking if git-in-here is still valid YAML")
        with open(CONTRIBUTORS_FILE_PATH, "r") as f:
            yaml.safe_load(f)
        return True
    except yaml.YAMLError:
        logger.error(f"Error: git-in-here does not contain valid YAML.")
        return False


def username_matches_submission(username: str, data: Union[Dict, List]) -> bool:
    """
    Checks if the username provided matches the user's submission in the YAML file.
    :param username: The username of the contributor.
    :return: Boolean indicating whether the provided username matches the submission.
    """
    logger.info(f"Checking if {username} is included in the submission")
    contributors = data.get('contributors', [])
    for contributor in contributors:
        if contributor.get('username', '').lower() == username.lower():
            logger.info(f"Found {username}")
            return True
    return False
    

def has_appended_to_end(username: str, data: Union[Dict, List]) -> bool:
    """
    Checks if the user has appended their contribution to the end of the contributors array.
    :param username: The username of the contributor.
    :return: Boolean indicating whether the contribution is at the end of the array.
    """
    logger.info(f"Checking if {username} has appended their contribution to the end of the array")
    contributors = data.get('contributors', [])
    return contributors[-1].get('username', '').lower() == username.lower()


def question_is_valid(username: str, data: Union[Dict, List]) -> bool:
    """
    Checks if the question for the given username exists in the YAML questions list.
    :param username: The username of the contributor.
    :return: Boolean indicating whether the question is valid.
    """
    logger.info(f"Checking if {username} has answered a valid question")
    questions = {k: v for k, v in data.items() if k.startswith('Q')}
    for contributor in data.get('contributors', []):
        if contributor['username'].lower() == username.lower():
            question_ref = contributor.get('question', '')
            return question_ref in questions.values()
    return False # If the user is not in the contributors list


def check_if_stargazer(username) -> bool:
    """
    Checks if a given user has starred the repository.
    :param user: The username to check.
    :return: Boolean indicating whether the user has starred the repo.
    """
    logging.info("Fetching all stargazers of the repository")
    stargazers: List[str] = []
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/stargazers"
    headers = {"Accept": "application/vnd.github.v3+json"}

    def get_next_url(headers: dict) -> Optional[str]:
        links = headers.get("Link", "").split(",")
        for link in links:
            if 'rel="next"' in link:
                return link.split(";")[0].replace("<", "").replace(">", "").strip()
        return None

    if GH_ACCESS_TOKEN:
        headers["Authorization"] = f"token {GH_ACCESS_TOKEN}"

    while url:
        try:
            res = requests.get(url, headers=headers, params={"per_page": 100})
            if res.status_code == 200:
                stargazers += [user["login"] for user in res.json()]
                url = get_next_url(res.headers)
            else:
                break
        except RequestException:
            break
    return True if username.lower() in [sg.lower() for sg in stargazers] else False


def response_length_is_valid(username: str, data: Union[Dict, List]) -> bool:
    """
    Checks if the response for the given username is between 64 and 512 characters.
    :param username: The username of the contributor.
    :return: Boolean indicating whether the response length is within bounds.
    """
    logger.info(f"Checking if {username} has a valid response length")
    for contributor in data.get('contributors', []):
        if contributor['username'].lower() == username.lower():
            response = contributor.get('response', '').strip()
            return 64 <= len(response) <= 512
    return False  # Return False if username is not found

def make_final_comment(user: str, errors: []) -> str:
    result = ""
    if user:
        result += f"Hello @{user}! 👋\n\n"
    result += f"Thanks for contributing to {REPO_NAME}! 🎉\n"
    if errors:
        result += "\n\nIn the meantime, I've spotted a few possible issues for you to address:\n"
        result += '\n'.join(errors)
        result += (
            "\n\nPlease ensure you've read and followed the "
            "[Contributing Guidelines](https://github.com/Lissy93/git-into-open-source/blob/main/.github/CONTRIBUTING.md#guidelines)"
        )
    else:
        result += "\n\nAll automated checks have passed, a human will review your PR soon :)"

    result += (
        "\n\n<sup>🤖 I'm a bot, and this message was automated. "
        "Follow me for updates.</sup>"
    )
    return result

def run_checks(user, contributor_data, pr_body):
    errors = []

    if not user:
        # If we don't have a user associated with the PR, we can't continue
        logger.error("Error: GITHUB_ACTOR environment variable not set.")
        return []

    if not check_if_stargazer(user):
        errors.append(
            "- Consider dropping this repo a star."
        )

    if not check_valid_yaml():
        errors.append(
            "- It looks like there is a syntax error in git-in-here.yml. "
            "You'll need to fix that before your PR can be reviewed. "
            "Using a [YAML Validator](https://appdevtools.com/yaml-validator) might help."
        )
        # We return early here, because can't continue if the YAML is invalid
        return errors
    
    if not username_matches_submission(user, contributor_data):
        errors.append(
            "- I couldn't find your response, ensure that your `username` matches your GitHub username."
        )
        # If we don't have the users response, we can't continue
        return errors

    if not question_is_valid(user, contributor_data):
        errors.append(
            "- Please ensure that the question you've answered is in the list."
        )

    if not has_appended_to_end(user, contributor_data):
        errors.append(
            "- Please append your contribution to the end of the `contributors` list. "
            "Do not add it to the top or in between other entries."
        )

    if not response_length_is_valid(user, contributor_data):
        errors.append(
            "- Ideally, the length of your response should be between 64 and 512 characters."
        )

    if not pr_body:
        # Skipping future checks, as don't have PR body
        logger.info("Skipping PR checks, as no PR body passed")
        return errors
    
    if len(pr_body) < 200:
        errors.append("- The PR body seems to be missing some content. Please make sure you didn't delete the PR template.")
        # If PR body is so short, no point checking for the rest...
        return errors
    
    if '___' in pr_body:
        errors.append("- Please specify the PR type (and delete the `___` placeholder).")
    
    if not any(box_checked in pr_body for box_checked in ['[x]', '[X]']):
        errors.append("- Please ensure you've checked the boxes in the PR template (use `[x]`).")

    return errors


def get_pr_body(pr_number: int) -> Optional[str]:
    """
    Fetch the body of the PR using the GitHub API.
    """
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GH_ACCESS_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("body")
        else:
            logger.error(f"Failed to fetch PR body for PR #{pr_number}.")
            return None
    except RequestException:
        logger.error(f"Request error while fetching PR body for PR #{pr_number}.")
        return None


def get_pr_number_from_event() -> Optional[int]:
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        return None
    with open(event_path, 'r') as f:
        event = json.load(f)
        return event.get("number")
    

def post_comment_to_pr(pr_number: int, comment_body: str) -> bool:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GH_ACCESS_TOKEN}"
    }
    data = {"body": comment_body}
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 201
    except RequestException:
        return False


def main():
    
    # Double check we've got the access token
    if not GH_ACCESS_TOKEN:
        logger.error("The GH_ACCESS_TOKEN environment variable not set.")
        return

    # Get the PR number for this request
    pr_number = get_pr_number_from_event()
    if not pr_number:
        logger.error("Could not get PR number from GitHub event.")

    # Get the body of the pull request (the description completed by user)
    pr_body = get_pr_body(pr_number) if pr_number else None

    # Get the username of the user who submitted the PR
    user = os.getenv('GITHUB_ACTOR')

    # Read the YAML data
    contributor_data = read_yaml_data(CONTRIBUTORS_FILE_PATH)

    # Run the checks
    errors = run_checks(user, contributor_data, pr_body)
    
    # Generate the markdown comment
    markdown = make_final_comment(user, errors)

    # Post the comment to the PR
    if not post_comment_to_pr(pr_number, markdown):
        logger.error(f"Failed to post comment to PR #{pr_number}.")


if __name__ == "__main__":
    main()
