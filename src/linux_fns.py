import os
import shutil

def source_to_target_directory(fpath_source: str, fpath_target: str) -> None:
    if not os.path.exists(fpath_source):
        raise Exception("source directory does not exist")
    if os.path.exists(fpath_target):
        shutil.rmtree(fpath_target)
    os.mkdir(fpath_target)
    dir_to_copy = os.listdir(fpath_source)
    for item in dir_to_copy:
        fpath_item_source = os.path.join(fpath_source, item)
        if os.path.isfile(fpath_item_source):
            shutil.copy(fpath_item_source, fpath_target)
        elif os.path.isdir(fpath_item_source):
            fpath_item_target = os.path.join(fpath_target, item)
            os.mkdir(fpath_item_target)
            source_to_target_directory(fpath_item_source, fpath_item_target)
        else:
            raise Exception("Items to be copied must be either files or directoriess")

    
