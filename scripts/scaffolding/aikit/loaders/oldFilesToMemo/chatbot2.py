import tiktoken
from typing import TypedDict, Literal

class Msg(TypedDict):
    content: str
    role: Literal["assistant", "user"]


def getTokenNum(msgs: list[Msg]):
    enc = tiktoken.get_encoding("o200k_base")
    return sum(len(enc.encode(m["content"])) for m in msgs)