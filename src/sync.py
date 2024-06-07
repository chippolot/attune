import subprocess
import os
import shutil

def sync(args):

    # Sync repo using git
    print("\nSyncing attune repo...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        result = subprocess.run(['git', 'pull'], cwd=script_dir, check=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git pull: {e.stderr}")

    # Check if 'oh-my-posh' is installed and install it using winget if not
    if shutil.which('oh-my-posh') is None:
        print("'oh-my-posh' is not installed. Installing using winget...")
        try:
            result = subprocess.run(['winget', 'install', '--id', 'JanDeDobbeleer.OhMyPosh', '-e', '--source', 'winget'], check=True, text=True, capture_output=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing 'oh-my-posh': {e.stderr}")
    else:
        print("'oh-my-posh' is already installed.")
