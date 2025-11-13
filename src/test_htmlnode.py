import unittest
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        tag = "a"
        value = "This is an html node."
        children = []
        props = {}
        props['href'] = "https://www.boot.dev"

        htmlnode = HTMLNode(tag=tag, value=value, children=children, props=props)
        # print(htmlnode)
        # print(f"HTML conversion to: {htmlnode.props_to_html()}.")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD text node")
    
    def test_link(self):
        node = TextNode("This is a LINK node", TextType.LINK, url="www.yahoo.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a LINK node")
        self.assertEqual(html_node.props['href'], "www.yahoo.com")

    def test_image(self):
        node = TextNode("This is an IMAGE node", TextType.IMAGE, url="www.blah.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props['src'], "www.blah.com/image.jpg")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")      

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "My link to blah.com", props={"href":"www.blah.com"})
        self.assertEqual(node.to_html(), "<a href=\"www.blah.com\">My link to blah.com</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "text")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>text</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild-text")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild-text</b></span></div>")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

# class TestHTMLNode(unittest.TestCase):
#     def test_to_html_props(self):
#         node = HTMLNode(
#             "div",
#             "Hello, world!",
#             None,
#             {"class": "greeting", "href": "https://boot.dev"},
#         )
    
#    def test_values(self):
#         node = HTMLNode(
#             "div",
#             "I wish I could read",
#         )
#         self.assertEqual(
#             node.tag,
#             "div",
#         )
#         self.assertEqual(
#             node.value,
#             "I wish I could read",
#         )
#         self.assertEqual(
#             node.children,
#             None,
#         )

if __name__ == "__main__":
    unittest.main()

