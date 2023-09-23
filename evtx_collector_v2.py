import os
import subprocess
import zipfile
from tqdm import tqdm

class EventLogCollector:
    def __init__(self):
        self.event_logs_path = os.path.join(os.environ["SystemRoot"], "System32", "winevt", "Logs")
        self.files = []

    def collect_logs(self):
        if os.path.exists(self.event_logs_path):
            for filename in os.listdir(self.event_logs_path):
                if filename.endswith(".evtx"):
                    self.files.append(os.path.join(self.event_logs_path, filename))

class ZipFileCreator:
    def __init__(self):
        self.target_dir = "C:\\temp\\XDR\\forenics\\lite-triage\\"
        self.hostname = subprocess.check_output("hostname", shell=True).strip().decode("utf-8")
        self.zip_filename = f"{self.hostname}_forensic_artifacts.zip"
        self.zip_filepath = os.path.join(self.target_dir, self.zip_filename)

    def create_zip_file(self, files):
        os.makedirs(self.target_dir, exist_ok=True)
        with zipfile.ZipFile(self.zip_filepath, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in tqdm(files, desc="Zipping files", unit="file", unit_scale=True, dynamic_ncols=True):
                try:
                    zip_file.write(file_path)
                except OSError as e:
                    print(f"Skipping file {file_path}: {e}")

if __name__ == "__main__":
    event_log_collector = EventLogCollector()
    event_log_collector.collect_logs()

    zip_file_creator = ZipFileCreator()
    zip_file_creator.create_zip_file(event_log_collector.files)

    print(f"All artifacts have been collected and saved to {zip_file_creator.zip_filepath}")
