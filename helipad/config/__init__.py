from yaml import load


def from_file(filename):
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    with open(filename) as config_file:
        config = load(config_file, Loader=Loader)
        return config
