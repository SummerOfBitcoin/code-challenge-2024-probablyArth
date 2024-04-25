from os import listdir
from json import loads
from entities.Transaction import Transaction
from output import addToOutput

pool_path = "./test_pool"

for filename in listdir(pool_path):
    file = open(f"{pool_path}/{filename}", "r").read()
    tx_data = loads(file)
    transaction = Transaction(
        tx_data["version"], tx_data["locktime"], tx_data["vin"], tx_data["vout"]
    )
    print(transaction.fees)
    if transaction.fees <= 0:
        continue
    for txIn in transaction.vin:
        if not txIn.verify():
            continue
    addToOutput("")
