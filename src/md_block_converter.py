import re

from src.textnode import BlockType


def markdown_to_blocks(markdown):
    paragraphs = markdown.split("\n\n")
    striped = list(map(lambda x: x.strip(), paragraphs))
    filtered = list(filter(lambda x: len(x) > 0, striped))
    return filtered


def block_to_block_type(md_block):
    if re.findall(r"^#{1,6}\s+.+", md_block):
        return BlockType.BLOCK_HEADING
    elif re.findall(r"`{3}[\s\S]*?`{3}", md_block):
        return BlockType.BLOCK_CODE
    elif re.findall(r"^>\s?.+", md_block):
        return BlockType.BLOCK_QUOTE
    elif re.findall(r"^[\-\*\+]\s.*", md_block):
        return BlockType.BLOCK_UNORDERED_LIST
    elif re.findall(r"^\d+\.\s.*", md_block):
        return BlockType.BLOCK_ORDERED_LIST
    else:
        return BlockType.BLOCK_PARAGRAPH
