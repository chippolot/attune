import subprocess
import os

def sync(args):

    # Sync repo
    print("\nSyncing attune repo...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        result = subprocess.run(['git', 'pull'], cwd=script_dir, check=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git pull: {e.stderr}")
