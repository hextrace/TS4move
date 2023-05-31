from pathlib import Path
from psutil import disk_partitions, disk_usage
from sys import platform

# Functions to make this work

# Default Environmental Stuff
ts4_dir = Path('The Sims 4')
old_ts4_root = Path('~/Documents/Electronic Arts/', ts4_dir).expanduser()

user_drives = {}
drive = ''

# Enumerate and display drives based on platform
a = 1
partitions = disk_partitions()
print('Available Drives:')

# This will not work for WINE installations
if platform == 'linux' or platform == 'linux2':
    print('You are running this in Linux which means you are probably running Sims 4 in WINE. This script does not '
          'support WINE installations of Linux.')
    exit(0)

# MacOS Magic
elif platform == 'darwin':
    for p in partitions:
        if p.mountpoint.startswith('/Volumes'):
            user_drives[a] = p.mountpoint
            free_space = format((disk_usage(user_drives[a]).free / 1073741824), ".2f")
            print(f'{a}) Mount Point: {user_drives[a]} :: Free Space: {free_space} GB')

# Windows Magic
elif platform == 'win32':
    print('This is a place holder.')

# Just in case someone tries to run this in something else altogether
else:
    print('You are running an OS that this script does not support.')
    exit(0)

while drive not in user_drives.keys():
    drive = int(input(f'Which drive would you like to move your Sims 4 folder to? [1 - {len(user_drives.keys())}] '))

print(f'You have selected {user_drives[drive]}')
new_ts4_root = Path(user_drives[drive], ts4_dir)

print(f'The Sims 4 default location: {old_ts4_root}')
print(f'The Sims 4 new location: {new_ts4_root}')
