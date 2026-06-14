from enum import Enum

class TextType(Enum):
    text_texttype = "text"
    bold_texttype = "bold"
    italic_texttype = "italic"
    code_texttype = "code"
    link_texttype = "link"
    image_texttype = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
