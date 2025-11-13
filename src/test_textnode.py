import unittest

from textnode import TextNode, TextType
from textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import extract_markdown_images, extract_markdown_links, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a **bold** text node", TextType.BOLD)
        node2 = TextNode("This is a **bold** text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is an _italic_ text node", TextType.ITALIC)
        node2 = TextNode("This is an _italic_ text node", TextType.ITALIC)
        self.assertEqual(node, node2)

        node = TextNode("This is an _italic_ text node", TextType.ITALIC, url=None)
        node2 = TextNode("This is an _italic_ text node", TextType.ITALIC)
        self.assertEqual(node, node2)

        node = TextNode("This is a **bold** text node", TextType.BOLD, url=None)
        node2 = TextNode("This is an _italic_ text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This text contains an _italics_ section.", TextType.TEXT)
        nodelist = split_nodes_delimiter([node], "_", TextType.ITALIC)
        exp_nodelist = [ 
                        TextNode("This text contains an ", TextType.TEXT),
                        TextNode("italics", TextType.ITALIC),
                        TextNode(" section.", TextType.TEXT)
                       ]
        self.assertEqual(nodelist, exp_nodelist)

        node = TextNode("This text contains a `code block` section.", TextType.TEXT)
        nodelist = split_nodes_delimiter([node], "`", TextType.CODE)
        exp_nodelist = [ 
                        TextNode("This text contains a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" section.", TextType.TEXT)
                       ]
        self.assertListEqual(nodelist, exp_nodelist)

        node = TextNode("This text contains a `code block` section.", TextType.TEXT)
        nodelist = split_nodes_delimiter([node, node], "`", TextType.CODE)
        exp_nodelist = [ 
                        TextNode("This text contains a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" section.", TextType.TEXT),
                        TextNode("This text contains a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" section.", TextType.TEXT)
               ]        
        self.assertListEqual(nodelist, exp_nodelist)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another copy of the image ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,        
        )


    

if __name__ == "__main__":
    unittest.main()

