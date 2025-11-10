import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

