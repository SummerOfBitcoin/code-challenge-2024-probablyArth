from typing import TypedDict
from .Script import Script


class Prevout(TypedDict, total=False):
    scriptpubkey: str
    scriptpubkey_asm: str
    scriptpubkey_type: str
    scriptpubkey_address: str
    value: int


class Vin:
    txid: str
    vout: int
    prevout: Prevout
    scriptsig: str
    scriptsig_asm: str
    is_coinbase: bool
    sequence: int

    def __init__(self, v):
        self.txid = v["txid"]
        self.vout = v["vout"]
        self.prevout = Prevout(v["prevout"])
        self.scriptsig = v["scriptsig"]
        self.scriptsig_asm = v["scriptsig_asm"]
        self.is_coinbase = v["is_coinbase"]
        self.sequence = v["sequence"]

    def verify(self) -> bool:
        match self.prevout["scriptpubkey_type"]:
            case "p2pkh":
                operations = []
                for operation in self.scriptsig_asm.split(" "):
                    if operation.startswith("OP_PUSHBYTES"):
                        operations.append("OP_PUSHBYTES")
                    else:
                        operations.append(operation)

                for operation in self.prevout["scriptpubkey_asm"].split(" "):
                    if operation.startswith("OP_PUSHBYTES"):
                        operations.append("OP_PUSHBYTES")
                    else:
                        operations.append(operation)
                script = Script(operations)
                return script.verify()

        return False
