from typing import List
from .Vin import Vin
from .Vout import Vout


class Transaction:
    version: int
    locktime: int
    vin: List[Vin]
    vout: List[Vout]
    fees: int

    def __init__(self, version, locktime, vin, vout):
        self.version = version
        self.locktime = locktime
        self.vin = [Vin(v) for v in vin]
        self.vout = [Vout(v) for v in vout]
        self.fees = self.calculateFees()

    def calculateFees(self):
        inSum: int = 0
        outSum: int = 0
        for i in self.vin:
            inSum += i.prevout["value"]
        for i in self.vout:
            outSum += i["value"]
        return inSum - outSum

    def __str__(self) -> str:
        return f"version: {self.version}\nlocktime: {self.locktime}\nvin: {self.vin}\nvout: {self.vout}"
