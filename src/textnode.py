from enum import Enum


class TextType(Enum):
    TEXT_PLAIN = "text_plain"
    TEXT_BOLD = "text_bold"
    TEXT_ITALIC = "text_italic"
    TEXT_CODE = "text_code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object, /) -> bool:
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
