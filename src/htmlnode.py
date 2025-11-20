import enum
from textnode import TextNode, TextType

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        report  = f"HTMLNode- tag:{self.tag}, value: {self.value}, children: "
        if self.children:
            for child in self.children:
                report += f" --> {child}"
        else:
            report += f"None"
        report += f", properties: "
        if self.props:
            for prop in self.props:
                report += f"{prop}: {self.props[prop]} "
        else:
            report += f"None"
    
        return report
    

    def to_html(self):        
        raise NotImplementedError

    def props_to_html(self):
        
        html = ""
        
        if self.props:
            for prop in self.props.items():
                html += f" {prop[0]}=\"{prop[1]}\""  
                # print(f"htmlvar={html}")
        
        return html

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        return (isinstance(other, LeafNode) and 
               self.tag == other.tag and 
               self.value == other.value and
               self.props == other.props)

    def __repr__(self):
        report = f"LeafNode- tag: {self.tag}, value: {self.value}, props: {self.props}"
        return report 
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node contains no value.")
        if self.tag is None:
            return self.value

        props_str = self.props_to_html()
        # print(f"Props_str: {props_str}")
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
       super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode- tag: {self.tag}, children: {self.children}, props: {self.props}"
    
    def __eq__(self, other):
        return (isinstance(other, ParentNode) and 
               self.tag == other.tag and 
               self.children == other.children and
               self.props == other.props)

    def to_html(self):
        # print(f"node: {self}")
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("Parent node contains no children.") 
        
        children_html = ""
        # print(f"Child list: {self.children}")
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
            
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Text type unknown.")
    
    return

