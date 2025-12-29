import os
from types import SimpleNamespace
import pytest

from tools import save_to_txt


def test_save_to_txt_writes_file(tmp_path):
    filename = tmp_path / "out.txt"
    res = save_to_txt("hello world", filename=str(filename))
    assert "successfully" in res.lower()
    assert filename.exists()
    text = filename.read_text(encoding="utf-8")
    assert "hello world" in text
