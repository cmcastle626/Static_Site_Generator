from textnode import TextNode, TextType

def main():
    text_object = TextNode("This is some anchor text", TextType("**Bold text**"), "https://www.boot.dev")
    print(f"{text_object}")

main()