import os
import shutil
import zipfile
import socket


def collect_bash_history(destination_dir):
    bash_history_dir = os.path.expanduser("~")
    bash_history_path = os.path.join(bash_history_dir, ".bash_history")
    if os.path.exists(bash_history_path):
        shutil.copy2(bash_history_path, os.path.join(destination_dir, "bash_history"))

def collect_network_interfaces(destination_dir):
    # Use the 'ip' command to retrieve network interface details
    ip_output = subprocess.check_output(["ip", "link"], universal_newlines=True)
    with open(os.path.join(destination_dir, "network_interfaces"), "w") as file:
        file.write(ip_output)

def collect_os_information(destination_dir):
    shutil.copy2("/etc/os-release", os.path.join(destination_dir, "os_release"))
    shutil.copy2("/etc/issue", os.path.join(destination_dir, "issue"))


def collect_recent_files(destination_dir):
    shutil.copytree(os.path.expanduser("~/.local/share/recently-used.xbel"), os.path.join(destination_dir, "recently_used"))


def collect_scheduled_tasks(destination_dir):
    shutil.copytree("/etc/cron.d", os.path.join(destination_dir, "cron_d"))
    shutil.copytree("/etc/cron.daily", os.path.join(destination_dir, "cron_daily"))
    shutil.copytree("/etc/cron.hourly", os.path.join(destination_dir, "cron_hourly"))
    shutil.copytree("/etc/cron.monthly", os.path.join(destination_dir, "cron_monthly"))
    shutil.copytree("/etc/cron.weekly", os.path.join(destination_dir, "cron_weekly"))


def collect_ssh_activity(destination_dir):
    shutil.copytree("/var/log/auth.log", os.path.join(destination_dir, "auth_log"))


def collect_startup_items(destination_dir):
    shutil.copytree("/etc/init.d", os.path.join(destination_dir, "init_d"))
    shutil.copytree("/etc/rc.local", os.path.join(destination_dir, "rc_local"))


def collect_system_logs(destination_dir):
    shutil.copytree("/var/log", os.path.join(destination_dir, "var_log"))


def collect_trash(destination_dir):
    shutil.copytree(os.path.expanduser("~/.local/share/Trash"), os.path.join(destination_dir, "trash"))


def collect_user_accounts(destination_dir):
    shutil.copy2("/etc/passwd", os.path.join(destination_dir, "passwd"))
    shutil.copy2("/etc/group", os.path.join(destination_dir, "group"))
    shutil.copy2("/etc/shadow", os.path.join(destination_dir, "shadow"))


# Get the hostname of the system
hostname = socket.gethostname()

# Create a directory to store the collected artifacts
destination_dir = os.path.join("/tmp/xdr/triage", hostname)
os.makedirs(destination_dir, exist_ok=True)

# Collect Linux artifacts
collect_bash_history(destination_dir)
collect_network_interfaces(destination_dir)
collect_os_information(destination_dir)
collect_recent_files(destination_dir)
collect_scheduled_tasks(destination_dir)
collect_ssh_activity(destination_dir)
collect_startup_items(destination_dir)
collect_system_logs(destination_dir)
collect_trash(destination_dir)
collect_user_accounts(destination_dir)

# Compress the collected artifacts into a zip file
zip_filename = os.path.join("/tmp/xdr/triage", f"{hostname}_triage.zip")
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as archive:
    for root, dirs, files in os.walk(destination_dir):
        for file in files:
            file_path = os.path.join(root, file)
            archive_path = os.path.relpath(file_path, destination_dir)
            archive.write(file_path, archive_path)

# Clean up the temporary directory
shutil.rmtree(destination_dir)
