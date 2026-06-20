import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from convert_fns import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


class TestExtractImages(unittest.TestCase):
    def test_basicextract(self):
        test = "Here is an image: ![this is the world](something something image.jpg)"
        res = extract_markdown_images(test)
        exp = [("this is the world","something something image.jpg")]
        self.assertEqual(res, exp)

    def test_multiextract(self):
        test = "![image 1](sampletest.gif) 1 image and 2 image ![image 2](sampletest 2.gif) huzzah!"
        res = extract_markdown_images(test)
        exp = [
            ("image 1", "sampletest.gif"),
            ("image 2", "sampletest 2.gif")
        ]
        self.assertEqual(res,exp)

    def test_imagelink(self):
        test = "here is link: [link1](www.link1.com) and here is image: ![image1](image 1.png)"
        res = extract_markdown_images(test)
        exp = [
            ("image1","image 1.png")
        ]
        self.assertEqual(res,exp)

class TestExtractLinks(unittest.TestCase):
    def test_basicextract(self):
        test = ("Here is a link: [the title](www.link.com)")
        res = extract_markdown_links(test)
        exp = [("the title","www.link.com")]
        self.assertEqual(res, exp)

    def test_multiextract(self):
        test = ("[title 1](www.link1.com) 1 link and 2 link [title 2](www.link2.com)")
        res = extract_markdown_links(test)
        exp = [
            ("title 1", "www.link1.com"),
            ("title 2", "www.link2.com")
        ]
        self.assertEqual(res, exp)

    def test_imagelink(self):
        test = "here is link: [link1](www.link1.com) and here is image: ![image1](image 1.png)"
        res = extract_markdown_links(test)
        exp = [
            ("link1","www.link1.com")
        ]
        self.assertEqual(res,exp)