import subprocess


def choose(options):
    result = subprocess.run(
        ["gum", "choose"] + options, stdout=subprocess.PIPE, text=True
    )
    return result.stdout.strip()


def spin(msg, cmd, style="dot"):
    subprocess.run(["gum", "spin", "--spinner", style, "--title", msg, "--", "cmd"])
