from enum import Enum

class TextType(Enum):
    PLAIN = "text"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.PLAIN, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
        
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return True
        
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
