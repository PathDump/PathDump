import hashlib

def md5 (filepath):
    hash_md5 = hashlib.md5()
    with open (filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update (chunk)
    return hash_md5.hexdigest()

def save_file (filepath, data):
    try:
        with open (filepath, 'w') as f:
            f.write (data)
    except EnvironmentError:
        return False

    return True

def load_file (filepath):
    with open (filepath, 'r') as f:
        return f.read()
