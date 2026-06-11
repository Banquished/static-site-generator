import re
from textnode import TextNode, TextType

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

def shared_split_nodes(old_nodes: list[TextNode], extract_func, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        items = extract_func(old_node.text)
        
        if not items:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        
        for alt_text, url in items:
            syntax = f"[{alt_text}]({url})" if text_type == TextType.LINK else f"![{alt_text}]({url})"
            
            parts = remaining_text.split(syntax, 1)
            if len(parts) != 2:
                raise ValueError(f"Unexpected error: could not split text by syntax '{syntax}'")
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.PLAIN))
                
            new_nodes.append(TextNode(alt_text, text_type, url))
            
            remaining_text = parts[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return shared_split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return shared_split_nodes(old_nodes, extract_markdown_links, TextType.LINK)
