import subprocess
import os
import shutil

from config import get_repo_file_path
from fonts import get_font_ids, get_font_config

def install_winget_prereq(app_desc, app_name, pkg_id):
    if shutil.which(app_name) is None:
        print(f"'{app_desc}' is not installed. Installing using winget...")
        try:
            result = subprocess.run(['winget', 'install', '--id', pkg_id, '-e', '--source', 'winget'], check=True, text=True, capture_output=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing winget pkg '{app_desc}': {e.stderr}")
    else:
        print(f"'{app_desc}' is already installed.")

def install_font_prereq(font_id):
    config = get_font_config(font_id)
    pkg_id = config.get('pkg')
    try:
        subprocess.run(['oh-my-posh', 'font', 'install', '--user', pkg_id], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing font '{pkg_id}': {e.stderr}")

def sync(args):
    # Sync repo using git
    print("\nSyncing attune repo...")
    script_dir = os.path.dirname(get_repo_file_path(""))
    try:
        result = subprocess.run(['git', 'pull'], cwd=script_dir, check=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git pull: {e.stderr}")

    # Install winget dependencies
    print("Checking dependencies...")
    install_winget_prereq('visual studio code', 'code', 'Microsoft.VisualStudioCode')
    install_winget_prereq('terminal', 'wt', 'Microsoft.WindowsTerminal')
    install_winget_prereq('oh-my-posh', 'oh-my-posh', 'JanDeDobbeleer.OhMyPosh')

    # Install fonts
    for id in get_font_ids():
        install_font_prereq(id)

    # Done!
    print("\nSync complete!")
