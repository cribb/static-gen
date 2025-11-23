import unittest
import os
import shutil
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from md_handler import *


class TestMain(unittest.TestCase):

    def test_generate_page(self):
        result = 0
        answer = 0
        self.assertEqual(result,answer)


    def test_generate_pages_recursive(self):
        result = 0
        answer = 0
        self.assertEqual(result,answer)


if __name__ == "__main__":
    unittest.main()
