from enum import Enum
from inline_convert_fns import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from inline_convert_fns import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

# splits the full markdown page into blocks.
# blocks are defined as sections separated by 2 new lines.
def markdown_to_blocks(markdown: str) -> list[str]:
    clean_markdown = markdown.strip()
    blocks = clean_markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue 
        final_blocks.append(block)
    return final_blocks

# determines what type the block is depending on what symbols are at the front
def block_to_block_type(md_block: str) -> BlockType:
    if md_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading
    if md_block[0:3] == "```" and md_block[-3:] == "```":
        return BlockType.code
    multi_line_blocks = md_block.split("\n")
    flag = True
    if multi_line_blocks[0][0] == ">":
        for line in multi_line_blocks:
            if line[0] != ">":
                flag = False
        if flag:
            return BlockType.quote
    if multi_line_blocks[0][0:2] == "- ":
        for line in multi_line_blocks:
            if line[0:2] != "- ":
                flag = False
        if flag:
            return BlockType.unordered_list
    if multi_line_blocks[0][0:3] == "1. ":
        count = 1
        for line in multi_line_blocks[1:]:
            count += 1
            if line[0:3] != f"{count}. ":
                flag = False
        if flag:
            return BlockType.ordered_list
    return BlockType.paragraph

# determines the heading tag used by the block
def markdown_heading_prep(md_block: str) -> tuple[str,str]:
    if md_block[0:7] == "###### ":
        prepped_heading = md_block.replace("###### ","",1)
        return ("h6", prepped_heading)
    if md_block[0:6] == "##### ":
        heading = "h5"
    elif md_block[0:5] == "#### ":
        heading = "h4"
    elif md_block[0:4] == "### ":
        heading = "h3"
    elif md_block[0:3] == "## ":
        heading = "h2"
    elif md_block[0:2] == "# ":
        heading = "h1"
    else:
        raise Exception("no valid heading found")
    prepped_heading = md_block.lstrip("# ")
    return (heading, prepped_heading)
    
# splits markdown ordered and unordered lists into a list of strings
# list indicators will automatically be added in html, so markdown indicators are removed
def markdown_lists_prep(md_block: str, block_type: BlockType) -> list[str]:
    list_list = md_block.split("\n")
    prepped_list = []
    if block_type == BlockType.unordered_list:
        for item in list_list:
            remove_indicator = item.lstrip("- ")
            prepped_list.append(remove_indicator)
    elif block_type == BlockType.ordered_list:
        for item in list_list:
            remove_indicator = item.split(". ", 1)
            prepped_list.append(remove_indicator[1])
    return prepped_list

# splits a quote block by the new line indicator, removes the markdown '>' quote character
# and returns a string of the entire quote put together (lines separated by spaces)
def markdown_quote_prep(md_block: str) -> str:
    prepped_quote = ""
    if md_block[0] != ">":
        raise Exception("not a quote block")
    split_quote = md_block.split("\n")
    first_line_flag = True
    for line in split_quote:
        if len(line) == 0:
            continue
        stripped_line = line.lstrip(">")
        stripped_line = stripped_line.strip()
        if first_line_flag:
            prepped_quote += stripped_line
            first_line_flag = False
        else:
            prepped_quote = prepped_quote + " " + stripped_line
    return prepped_quote

def markdown_code_prep(md_block: str) -> str:
    prepped_code = md_block.strip("\n")
    prepped_code = prepped_code.strip("```")
    prepped_code = prepped_code.lstrip()
    return prepped_code

def markdown_text_prep(md_block: str) -> str:
    stripped_block = md_block.strip()
    split_block = stripped_block.split("\n")
    prepped_text = ""
    first_line_flag = True
    for line in split_block:
        if len(line) == 0:
            continue
        stripped_line = line.strip()
        if first_line_flag:
            prepped_text += stripped_line
            first_line_flag = False
        else:
            prepped_text += f" {stripped_line}"
    return prepped_text

# takes prepped markdown text and turns it into html leaf nodes
def text_to_children(prepped_md_text: str) -> list[LeafNode]:
    inline_children = text_to_textnodes(prepped_md_text)
    html_inline_children = []
    for child in inline_children:
        new_leaf = text_node_to_html_node(child)
        html_inline_children.append(new_leaf)
    return html_inline_children
    

def block_to_nodes(md_block: str, block_type: BlockType) -> list[ParentNode]:
    block_node = None
    child_nodes = None
    parent_nodes = None
    if block_type == BlockType.code:
        prepped_text = markdown_code_prep(md_block)
        child_nodes = TextNode(prepped_text, TextType.code)
        child_nodes = text_node_to_html_node(child_nodes)
        block_node = ParentNode("pre", [child_nodes], None)
    elif block_type == BlockType.paragraph:
        prepped_text = markdown_text_prep(md_block)
        child_nodes = text_to_children(prepped_text)
        block_node = ParentNode("p", child_nodes, None)
    elif block_type == BlockType.ordered_list:
        prepped_text = markdown_lists_prep(md_block, block_type)
        parent_nodes = []
        for item in prepped_text:
            child_nodes = text_to_children(item)
            parent_nodes.append(ParentNode("li", child_nodes))
        block_node = ParentNode("ol", parent_nodes)
    elif block_type == BlockType.unordered_list:
        prepped_text= markdown_lists_prep(md_block, block_type)
        parent_nodes = []
        for item in prepped_text:
            child_nodes = text_to_children(item)
            parent_nodes.append(ParentNode("li", child_nodes))
        block_node = ParentNode("ul", parent_nodes)
    elif block_type == BlockType.heading:
        prepped_text = markdown_heading_prep(md_block)
        child_nodes = text_to_children(prepped_text[1])
        block_node = ParentNode(prepped_text[0], child_nodes)
    elif block_type == BlockType.quote:
        prepped_text = markdown_quote_prep(md_block)
        child_nodes = text_to_children(prepped_text)
        block_node = ParentNode("blockquote", child_nodes)
    elif block_type == BlockType.paragraph:
        prepped_text = markdown_text_prep(md_block)
        child_nodes = text_to_children(md_block)
        block_node = ParentNode("p",child_nodes)
    else:
        raise Exception("no valid block type found for node conversion")
    return block_node



def markdown_to_html_node(markdown) -> list[ParentNode]:
    md_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_nodes(block, block_type)
        block_nodes.append(block_node)
    full_html_node = ParentNode("div", block_nodes)
    return full_html_node



        



