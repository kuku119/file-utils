"""JSON 的读取和写入"""

from __future__ import annotations

from json import loads as json_loads, dumps as json_dumps
from typing import TYPE_CHECKING, overload

from ._base import read_file, write_file

if TYPE_CHECKING:
    from json import JSONEncoder, JSONDecoder
    from typing import Any, Literal, Awaitable, Optional, Callable

    from ._base import PathOrStr, Path


@overload
async def read_json(
    f: PathOrStr,
    async_mode: Literal[True],
    /,
    *,
    encoding: str = 'utf-8',
    cls: Optional[type[JSONDecoder]] = None,
    object_hook: Optional[Callable[[dict[Any, Any]], Any]] = None,
    parse_float: Optional[Callable[[str], Any]] = None,
    parse_int: Optional[Callable[[str], Any]] = None,
    parse_constant: Optional[Callable[[str], Any]] = None,
    object_pairs_hook: Optional[Callable[[list[tuple[Any, Any]]], Any]] = None,
) -> Any: ...
@overload
def read_json(
    f: PathOrStr,
    async_mode: Literal[False],
    /,
    *,
    encoding: str = 'utf-8',
    cls: Optional[type[JSONDecoder]] = None,
    object_hook: Optional[Callable[[dict[Any, Any]], Any]] = None,
    parse_float: Optional[Callable[[str], Any]] = None,
    parse_int: Optional[Callable[[str], Any]] = None,
    parse_constant: Optional[Callable[[str], Any]] = None,
    object_pairs_hook: Optional[Callable[[list[tuple[Any, Any]]], Any]] = None,
) -> Any: ...
def read_json(
    f: PathOrStr,
    async_mode: bool,
    /,
    *,
    encoding: str = 'utf-8',
    cls: Optional[type[JSONDecoder]] = None,
    object_hook: Optional[Callable[[dict[Any, Any]], Any]] = None,
    parse_float: Optional[Callable[[str], Any]] = None,
    parse_int: Optional[Callable[[str], Any]] = None,
    parse_constant: Optional[Callable[[str], Any]] = None,
    object_pairs_hook: Optional[Callable[[list[tuple[Any, Any]]], Any]] = None,
) -> Any:
    """读取 JSON"""
    if async_mode:
        return read_json_async(
            f,
            encoding=encoding,
            cls=cls,
            object_hook=object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            object_pairs_hook=object_pairs_hook,
        )
    else:
        return read_json_sync(
            f,
            encoding=encoding,
            cls=cls,
            object_hook=object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            object_pairs_hook=object_pairs_hook,
        )


async def read_json_async(
    f: PathOrStr,
    /,
    *,
    encoding: str = 'utf-8',
    cls: Optional[type[JSONDecoder]] = None,
    object_hook: Optional[Callable[[dict[Any, Any]], Any]] = None,
    parse_float: Optional[Callable[[str], Any]] = None,
    parse_int: Optional[Callable[[str], Any]] = None,
    parse_constant: Optional[Callable[[str], Any]] = None,
    object_pairs_hook: Optional[Callable[[list[tuple[Any, Any]]], Any]] = None,
) -> Any:
    """异步读取 JSON"""
    json_str = await read_file(f, 'str', True, encoding=encoding)
    return json_loads(
        json_str,
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
    )


def read_json_sync(
    f: PathOrStr,
    /,
    *,
    encoding: str = 'utf-8',
    cls: Optional[type[JSONDecoder]] = None,
    object_hook: Optional[Callable[[dict[Any, Any]], Any]] = None,
    parse_float: Optional[Callable[[str], Any]] = None,
    parse_int: Optional[Callable[[str], Any]] = None,
    parse_constant: Optional[Callable[[str], Any]] = None,
    object_pairs_hook: Optional[Callable[[list[tuple[Any, Any]]], Any]] = None,
) -> Any:
    """同步读取 JSON"""
    json_str = read_file(f, 'str', False, encoding=encoding)
    return json_loads(
        json_str,
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
    )


@overload
async def write_json(
    f: PathOrStr,
    data: Any,
    async_mode: Literal[True],
    /,
    *,
    encoding: str = 'utf-8',
    skipkeys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    cls: Optional[type[JSONEncoder]] = None,
    indent: Optional[int | str] = None,
    separators: Optional[tuple[str, str]] = None,
    default: Optional[Callable[[Any], None]] = None,
    sort_keys: bool = False,
) -> Path: ...
@overload
def write_json(
    f: PathOrStr,
    data: Any,
    async_mode: Literal[False],
    /,
    *,
    encoding: str = 'utf-8',
    skipkeys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    cls: Optional[type[JSONEncoder]] = None,
    indent: Optional[int | str] = None,
    separators: Optional[tuple[str, str]] = None,
    default: Optional[Callable[[Any], None]] = None,
    sort_keys: bool = False,
) -> Path: ...
def write_json(
    f: PathOrStr,
    data: Any,
    async_mode: bool,
    /,
    *,
    encoding: str = 'utf-8',
    skipkeys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    cls: Optional[type[JSONEncoder]] = None,
    indent: Optional[int | str] = None,
    separators: Optional[tuple[str, str]] = None,
    default: Optional[Callable[[Any], None]] = None,
    sort_keys: bool = False,
) -> Path | Awaitable[Path]:
    """写入 JSON"""
    json_str = json_dumps(
        data,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
    )
    if async_mode:
        return write_file(f, json_str, True, replace=True, encoding=encoding)
    else:
        return write_file(f, json_str, False, replace=True, encoding=encoding)
