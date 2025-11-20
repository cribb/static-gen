import os
import shutil
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from md_handler import *

def prep_public_path(static_path, public_path):

    if os.path.exists(public_path):
        print("Removing public path for freshening.")
        shutil.rmtree(public_path)

    # shutil.copytree(static_path, public_path)
    

def main():
    root_path = "/home/jeremy/src/bootdev/static-gen/"
    static_path = rootpath + "static/"
    public_path = rootpath + "public/"
    
    prep_public_path(static_path, public_path)




main()