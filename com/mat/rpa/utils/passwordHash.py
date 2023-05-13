import hashlib

# MD5哈希函数
def passwordHash(text) -> str:
    if type(text) == str:
        return hashlib.md5(bytes(text.encode())).hexdigest()
    elif type(text) == bytes:
        return hashlib.md5(text).hexdigest()
    else:
        return hashlib.md5(bytes(text)).hexdigest()
