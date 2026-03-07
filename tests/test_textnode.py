import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Test anchor text", TextType.LINK)
        node2 = TextNode("Test anchor text", TextType.LINK)

        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("Test anchor text", TextType.LINK)
        node2 = TextNode("Test anchor text different", TextType.LINK)

        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("Test anchor text", TextType.TEXT_BOLD)
        node2 = TextNode("Test anchor text", TextType.LINK)

        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT_PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.TEXT_BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.TEXT_ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.TEXT_CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "google")
        self.assertEqual(html_node.props.get("href"), "https://www.google.com")

    def test_image(self):
        node = TextNode(
            "cool image", TextType.IMAGE, "https://images.com/coolimage.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props.get("src"), "https://images.com/coolimage.png")
        self.assertEqual(html_node.props.get("alt"), "cool image")

    def test_invalid_type(self):
        node = TextNode("invalid type node", "invalid type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
