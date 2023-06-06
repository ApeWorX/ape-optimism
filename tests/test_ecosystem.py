import pytest

from ape_ethereum.transactions import TransactionType


@pytest.mark.parametrize("type", (0, "0x0"))
def test_create_transaction(networks, type):
    optimism = networks.optimism
    txn = optimism.create_transaction(type=type)
    assert txn.type == TransactionType.STATIC.value
