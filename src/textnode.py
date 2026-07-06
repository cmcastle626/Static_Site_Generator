from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

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
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    ttype = text_node.text_type
    if ttype == TextType.text:
        return LeafNode(None, text_node.text, None)
    elif ttype == TextType.bold:
        return LeafNode("b", text_node.text)
    elif ttype == TextType.italic:
        return LeafNode("i", text_node.text)
    elif ttype == TextType.code:
        return LeafNode("code", text_node.text)
    elif ttype == TextType.link:
        return LeafNode("a", text_node.text,{"href":text_node.url})
    elif ttype == TextType.image:
        return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
    else:
        raise Exception("not using supported text type")
    

