import re
from textnode import TextNode, TextType

text_type_delimiter_map = {
    TextType.TEXT_PLAIN: " ",
    TextType.TEXT_BOLD: "**",
    TextType.TEXT_ITALIC: "_",
    TextType.TEXT_CODE: "`",
}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter != text_type_delimiter_map.get(text_type):
        raise ValueError("TextType does not match delimiter")

    new_nodes = []
    for old_node in old_nodes:
        if (
            old_node.text_type == TextType.IMAGE
            or old_node.text_type == TextType.LINK
            or old_node.text_type == TextType.TEXT_PLAIN
        ):
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid Markdown Syntax")

        for i, text in enumerate(split_text):
            if i % 2 == 0:
                new_node = TextNode(text, TextType.TEXT_PLAIN)
            else:
                new_node = TextNode(text, text_type)

            new_nodes.append(new_node)

    return new_nodes


def extract_markdown_links_and_images(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
