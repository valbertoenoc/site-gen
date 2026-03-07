import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a", "test anchor", None, {"href": "https://boot.dev", "_target": "_blank"}
        )

        actual = node.props_to_html()
        expected = ' href="https://boot.dev" _target="_blank"'
        self.assertEqual(actual, expected)
