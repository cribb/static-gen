import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        tag = "a"
        value = "This is an html node."
        children = []
        props = {}
        props['href'] = "https://www.boot.dev"

        htmlnode = HTMLNode(tag=tag, value=value, children=children, props=props)
        print(htmlnode)
        print("HTML conversion to:\n")
        print(htmlnode.props_to_html())

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")      

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "mylink", props={"href":"www.blah.com"})
        self.assertEqual(node.to_html(), "<a href=\"www.blah.com\">mylink</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

