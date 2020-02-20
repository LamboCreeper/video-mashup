import os


def empty_directory(directory: str):
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(os.path.join(root, file))
