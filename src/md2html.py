import re
from src import htmlnode
from src.htmlnode import HTMLNode, ParentNode
from src.md_block_converter import block_to_block_type, markdown_to_blocks
from src.md_text_converter import text_to_textnodes
from src.textnode import BlockType, TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        children.append(block_node)

    return ParentNode("div", children=children)


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.BLOCK_PARAGRAPH:
            html_nodes = text_to_children(block.replace("\n", " "))
            return ParentNode("p", children=html_nodes)
        case BlockType.BLOCK_HEADING:
            html_nodes = text_to_children(block.lstrip("#").strip())
            count_hashtags = len(block) - len(block.lstrip("#"))
            return ParentNode(f"h{count_hashtags}", children=html_nodes)
        case BlockType.BLOCK_CODE:
            html_code_node = strip_backticks_by_line(block)
            return ParentNode("pre", children=[html_code_node])
        case BlockType.BLOCK_QUOTE:
            stripped_block = strip_quotes_by_line(block)
            html_nodes = text_to_children(stripped_block)
            return ParentNode("blockquote", children=html_nodes)
        case BlockType.BLOCK_UNORDERED_LIST:
            li_nodes = text_to_html_unordered_item_list(block)
            return ParentNode("ul", children=li_nodes)
        case BlockType.BLOCK_ORDERED_LIST:
            li_nodes = text_to_html_ordered_item_list(block)
            return ParentNode("ol", children=li_nodes)


def text_to_children(text_block: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text_block)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes


def text_to_html_unordered_item_list(text_block: str) -> list[HTMLNode]:
    lines = text_block.splitlines()
    list_nodes = []
    for line in lines:
        if (
            line.startswith("-")
            or line.startswith("*")
            or line.startswith("+")
            or re.match(r"\d\.", line)
        ):
            li_nodes = text_to_children(line[2:])
            list_nodes.append(ParentNode("li", children=li_nodes))

    return list_nodes


def text_to_html_ordered_item_list(text_block: str) -> list[HTMLNode]:
    lines = text_block.splitlines()
    list_nodes = []
    for line in lines:
        if re.match(r"\d\.", line):
            line_after_space = line.split(" ", 1)[1]
            li_nodes = text_to_children(line_after_space)
            list_nodes.append(ParentNode("li", children=li_nodes))

    return list_nodes


def strip_quotes_by_line(text_block: str) -> str:
    lines = text_block.splitlines()
    stripped_lines = list(map(lambda x: x.lstrip("> "), lines))
    stripped_block = "\n".join(stripped_lines)
    return stripped_block


def strip_backticks_by_line(text_block: str) -> HTMLNode:
    lines = text_block.split("\n")
    content = "\n".join(lines[1:-1]) + "\n"
    code_node = TextNode(text=content, text_type=TextType.TEXT_CODE)
    html_code_node = text_node_to_html_node(code_node)
    return html_code_node


def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if not line.startswith("# "):
            continue

        line_split = line.split()
        title = " ".join(line_split[1:])
        return title

    raise ValueError("No title found")
