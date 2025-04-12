from pathlib import Path
import random

import pytest

from .util import generate_random_text, TEMP_DIR


@pytest.fixture(scope='function')
def temp_text_file() -> tuple[Path, str]:
    """生成临时文本文件"""
    file = TEMP_DIR / f'{generate_random_text(10)}.txt'

    if file.exists():
        file.unlink()
    else:
        file.touch()

    text = generate_random_text()
    file.write_text(text)

    return file, text


@pytest.fixture(scope='function')
def temp_bytes_file() -> tuple[Path, bytes]:
    """生成随机二进制文件"""
    file = TEMP_DIR / f'{generate_random_text(10)}.bytes'

    if file.exists():
        file.unlink()
    else:
        file.touch()

    b = random.randbytes(random.randint(1, 1000))
    file.write_bytes(b)

    return file, b
