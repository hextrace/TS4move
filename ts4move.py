from pathlib import Path
from psutil import disk_partitions, disk_usage
import subprocess
from shutil import which
from sys import platform

# Exit if OS is not macOS or Windows
if (not platform == 'darwin') and (not platform == 'win32'):
    print(f'{platform} is not a supported OS. Exiting.')
    exit(0)


# Get the default path for the EA folder, exit if it does not exist
def get_ea_folder():
    if 'win32' == platform:
        shell = "pwsh.exe -Command" if which("pwsh.exe") is not None else "powershell.exe"
        pwsh_cmd = subprocess.run(f"{shell} [Environment]::GetFolderPath('MyDocuments')", shell=True, capture_output=True, text=True)
        usr_docs = pwsh_cmd.stdout.strip('\n')
        ea_folder = Path(Path(str(usr_docs)), Path('Electronic Arts'))
    else:
        ea_folder = Path(Path('~/Documents').expanduser(), Path('Electronic Arts'))

    if ea_folder.is_dir():
        return ea_folder
    else:
        print(f'{ea_folder} cannot be found. Please start and exit The Sims 4 at least once before trying again.')
        exit(0)


# Create and return a dictionary of non-root drives
def get_drives():
    a = 1
    partitions = disk_partitions()
    drives = {}
    # MacOS Magic
    if 'darwin' == platform:
        p: sdiskpart
        for p in partitions:
            if p.mountpoint.startswith('/Volumes'):
                drives[a] = p.mountpoint
                a += 1

    # Windows Magic
    elif 'win32' == platform:
        for p in partitions:
            if 'C:\\' not in p.mountpoint:
                drives[a] = p.mountpoint
                a += 1
    return drives


if '__main__' == __name__:

    ts4_dir: Path = Path('The Sims 4')                                  # The folder to move
    old_ts4_root: Path = Path(Path(get_ea_folder()), Path(ts4_dir))     # The Default TS4 folder
    drive = -1                                                          # Initialize user input

    print(f'{"=" * 75}')
    print(f'Operating System: {"macOS" if "darwin" == platform else "Windows"}')
    print(f'Default path to The Sims 4: \n\t{old_ts4_root}')
    print(f'{"=" * 75}')
    print('Available Drives:'.center(75))
    print(f'{"-" * 75}')

    user_drives = get_drives()

    for k, v in user_drives.items():
        free_space = format((disk_usage(str(v)).free / 1073741824), ".2f")
        print(f'{k}) Drive/Mount: {v} :: Free Space: {free_space} GB')

    print(f'{"-" * 75}\n')

    while drive not in user_drives.keys():
        try:
            drive = int(input(f'Which drive would you like to move your Sims 4 folder to? '
                              f'[1 - {len(user_drives.keys())}] '))
        except ValueError:
            print(f'Invalid selection. Please try again.')

    print(f'{"-" * 75}')
    print(f'You have selected {user_drives[drive]}')
    new_ts4_root = Path(user_drives[drive], ts4_dir)

    print(f'The Sims 4 default location: {old_ts4_root}')
    print(f'The Sims 4 new location: {new_ts4_root}')
    print(f'{"-" * 75}')
