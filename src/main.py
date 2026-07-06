from linux_fns import source_to_target_directory
from generate_page_fns import generating_page
import os
import shutil

def main():
    fpath_target = r"/home/chloe/workspace/bootdotdev/curriculum/Static_Site_Generator/public"
    fpath_source = r"/home/chloe/workspace/bootdotdev/curriculum/Static_Site_Generator/static"
    print("Deleting public directory...")
    if os.path.exists(fpath_target):
        shutil.rmtree(fpath_target)
    source_to_target_directory(fpath_source, fpath_target)
    
    from_path = "./content/index.md"
    dest_path = "./public/index.html"
    template_path = "./template.html"
    generating_page(from_path, template_path, dest_path)


main()