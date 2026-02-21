import unittest

from textnode import TextNode, TextType


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
