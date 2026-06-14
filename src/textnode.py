from enum import Enum

class TextType(Enum):
    bold_texttype = "bold"
    italic_texttype = "italic"
    code_texttype = "cod"
    link_texttype = "link"
    image_texttype = "image"

class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = None

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
