from enum import Enum
from htmlnode import LeafNode

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
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    ttype = text_node.text_type
    print(f"proccing ttype check... ttype: {ttype}")
    if ttype == TextType.text_texttype:
        return LeafNode(None, text_node.text, None)
    elif ttype == TextType.bold_texttype:
        return LeafNode("b", text_node.text)
    elif ttype == TextType.italic_texttype:
        return LeafNode("i", text_node.text)
    elif ttype == TextType.code_texttype:
        return LeafNode("code", text_node.text)
    elif ttype == TextType.link_texttype:
        return LeafNode("a", text_node.text,{"href":text_node.url})
    elif ttype == TextType.image_texttype:
        return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})
    else:
        raise Exception("not using supported text type")
    
