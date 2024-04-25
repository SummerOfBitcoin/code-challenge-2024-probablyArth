import hashlib


class Script:
    operations: list[str]
    stack: list[str] = []
    CMD = {}
    pointer = 0

    def __init__(self, operations: list[str]):
        self.operations = operations
        self.CMD = {
            "OP_0": self.op_0,
            "OP_1": self.op_1,
            "OP_DUP": self.op_dup,
            "OP_EQUAL": self.op_equal,
            "OP_EQUALVERIFY": self.op_equal_verify,
            "OP_PUSHBYTES": self.push_bytes,
            "OP_HASH160": self.op_hash160,
        }

    def verify(self):
        while self.pointer < len(self.operations):
            print(f"Executing: {self.operations[self.pointer]}")
            self.CMD[self.operations[self.pointer]]()
            self.pointer += 1
            print(self.stack)

    def op_hash160(self):
        if not self.stack:
            return False
        element = self.stack.pop()
        hashed = hashlib.new("ripemd160", hashlib.sha256(element)).digest()
        self.stack.append(hashed)
        return True

    def push_bytes(self):
        self.pointer += 1
        self.stack.append(self.operations[self.pointer])

    def op_equal_verify(self):
        if not self.op_equal():
            return False
        if not self.op_verify():
            return False
        return True

    def op_equal(self):
        if len(self.stack) < 2:
            return False
        a = self.stack.pop()
        b = self.stack.pop()
        if a == b:
            self.op_1()
        else:
            self.op_0()
        return True

    def op_verify(self):
        if not self.stack:
            return False
        top = self.stack[-1]
        if len(top) == 0:
            return False
        return True

    def op_dup(self):
        if len(self.stack) < 1:
            return False
        self.stack.append(self.stack[-1])
        return True

    def op_0(self):
        self.stack.append(hex(0))
        return True

    def op_1(self):
        self.stack.append(hex(1))
        return True

    def op_2(self):
        self.stack.append(hex(2))
        return True

    def op_3(self):
        self.stack.append(hex(3))
        return True


# Operations = {
#     OpCode.OP_RIPEMD160: op_ripemd160,
#     OpCode.OP_SHA1: op_sha1,
#     OpCode.OP_SHA256: op_sha256,
#     OpCode.OP_HASH160: op_hash160,
#     OpCode.OP_HASH256: op_hash256,
#     OpCode.OP_CHECKSIG: op_check_sig,
#     OpCode.OP_CHECKSIGVERIFY: op_check_sig_verify,
#     OpCode.OP_CHECKMULTISIG: op_check_multi_sig,
# }


def encode_num(num):
    if num == 0:
        return b""
    bytes_arr = []
    neg = num < 0
    abs_num = num if num > 0 else -num

    while abs_num > 0:
        bytes_arr.append(abs_num & 0xFF)
        abs_num >>= 8

    if bytes_arr[-1] & 0x80:
        if neg:
            bytes_arr.append(0x80)
        else:
            bytes_arr.append(0x00)
    else:
        if neg:
            bytes_arr[-1] |= 0x80

    return bytes(bytes_arr)


def decode_num(buf):
    if not buf:
        return 0

    be = buf[::-1]

    neg = False
    result = 0

    if be[0] & 0x80:
        neg = True
        be[0] &= 0x7F

    result = be[0]

    for b in be[1:]:
        result <<= 8
        result += b

    if neg:
        return -result
    else:
        return result
