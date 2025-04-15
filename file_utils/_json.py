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
    **kwargs,
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
    **kwargs,
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
    **kwargs,
) -> Any:
    """
    从文件读取 JSON

    :param f: 目标文件路径
    :type f: str | Path
    :param async_mode: 是否启用异步
    :type async_mode: bool
    :param encoding: 文件编码
    :type encoding: str
    :param parse_float: 浮点数解码器。
    :type parse_float: Callable[[str], Any] | None
    :param parse_int: 整数解码器。
    :type parse_int: Callable[[str], Any] | None
    :param parse_constant: '-Infinity', 'Infinity' 或 'NaN' 的解码器。
    :type parse_constant: Callable[[str], Any] | None
    :param cls: JSON 解码器。
    :type cls: JSONDecoder | None
    :param object_hook: 默认值为 None。
    :type object_hook: Callable[dict[Any, Any]] | None
    :param object_pairs_hook: 默认值为 None。
    :type object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None

    :return: 结果
    :rtype: Any
    """
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
            **kwargs,
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
            **kwargs,
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
    **kwargs,
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
        **kwargs,
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
    **kwargs,
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
        **kwargs,
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
    default: Optional[Callable[[Any], Any]] = None,
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
    default: Optional[Callable[[Any], Any]] = None,
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
    default: Optional[Callable[[Any], Any]] = None,
    sort_keys: bool = False,
) -> Path | Awaitable[Path]:
    """
    写入 JSON 到文件

    :param f: 期望保存路径
    :type f: str | Path
    :param data: 要保存的数据
    :type data: Any
    :param async_mode: 是否启用异步
    :type async_mode: bool
    :param encoding: 文件编码
    :type encoding: str
    :param skipkeys: 是否跳过非基本类型的键，若为 False 则遇到非基本类型的键时将抛出 TypeError。
    :type skipkeys: bool
    :param ensure_ascii: 是否保证每个字符都是 ASCII。
    :type ensure_ascii: bool
    :param check_circular: 是否检查循环引用。
    :type check_circular: bool
    :param allow_nan: 是否允许超范围的 float 值 (nan, inf, -inf)。
    :type allow_nan: bool
    :param cls: 如果设置，则重写为一个带有 default() 方法的自定义 JSON 编码器，用以序列化为自定义的数据类型。
    如为 None (默认值)，则使用 JSONEncoder。
    :type cls: JSONEncoder | None
    :param indent: 缩进。
    :type indent: int | str | None
    :param separators: 一个二元组: (item_separator, key_separator)。
    :type separators: tuple[str, str] | None
    :param default: 当对象无法被序列化时将被调用的函数。它应该返回一个可被 JSON 编码的版本或是引发 TypeError。
    :type default: Callable[[Any], Any] | None
    :param sort_keys: 字典输出是否按键排序。
    :type sort_keys: bool

    :return: 保存路径
    :rtype: Path | Awaitable[Path]
    """
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
    return write_file(f, json_str, async_mode, replace=True, encoding=encoding)
