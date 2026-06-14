from copy_static import copy_directory
from generate_pages import generate_pages_recursive


def main() -> None:
    print("Starting static site generation...")
    print("-" * 50)
    # Call the copy_directory function to copy contents from 'static' to 'public'
    copy_directory("static", "public")
    print("Static files copied successfully!")
    print("-" * 50)
    # Generate pages recursively from the `content` directory using `template.html` and write them to the `public` directory.
    generate_pages_recursive("content", "template.html", "public")
    print("Pages generated successfully!")
    print("-" * 50)
    print("Static site generation completed!")
    print("-" * 50)


if __name__ == "__main__":
    main()
