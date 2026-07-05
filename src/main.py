from linux_fns import source_to_target_directory

def main():
    fpath_target = r"/home/chloe/workspace/bootdotdev/curriculum/Static_Site_Generator/public"
    fpath_source = r"/home/chloe/workspace/bootdotdev/curriculum/Static_Site_Generator/static"
    source_to_target_directory(fpath_source, fpath_target)
    

main()