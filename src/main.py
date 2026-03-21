import os, shutil


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


if __name__ == "__main__":
    main()
