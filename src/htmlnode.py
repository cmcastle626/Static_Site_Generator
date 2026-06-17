class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        if self.props == None or len(self.props) < 1:
            return ""
        val = ""
        for prop in self.props:
            val += f'{prop}="{self.props[prop]}" '
        val = val[:-1]
        return val
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None:
            raise ValueError("missing children")
        res = f"<{self.tag}>"
        for child in self.children:
            res += child.to_html()
        res += f"</{self.tag}>"
        return res
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

