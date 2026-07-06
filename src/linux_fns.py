import os
import shutil

def source_to_target_directory(fpath_source: str, fpath_target: str) -> None:
    if not os.path.exists(fpath_source):
            os.mkdir(fpath_target)

    for filename in os.listdir(fpath_source):
        from_path = os.path.join(fpath_source, filename)
        dest_path = os.path.join(fpath_target, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            source_to_target_directory(from_path, dest_path)

    
