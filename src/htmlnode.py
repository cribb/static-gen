
class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        report  = f"__HTMLNode__\n"
        report += f"tag: {self.tag}\n"
        report += f"value: {self.value}\n"
        report += f"children: \n"
        if self.children:
            for child in self.children:
                report += f" --> {child}\n"
        report += f"properties: \n"
        if self.props:
            for prop in self.props:
                report += f" --> {prop}: {self.props[prop]}\n"    
        report += "\n"
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
    def __init__(self, tag, value, children, props)