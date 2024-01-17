import pytest
from ape_ethereum.transactions import TransactionType
from ethpm_types.abi import MethodABI


def test_gas_limit(optimism):
    assert optimism.config.local.gas_limit == "max"


@pytest.mark.parametrize(
    "tx_kwargs",
    [
        {"type": 0},
        {"gas_price": 0},
        {"gasPrice": 0},
    ],
)
def test_create_transaction_type_0(optimism, tx_kwargs):
    txn = optimism.create_transaction(**tx_kwargs)
    assert txn.type == TransactionType.STATIC.value


@pytest.mark.parametrize(
    "tx_kwargs",
    [
        {},  # Default is type 2 in Optimism.
        {"type": 2},
        {"max_fee": 0},
        {"max_fee_per_gas": 0},
        {"maxFee": 0},
        {"max_priority_fee_per_gas": 0},
        {"max_priority_fee": 0},
        {"maxPriorityFeePerGas": 0},
    ],
)
def test_create_transaction_type_2(optimism, tx_kwargs):
    """
    Show is smart-enough to deduce type 2 transactions.
    """

    txn = optimism.create_transaction(**tx_kwargs)
    assert txn.type == TransactionType.DYNAMIC.value


@pytest.mark.parametrize(
    "tx_type",
    (TransactionType.STATIC.value, TransactionType.DYNAMIC.value),
)
def test_encode_transaction(tx_type, optimism, eth_tester_provider):
    abi = MethodABI.model_validate(
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
