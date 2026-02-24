import unittest

from md_converter import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestMDConverter(unittest.TestCase):
    def test_text_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT_PLAIN)
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
        node = TextNode("This is a text with an _italic_ word", TextType.TEXT_PLAIN)
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
        node = TextNode("This is a text with a `code` block", TextType.TEXT_PLAIN)
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
            "This is a text with **two** **bold** words", TextType.TEXT_PLAIN
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

    def test_split_image(self):
        node = TextNode(
            "This is text with an image ![bootdev logo](https://i.imgur.com/aKaOqIh.gif) and ![sonic img](https://i.imgur.com/aKaOqIh.gif)",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_images([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an image ", TextType.TEXT_PLAIN),
                TextNode(
                    "bootdev logo",
                    TextType.IMAGE,
                    "https://i.imgur.com/aKaOqIh.gif",
                ),
                TextNode(" and ", TextType.TEXT_PLAIN),
                TextNode(
                    "sonic img", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
            ],
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT_PLAIN,
        )
        new_nodes = split_nodes_links([node])

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT_PLAIN),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT_PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT_PLAIN),
                TextNode("text", TextType.TEXT_BOLD),
                TextNode(" with an ", TextType.TEXT_PLAIN),
                TextNode("italic", TextType.TEXT_ITALIC),
                TextNode(" word and a ", TextType.TEXT_PLAIN),
                TextNode("code block", TextType.TEXT_CODE),
                TextNode(" and an ", TextType.TEXT_PLAIN),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT_PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestLinkImageExtractor(unittest.TestCase):
    def test_link_extractor(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_image_extractor(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
