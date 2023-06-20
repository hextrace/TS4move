import os
import shutil
from pathlib import Path
from progress.bar import IncrementalBar
from psutil import disk_partitions, disk_usage, process_iter
import subprocess
from shutil import which, move
from sys import platform

# Exit if OS is not macOS or Windows
if (not platform == 'darwin') and (not platform == 'win32'):
    print(f'{platform} is not a supported OS. Exiting.')
    exit(0)

# Exit if The Sims 4 is running
if "The Sims 4" in (p.name() for p in process_iter()):
    print(f'The Sims 4 is currently running. Please save and quit before running this program.')
    exit(0)


# Get the default path for the EA folder, exit if it does not exist
def get_ea_folder():
    if 'win32' == platform:
        shell = "pwsh.exe -Command" if which("pwsh.exe") is not None else "powershell.exe"
        pwsh_cmd = subprocess.run(f"{shell} [Environment]::GetFolderPath('MyDocuments')", shell=True,
                                  capture_output=True, text=True)
        usr_docs = pwsh_cmd.stdout.strip('\n')
        ea_folder = Path(Path(str(usr_docs)), Path('Electronic Arts'))
    else:
        ea_folder = Path(Path('~/Documents').expanduser(), Path('Electronic Arts'))

    if os.path.islink(Path(ea_folder, 'The Sims 4')):
        print(f'{Path(ea_folder, "The Sims 4")} appears to be a symlink already. Exiting program.')
        exit(0)
    elif ea_folder.is_dir():
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


# Print '=' x times.
def print_bars(num: int):
    print(f'{"=" * num}')


# Print '-' x times.
def print_line(num: int):
    print(f'{"-" * num}')


def dir_walk(source: Path):
    folders = list(d for d in sorted(source.iterdir()) if d.is_dir())
    files = list(f for f in sorted(source.iterdir()) if f.is_file())
    yield source, folders, files
    for folder in folders:
        yield from dir_walk(folder)


# Count files
def count_files(folder: Path):
    files = []

    if Path.is_dir(folder):
        for root, folders, filenames in dir_walk(folder):
            files.extend(filenames)

    return len(files)


# Make folders that do not exist
def make_folders(folder: Path):
    if not Path.exists(folder):
        Path.mkdir(folder)


# Move folder
def move_folder(source: Path, destination: Path):

    number_of_files = count_files(source)

    if number_of_files > 0:
        make_folders(destination)

    with IncrementalBar('Moving', max=number_of_files) as bar:
        for root, folders, filenames in dir_walk(source):
            for folder in folders:
                source_path = Path(root, folder)
                destination_path = Path(str(source_path).replace(str(source), str(destination)))
                make_folders(destination_path)

            for file in filenames:
                source_path = Path(root, file)
                destination_path = Path(str(source_path).replace(str(source), str(destination)))
                print(f'Moving {source_path} to {destination_path}')
                move(source_path, destination_path)

            bar.next()


def make_link(source: Path, destination: Path):

    if Path.exists(source) and Path.is_dir(source):
        shutil.rmtree(source)

    Path(source).symlink_to(destination, target_is_directory=True)


if '__main__' == __name__:

    opsys = "macOS" if "darwin" == platform else "Windows"
    ts4_dir = Path('The Sims 4')                                # The folder to move
    old_ts4_root = Path(Path(get_ea_folder()), Path(ts4_dir))   # The Default TS4 folder
    drive = -1                                                  # Initialize user input
    QUIT = 0                                                    # User abort

    print_bars(75)
    print(f'\nOperating System: {opsys}')
    print(f'Default path to The Sims 4: \n\t{old_ts4_root}')
    print_bars(75)
    print('Available Drives:'.center(75))
    print_line(75)

    if len(get_drives()) == 0:
        print(f'No drives available.')
        print(f'Make sure your drives are connected properly and have been formatted.')
        exit(0)
    else:
        user_drives = get_drives()

    for k, v in user_drives.items():
        free_space = format((disk_usage(str(v)).free / 1073741824), ".2f")
        print(f'{k}) Drive/Mount: {v} :: Free Space: {free_space} GB')

    print_line(75)

    # Loop until user puts in correct information
    while drive not in user_drives.keys() or QUIT:
        try:
            if drive == QUIT:
                print(f'\nExiting ...')
                exit(0)
            else:
                drive = int(input(f'\nWhich drive would you like to move your Sims 4 folder to? '
                                  f'[1 - {len(user_drives.keys())}] Press "0" to quit. '))
        except ValueError:
            print(f'Invalid selection. Please try again.')

    # Set target location
    print_line(75)
    print(f'You have selected {user_drives[drive]}')
    new_ts4_root = Path(user_drives[drive], ts4_dir)

    print(f'The Sims 4 default location: {old_ts4_root}')
    print(f'The Sims 4 new location: {new_ts4_root}')
    print(f'Files to move: {count_files(old_ts4_root)}')

    # Move the stuff
    print_line(75)
    move_folder(old_ts4_root, new_ts4_root)

    # Link the stuff
    print_line(75)
    print(f'Creating link from {old_ts4_root} to {new_ts4_root} ...')
    make_link(old_ts4_root, new_ts4_root)
    print(f'Done.')
