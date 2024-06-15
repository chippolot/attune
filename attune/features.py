from enum import StrEnum

from attune.config import Config


class Features(StrEnum):
    GIT = "git"
    VSCODE = "vscode"
    CHATGPT = "chatgpt"


def get_all():
    return [e.value for e in Features]


def is_enabled(feature):
    config = Config.load()
    features = config.get("features", [])
    return feature in features


def enable(feature):
    config = Config.load()
    features = config.get("features", [])
    if feature not in features:
        features.append(feature)
    config.save()


def disable(feature):
    config = Config.load()
    features = config.get("features", [])
    if feature not in features:
        features.remove(feature)
    config.save()


def clear():
    config = Config.load()
    config.set("features", [])
    config.save()
