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
        if old_node.text_type != TextType.TEXT_PLAIN:
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


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def split_nodes_images(old_nodes):
    new_nodes = []
    for old in old_nodes:
        matches = extract_markdown_images(old.text)

        if not matches:
            new_nodes.append(old)
            continue

        remaining_text = old.text
        for m in matches:
            alt, url = m
            split_text = remaining_text.split(f"![{alt}]({url})", 1)

            if len(split_text) == 1:
                new_nodes.append(TextNode(old.text, TextType.TEXT_PLAIN))
                continue

            new_nodes.extend(
                [
                    TextNode(split_text[0], TextType.TEXT_PLAIN),
                    TextNode(alt, TextType.IMAGE, url),
                ]
            )

            remaining_text = split_text[-1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT_PLAIN))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old in old_nodes:
        matches = extract_markdown_links(old.text)

        if not matches:
            new_nodes.append(old)
            continue

        remaining_text = old.text
        for m in matches:
            alt, url = m
            split_text = remaining_text.split(f"[{alt}]({url})", 1)

            if len(split_text) == 1:
                new_nodes.append(TextNode(old.text, TextType.TEXT_PLAIN))
                continue

            new_nodes.extend(
                [
                    TextNode(split_text[0], TextType.TEXT_PLAIN),
                    TextNode(alt, TextType.LINK, url),
                ]
            )

            remaining_text = split_text[-1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT_PLAIN))

    return new_nodes


text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT_PLAIN)
    new_nodes = split_nodes_delimiter([node], "**", TextType.TEXT_BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.TEXT_ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.TEXT_CODE)
    new_nodes = split_nodes_images(new_nodes)
    new_nodes = split_nodes_links(new_nodes)

    return new_nodes


def markdown_to_blocks(markdown):
    paragraphs = markdown.split("\n\n")
    striped = list(map(lambda x: x.strip(), paragraphs))
    filtered = list(filter(lambda x: len(x) > 0, striped))
    return filtered


md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""

markdown_to_blocks(md)
