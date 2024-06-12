import subprocess


def choose(choices, limit=1, header=None):
    opts = []
    if limit is None:
        opts.append("--no-limit")
    elif limit > 1:
        opts += ["--limit", limit]
    if header is not None:
        opts += ["--header", header]
    result = subprocess.run(
        ["gum", "choose"] + choices + opts, stdout=subprocess.PIPE, text=True
    )
    selected = result.stdout.strip().splitlines()
    if selected is None or len(selected) == 0:
        return None
    elif limit == 1:
        return selected[0]
    else:
        return selected


def input(
    cursor_foreground=None,
    prompt_foreground=None,
    placeholder=None,
    prompt=None,
    width=None,
    value=None,
):
    command = ["gum", "input"]

    if cursor_foreground:
        command.extend(["--cursor.foreground", cursor_foreground])
    if prompt_foreground:
        command.extend(["--prompt.foreground", prompt_foreground])
    if placeholder:
        command.extend(["--placeholder", placeholder])
    if prompt:
        command.extend(["--prompt", prompt])
    if width:
        command.extend(["--width", str(width)])
    if value:
        command.extend(["--value", value])

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()


def spin(msg, cmd, style="dot"):
    subprocess.run(["gum", "spin", "--spinner", style, "--title", msg, "--", "cmd"])


def style(
    texts,
    foreground=None,
    border_foreground=None,
    border=None,
    align=None,
    width=None,
    margin=None,
    padding=None,
):
    command = ["gum", "style"]

    if foreground:
        command.extend(["--foreground", str(foreground)])
    if border_foreground:
        command.extend(["--border-foreground", str(border_foreground)])
    if border:
        command.extend(["--border", border])
    if align:
        command.extend(["--align", align])
    if width:
        command.extend(["--width", str(width)])
    if margin:
        command.extend(["--margin", margin])
    if padding:
        command.extend(["--padding", padding])

    if isinstance(texts, list):
        command.extend(texts)
    else:
        command.append(texts)

    subprocess.run(command, text=True)
