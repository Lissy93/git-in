"""
Reads list of resources from the resources.yml
Then inserts a link to each into the README.md
"""

import os
import yaml
import logging
from urllib.parse import urlparse

# Configure Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# Determine the project root based on the script's location
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resources_file_path = os.path.join(project_root, 'resources.yml')
guides_directory = os.path.join(project_root, 'guides')
readme_path = os.path.join(project_root, '.github/README.md')
icon_size=20

logger.info("Reading the resources.yml file...")
# Read the resources.yml
with open(resources_file_path, 'r') as file:
    data = yaml.safe_load(file)

# Check which guide files exist and prepare their markdown links
guide_links = []

for guide in data.get("guides", []):
    guide_file_path = os.path.join(guides_directory, f"{guide['file']}.md")
    if os.path.exists(guide_file_path):
        iconParams = f"?height={icon_size}&color=%23{guide.get('color', '00BBF9')}"
        icon = f'<img width="{icon_size}" src="https://api.iconify.design/{guide.get("icon")}.svg{iconParams}" />' if guide.get("icon") else ""
        guide_links.append(f"- {icon} [{guide['title']}](/guides/{guide['file']}.md)")
        logger.info(f"Guide file found and link prepared: {guide_file_path}")
    else:
        logger.warning(f"Guide file not found: {guide_file_path}")

# Prepare markdown links for external resources
logger.info("Preparing external resource links...")
resource_links = []
for resource in data.get("resources", []):
    resource_host = urlparse(resource['url']).hostname
    icon_tag = f"<img src='https://icon.horse/icon/{resource_host}' width='{icon_size}' />"
    resource_links.append(f"- {icon_tag} [{resource['title']}]({resource['url']})")

logger.info("Preparing to insert project links...")
project_links = []
for project in data.get("projects", []):
    project_links.append(f"- [{project.get('title', project['repo'])}]({project['repo']})")

# Update the README.md between markers
logger.info("Reading README.md file...")
with open(readme_path, 'r') as file:
    readme_content = file.read()

def update_content_between_markers(content, start_marker, end_marker, new_content):
    logger.info(f"Updating content between {start_marker} and {end_marker} markers...")
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index != -1 and end_index != -1:
        before_section = content[:start_index + len(start_marker)]
        after_section = content[end_index:]
        updated_content = before_section + '\n' + '\n'.join(new_content) + '\n' + after_section
        return updated_content
    else:
        logger.error(f"Markers {start_marker} and {end_marker} not found.")
        return content

# Update guides and resources in README.md
readme_content = update_content_between_markers(readme_content, "<!-- guides-start -->", "<!-- guides-end -->", guide_links)
readme_content = update_content_between_markers(readme_content, "<!-- resources-start -->", "<!-- resources-end -->", resource_links)
readme_content = update_content_between_markers(readme_content, "<!-- projects-start -->", "<!-- projects-end -->", project_links)

# Write back the updated content to README.md
logger.info("Writing back to README.md...")
with open(readme_path, 'w') as file:
    file.write(readme_content)

logger.info("Script completed successfully!")
