from enum import StrEnum

from attune.config import Config


class Modules(StrEnum):
    GIT = "git"
    VSCODE = "vscode"
    CHATGPT = "chatgpt"
    RIDER = "rider"


def get_all():
    return [e.value for e in Modules]


def is_enabled(module):
    config = Config.load()
    modules = config.get("modules", [])
    return module in modules


def enable(module):
    config = Config.load()
    modules = config.get("modules", [])
    if module not in modules:
        modules.append(module)
    config.save()


def disable(module):
    config = Config.load()
    modules = config.get("modules", [])
    if module not in modules:
        modules.remove(module)
    config.save()


def clear():
    config = Config.load()
    config.set("modules", [])
    config.save()
