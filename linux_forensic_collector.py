import os
import shutil
import zipfile
import subprocess

# Define the artifacts to collect with their descriptions
artifacts = {
    'OS release information': {
        'path': '/etc/os-release',
        'description': 'OS release information'
    },
    'User accounts information': {
        'path': '/etc/passwd',
        'description': 'User accounts information'
    },
    'User group information': {
        'path': '/etc/group',
        'description': 'User group information'
    },
    'Sudoers list': {
        'path': '/etc/sudoers',
        'description': 'Sudoers list'
    },
    'Login information': {
        'path': '/var/log/wtmp',
        'description': 'Login information'
    },
    'Authentication logs': {
        'path': '/var/log/auth.log',
        'description': 'Authentication logs'
    },
    'Cron jobs': {
        'path': '/etc/crontab',
        'description': 'Cron jobs'
    },
    'Services': {
        'path': '/etc/init.d/',
        'description': 'Registered services'
    },
    'Bash shell startup': {
        'path': [
            '/home/<user>/.bashrc',
            '/etc/bash.bashrc',
            '/etc/profile'
        ],
        'description': 'Bash shell startup'
    },
    'Persistence mechanism - Authentication logs': {
        'path': '/var/log/auth.log*',
        'description': 'Persistence mechanism - Authentication logs'
    },
    'Persistence mechanism - Bash history': {
        'path': '/home/<user>/.bash_history',
        'description': 'Persistence mechanism - Bash history'
    },
    'Persistence mechanism - Vim history': {
        'path': '/home/<user>/.viminfo',
        'description': 'Persistence mechanism - Vim history'
    },
    'Syslogs': {
        'path': '/var/log/syslog',
        'description': 'Syslogs'
    },
    'Third-party logs': {
        'path': '/var/log/',
        'description': 'Third-party logs'
    },
    'Log files - /root/.bash_history': {
        'path': '/root/.bash_history',
        'description': 'Root Bash history'
    },
    'Log files - /var/log/daemon.log': {
        'path': '/var/log/daemon.log',
        'description': 'Daemon log'
    },
    'Log files - /var/log/syslog': {
        'path': '/var/log/syslog',
        'description': 'System log'
    },
    'Log files - /var/log/btmp': {
        'path': '/var/log/btmp',
        'description': 'Bad login attempts log'
    },
    'Log files - /var/log/wtmp': {
        'path': '/var/log/wtmp',
        'description': 'Login information log'
    },
    'Log files - /etc/dnsmasq.conf': {
        'path': '/etc/dnsmasq.conf',
        'description': 'DNSMasq configuration'
    },
    'Log files - /etc/wpa_supplicant/*.conf': {
        'path': '/etc/wpa_supplicant/*.conf',
        'description': 'WPA Supplicant configuration'
    }
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
    for artifact, config in artifacts.items():
        path = config['path']
        description = config['description']
        if isinstance(path, list):
            for file_path in path:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        output = f.read()
                    zipf.writestr(f'{description}/{os.path.basename(file_path)}', output)
                except Exception as e:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f'Error collecting {file_path}: {str(e)}\n')
        elif '*' in path:
            try:
                file_list = subprocess.check_output(f'ls {path}', shell=True, text=True, stderr=subprocess.DEVNULL).split('\n')
                for file_path in file_list:
                    if file_path.strip():
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                            output = f.read()
                        zipf.writestr(f'{description}/{os.path.basename(file_path)}', output)
            except Exception as e:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f'Error collecting {path}: {str(e)}\n')
        else:
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    output = f.read()
                zipf.writestr(f'{description}/{os.path.basename(path)}', output)
            except Exception as e:
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f'Error collecting {path}: {str(e)}\n')

# Move the log file to the output directory
shutil.move(log_file, os.path.join(output_dir, 'error_logs.txt'))
