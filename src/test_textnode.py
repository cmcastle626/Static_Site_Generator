import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold_texttype)
        node2 = TextNode("This is a text node", TextType.bold_texttype)
        self.assertEqual(node,node2)

    def test_difftexttype(self):
        node = TextNode("This is a text node", TextType.bold_texttype)
        node2 = TextNode("This is a text node", TextType.italic_texttype)
        self.assertNotEqual(node,node2)

    def test_difftext(self):
        node = TextNode("This is a text node", TextType.bold_texttype)
        node2 = TextNode("This is a different text node", TextType.bold_texttype)
        self.assertNotEqual(node, node2)

    def test_diffurl(self):
        node = TextNode("This is a text node", TextType.bold_texttype)
        node2 = TextNode("This is a text node", TextType.bold_texttype,"www.bootdev.com")
        self.assertNotEqual(node,node2)

    def test_sameurl(self):
        node = TextNode("This is a text node", TextType.bold_texttype,"www.bootdev.com")
        node2 = TextNode("This is a text node", TextType.bold_texttype,"www.bootdev.com")
        self.assertEqual(node,node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.text_texttype, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))

if __name__ == "__main__":
    unittest.main()