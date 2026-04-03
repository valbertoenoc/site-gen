import os, shutil
from pathlib import Path

from src.md2html import extract_title, markdown_to_html_node


def convert_root_to_dst_dir(input_path, dst_path):
    input_parts = list(Path(input_path).parts)
    input_parts[0] = dst_path
    return Path(*input_parts)


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

    if not os.path.exists(dst_path):
        # print(f"Destination directory does not exist. Creating: {dst_path}")
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(dst_path, "w") as f:
        f.write(template_data)


def generate_page_recursive(dir_path_content, template_path, dst_dir_path):
    print(
        f"generating page from {dir_path_content} to {dst_dir_path} using {template_path}"
    )

    for root, _, files in os.walk(dir_path_content):
        for filename in files:
            # input file path markdown
            md_fullpath = os.path.join(root, filename)
            # print("md_fullpath - ", md_fullpath)

            # output file path html
            if filename != "index.md":
                html_dst_fullpath = md_fullpath.replace(".md", "/index.html")
            else:
                html_dst_fullpath = Path(md_fullpath).with_suffix(".html")

            html_dst_fullpath = convert_root_to_dst_dir(html_dst_fullpath, dst_dir_path)
            # print("html_dst_fullpath", html_dst_fullpath)

            # full md content to public html
            generate_page(md_fullpath, template_path, html_dst_fullpath)


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
    # # generate page and write to dst path
    # generate_page("content/index.md", "template.html", "public/index.html")

    # generate page and write to dst path recursively
    generate_page_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
