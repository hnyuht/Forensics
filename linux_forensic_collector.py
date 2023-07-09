import os
import shutil
import zipfile
import socket

# Get the hostname of the system
hostname = socket.gethostname()

# Create a directory to store the collected logs and artifacts
destination_dir = "collected_data"
os.makedirs(destination_dir, exist_ok=True)

# Collect logs from /etc and /var/log, including all subdirectories
shutil.copytree("/etc", os.path.join(destination_dir, "etc"), dirs_exist_ok=True)
shutil.copytree("/var/log", os.path.join(destination_dir, "var_log"), dirs_exist_ok=True)

# Get a list of all users on the system
with open("/etc/passwd") as passwd_file:
    users = [line.split(":")[0] for line in passwd_file.readlines()]

# Collect artifacts from the home directory of each user
for user in users:
    shutil.copytree("/home/" + user, os.path.join(destination_dir, "home_" + user), dirs_exist_ok=True)
    # Collect web browser artifacts (Firefox and Chromium)
    if os.path.exists("/home/" + user + "/.mozilla/firefox"):
        shutil.copytree("/home/" + user + "/.mozilla/firefox", os.path.join(destination_dir, "firefox_" + user), dirs_exist_ok=True)
    if os.path.exists("/home/" + user + "/.config/chromium"):
        shutil.copytree("/home/" + user + "/.config/chromium", os.path.join(destination_dir, "chromium" + user), dirs_exist_ok=True)
    # Collect Nautilus artifacts
    if os.path.exists("/home/" + user + "/.config/nautilus"):
        shutil.copytree("/home/" + user + "/.config/nautilus", os.path.join(destination_dir, "nautilus_" + user), dirs_exist_ok=True)
    # Collect Bash history
    if os.path.exists("/home/" + user + "/.bash_history"):
        shutil.copy2("/home/" + user + "/.bash_history", os.path.join(destination_dir, "bash_history_" + user))
    # Collect SSH artifacts
    if os.path.exists("/home/" + user + "/.ssh"):
        shutil.copytree("/home/" + user + "/.ssh", os.path.join(destination_dir, "ssh_" + user), dirs_exist_ok=True)

# Compress the collected logs and artifacts into a zip archive
zip_filename = os.path.join("/tmp/XDR", hostname + ".zip")
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as archive:
    for root, dirs, files in os.walk(destination_dir):
        for file in files:
            file_path = os.path.join(root, file)
            archive_path = os.path.relpath(file_path, destination_dir)
            archive.write(file_path, archive_path)

# Clean up the temporary directory
shutil.rmtree(destination_dir)
