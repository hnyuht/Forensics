import os
import time

def scan_directory(directory, output_file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(output_file, "w") as file:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_info = {
                    "Filename": filename,
                    "Path": filepath,
                    "Creation Time": time.ctime(os.path.getctime(filepath)),
                    "Last Access Time": time.ctime(os.path.getatime(filepath)),
                    "Modification Time": time.ctime(os.path.getmtime(filepath)),
                    "Size": os.path.getsize(filepath)
                }
                file.write(str(file_info) + "\n")

scan_directory("C:\\", "C:\\temp\\XDR\\file_info.txt")
