# markdown
import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING   = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
                 
def split_nodes_delimiter(old_node_list, delimiter, text_type):
    
    new_node_list = []

    for node in old_node_list:
        if node.text_type is not TextType.TEXT:
            # print('Text type is not TEXT, so passing off old node as new node without changes.')
            new_node_list.append(node)
            continue 
        
        if node.text.count(delimiter) % 2 > 0: # not even
            raise ValueError("Invalid Markdown syntax.")
        
        delimited_text = node.text.split(delimiter)

        count = 0
        for chunk in delimited_text:
            if not count % 2:    # `count` is even
                chunk_node = TextNode(chunk, TextType.TEXT)
            else:                # `count` is odd
                chunk_node = TextNode(chunk, text_type)
            
            # print(f"ChunkNode: {chunk_node}")
            new_node_list.append(chunk_node)
            count += 1
        
    return new_node_list


def extract_markdown_images(text):
    # regex -> markdown image tokens ![](): "\!\[(.*?)\]\((.*?)\)""
    # !\[([^\[\]]*)\]\(([^\(\)]*)\)
    markdown_image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(markdown_image_regex, text)
    return matches


def extract_markdown_links(text):
    # regex -> markdown link tokens with negative look-behind to 
    # avoid collisions with image limks: "(?<!\!)\[(.*?)\]\((.*?)\)"
    # "(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    markdown_link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(markdown_link_regex, text)
    return matches


def split_nodes_link(nodelist):
    regex_link_delimiter = r"(?<!!)(\[[^\[\]]*\]\([^\(\)]*\))"

    new_nodelist = []
    
    for node in nodelist:
        # print(f"Node in nodelist: {node}")
        if node.text_type is not TextType.TEXT:
            # print('Text type is not TEXT, so passing off old node as new node without changes.')
            new_nodelist.append(node)
            continue 

        split_list = re.split(regex_link_delimiter, node.text)
        count = 0    
        for chunk in split_list:
            if len(chunk) == 0:
                continue
            if count % 2 == 0:  # i is even
                chunk_node = TextNode(chunk, TextType.TEXT)
            else:  # i is odd (and is an image node)
                tmp = extract_markdown_links(chunk)
                text, url = tmp[0][0], tmp[0][1]
                chunk_node = TextNode(text, TextType.LINK, url=url)
            # print(f"[i={count}, ChunkNode: {chunk_node}]")
            new_nodelist.append(chunk_node)
            count += 1

    return new_nodelist


def split_nodes_image(nodelist):
    regex_image_delimiter = r"(!\[[^\[\]]*\]\([^\(\)]*\))"    

    new_nodelist = []
    
    for node in nodelist:
        # print(f"Node in nodelist: {node}")
        if node.text_type is not TextType.TEXT:
            # print('Text type is not TEXT, so passing off old node as new node without changes.')
            new_nodelist.append(node)
            continue 

        split_list = re.split(regex_image_delimiter, node.text)
        count = 0    
        for chunk in split_list:
            if len(chunk) == 0:
                continue
            if count % 2 == 0:  # i is even
                chunk_node = TextNode(chunk, TextType.TEXT)
            else:  # i is odd (and is an image node)
                tmp = extract_markdown_images(chunk)
                text, url = tmp[0][0], tmp[0][1]
                chunk_node = TextNode(text, TextType.IMAGE, url=url)
            # print(f"[i={count}, ChunkNode: {chunk_node}]")
            new_nodelist.append(chunk_node)
            count += 1

    return new_nodelist

def text_to_textnodes(text):
    starting_node = TextNode(text, TextType.TEXT, url=None)
    nodelist = split_nodes_image([starting_node])
    nodelist = split_nodes_link(nodelist)
    nodelist = split_nodes_delimiter(nodelist, '**', TextType.BOLD)
    nodelist = split_nodes_delimiter(nodelist, '_', TextType.ITALIC)
    nodelist = split_nodes_delimiter(nodelist, '`', TextType.CODE)
    # print(f"NodeList: {nodelist}")
    return nodelist

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    child_nodes = list(map(text_node_to_html_node, textnodes))
    return child_nodes

def markdown_to_blocks(markdown):
    
    split_md = markdown.split('\n\n')
    striplist = list(map(lambda x:x.strip(), split_md))
    blocklist = list(filter(None, striplist))

    return blocklist


def block_to_block_type(md_block):

    split_block = md_block.split(sep=None, maxsplit=1)
    header = split_block[0]
    # N = len(header)
    # print(f"My block header is: {header}, which is {N} characters long.")
    
    # text = md_block.strip(header)
    # print(f"header: {header}")
    # print(f"text: {text}")

    match header:
        case '#' | '##' | '###' | '####' | '#####' | '######':
            return BlockType.HEADING
        case '>':
            return BlockType.QUOTE
        case '```':
            return BlockType.CODE
        case '-':
            return BlockType.UNORDERED_LIST
        case '1.': 
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    hnodes = []
    for block in blocks:
        hnode = block_to_html_node(block)
        print(hnode)
        hnodes.append(hnode)        
    
    return ParentNode("div", hnodes, None)


def block_to_html_node(block):
    blocktype = block_to_block_type(block)

    match blocktype:
        case BlockType.PARAGRAPH:
            return paragraph_to_htmlnode(block)
        case BlockType.HEADING:
            return heading_to_htmlnode(block)
        case BlockType.QUOTE:
            return quote_to_htmlnode(block)         
        case BlockType.CODE:
            return code_to_htmlnode(block)
        case BlockType.UNORDERED_LIST:
            return unorderedlist_to_htmlnode(block)
        case BlockType.ORDERED_LIST:
            return orderedlist_to_htmlnode(block)
        case _:
            raise ValueError("Unknown BlockType")
            

def paragraph_to_htmlnode(block):
    tmp = block.strip()
    pgraph = tmp.replace('\n', ' ')
    children = text_to_children(pgraph)
    return ParentNode("p", children)

def heading_to_htmlnode(block):
    # isolate the #'s that demarcate the heading texttype
    mdheading = r"^(\#{1,6})\s*([^\#]*)\s*"
    tmp = re.findall(mdheading, block)
    heading,text = tmp[0][0],tmp[0][1]
    children = text_to_children(text)
    return ParentNode(f"h{len(heading)}", children)

def quote_to_htmlnode(block):
    # isolate the '>' that demarcates the quote texttype
    text = block.lstrip("> ").strip()
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def code_to_htmlnode(block):
    text = block[4:-3]
    tn = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(tn)
    # child = text_node_to_html_node(textnode)
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])

def unorderedlist_to_htmlnode(block):
    lines = block.split('\n')
    new_lines = list(filter(None, lines))
    list_nodes = []
    for line in new_lines: 
        text = line.lstrip('- ').strip()
        children = text_to_children(text)
        list_nodes.append(ParentNode("li", children))
    return ParentNode("ul", list_nodes)

def orderedlist_to_htmlnode(block):
    lines = block.split('\n')
    new_lines = list(filter(None, lines))
    list_nodes = []
    for line in new_lines:
        text = line[3:].strip()
        children = text_to_children(text)
        list_nodes.append(ParentNode("li", children))
    return ParentNode("ol", list_nodes)




