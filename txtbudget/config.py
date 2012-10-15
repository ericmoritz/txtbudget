from itertools import imap
import os
import json


def json_config(config_file):
    if os.path.exists(config_file):
        with open(config_file) as fh:
            return json.load(fh)
    else:
        return {}


def load_config(configurators):
    def dictmerge(x, y):
        x.update(y)
        return x

    return reduce(
        dictmerge,
        imap(
            lambda f: f(),
            configurators
        ),
        {}
    )
