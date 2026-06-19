import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from convert_fns import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node,node2)

    def test_difftexttype(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.italic)
        self.assertNotEqual(node,node2)

    def test_difftext(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a different text node", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_diffurl(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold,"www.bootdev.com")
        self.assertNotEqual(node,node2)

    def test_sameurl(self):
        node = TextNode("This is a text node", TextType.bold,"www.bootdev.com")
        node2 = TextNode("This is a text node", TextType.bold,"www.bootdev.com")
        self.assertEqual(node,node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.text, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_notype(self):
        node = TextNode("hello world", "nothere")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()