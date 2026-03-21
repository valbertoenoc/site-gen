class HTMLNode:
    def __init__(
        self, tag=None, value=None, children=None, props: dict[str, str] = {}
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        props_str = ""
        for k, v in self.props.items():
            props_str += f' {k}="{v}"'

        return props_str

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: dict[str, str] = {}) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: dict[str, str] = {}) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")

        if self.children is None:
            raise ValueError("parent without children is not allowed")

        parts = []
        for child in self.children:
            parts.append(child.to_html())
        inner = "".join(parts)

        return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"
