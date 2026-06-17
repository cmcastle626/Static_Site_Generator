import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node.props, None)

    def test_tohtml_emptyvalue(self):
        node = LeafNode("p",None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_values(self):
        node = LeafNode("p", "hello", {"calvin":"hobbes"})
        self.assertEqual(node.children, None)
        self.assertEqual(node.props,{'calvin': 'hobbes'})

    def test_rep(self):
            node = LeafNode(None, "hello world", {"mouse":"cookie","moose":"muffin"})
            self.assertEqual("LeafNode(None, hello world, {'mouse': 'cookie', 'moose': 'muffin'})",
                         repr(node))
            

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_Nonechildren(self):
        node = ParentNode("h",None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_rep(self):
        leaf = LeafNode("p","hello world",None)
        node = ParentNode("h1", leaf, {"calvin":"hobbes"})
        self.assertEqual(repr(node),"ParentNode(h1, children: LeafNode(p, hello world, None), {'calvin': 'hobbes'})")