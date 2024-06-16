from attune.config import Config


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
