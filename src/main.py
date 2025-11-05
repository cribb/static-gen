from textnode import TextNode, TextType
def main():
    anchortext = "This is some anchor text"
    url = "https://www.boot.dev"
    tn = TextNode(text=anchortext, 
                  text_type=TextType.HTML_LINK, 
                  url=url)

    print(tn)





main()