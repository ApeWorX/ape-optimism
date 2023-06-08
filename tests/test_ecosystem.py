import pytest
from ape_ethereum.transactions import TransactionType


<<<<<<< HEAD
def test_gas_limit(optimism):
=======
def test_gas_limit(networks):
    optimism = networks.optimism
>>>>>>> main
    assert optimism.config.local.gas_limit == "max"


@pytest.mark.parametrize("type", (0, "0x0"))
<<<<<<< HEAD
def test_create_transaction(optimism, type):
=======
def test_create_transaction(networks, type):
    optimism = networks.optimism
>>>>>>> main
    txn = optimism.create_transaction(type=type)
    assert txn.type == TransactionType.STATIC.value
