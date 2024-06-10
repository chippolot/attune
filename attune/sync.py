import subprocess
import os
import shutil

from attune.paths import *
from attune.fonts import *
from attune.themes import *
from attune.windows import *
from attune.template import *


def patch_setup_block(file_to_patch, setup_block_file):
    block_start_marker = "# >> Attune Setup Start >> DO NOT MODIFY"
    block_end_marker = "# >> Attune Setup End >> DO NOT MODIFY"

    # Load file to patch
    if os.path.exists(file_to_patch):
        with open(file_to_patch, "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = []

    # Load block
    with open(setup_block_file, "r", encoding="utf-8") as file:
        setup_block = file.read()

    # Apply template replacements
    setup_block = template_apply(setup_block)

    # Apply block markers
    setup_block = f"{block_start_marker}\n{setup_block}\n{block_end_marker}"

    # Split setup block into lines
    setup_block_lines = [line + "\n" for line in setup_block.split("\n")]

    # Find the start and end of the existing block, if any
    start_index = end_index = -1
    for i, line in enumerate(lines):
        if block_start_marker in line:
            start_index = i
        if block_end_marker in line:
            end_index = i
            break

    # Check if the existing block is the same as the new block
    if start_index != -1 and end_index != -1:
        existing_block_lines = lines[start_index : end_index + 1]
        if existing_block_lines == setup_block_lines:
            print(f"'{file_to_patch}' is already up-to-date.")
            return

    # Replace the existing block if found, otherwise append the new block
    if start_index != -1 and end_index != -1:
        lines[start_index : end_index + 1] = setup_block_lines
    else:
        lines.append("\n")
        lines.extend(setup_block_lines)

    # Rewrite patched file
    with open(file_to_patch, "w", encoding="utf-8") as file:
        file.writelines(lines)

    print(f"'{file_to_patch}' patched.")


def copy_template(src, dst):
    with open(src, "r", encoding="utf-8") as file:
        src_content = file.read()
    src_content = template_apply(src_content)
    with open(dst, "w", encoding="utf-8") as file:
        file.write(src_content)

    print(f"'{dst}' copied.")


def install_winget_prereq(app_desc, app_name, pkg_id):
    if shutil.which(app_name) is None:
        print(f"'{app_desc}' is not installed. Installing using winget...")
        try:
            result = subprocess.run(
                ["winget", "install", "--id", pkg_id, "-e", "--source", "winget"],
                check=True,
                text=True,
                capture_output=True,
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(
                f"An error occurred while installing winget pkg '{app_desc}': {e.stderr}"
            )
    else:
        print(f"'{app_desc}' is already installed.")


def install_font_prereq(font_id):
    config = get_font_config(font_id)
    family = config.get("family")

    if is_font_installed(family):
        print(f"'{family}' is already installed.")
        return

    print(f"'{family}' is not installed. Installing using oh-my-posh...")
    pkg_id = config.get("pkg")
    try:
        subprocess.run(["oh-my-posh", "font", "install", "--user", pkg_id], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing font '{pkg_id}': {e.stderr}")


def sync(args):
    # Sync repo using git
    print("\nSyncing attune repo...")
    script_dir = os.path.dirname(get_repo_file_path())
    try:
        result = subprocess.run(
            ["git", "pull"], cwd=script_dir, check=True, text=True, capture_output=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git pull: {e.stderr}")

    # Patch dotfiles with setup blocks
    print("Patching dotfiles with setup code...")
    patch_setup_block(
        os.path.expanduser("~/.bash_profile"),
        get_repo_file_path("dotfiles/setup/.bash_profile", validate=True),
    )
    patch_setup_block(
        os.path.expanduser("~/.gitconfig"),
        get_repo_file_path("dotfiles/setup/.gitconfig", validate=True),
    )

    # Copy dotfiles to config folder
    print("\nCopying dotfiles...")
    copy_template(
        get_repo_file_path("dotfiles/.bash_profile", validate=True),
        get_attune_file_path(".bash_profile"),
    )
    copy_template(
        get_repo_file_path("dotfiles/.gitconfig", validate=True),
        get_attune_file_path(".gitconfig"),
    )

    # Install winget dependencies
    print("\nChecking app dependencies...")
    install_winget_prereq("visual studio code", "code", "Microsoft.VisualStudioCode")
    install_winget_prereq("terminal", "wt", "Microsoft.WindowsTerminal")
    install_winget_prereq("oh-my-posh", "oh-my-posh", "JanDeDobbeleer.OhMyPosh")

    # Install fonts
    print("\nChecking font dependencies...")
    for id in get_font_ids():
        install_font_prereq(id)

    # Apply default theme if none is set
    if get_active_theme_name() == None:
        print("\nNo theme set. Setting default theme...")
        set_theme(get_default_theme_name())

    # Done!
    print("\nSync complete!")
