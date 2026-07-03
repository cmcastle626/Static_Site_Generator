import unittest
from block_convert_fns import (markdown_to_blocks,
                               block_to_block_type,
                               markdown_code_prep,
                               markdown_heading_prep,
                               markdown_lists_prep,
                               markdown_quote_prep,
                               markdown_to_html_node,
                               text_to_children,
                               BlockType)
from htmlnode import LeafNode
from inline_convert_fns import text_to_textnodes

class TestMarkdownToBlocks(unittest.TestCase):
    def test_BootDevExample(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        res = markdown_to_blocks(md)
        exp = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        self.assertEqual(res, exp)

    def test_BootDevExample2(self):
        md = """This is a **bolded** paragraph.




This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items
"""
        res = markdown_to_blocks(md)
        exp = [
            "This is a **bolded** paragraph.",
            "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.",
            "- This is a list\n- with items"
        ]
        self.assertEqual(res, exp)

class Test_BlocktoBlockTypes(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a regular paragraph.\nThis is part of the same paragraph."
        res = block_to_block_type(md)
        exp = BlockType.paragraph
        self.assertEqual(res, exp)
    
    def test_quote(self):
        md = "> quote line 1\n>quote line 2"
        res = block_to_block_type(md)
        exp = BlockType.quote
        self.assertEqual(res, exp)

    def test_orderedlist(self):
        md = "1. hello\n2. world\n3. ???\n4. profit"
        res = block_to_block_type(md)
        exp = BlockType.ordered_list
        self.assertEqual(res, exp)

    def test_unorderedlist(self):
        md = "- hola\n- amigo"
        res = block_to_block_type(md)
        exp = BlockType.unordered_list
        self.assertEqual(res, exp)

    def test_header(self):
        md = "## heading2"
        res = block_to_block_type(md)
        exp = BlockType.heading
        self.assertEqual(res, exp)
    
    def test_code(self):
        md = "```\nhere is a code block\nsome more lines\nlast line\n```"
        res = block_to_block_type(md)
        exp = BlockType.code
        self.assertEqual(res, exp)

    def test_brokenquote(self):
        md = "> line 1\nline 2\n>line3"
        res = block_to_block_type(md)
        exp = BlockType.paragraph
        self.assertEqual(res, exp)


class Test_MarkDownPreppers(unittest.TestCase):
    def test_heading6(self):
        md_block = "###### #Heading 6 Hello World"
        res = markdown_heading_prep(md_block)
        exp = ("h6","#Heading 6 Hello World")
        self.assertEqual(res,exp)

    def test_heading3(self):
        md_block = "### Heading 3 Hello\nWorld"
        res = markdown_heading_prep(md_block)
        exp = ("h3", "Heading 3 Hello\nWorld")
        self.assertEqual(res,exp)

    def test_codeblock(self):
        md_block = """```
Here is some coding block.
Even on a new line!
```"""
        res = markdown_code_prep(md_block)
        exp = "Here is some coding block.\nEven on a new line!\n"
        self.assertEqual(res,exp)

    def test_orderedlist4(self):
        md_block = """1. Give a Mouse
2. A Cookie
3. Give a Moose
4. A Muffin"""
        res = markdown_lists_prep(md_block, BlockType.ordered_list)
        exp = ["Give a Mouse", "A Cookie", "Give a Moose", "A Muffin"]
        self.assertEqual(res,exp)

    def test_unorderedlist4(self):
        md_block = """- Give a Mouse
- A Cookie
- Give a Moose
- A Muffin"""
        res = markdown_lists_prep(md_block, BlockType.unordered_list)
        exp = ["Give a Mouse", "A Cookie", "Give a Moose", "A Muffin"]
        self.assertEqual(res,exp)

    def test_quote(self):
        md_block = """>"Did you put your name into the goblet of fire?"
> Dumbledore asked calmly.
"""
        res = markdown_quote_prep(md_block)
        exp = '"Did you put your name into the goblet of fire?" Dumbledore asked calmly.'
        self.assertEqual(res, exp)

class Test_preppedtext_to_children(unittest.TestCase):
    def test_preppedquote(self):
        md_prepped = '"Did **you** put _your name_ into the `goblet of fire`?" Dumbledore asked calmly.![FIYA](dumbleshout.jpeg)'
        res = text_to_children(md_prepped)
        exp = [
            LeafNode(None, '"Did '),
            LeafNode("b", "you"),
            LeafNode(None, " put "),
            LeafNode("i", "your name"),
            LeafNode(None, " into the "),
            LeafNode("code", "goblet of fire"),
            LeafNode(None, '?" Dumbledore asked calmly.'),
            LeafNode("img", "", {"src":"dumbleshout.jpeg", "alt":"FIYA"})
        ]
        self.assertEqual(res, exp)


class Test_markdown_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_multiblock_lists(self):
        md = """
1. Hello world
2. Turn around **bright eyes**

- Woe is me
- Moop Moop
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        exp = "<div><ol><li>Hello world</li><li>Turn around <b>bright eyes</b></li></ol><ul><li>Woe is me</li><li>Moop Moop</li></ul></div>"
        self.assertEqual(html, exp)

    def test_multiblock_headsquotes(self):
        md = """
> This be a _quote_.
>Let me know what you think!

### Heading be three

###### #Heading be 6 with an extra
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        exp = "<div><blockquote>This be a <i>quote</i>. Let me know what you think!</blockquote><h3>Heading be three</h3><h6>#Heading be 6 with an extra</h6></div>"
        self.assertEqual(html, exp)


    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )




if __name__ == "__main__":
    unittest.main()