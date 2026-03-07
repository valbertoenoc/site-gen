from enum import Enum

from .htmlnode import LeafNode


class TextType(Enum):
    TEXT_PLAIN = "text_plain"
    TEXT_BOLD = "text_bold"
    TEXT_ITALIC = "text_italic"
    TEXT_CODE = "text_code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    BLOCK_PARAGRAPH = "block_paragraph"
    BLOCK_HEADING = "block_heading"
    BLOCK_CODE = "block_code"
    BLOCK_QUOTE = "block_quote"
    BLOCK_UNORDERED_LIST = "block_unordered_list"
    BLOCK_ORDERED_LIST = "block_ordered_list"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TextNode):
            raise NotImplementedError
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


# --- Methods --- #
def text_node_to_html_node(text_node) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT_PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.TEXT_BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.TEXT_ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.TEXT_CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": text_node.url},
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("invalid TextType")
