class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}
    
    def to_html(self) -> str:
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None) -> None:
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
