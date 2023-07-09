import os
import subprocess
import shutil
import zipfile

# Define the artifacts and their commands
artifacts = {
    'generic': [
        'env',
        'uptime',
        'uname -a',
        'lsmod',
        '/etc/passwd',
        '/etc/group',
        'date',
        'who',
        'cpuinfo',
        'lsof',
        'sudoers',
        'mount',
        'fstab',
        'last'
    ],
    'ssh': [
        'authorized_keys',
        'known_hosts'
    ],
    'network': [
        'ip',
        'netstat',
        'arp'
    ],
    'processus': [
        'ps'
    ],
    'browsers': [
        'firefox',
        'google chrome',
        'chromium'
    ],
    'log': [
        '/var/log/auth.log',
        '/var/log/syslog'
    ],
    'home': [
        '.gitconfig',
        '.bash_history',
        '.zsh_history',
        '.viminfo'
    ],
    'desktop': [
        '.local/share/Trash'
    ],
    'files': [
        'hashes.md5',
        'file perm',
        'timeline'
    ],
    'dump': [
        'avml',
        'LiME',
        '/boot/System.map-$(uname -r)',
        '/boot/vmlinuz'
    ],
    'antivirus': [
        'CLAMAV'
    ]
}

# Define the output directory and log file path
output_dir = '/tmp/xdr/traige'
log_file = os.path.join(output_dir, 'ERRORS.log')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get the hostname
hostname = os.uname().nodename

# Create a zip file with the hostname as the filename
zip_filename = f'{hostname}_linux_xdr_traige.zip'
zip_filepath = os.path.join(output_dir, zip_filename)

# Create a log file for errors
with open(log_file, 'w') as f:
    f.write('')

# Collect the artifacts and add them to the zip file
with zipfile.ZipFile(zip_filepath, 'w') as zipf:
    for category, commands in artifacts.items():
        for command in commands:
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode('utf-8')
                zipf.writestr(f'{category}/{command}.txt', output)
            except subprocess.CalledProcessError:
                with open(log_file, 'a') as f:
                    f.write(f'Error collecting {command} in {category}\n')

# Copy the log file to the zip file
shutil.copy(log_file, os.path.join(output_dir, 'ERRORS.log'))
