import os
import subprocess
import zipfile

# Collect the Windows event logs and initialize files list
event_logs_path = os.path.join(os.environ["SystemRoot"], "System32", "winevt", "Logs")
files = []
if os.path.exists(event_logs_path):
    for filename in os.listdir(event_logs_path):
        if filename.endswith(".evtx"):
            files.append(os.path.join(event_logs_path, filename))

# Zip up all the collected files
hostname = subprocess.check_output("hostname", shell=True).strip().decode("utf-8")
zip_filename = f"{hostname}_forensic_artifacts.zip"
target_dir = "C:\\temp\\XDR\\forenics\\lite-triage\\"
os.makedirs(target_dir, exist_ok=True)
zip_filepath = os.path.join(target_dir, zip_filename)
with zipfile.ZipFile(zip_filepath, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
    for file_path in files:
        try:
            zip_file.write(file_path)
        except OSError as e:
            print(f"Skipping file {file_path}: {e}")

print(f"All artifacts have been collected and saved to {zip_filepath}")
