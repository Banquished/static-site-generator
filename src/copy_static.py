import os
import shutil


# Write a recursive function that copies all the contents from a source directory
# to a destination directory. (in our case, `static` to `public`).
def copy_directory(src: str, dst: str) -> None:
    # 1. It should first delete all the contents of the destination directory (public)
    #    to ensure that the copy is clean.
    if os.path.exists(dst):
        shutil.rmtree(dst)  # Delete the destination directory and its contents

    # 2. Recursively copy all contents from src to dst
    _copy_recursive(src, dst)  # Call the recursive copy function


def _copy_recursive(src: str, dst: str) -> None:
    # Ensure the destination directory exists
    os.makedirs(dst, exist_ok=True)

    # Iterate through each item in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)  # Get the full path of the source item
        dst_path = os.path.join(dst, item)  # Get the full path of the destination item

        if os.path.isdir(src_path):
            # Recursively handle nested subdirectories
            _copy_recursive(src_path, dst_path)
        else:
            # Log and copy individual files
            print(f"Copied file: {src_path} to {dst_path}")
            shutil.copy2(src_path, dst_path)  # Copy the file with metadata
