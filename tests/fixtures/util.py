from pathlib import Path
import random
import string


TEMP_DIR = Path.cwd() / 'pytest_temp'
"""临时文件的存放目录"""
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def generate_random_text(length: int | None = None, /) -> str:
    """生成随机字符"""
    if length is not None:
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 1000)))


def generate_random_bytes(length: int | None = None, /) -> bytes:
    """生成随机字节"""
    return random.randbytes(length if length is not None else random.randint(1, 1000))
