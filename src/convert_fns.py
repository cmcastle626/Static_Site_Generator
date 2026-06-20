import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            new_list.append(node)
        else:
            temp_str_list = node.text.split(delimiter)
            if len(temp_str_list) % 2 != 1:
                raise Exception("no matching delimiter found")
            for k in range(0, len(temp_str_list)):
                if k % 2 == 0:
                    if temp_str_list[k] != "":
                        new_list.append(TextNode(temp_str_list[k], TextType.text))
                else:
                    new_list.append(TextNode(temp_str_list[k], text_type))
    return new_list
    
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pairs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return pairs

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pairs = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return pairs