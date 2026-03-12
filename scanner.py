import os

supported_types = [".pdf", ".docx", ".txt"]

def scan_folder(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_types:
                file_list.append(path)
    return file_list