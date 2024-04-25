from typing import TypedDict


class Vout(TypedDict):
    scriptpubkey: str
    scriptpubkey_asm: str
    scriptpubkey_type: str
    scriptpubkey_address: str
    value: int
