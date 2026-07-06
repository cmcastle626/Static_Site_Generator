from linux_fns import source_to_target_directory
from generate_page_fns import generate_pages_recursive
import os, shutil
import sys

copy_from = r"./static"
copy_to = r"./docs"
from_path = "./content"
dest_path = "./docs"
template_path = "./template.html"

def main():
    basepath = sys.argv[1]
    if len(basepath)<1:
        basepath = "/"
    print(f"basepath: {basepath}")

    print("Deleting public directory...")
    if os.path.exists(copy_to):
        shutil.rmtree(copy_to)
    print("Copying static files to public directory...")
    source_to_target_directory(copy_from, copy_to)
    
    print("Generating content...")
    generate_pages_recursive(from_path, template_path, dest_path, basepath)


main()