"""文件的基础操作（存在、读取、写入）"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, overload

from aiofiles import open as async_open

if TYPE_CHECKING:
    from typing import Awaitable, Literal, Optional

    type AwaitableBytesOrStr = Awaitable[bytes] | Awaitable[str]
    type BytesOrStr = bytes | str
    type PathOrStr = Path | str


__all__ = [
    'exist_file',
    'read_file',
    'write_file',
]


sync_open = open


def exist_file(f: PathOrStr, /) -> bool:
    """
    文件是否存在

    :param f: 目标文件
    :type f: str | Path

    :return: 文件是否存在
    :rtype: bool
    """
    return Path(f).exists() if isinstance(f, str) else f.exists()


##### 读取文件 #####


def check_before_read(f: PathOrStr, /) -> Path:
    """将 `f` 转为 `Path` 类型，判断 `f` 是否存在。"""
    if isinstance(f, str):
        f = Path(f)

    if not exist_file(f):
        raise FileNotFoundError(f'"{f}" not exist')

    if not f.is_file():
        raise IsADirectoryError(f'"{f}" is a directory')

    return f


@overload
async def read_file(f: PathOrStr, mode: Literal['bytes'], async_mode: Literal[True], /) -> bytes: ...
@overload
async def read_file(
    f: PathOrStr, mode: Literal['str'], async_mode: Literal[True], /, encoding: str = 'utf-8'
) -> str: ...
@overload
def read_file(f: PathOrStr, mode: Literal['bytes'], async_mode: Literal[False], /) -> bytes: ...
@overload
def read_file(
    f: PathOrStr, mode: Literal['str'], async_mode: Literal[False], /, encoding: str = 'utf-8'
) -> str: ...
def read_file(
    f: PathOrStr, mode: Literal['bytes', 'str'], async_mode: bool, /, encoding: Optional[str] = None
) -> BytesOrStr | AwaitableBytesOrStr:
    """
    读取文件

    :param f: 目标文件
    :type f: str | Path
    :param mode: 读取字节还是字符
    :type mode: Literal['bytes', 'str']
    :param async_mode: 是否启用异步
    :type async_mode: bool
    :param encoding: 文件编码，仅在读取字符时可用
    :type encoding: str | None

    :return: 文件内容
    :rtype: bytes | str | Awaitable[bytes] | Awaitable[str]
    """
    if async_mode:
        return read_file_async(f, mode, encoding=encoding)
    else:
        return read_file_sync(f, mode, encoding=encoding)


@overload
async def read_file_async(
    f: PathOrStr, mode: Literal['bytes'], /, encoding: Optional[str] = None
) -> bytes: ...
@overload
async def read_file_async(f: PathOrStr, mode: Literal['str'], /, encoding: Optional[str] = None) -> str: ...
async def read_file_async(
    f: PathOrStr, mode: Literal['bytes', 'str'], /, encoding: Optional[str] = None
) -> BytesOrStr:
    """异步读取文件"""
    f = check_before_read(f)
    match mode:
        case 'bytes':
            async with async_open(f, 'rb') as fp:
                return await fp.read()
        case 'str':
            async with async_open(f, 'r', encoding=encoding) as fp:
                return await fp.read()


@overload
def read_file_sync(f: PathOrStr, mode: Literal['bytes'], /, encoding: Optional[str] = None) -> bytes: ...
@overload
def read_file_sync(f: PathOrStr, mode: Literal['str'], /, encoding: Optional[str] = None) -> str: ...
def read_file_sync(
    f: PathOrStr, mode: Literal['bytes', 'str'], /, encoding: Optional[str] = None
) -> BytesOrStr:
    """同步读取文件"""
    f = check_before_read(f)
    match mode:
        case 'bytes':
            with sync_open(f, 'rb') as fp:
                return fp.read()
        case 'str':
            with sync_open(f, 'r', encoding=encoding) as fp:
                return fp.read()


##### 写入文件 #####


def check_before_write(f: PathOrStr, /) -> Path:
    """将 `f` 转为 `Path` 类型，检查 `f` 是否为文件夹，为 `f` 创建各上层文件夹。"""
    if isinstance(f, str):
        f = Path(f)

    if exist_file(f) and not f.is_file():
        raise IsADirectoryError(f'"{f}" is a directory')

    f.parent.mkdir(parents=True, exist_ok=True)

    return f


@overload
async def write_file(
    f: PathOrStr, data: bytes, async_mode: Literal[True], /, replace: bool = True
) -> Path: ...
@overload
async def write_file(
    f: PathOrStr, data: str, async_mode: Literal[True], /, replace: bool = True, encoding: str = 'utf-8'
) -> Path: ...
@overload
def write_file(f: PathOrStr, data: bytes, async_mode: Literal[False], /, replace: bool = True) -> Path: ...
@overload
def write_file(
    f: PathOrStr, data: str, async_mode: Literal[False], /, replace: bool = True, encoding: str = 'utf-8'
) -> Path: ...
def write_file(
    f: PathOrStr, data: BytesOrStr, async_mode: bool, /, replace: bool = True, encoding: str = 'utf-8'
) -> Path | Awaitable[Path]:
    """
    写入文件

    :param f: 目标路径
    :type f: str | Path
    :param data: 待写入数据
    :type data: bytes | str
    :param async_mode: 是否启用异步
    :type async_mode: bool
    :param replace: 是否启用覆盖
    :type replace: bool
    :param encoding: 文件编码
    :type encoding: str

    :return: 写入路径
    :rtype: Path | Awaitable[Path]
    """
    if async_mode:
        return write_file_async(f, data, replace=replace, encoding=encoding)
    else:
        return write_file_sync(f, data, replace=replace, encoding=encoding)


@overload
async def write_file_async(
    f: PathOrStr, data: bytes, /, replace: bool = True, encoding: Optional[str] = None
) -> Path: ...
@overload
async def write_file_async(
    f: PathOrStr, data: str, /, replace: bool = True, encoding: Optional[str] = None
) -> Path: ...
async def write_file_async(
    f: PathOrStr, data: BytesOrStr, /, replace: bool = True, encoding: Optional[str] = None
) -> Path:
    """异步写入文件"""
    f = check_before_write(f)
    match data:
        case bytes():
            async with async_open(f, 'wb' if replace else 'ab') as fp:
                await fp.write(data)
            return f
        case str():
            async with async_open(
                f, 'w' if replace else 'a', encoding='utf-8' if encoding is None else encoding
            ) as fp:
                await fp.write(data)
            return f
        case _:
            raise TypeError(f'Wrong type of `data`: {type(data)}')


@overload
def write_file_sync(
    f: PathOrStr, data: bytes, /, replace: bool = True, encoding: Optional[str] = None
) -> Path: ...
@overload
def write_file_sync(
    f: PathOrStr, data: str, /, replace: bool = True, encoding: Optional[str] = None
) -> Path: ...
def write_file_sync(
    f: PathOrStr, data: BytesOrStr, /, replace: bool = True, encoding: Optional[str] = None
) -> Path:
    """同步写入文件"""
    f = check_before_write(f)
    match data:
        case bytes():
            with sync_open(f, 'wb' if replace else 'ab') as fp:
                fp.write(data)
            return f
        case str():
            with sync_open(
                f, 'w' if replace else 'a', encoding='utf-8' if encoding is None else encoding
            ) as fp:
                fp.write(data)
            return f
        case _:
            raise TypeError(f'Wrong type of `data`: {type(data)}')
