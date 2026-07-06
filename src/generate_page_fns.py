from block_convert_fns import markdown_to_html_node
import os

def extract_title(markdown: str):
    clean_markdown = markdown.strip()
    split_markdown = clean_markdown.split("\n")
    if not split_markdown[0].startswith("# "):
        raise Exception("markdown should start with an h1 header")
    title = split_markdown[0].replace("# ","")
    title = title.strip()
    return title

def generating_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path) or not os.path.exists(template_path):
        raise Exception("Content and/or template path do not exist")
    
    dir_dest = os.path.dirname(dest_path)
    if not os.path.exists(dir_dest):
        os.makedirs(dir_dest)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    markdown = from_file.read()
    from_file.close()
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    
    converted_markdown_to_html = markdown_to_html_node(markdown)
    html_result = converted_markdown_to_html.to_html()
    title = extract_title(markdown)
    modified_template = template.replace("{{ Title }}", title)
    modified_template = modified_template.replace("{{ Content }}", html_result)

    new_file = open(dest_path, "w+")
    new_file.write(modified_template)
    new_file.close()

