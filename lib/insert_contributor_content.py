"""
This script generates markdown from the user-contributed YAML file,
enriched with data from the GitHub API, and inserts it into the readme.
Python 3.6+ is required

Environment Variables (all optional)
    - LOG_LEVEL: The log level to use: info | warn | error (default: INFO).
    - GH_ACCESS_TOKEN: The GitHub API token used for authentication.
    - REPO_OWNER: The username / org where the repository is located.
    - REPO_NAME: The name of the repository.
"""

# Imports
import os
import yaml
import json
import requests
import logging
import time
from typing import Dict, List, Union, Optional
from requests.exceptions import RequestException

# Constants
""" The username / org where the repository is located """
REPO_OWNER = os.environ.get("REPO_OWNER", "lissy93")
""" The name of the repository """
REPO_NAME = os.environ.get("REPO_NAME", "git-into-open-source")
""" A GitHub access token, required for higher rate-limit when fetching data """
GH_ACCESS_TOKEN = os.environ.get("GH_ACCESS_TOKEN", None)
""" Used for users who don't have a GitHub profile picture """
PLACEHOLDER_PROFILE_PICTURE = "https://i.ibb.co/X231Rq8/octo-no-one.png"
""" The directory where this script is located """
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
""" The relative path to the markdown file to update"""
README_PATH = os.path.join(SCRIPT_DIR, "..", ".github/README.md")
""" The relative path to the YAML file containing the user-contributed content """
CONTRIBUTORS_FILE_PATH = os.path.join(SCRIPT_DIR, "..", "git-in-here.yml")
""" Need to use a cache file to avoid hitting the rate limit """
CACHE_FILE = os.path.join(SCRIPT_DIR, "cache.json")


def read_cache() -> dict:
    """
    Read cached GitHub data from the local file.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}


def write_cache(cache: dict) -> None:
    """
    Write GitHub data to cache file.
    """
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)


def handle_rate_limit(response) -> None:
    if response.status_code == 429 or response.status_code == 403:
        try:
            reset_time = int(response.headers.get('X-RateLimit-Reset'))
        except ValueError:
            logger.error("Rate limit likely exceeded, but no reset time provided.")
            return
        sleep_duration = reset_time - int(time.time()) + 1
        if sleep_duration > 30:
            logger.warning(f"Rate limit exceeded - quota will reset in {sleep_duration} seconds. "
                           "Skipping, as this is too long to wait.")
        else:
            logger.info(f"Sleeping for {sleep_duration} seconds")
            time.sleep(sleep_duration)

# Configure Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def read_file(file_path: str, mode: str = "r") -> str:
    """
    Opens, reads and returns the contents of a given file.
    :param file_path: The path to the file.
    :param mode: The mode to open the file in.
    :return: The contents of the file.
    """
    try:
        with open(file_path, mode) as f:
            logger.info(f"Reading file: {file_path}")
            return f.read()
    except FileNotFoundError:
        logger.error(f"Error: File {file_path} not found.")
        exit(1)


def write_file(file_path: str, content: str, mode: str = "w") -> None:
    """
    Opens a given file and writes the given content to it.
    :param file_path: The path to the file.
    :param content: The content to write to the file.
    :param mode: The mode to open the file in.
    """
    with open(file_path, mode) as f:
        logging.info(f"Writing to file: {file_path}")
        f.write(content)


def get_profile_picture(username: str) -> str:
    """
    Returns either the URL to a users profile, or a placeholder image.
    :param username: The username of the GitHub user.
    :return: The URL of the profile picture of the GitHub user.
    """
    url_to_check = f"https://github.com/{username}.png"
    response = requests.get(url_to_check)
    if response.status_code == 200:
        return url_to_check
    return PLACEHOLDER_PROFILE_PICTURE


def fetch_github_info(username: str) -> Dict[str, Union[str, None]]:
    """
    Fetches the name and avatar URL of a GitHub user.
    :param username: The username of the GitHub user.
    :return: A dictionary containing the name and avatar URL of the GitHub user.
    """
    logging.info(f"Fetching GitHub info for user: {username}")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GH_ACCESS_TOKEN:
        headers["Authorization"] = f"token {GH_ACCESS_TOKEN}"

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    handle_rate_limit(response)
    if response.status_code != 200:
        logger.error(f"GitHub API returned status code {response.status_code} for user {username}.")
        return { "name": username, "avatar_url": get_profile_picture(username) }
    logger.info(f"Successfully fetched GitHub info for user: {username}")
    return response.json()
    

def map_question_to_heading(question: str) -> str:
    """
    Maps the question to a heading that will be displayed in the README.
    :param question: The question to map.
    :return: The mapped question.
    """
    question_mappings = {
        "What's your 'Aha!' moment with open source?": "My 'Aha!' moment in open source was:",
        "What's the coolest open source project you've ever used or contributed to?": "The coolest open source project I've ever used or contributed to is:",
        "What advice would you give to someone new to open source?": "The advice I would give to someone new to open source is:",
    }
    return question_mappings.get(question, question)


def fetch_all_stargazers(
    repo_owner: str, repo_name: str, access_token: Optional[str] = None
) -> List[str]:
    """
    Fetches all stargazers of a given GitHub repository.
    :param repo_owner: The owner of the repository.
    :param repo_name: The name of the repository.
    :param access_token: An optional access token to authenticate with the GitHub API.
    :return: A list of all stargazers of the repository.
    """
    logging.info("Fetching all stargazers of the repository")
    stargazers: List[str] = []
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/stargazers"
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
    return stargazers


def format_url(url: str) -> str:
    """
    Makes URLs to users blogs and twitter profiles look nicer.
    Removes www., http://, https:// and trailing slashes from a URL.
    Also limits to 25 characters and replaces with ellipse if longer
    """
    url = url.replace("www.", "").replace("http://", "").replace("https://", "")
    url = url.rstrip("/")
    return url[:25] + (url[25:] and "...")


def build_markdown_content(
    contributors: List[Dict[str, str]], stargazers: List[str]
) -> str:
    """
    Use the content returned from the YAML + complimentary data (like stargazers),
    to build the markdown content that will be inserted into the README.
    :param contributors: The list of contributors from the YAML file.
    :param stargazers: The list of stargazers of the repository.
    :return: The markdown content to be inserted into the README.
    """

    if not contributors:
        logger.info(f"No contributors found yet, cancelling markdown generation")
        return ""

    md_content = "User | Contribution\n---|---\n"
    for contributor in reversed(contributors):
        username = contributor["username"]
        question = contributor["question"]
        response = contributor["response"]
        question_heading = map_question_to_heading(question)
        info = fetch_github_info(username)
        name = info["name"] if info["name"] else username
        picture = info.get("avatar_url", PLACEHOLDER_PROFILE_PICTURE)
        is_stargazer = "⭐ " if username.lower() in [sg.lower() for sg in stargazers] else ""
        blog = f"<br /><sup>🌐 [{format_url(info['blog'])}]({info['blog']})</sup>" if info.get("blog") else ""
        bio = info["bio"] if info.get("bio") else ""

        if info.get("public_repos") and info.get("followers") and info.get("following"):
            stats = (
                f"<br /><kbd>👣 {info['following']} ┃ "
                f"🫂 {info['followers']} ┃ "
                f"🗃 {info['public_repos']}</kbd>"
            )
        else:
            stats = ""
        
        if info.get("twitter_username") and not blog:
            twitter = (
                f"<br /><sup>🐦 [@{format_url(info['twitter_username'])}]"
                "(https://x.com/{info['twitter_username']})</sup>"
            )
        else:
            twitter = ""

        # Put it all together!
        md_content += (
            f"<a href='https://github.com/{username}' title='{bio}'>{name}{is_stargazer}<br />"
            f"<img src='{picture}' width='80' /></a> {stats} {blog} {twitter} | "
            f"**{question_heading}**<br />{response}\n"
        )
        time.sleep(0.5) # Reduce rate-limiting from GitHub API
    return md_content



""" The main entrypoint of the script """
if __name__ == "__main__":
    # Fetch list of stargazers (to insert special emoji next to name)
    all_stargazers = fetch_all_stargazers(REPO_OWNER, REPO_NAME, GH_ACCESS_TOKEN)
    # Read YAML
    yaml_content = yaml.safe_load(read_file(CONTRIBUTORS_FILE_PATH))
    # Read current README
    readme_content = read_file(README_PATH)
    # Generate content to be inserted
    new_md_content = build_markdown_content(
        yaml_content["contributors"], all_stargazers
    )
    # Locate and replace content in README
    start_marker = "<!-- git-in-start -->"
    end_marker = "<!-- git-in-end -->"
    start_index = readme_content.find(start_marker) + len(start_marker)
    end_index = readme_content.find(end_marker)
    # Create new readme (from old readme + new content)
    new_readme_content = (
        readme_content[:start_index]
        + "\n"
        + new_md_content
        + readme_content[end_index:]
    )
    # Write readme content back to file
    write_file(README_PATH, new_readme_content)
    logging.info("All Done!")

"""
Okay, you've got this far...
As you can tell this is a pretty quickly-put-together and hacky script
And there's definitely plenty of room for improvement! 
So if you're up for it, feel free to submit a PR :)
"""
