from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self, text: str, text_type: TextType = TextType.PLAIN, url: str | None = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


# Write a function that takes a TextNode and returns the corresponding HTML string representation
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(
            "a",
            text_node.text,
            props={"href": text_node.url} if text_node.url else None,
        )
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            "img",
            "",
            props={"src": text_node.url, "alt": text_node.text}
            if text_node.url
            else None,
        )
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
