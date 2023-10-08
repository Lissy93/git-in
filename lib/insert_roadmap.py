"""
Inserts the dynamic roadmap into the readme, as a mermaid diagram.
Also adds fallback .png with pako-encoded link to mermaid.live.
"""

import os
import json
import zlib
import base64
import logging

# Configure Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# Determine the project root based on the script's location
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mermaid_file = os.path.join(project_root, 'guides/roadmap.mmd')
readme_path = os.path.join(project_root, '.github/README.md')


def js_string_to_byte(data: str) -> bytes:
    """Convert a string to bytes using ascii encoding."""
    return bytes(data, 'ascii')


def js_bytes_to_string(data: bytes) -> str:
    """Decode bytes to a string using ascii decoding."""
    return data.decode('ascii')


def js_btoa(data: bytes) -> bytes:
    """Encode bytes to base64."""
    return base64.b64encode(data)


def pako_deflate(data: bytes) -> bytes:
    """Compress the given bytes using zlib."""
    compress = zlib.compressobj(9, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data


def encode_to_pako(graphMarkdown: str) -> str:
    """Encode the graph markdown to a pako format."""
    jGraph = {
        "code": graphMarkdown,
        "mermaid": {"theme": "default"}
    }
    byteStr = js_string_to_byte(json.dumps(jGraph))
    deflated = pako_deflate(byteStr)
    dEncode = js_btoa(deflated)
    return js_bytes_to_string(dEncode)


def insert_mermaid_into_readme(mermaid_content: str) -> None:
    """Insert the mermaid content into the readme file."""
    logger.info("Preparing to insert mermaid content into readme")

    encoded_pako = encode_to_pako(mermaid_content)
    view_link = f"https://mermaid.live/view#pako:{encoded_pako}"
    edit_link = f"https://mermaid.live/edit#pako:{encoded_pako}"
    # image_link = f"https://mermaid.ink/img/pako:{encoded_pako}?type=png"
    # Todo: Dynamically generated png link doesn't seem to be working...
    image_link = "https://tinyurl.com/open-source-roadmap"
    
    try:
        with open(readme_path, "r") as f:
            readme_content = f.read()
    
        start_tag = "<!-- roadmap-start -->"
        end_tag = "<!-- roadmap-end -->"

        start_idx = readme_content.index(start_tag) + len(start_tag)
        end_idx = readme_content.index(end_tag)

        before = (
            "\n<details>\n"
            "<summary><sub>🦯 Click here if you cannot see the chart</sub></summary>\n\n"
            f"This diagram is written using Mermaid- [view the chart source here]({edit_link})\n\n"
            f"[![roadmap]({image_link})]({view_link})\n"
            "</details>\n"
            "\n```mermaid\n"
        )

        after = "\n```\n"

        new_content = (
          readme_content[:start_idx] +
          before +
          mermaid_content +
          after +
          readme_content[end_idx:]
        )

        with open(readme_path, "w") as f:
            f.write(new_content)
            
        logger.info("Mermaid content successfully inserted into readme")
    
    except Exception as e:
        logger.error(f"Error inserting mermaid content: {e}")
        raise


if __name__ == "__main__":
    try:
        logger.info("Starting the process...")
        
        with open(mermaid_file, 'r') as f:
            mermaid_content = f.read()
        
        insert_mermaid_into_readme(mermaid_content)
        logger.info("All Done!")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
