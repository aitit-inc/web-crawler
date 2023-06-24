from web_crawler.search import hello
import pytest as pytest


def test_hello(capsys):
    hello()
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'
