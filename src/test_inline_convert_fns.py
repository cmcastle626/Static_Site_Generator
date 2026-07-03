import unittest
from textnode import TextNode, TextType
from inline_convert_fns import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes)


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

    def test_sameimage(self):
        test = "Here is image: ![img1](image1.jpeg) and here it is again: ![img1](image1.jpeg)"
        res = extract_markdown_images(test)
        exp = [
            ("img1", "image1.jpeg"),
            ("img1", "image1.jpeg")
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


class TestSplitNodesImage(unittest.TestCase):
    def test_basicsplit(self):
        nodes = [TextNode(
            "Here is an image ![img1](image1here.png) in the middle.",
            TextType.text
        )]
        res = split_nodes_image(nodes)
        exp = [
            TextNode("Here is an image ", TextType.text),
            TextNode("img1", TextType.image, "image1here.png"),
            TextNode(" in the middle.", TextType.text)
        ]
        self.assertEqual(res, exp)

    def test_sameimage(self):
        nodes = [TextNode(
            "![img1](image1here.png)Same image at beginning and end.![img1](image1here.png)",
            TextType.text
        )]
        res = split_nodes_image(nodes)
        exp = [
            TextNode("img1", TextType.image, "image1here.png"),
            TextNode("Same image at beginning and end.", TextType.text),
            TextNode("img1", TextType.image, "image1here.png")
        ]
        self.assertEqual(res,exp)

    def test_NodeList(self):
        nodes = [
            TextNode("I'm a **bold** line oo-RAH!", TextType.bold),
            TextNode("I'm a text node with an image!!!![img1](img1.png)", TextType.text),
            TextNode("I'm another ![img2](img2.jpeg) text with an image!", TextType.text),
            TextNode("I'm a regular text node.", TextType.text)
        ]
        res = split_nodes_image(nodes)
        exp = [
            TextNode("I'm a **bold** line oo-RAH!", TextType.bold),
            TextNode("I'm a text node with an image!!!", TextType.text),
            TextNode("img1", TextType.image, "img1.png"),
            TextNode("I'm another ", TextType.text),
            TextNode("img2", TextType.image, "img2.jpeg"),
            TextNode(" text with an image!", TextType.text),
            TextNode("I'm a regular text node.", TextType.text)
        ]
        self.assertEqual(res,exp)

    def test_NoTextInNode(self):
        nodes = [
            TextNode("Hello", TextType.text),
            TextNode("",TextType.text),
            TextNode("World", TextType.text),
            TextNode("![img1](img1.png)", TextType.text)
        ]
        res = split_nodes_image(nodes)
        exp = [
            TextNode("Hello", TextType.text),
            TextNode("World", TextType.text),
            TextNode("img1", TextType.image, "img1.png")
        ]
        self.assertEqual(res,exp)


class TestSplitNodesLink(unittest.TestCase):
    def test_basicsplit(self):
        nodes = [TextNode(
            "Here is a link [hello world](www.world.com) in the middle.",
            TextType.text
        )]
        res = split_nodes_link(nodes)
        exp = [
            TextNode("Here is a link ", TextType.text),
            TextNode("hello world", TextType.link, "www.world.com"),
            TextNode(" in the middle.", TextType.text)
        ]
        self.assertEqual(res, exp)

    def test_samelink(self):
        nodes = [TextNode(
            "[hello](www.hello.net)Same link at beginning and end.[hello](www.hello.net)",
            TextType.text
        )]
        res = split_nodes_link(nodes)
        exp = [
            TextNode("hello", TextType.link, "www.hello.net"),
            TextNode("Same link at beginning and end.", TextType.text),
            TextNode("hello", TextType.link, "www.hello.net")
        ]
        self.assertEqual(res,exp)

    def test_NodeList(self):
        nodes = [
            TextNode("I'm an _italic_ line oo-RAH!", TextType.italic),
            TextNode("I'm a text node with a link!!! [link1](www.link1.com)", TextType.text),
            TextNode("I'm another [link2 text](www.link2.com) text with a link!", TextType.text),
            TextNode("I'm a regular text node.", TextType.text)
        ]
        res = split_nodes_link(nodes)
        exp = [
            TextNode("I'm an _italic_ line oo-RAH!", TextType.italic),
            TextNode("I'm a text node with a link!!! ", TextType.text),
            TextNode("link1", TextType.link, "www.link1.com"),
            TextNode("I'm another ", TextType.text),
            TextNode("link2 text", TextType.link, "www.link2.com"),
            TextNode(" text with a link!", TextType.text),
            TextNode("I'm a regular text node.", TextType.text)
        ]
        self.assertEqual(res,exp)

    def test_NoTextInNode(self):
        nodes = [
            TextNode("Hello", TextType.text),
            TextNode("",TextType.text),
            TextNode("World", TextType.text),
            TextNode("[link1](www.link1.com)", TextType.text)
        ]
        res = split_nodes_link(nodes)
        exp = [
            TextNode("Hello", TextType.text),
            TextNode("World", TextType.text),
            TextNode("link1", TextType.link, "www.link1.com")
        ]
        self.assertEqual(res,exp)


class TestTextToTextNodes(unittest.TestCase):
    def test_BootDevExample(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_textnodes(text)
        exp = [
            TextNode("This is ", TextType.text),
            TextNode("text", TextType.bold),
            TextNode(" with an ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" word and a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" and an ", TextType.text),
            TextNode("obi wan image", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.text),
            TextNode("link", TextType.link, "https://boot.dev"),
        ]
        self.assertEqual(res, exp)

    def test_ItalicsBoldImage(self):
        text = "It's _levi_**OH**_sah_, not _levioh_**SAH**.![hermoine eye roll](hermoine.gif)"
        res = text_to_textnodes(text)
        exp = [
            TextNode("It's ", TextType.text),
            TextNode("levi", TextType.italic),
            TextNode("OH", TextType.bold),
            TextNode("sah", TextType.italic),
            TextNode(", not ", TextType.text),
            TextNode("levioh", TextType.italic),
            TextNode("SAH", TextType.bold),
            TextNode(".", TextType.text),
            TextNode("hermoine eye roll", TextType.image, "hermoine.gif")
        ]
        self.assertEqual(res, exp)