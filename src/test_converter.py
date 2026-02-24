import unittest

from md_converter import extract_markdown_links_and_images, split_nodes_delimiter
from textnode import TextNode, TextType


class TestMDConverter(unittest.TestCase):
    def test_text_plain(self):
        node = TextNode("This is a plain text", TextType.TEXT_PLAIN)
        nodes = split_nodes_delimiter([node], " ", TextType.TEXT_PLAIN)
        self.assertListEqual(
            nodes, [TextNode("This is a plain text", TextType.TEXT_PLAIN)]
        )

    def test_text_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT_BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.TEXT_BOLD)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT_PLAIN),
                TextNode("bold", TextType.TEXT_BOLD),
                TextNode(" word", TextType.TEXT_PLAIN),
            ],
        )

    def test_text_italic(self):
        node = TextNode("This is a text with an _italic_ word", TextType.TEXT_ITALIC)
        nodes = split_nodes_delimiter([node], "_", TextType.TEXT_ITALIC)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT_PLAIN),
                TextNode("italic", TextType.TEXT_ITALIC),
                TextNode(" word", TextType.TEXT_PLAIN),
            ],
        )

    def test_text_code(self):
        node = TextNode("This is a text with a `code` block", TextType.TEXT_CODE)
        nodes = split_nodes_delimiter([node], "`", TextType.TEXT_CODE)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT_PLAIN),
                TextNode("code", TextType.TEXT_CODE),
                TextNode(" block", TextType.TEXT_PLAIN),
            ],
        )

    def test_mismatch_inline(self):
        node = TextNode("This is a text with a `code` block", TextType.TEXT_BOLD)
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([node], "`", TextType.TEXT_BOLD)

    def test_text_invalid_markdown(self):
        node = TextNode(
            "This is a text with an invalid syntax `code block", TextType.TEXT_CODE
        )

        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([node], " ", TextType.TEXT_CODE)

    def test_multiple_text_bold(self):
        node = TextNode(
            "This is a text with **two** **bold** words", TextType.TEXT_BOLD
        )
        nodes = split_nodes_delimiter([node], "**", TextType.TEXT_BOLD)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is a text with ", TextType.TEXT_PLAIN),
                TextNode("two", TextType.TEXT_BOLD),
                TextNode(" ", TextType.TEXT_PLAIN),
                TextNode("bold", TextType.TEXT_BOLD),
                TextNode(" words", TextType.TEXT_PLAIN),
            ],
        )


class TestLinkImageExtractor(unittest.TestCase):
    def test_link_extractor(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links_and_images(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_image_extractor(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_links_and_images(text)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
