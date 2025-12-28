import pytest

from template_project import hello


def test_hello() -> None:
    assert hello() == "Hello, World!"


@pytest.mark.asyncio
async def test_async_dummy() -> None:
    assert True
