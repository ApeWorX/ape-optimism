from ape_ethereum.transactions import TransactionType


def test_create_transaction(networks):
    optimism = networks.optimism
    txn = optimism.create_transaction(type=0)
    assert txn.type == TransactionType.STATIC.value
