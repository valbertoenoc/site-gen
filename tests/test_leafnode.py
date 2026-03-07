import unittest

from src.htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_p_tag(self):
        node = LeafNode("p", "hello world!")

        actual = node.to_html()
        expected = "<p>hello world!</p>"

        self.assertEqual(actual, expected)

    def test_a_tag(self):
        node_value = "check out BootDev!"
        node = LeafNode("a", node_value, {"href": "https://boot.dev"})

        actual = node.to_html()
        expected = f'<a href="https://boot.dev">{node_value}</a>'

        self.assertEqual(actual, expected)
