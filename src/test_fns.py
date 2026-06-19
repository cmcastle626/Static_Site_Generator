import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from convert_fns import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_boldphrase(self):
        nodes = [TextNode("This is text with a **bolded phrase** in the middle.", TextType.text)]
        exp = [TextNode("This is text with a ", TextType.text),
            TextNode("bolded phrase", TextType.bold),
            TextNode(" in the middle.", TextType.text),
            ]
        self.assertEqual(split_nodes_delimiter(nodes,"**",TextType.bold),exp)

    def test_frontbackitalics(self):
        nodes = [TextNode("_This_ is text with italics at the beginning and _end._", TextType.text)]
        exp = [TextNode("This", TextType.italic),
            TextNode(" is text with italics at the beginning and ", TextType.text),
            TextNode("end.", TextType.italic),
            ]
        self.assertEqual(split_nodes_delimiter(nodes,"_",TextType.italic),exp)

    def test_multipass(self):
        first_node = [TextNode("This is text with _italics_ and `code block` in the middle.",
            TextType.text)]
        new_nodes = split_nodes_delimiter(first_node, "_", TextType.italic)
        final_nodes = split_nodes_delimiter(new_nodes, "`", TextType.code)
        new_exp = [
            TextNode("This is text with ", TextType.text),
            TextNode("italics", TextType.italic),
            TextNode(" and `code block` in the middle.", TextType.text)
        ]
        final_exp = [
            TextNode("This is text with ", TextType.text),
            TextNode("italics", TextType.italic),
            TextNode(" and ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" in the middle.", TextType.text)
        ]
        self.assertEqual(new_nodes, new_exp)
        self.assertEqual(final_nodes, final_exp)

    def test_uncloseddelimiter(self):
        node = [TextNode("This is **crazy.", TextType.text)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "**", TextType.bold)