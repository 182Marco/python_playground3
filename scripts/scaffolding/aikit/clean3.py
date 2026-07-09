from collections.abc import Callable


def clean(text: str, steps:list[Callable[[str], str]]) -> str:
    for step in steps:
        text = step(text)
    return text