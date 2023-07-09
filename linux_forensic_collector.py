import os
import shutil
import zipfile
import subprocess

# Define the artifacts to collect with their descriptions
artifacts = {
    'OS release information': {
        'path': '/etc/os-release',
        'description': 'Details about the operating system installed on the system. It typically includes information such as the name of the operating system, version, and other release-specific details.'
    },
    'User accounts information': {
        'path': '/etc/passwd',
        'description': 'Information about user accounts on the system.'
    },
    'User group information': {
        'path': '/etc/group',
        'description': 'Information about user groups on the system.'
    },
    'Sudoers list': {
        'path': '/etc/sudoers',
        'description': 'List of users or groups with sudo (superuser) access.'
    },
    'Login information': {
        'path': '/var/log/wtmp',
        'description': 'Records of login and logout events.'
    },
    'Authentication logs': {
        'path': '/var/log/auth.log',
        'description': 'Logs related to authentication events, such as successful and failed login attempts.'
    },
    'Cron jobs': {
        'path': '/etc/crontab',
        'description': 'Scheduled tasks and cron jobs configured on the system.'
    },
    'Services': {
        'path': '/etc/init.d/',
        'description': 'List of registered services and their configurations.'
    },
    'Bash history': {
        'path': '/home/<user>/.bash_history',
        'description': 'Command history of the Bash shell for each user.'
    },
    'Persistence mechanism - Vim history': {
        'path': '/home/<user>/.viminfo',
        'description': 'Command history and settings of the Vim text editor for each user.'
    },
    'Root Bash history': {
        'path': '/root/.bash_history',
        'description': 'Command history of the Bash shell for the root user.'
    },
    'Daemon log': {
        'path': '/var/log/daemon.log',
        'description': 'Log file containing information about system daemons.'
    },
    'Bad login attempts log': {
        'path': '/var/log/btmp',
        'description': 'Log file recording unsuccessful login attempts.'
    },
    'DNSMasq configuration': {
        'path': '/etc/dnsmasq.conf',
        'description': 'Configuration file for the DNSMasq DNS forwarder and DHCP server.'
    },
    'WPA Supplicant configuration': {
        'path': '/etc/wpa_supplicant/*.conf',
        'description': 'Configuration files for the WPA Supplicant, which manages wireless connections.'
    },
    'Network configurations': {
        'path': [
            '/etc/network/interfaces',
            'ip address show',
            'netstat -nr',
            '/etc/resolv.conf'
        ],
        'description': 'Network interface configurations and DNS settings.'
    },
    'System configuration files': {
        'path': [
            '/etc/hosts',
            '/etc/sysctl.conf',
            '/etc/ssh/sshd_config'
        ],
        'description': 'System-wide configuration files for hostname resolution, kernel settings, and SSH server.'
    },
    'System log': {
        'path': '/var/log/syslog',
        'description': 'General system log containing various system events and messages.'
    },
    'Kernel logs': {
        'path': '/var/log/kern.log',
        'description': 'Logs related to the Linux kernel and its operations.'
    },
    'Package manager logs': {
        'path': [
            '/var/log/dpkg.log',
            '/var/log/yum.log'
        ],
        'description': 'Logs of package installation, removal, and updates performed using package managers like dpkg or yum.'
    },
    'User directories': {
        'path': '/home/*',
        'description': 'Contents of user directories, including user-specific configuration files and data.'
    },
    'User configuration files': {
        'path': [
            '/home/*/.bashrc',
            '/home/*/.bash_profile'
        ],
        'description': 'Configuration files specific to each user, such as Bash shell settings.'
    },
    'Web browser artifacts': {
        'path': [
            '/home/*/.mozilla/firefox/*.default',
            '/home/*/.config/google-chrome',
            '/home/*/.config/chromium'
        ],
        'description': 'Artifacts related to web browsers, including profiles, settings, and cached data.'
    },
    'Installed packages': {
        'path': 'dpkg -l',
        'description': 'List of installed packages on the system.'
    },
    'Running processes': {
        'path': 'ps aux',
        'description': 'List of currently running processes and their details.'
    },
    'Open ports': {
        'path': 'netstat -tuln',
        'description': 'Information about open network ports on the system.'
    },
    'Loaded kernel modules': {
        'path': 'lsmod',
        'description': 'List of kernel modules currently loaded into the system.'
    },
    'System hardware details': {
        'path': [
            'lshw',
            'lscpu'
        ],
        'description': 'Hardware details of the system, including CPU, memory, and other components.'
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
            for item in path:
                try:
                    if '*' in item:
                        file_list = subprocess.check_output(f'ls {item}', shell=True, text=True, stderr=subprocess.DEVNULL).split('\n')
                        for file_path in file_list:
                            if file_path.strip():
                                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                                    output = f.read()
                                zipf.writestr(f'{description}/{os.path.basename(file_path)}', output)
                    else:
                        with open(item, 'r', encoding='utf-8', errors='replace') as f:
                            output = f.read()
                        zipf.writestr(f'{description}/{os.path.basename(item)}', output)
                except Exception as e:
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f'Error collecting {item}: {str(e)}\n')
                        continue

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

# Add the log file to the zip file
zipf.write(os.path.join(output_dir, 'error_logs.txt'), 'error_logs.txt')

# Remove the log file from the output directory
os.remove(os.path.join(output_dir, 'error_logs.txt'))

# Print the path of the generated zip file
print(f"Artifact collection completed. Zip file created: {zip_filepath}")
