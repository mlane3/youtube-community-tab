import json
import time
from hashlib import sha1

CLIENT_VERSION = "2.20220224.07.00"

def safely_get_value_from_key(*args, default=None):
    obj = args[0]
    keys = args[1:]

    for key in keys:
        try:
            obj = obj[key]
        except Exception:
            return default

    return obj


def save_object_to_file(obj, path):
    with open(path, "w") as f:
        f.write(json.dumps(obj, indent=4))


def get_auth_header(sapisid):
    timestring = str(int(time.time()))
    return f"SAPISIDHASH {timestring}_" + sha1(' '.join([timestring, sapisid, "https://www.youtube.com"]).encode()).hexdigest()
