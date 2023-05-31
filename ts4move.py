from pathlib import Path
from psutil import disk_partitions, disk_usage
from sys import platform

if (not platform == 'darwin') and (not platform == 'win32'):
    print(f'{platform} is not a supported OS. Exiting.')
    exit(0)

# Default Environmental Stuff
ts4_dir = Path('The Sims 4')
old_ts4_root = Path('~/Documents/Electronic Arts/', ts4_dir).expanduser()
drive = ''


# Functions
# Enumerate and display drives based on platform
def get_drives():
    a = 1
    partitions = disk_partitions()
    drives = {}
    # MacOS Magic
    if platform == 'darwin':
        for p in partitions:
            if p.mountpoint.startswith('/Volumes'):
                drives[a] = p.mountpoint
                a += 1

    # Windows Magic
    elif platform == 'win32':
        for p in partitions:
            if 'C:\\' not in p.mountpoint:
                drives[a] = p.mountpoint
                a += 1
    return drives


print(f'{"=" * 75}')
print('Available Drives:'.center(75))
print(f'{"-" * 75}')

user_drives = get_drives()
for k, v in user_drives.items():
    free_space = format((disk_usage(v).free / 1073741824), ".2f")
    print(f'{k}) Drive/Mount: {v} :: Free Space: {free_space} GB')

print(f'{"-" * 75}\n')

while drive not in user_drives.keys():
    try:
        drive = int(input(f'Which drive would you like to move your Sims 4 folder to? [1 - {len(user_drives.keys())}] '))
    except ValueError:
        print(f'Invalid selection. Please try again.')

print(f'You have selected {user_drives[drive]}')
new_ts4_root = Path(user_drives[drive], ts4_dir)

print(f'The Sims 4 default location: {old_ts4_root}')
print(f'The Sims 4 new location: {new_ts4_root}')
