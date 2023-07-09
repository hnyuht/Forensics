import os
import shutil
import zipfile
import subprocess

# Define the artifacts to collect
artifacts = {
    'OS release information': '/etc/os-release',
    'User accounts information': '/etc/passwd',
    'User group information': '/etc/group',
    'Sudoers list': '/etc/sudoers',
    'Login information': '/var/log/wtmp',
    'Authentication logs': '/var/log/auth.log',
    'Cron jobs': '/etc/crontab',
    'Services': '/etc/init.d/',
    'Bash shell startup': [
        '/home/<user>/.bashrc',
        '/etc/bash.bashrc',
        '/etc/profile'
    ],
    'Persistence mechanism - Authentication logs': '/var/log/auth.log*',
    'Persistence mechanism - Bash history': '/home/<user>/.bash_history',
    'Persistence mechanism - Vim history': '/home/<user>/.viminfo',
    'Syslogs': '/var/log/syslog',
    'Third-party logs': '/var/log/',
    'Hostname': '/etc/hostname',
    'Timezone information': '/etc/timezone',
    'Network Interfaces': '/etc/network/interfaces',
    'DNS information - Hostname resolutions': '/etc/hosts',
    'DNS information - DNS servers': '/etc/resolv.conf'
}

# Define the output directory and log file path
output_dir = '/tmp/xdr'
log_file = os.path.join(output_dir, 'error_logs.txt')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get the hostname
hostname = subprocess.check_output('hostname', shell=True, text=True).strip()

# Create a zip file with the hostname as the filename
zip_filename = f'{hostname}_xdr_linux_triage.zip'
zip_filepath = os.path.join(output_dir, zip_filename)

# Create a log file for errors
with open(log_file, 'w', encoding='utf-8') as f:
    f.write('')

# Collect the artifacts and add them to the zip file
with zipfile.ZipFile(zip_filepath, 'w') as zipf:
    for artifact, path in artifacts.items():
        if isinstance(path, list):
            for file_path in path:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        output = f.read()
                    zipf.writestr(f'{artifact}/{os.path.basename(file_path)}', output)
                except Exception as e:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f'Error collecting {file_path}: {str(e)}\n')
        else:
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    output = f.read()
                zipf.writestr(f'{artifact}/{os.path.basename(path)}', output)
            except Exception as e:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f'Error collecting {path}: {str(e)}\n')

# Move the log file to the output directory
shutil.move(log_file, os.path.join(output_dir, 'error_logs.txt'))
