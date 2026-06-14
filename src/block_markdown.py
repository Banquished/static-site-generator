from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    HEADING_4 = "heading_4"
    HEADING_5 = "heading_5"
    HEADING_6 = "heading_6"
    BLOCKQUOTE = "blockquote"
    CODE_BLOCK = "code_block"
    UNORDERED_LIST_ITEM = "unordered_list_item"
    ORDERED_LIST_ITEM = "ordered_list_item"
    TOGGLE = "toggle"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("# "):
        return BlockType.HEADING_1
    elif block.startswith("## "):
        return BlockType.HEADING_2
    elif block.startswith("### "):
        return BlockType.HEADING_3
    elif block.startswith("#### "):
        return BlockType.HEADING_4
    elif block.startswith("##### "):
        return BlockType.HEADING_5
    elif block.startswith("###### "):
        return BlockType.HEADING_6
    elif block.startswith("> "):
        return BlockType.BLOCKQUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST_ITEM
    elif block.startswith("1. "):
        return BlockType.ORDERED_LIST_ITEM
    elif block.startswith("```"):
        return BlockType.CODE_BLOCK
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    # 1. Convert markdown to blocks (step 1)
    blocks = markdown_to_blocks(markdown)
    html_nodes: list[HTMLNode] = []
    # 2. Loop over each block and determine its type (step 2)
    for block in blocks:
        html_nodes.append(block_to_html_node(block))
    return ParentNode("div", html_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    # It takes a string of text and returns a list of HTMLNode's ...
    # using previously created functions (think `TextNode` -> `HTMLNode`).
    # 1. Utilize `text_to_textnodes` to convert the text into a list of `TextNode` objects.
    text_nodes = text_to_textnodes(text)
    # 2. Convert each `TextNode` into an `HTMLNode` using `text_node_to_html_node`.
    children: list[HTMLNode] = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING_1:
        return heading_to_html_node(block, 1)
    elif block_type == BlockType.HEADING_2:
        return heading_to_html_node(block, 2)
    elif block_type == BlockType.HEADING_3:
        return heading_to_html_node(block, 3)
    elif block_type == BlockType.HEADING_4:
        return heading_to_html_node(block, 4)
    elif block_type == BlockType.HEADING_5:
        return heading_to_html_node(block, 5)
    elif block_type == BlockType.HEADING_6:
        return heading_to_html_node(block, 6)
    elif block_type == BlockType.BLOCKQUOTE:
        return blockquote_to_html_node(block)
    elif block_type == BlockType.CODE_BLOCK:
        return code_block_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST_ITEM:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST_ITEM:
        return ordered_list_to_html_node(block)
    else:
        return paragraph_to_html_node(block)


def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split())
    children = text_to_children(text)
    return ParentNode("p", children)


def heading_to_html_node(block: str, level: int) -> ParentNode:
    children = text_to_children(block[level + 1 :].strip())
    return ParentNode(f"h{level}", children)


def blockquote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            new_lines.append(line[2:])
        elif line.startswith(">"):
            new_lines.append(line[1:])
        else:
            new_lines.append(line)
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def code_block_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    content_lines = lines[1:-1]
    code_text = "\n".join(content_lines) + "\n"
    text_node = TextNode(code_text, TextType.PLAIN)
    code_child = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [code_child])])


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    li_nodes: list[HTMLNode] = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    ol_nodes: list[HTMLNode] = []
    for item in items:
        # Assuming the format is "1. ", "2. ", etc., we can find the index of the first space after the period to get the text
        space_index = item.find(" ")
        if space_index == -1:
            # If there's no space, we can just take the text after the period
            text = item[item.find(".") + 1 :].strip()
        else:
            text = item[space_index + 1 :].strip()
        children = text_to_children(text)
        ol_nodes.append(ParentNode("li", children))
    return ParentNode("ol", ol_nodes)
