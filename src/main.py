import sys

from copy_static import copy_directory
from generate_pages import generate_pages_recursive

if len(sys.argv) > 1:
    print(f"Base path provided: {sys.argv[1]}")
    basepath = sys.argv[1]
else:
    print("No base path provided, using / as default.")
    basepath = "/"


def main() -> None:
    print("Starting static site generation...")
    print("-" * 50)
    # Call the copy_directory function to copy contents from 'static' to 'docs'
    copy_directory("static", "docs")
    print("Static files copied successfully!")
    print("-" * 50)
    # Generate pages recursively from the `content` directory using `template.html` and write them to the `docs` directory.
    generate_pages_recursive("content", "template.html", "docs", basepath=basepath)
    print("Pages generated successfully!")
    print("-" * 50)
    print("Static site generation completed!")
    print("-" * 50)


if __name__ == "__main__":
    main()
