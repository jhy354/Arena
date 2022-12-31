import os
from shutil import copytree
from shutil import rmtree
from pathlib import Path

retained_files = [
    "assets",
    "pygame",
    "main.exe",
    "_socket.pyd",
    "base_library.zip",
    "pyexpat.pyd",
    "select.pyd"
]

retained_keywords = [
    "python",
    "SDL",
    "lib"
]

if __name__ == "__main__":
    root_path = Path(r"./").absolute()
    path = Path(r"./dist/main/").absolute()

    print("Cleaning files...")
    if os.path.exists("./build"):
        rmtree("./build")
    if os.path.exists("./dist"):
        rmtree("./dist")
    print("DONE")

    print("Building...")
    os.system("pyinstaller --icon=logo.ico -w main.py --upx-dir=" + str(root_path))
    print("DONE")

    print("Removing files...")
    for file_name in os.listdir(path):
        if file_name not in retained_files:
            flag = False
            for keyword in retained_keywords:
                if keyword in str(file_name):
                    flag = True
            if not flag:
                try:
                    os.remove(str(path) + "\\" + str(file_name))
                except FileNotFoundError:
                    pass
    print("DONE")

    print("Copying files...")
    copytree(r"./assets", str(path) + "\\" + "assets")
    print("DONE")

    print("Renaming files...")
    os.rename("./dist/main/main.exe", "./dist/main/Arena.exe")
    os.rename("./dist/main", "./dist/Arena")
    print("DONE")
