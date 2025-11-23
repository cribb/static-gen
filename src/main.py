import os
import glob
import shutil
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from md_handler import *

def prep_public_path(static_path, public_path):

    if os.path.exists(public_path):
        print("Removing public path for fresher instance.")
        shutil.rmtree(public_path)

    shutil.copytree(static_path, public_path)

    return

def generate_page(from_path, template_path, dest_file):
    print(f"Generating page from {from_path} to {dest_file}, using {template_path}.")

    file_ptr = open(from_path,mode='r')
    page_contents_md = file_ptr.read()
    file_ptr.close()

    template_ptr = open(template_path, mode='r')
    page = template_ptr.read()
    template_ptr.close()

    title = extract_title(page_contents_md)
    hnode = markdown_to_html_node(page_contents_md)
    html = hnode.to_html()


    newpage = page.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html)

    # print("Resulting page...")
    # print(newpage)


    dest_dir = os.path.dirname(dest_file)
    print(f"Destination directory for file: {dest_dir}")
    if not os.path.isdir(dest_dir):
        print("Destination directory does not exist. Creating now...")
        os.makedirs(dest_dir)
    
    os.path.isfile(dest_file)

    dest_file_ptr = open(dest_file,mode="w")
    print(f'Writing destination html file: {dest_file}.')
    dest_file_ptr.write(newpage)
    dest_file_ptr.close()

    print(f"Title: {title}")
    # print("Markdown to html:")
    # print(html)
    
    # print("Template contents:")
    # print(template_contents_html)

    return
    
def generate_pages_recursive(dir_content_path, template_file, dest_dir_path):
    filelist = []
    for item in os.walk(dir_content_path):
        print(f"item: {item}")
        for file in glob.glob(os.path.join(item[0], "*.md")):
            filelist.append(file)
        
    print(f"Filelist: {filelist}")
    # generate_page(from_path, template_path, dest_file):
    for md_filename in filelist:
        site_filename = md_filename.replace(dir_content_path, dest_dir_path)
        html_filename = site_filename.replace(".md", ".html")
        print(f"source Markdown file: {md_filename}")
        print(f"destination html file: {html_filename}")
        generate_page(md_filename, template_file, html_filename)
    
    return

def main():
    root_path = "/home/jeremy/src/bootdev/static-gen/"
    static_path = root_path + "static/"
    public_path = root_path + "public/"
    content_path = root_path + "content/"

    index_file = content_path + "index.md"
    template_file = root_path + "template.html"
    dest_file = public_path + "index.html"

    print('Static Site Generator')
    print("---------------------")
    if os.path.exists(root_path):
        print(f"Root path: {root_path}")    
    if os.path.exists(static_path):
        print(f"Static path: {static_path}")
    if os.path.exists(public_path):
        print(f"Public path: {public_path}")
    if os.path.exists(content_path):
        print(f"Content path: {content_path}")
    if os.path.exists(index_file):
        print(f"Index file: \"{index_file}\" found.")
    else:
        raise FileNotFoundError("Index html file not found.")

    if os.path.exists(template_file):
        print(f"Template file: \"{template_file}\" found.")
    else:
        raise FileNotFoundError("Template html file not found.")
    


    prep_public_path(static_path, public_path)
    generate_pages_recursive(content_path, template_file, public_path)
    # stage_site(content_path, public_path)
    # generate_page(index_file, template_file, dest_file)

    return 


main()