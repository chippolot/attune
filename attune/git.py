import os
import subprocess


def pull(cwd):
    try:
        result = subprocess.run(
            ["git", "pull"],
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout.strip("\n"))
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git pull: {e.stderr}")


def clone(url, dst):
    try:
        result = subprocess.run(
            ["git", "clone", url, dst],
            cwd=os.cwd(),
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout.strip("\n"))
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git pull: {e.stderr}")
