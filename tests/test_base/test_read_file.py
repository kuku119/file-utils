import pytest


from tests.fixtures.file_fixture import temp_text_file, temp_bytes_file


def test_read_sync_bytes(temp_bytes_file):
    from file_utils import read_file_sync

    target_path, target_bytes = temp_bytes_file
    assert read_file_sync(target_path, 'bytes') == target_bytes


def test_read_sync_str(temp_text_file):
    from file_utils import read_file_sync

    target_path, target_text = temp_text_file
    assert read_file_sync(target_path, 'str') == target_text


async def test_read_async_bytes(temp_bytes_file):
    from file_utils import read_file_async

    target_path, target_bytes = temp_bytes_file
    assert await read_file_async(target_path, 'bytes') == target_bytes


async def test_read_async_str(temp_text_file):

    from file_utils import read_file_async

    target_path, target_text = temp_text_file
    assert await read_file_async(target_path, 'str') == target_text


def test_read_bytes_1(temp_bytes_file):
    from file_utils import read_file

    target_path, target_bytes = temp_bytes_file
    assert read_file(target_path, 'bytes', False) == target_bytes


async def test_read_bytes_2(temp_bytes_file):
    from file_utils import read_file

    target_path, target_bytes = temp_bytes_file
    assert await read_file(target_path, 'bytes', True) == target_bytes


def test_read_str_1(temp_text_file):
    from file_utils import read_file

    target_path, target_text = temp_text_file
    assert read_file(target_path, 'str', False) == target_text


async def test_read_str_2(temp_text_file):
    from file_utils import read_file

    target_path, target_text = temp_text_file
    assert await read_file(target_path, 'str', True) == target_text
