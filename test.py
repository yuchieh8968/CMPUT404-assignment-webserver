from urllib import request

import os

url = "deep/"
url2 = "index.html"


def find_file(file_name, directory):
    if file_name[-1] == "/":
        file_name = file_name[:-1]
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            print("fixed file path", os.path.join(root, file_name))
            return os.path.join(root, file_name)
        elif file_name in root:
            print("fixed file path", os.path.join(root)+"/")
            return os.path.join(root)
    return None


find_file(url, ".")
find_file(url2, ".")