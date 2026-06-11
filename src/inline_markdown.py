import re

# 1. Create a function `extract_markdown_images(text)` that takes raw markdown text and returns a list of tuples.
#    Each tuple should contain the alt text and the URL of any markdown images.
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # Regular expression to match markdown image syntax: ![alt text](url)
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches
# 2. Create a similar function `extract_markdown_links(text)` that extracts markdown links instead of images.
#    It should return tuples of anchor text and URLs.
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # Regular expression to match markdown link syntax: [anchor text](url)
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches
