import re
from textnode import TextNode, TextType

# Function to split markdown text into multiple textnodes with varying texttypes
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


# Function to extract images from markdown text    
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pairs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return pairs


# Function to extract links from markdown text
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pairs = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return pairs


# Function to take list of textnodes, extract image info from them, then create new list of text and image nodes
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if len(node.text) < 1:
            continue
        if node.text_type != TextType.text:
            new_nodes.append(node)
            continue
        image_info = extract_markdown_images(node.text)
        if len(image_info) < 1:
            new_nodes.append(node)
            continue                         
        org_text = node.text
        for pair in image_info:
            split_text = org_text.split(f"![{pair[0]}]({pair[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if len(split_text[0]) >0:
                new_nodes.append(TextNode(split_text[0], TextType.text))
            new_nodes.append(TextNode(pair[0], TextType.image, pair[1]))
            org_text = split_text[1]
        if len(org_text) > 1:
            new_nodes.append(TextNode(org_text, TextType.text))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if len(node.text) < 1:
            continue
        if node.text_type != TextType.text:
            new_nodes.append(node)
            continue
        link_info = extract_markdown_links(node.text)
        if len(link_info) < 1:
            new_nodes.append(node)
            continue                         
        org_text = node.text
        for pair in link_info:
            split_text = org_text.split(f"[{pair[0]}]({pair[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if len(split_text[0]) >0:
                new_nodes.append(TextNode(split_text[0], TextType.text))
            new_nodes.append(TextNode(pair[0], TextType.link, pair[1]))
            org_text = split_text[1]
        if len(org_text) > 1:
            new_nodes.append(TextNode(org_text, TextType.text))
    return new_nodes

        

