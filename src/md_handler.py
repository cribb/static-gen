# markdown
import re
from textnode import TextNode, TextType

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

def markdown_to_blocks(markdown):
    pass


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

