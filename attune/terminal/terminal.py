import platform

if platform.system() == "Windows":
    from attune.terminal.windows_terminal import Terminal
elif platform.system() == "Darwin":
    from attune.terminal.iterm2_terminal import Terminal


def get_terminal():
    return Terminal()
