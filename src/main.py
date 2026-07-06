from linux_fns import source_to_target_directory
from generate_page_fns import generate_pages_recursive
import os
import shutil

def main():
    fpath_target = r"./public"
    fpath_source = r"./static"
    print("Deleting public directory...")
    if os.path.exists(fpath_target):
        shutil.rmtree(fpath_target)
    source_to_target_directory(fpath_source, fpath_target)
    
    from_path = "./content"
    dest_path = "./public"
    template_path = "./template.html"
    generate_pages_recursive(from_path, template_path, dest_path)


main()