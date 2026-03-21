import os, shutil

from src.md2html import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dst_path):
    print(f"generating page from {from_path} to {dst_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_data = f.read()

    with open(template_path, "r") as f:
        template_data = f.read()

    html_nodes = markdown_to_html_node(markdown_data)
    html_data = html_nodes.to_html()
    page_title = extract_title(markdown_data)

    template_data = template_data.replace("{{ Title }}", page_title)
    template_data = template_data.replace("{{ Content }}", html_data)

    with open(dst_path, "w") as f:
        f.write(template_data)


def rm_dir_content(path: str):
    try:
        print(f"Attempting directory removal: {path}")
        shutil.rmtree(path)
        print("Directory removed successfully")
    except Exception as e:
        print(f"could not remove directory: {path}", e)


def copy_dir_content(src: str, dst: str):
    shutil.copytree(src, dst)


def main():
    # remove public/ dir
    rm_dir_content("public/")
    # copy content from src to dst
    copy_dir_content("static/", "public/")
    # generate page and write to dst path
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
