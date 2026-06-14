from copy_static import copy_directory
from generate_pages import generate_page


def main() -> None:
    print("Starting static site generation...")
    print("-" * 50)
    # Call the copy_directory function to copy contents from 'static' to 'public'
    copy_directory("static", "public")
    print("Static files copied successfully!")
    print("-" * 50)
    # Generate a page from `content/index.md` using `template.html` and write it to `public/index.html`.
    generate_page("content/index.md", "template.html", "public/index.html")
    print("Page generated successfully!")
    print("-" * 50)
    print("Static site generation completed!")
    print("-" * 50)


if __name__ == "__main__":
    main()
