import unittest

from src.md_block_converter import block_to_block_type, markdown_to_blocks
from src.textnode import BlockType


class TestBlockConverter(unittest.TestCase):
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

    def test_block_to_type_code(self):
        md_code = """```
        def python_function():
            pass
```"""
        self.assertEqual(block_to_block_type(md_code), BlockType.BLOCK_CODE)

    def test_block_to_type_heading(self):
        md_heading1 = """# heading
paragraph
"""
        md_heading2 = """## heading
paragraph
"""
        md_heading3 = """### heading
paragraph
"""
        md_heading4 = """#### heading
paragraph
"""
        md_heading5 = """##### heading
paragraph
"""
        md_heading6 = """##### heading
paragraph
"""

        self.assertEqual(block_to_block_type(md_heading1), BlockType.BLOCK_HEADING)
        self.assertEqual(block_to_block_type(md_heading2), BlockType.BLOCK_HEADING)
        self.assertEqual(block_to_block_type(md_heading3), BlockType.BLOCK_HEADING)
        self.assertEqual(block_to_block_type(md_heading4), BlockType.BLOCK_HEADING)
        self.assertEqual(block_to_block_type(md_heading5), BlockType.BLOCK_HEADING)
        self.assertEqual(block_to_block_type(md_heading6), BlockType.BLOCK_HEADING)

    def test_block_to_type_quote(self):
        md_quote = """> quoted text """
        md_quote_no_space = """>quoted text """

        self.assertEqual(block_to_block_type(md_quote), BlockType.BLOCK_QUOTE)
        self.assertEqual(block_to_block_type(md_quote_no_space), BlockType.BLOCK_QUOTE)

    def test_block_to_type_unordered_list(self):
        md_unordered_list = """- item 1
- item 2
- item 3

* item 1
* item 2
* item 3

+ item 1
+ item 2
+ item 2
"""
        self.assertEqual(
            block_to_block_type(md_unordered_list), BlockType.BLOCK_UNORDERED_LIST
        )

    def test_block_to_type_ordered_list(self):
        md_ordered_list = """1. item 1
2. item 2
3. item 3
"""

        self.assertEqual(
            block_to_block_type(md_ordered_list), BlockType.BLOCK_ORDERED_LIST
        )
