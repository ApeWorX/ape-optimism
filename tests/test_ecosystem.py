import pytest
from ape_ethereum.transactions import TransactionType
from ethpm_types.abi import MethodABI


def test_gas_limit(optimism):
    assert optimism.config.local.gas_limit == "max"


# NOTE: None because we want to show the default is STATIC
@pytest.mark.parametrize("tx_type", (None, 0, "0x0"))
def test_create_transaction(optimism, tx_type, eth_tester_provider):
    txn = optimism.create_transaction(type=tx_type)
    assert txn.type == TransactionType.STATIC.value


@pytest.mark.parametrize(
    "tx_type",
    (TransactionType.STATIC.value, TransactionType.DYNAMIC.value),
)
def test_encode_transaction(tx_type, optimism, eth_tester_provider):
    abi = MethodABI.parse_obj(
        {
            "type": "function",
            "name": "fooAndBar",
            "stateMutability": "nonpayable",
            "inputs": [],
            "outputs": [],
        }
    )
    address = "0x274b028b03A250cA03644E6c578D81f019eE1323"
    actual = optimism.encode_transaction(address, abi, sender=address, type=tx_type)
    assert actual.gas_limit == eth_tester_provider.max_gas
