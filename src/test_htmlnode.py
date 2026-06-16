import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_autonone(self):
        node = HTMLNode("h1","hello world",["lions","tigers","and bears"])
        self.assertEqual(node.props,None)

    def test_diffvalue(self):
        node = HTMLNode(value="h1")
        node2 = HTMLNode(value="h2")
        self.assertNotEqual(node.value, node2.value)

    def test_propstohtml(self):
        node = HTMLNode(props={"mouse":"cookie","moose":"muffin","calvin":"hobbes"})
        self.assertEqual('mouse="cookie" moose="muffin" calvin="hobbes"',node.props_to_html())

    def test_tohtmlerror(self):
        node = HTMLNode("tag","value")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_values(self):
        node = HTMLNode("h1", None, ["lions","tigers","bears"],{"mouse":"cookie","moose":"muffin"})
        self.assertEqual("h1",node.tag)
        self.assertEqual(None,node.value)
        self.assertEqual(["lions", "tigers", "bears"],node.children)
        self.assertEqual({"mouse":"cookie","moose":"muffin"}, node.props)

    def test_rep(self):
        node = HTMLNode("h1", None, ["lions","tigers","bears"],{"mouse":"cookie","moose":"muffin"})
        self.assertEqual("HTMLNode(h1, None, children: ['lions', 'tigers', 'bears'], {'mouse': 'cookie', 'moose': 'muffin'})",
                         repr(node))