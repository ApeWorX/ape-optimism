from typing import Dict, Optional, Type, Union, cast

from ape.api import TransactionAPI
from ape.api.config import PluginConfig
from ape.api.networks import LOCAL_NETWORK_NAME
from ape.exceptions import ApeException
from ape.types import TransactionSignature
from ape_ethereum.ecosystem import Ethereum, NetworkConfig
from ape_ethereum.transactions import (
    AccessListTransaction,
    DynamicFeeTransaction,
    StaticFeeTransaction,
    TransactionType,
)

NETWORKS = {
    # chain_id, network_id
    "mainnet": (10, 10),
    "goerli": (420, 420),
}


class ApeOptimismError(ApeException):
    """
    Raised in the ape-optimism plugin.
    """


def _create_network_config(
    required_confirmations: int = 1, block_time: int = 2, **kwargs
) -> NetworkConfig:
    return NetworkConfig(
        required_confirmations=required_confirmations, block_time=block_time, **kwargs
    )


def _create_local_config(default_provider: Optional[str] = None) -> NetworkConfig:
    return _create_network_config(
        required_confirmations=0, block_time=0, default_provider=default_provider, gas_limit="max"
    )


class OptimismConfig(PluginConfig):
    mainnet: NetworkConfig = _create_network_config()
    mainnet_fork: NetworkConfig = _create_local_config()
    goerli: NetworkConfig = _create_network_config()
    goerli_fork: NetworkConfig = _create_local_config()
    local: NetworkConfig = _create_local_config(default_provider="test")
    default_network: str = LOCAL_NETWORK_NAME


class Optimism(Ethereum):
    @property
    def config(self) -> OptimismConfig:  # type: ignore
        return cast(OptimismConfig, self.config_manager.get_config("optimism"))

    def create_transaction(self, **kwargs) -> TransactionAPI:
        """
        Returns a transaction using the given constructor kwargs.
        Overridden because does not support

        **kwargs: Kwargs for the transaction class.

        Returns:
            :class:`~ape.api.transactions.TransactionAPI`
        """

        transaction_type = self.get_transaction_type(kwargs.get("type"))
        kwargs["type"] = transaction_type.value
        txn_class = _get_transaction_cls(transaction_type)

        if "required_confirmations" not in kwargs or kwargs["required_confirmations"] is None:
            # Attempt to use default required-confirmations from `ape-config.yaml`.
            required_confirmations = 0
            active_provider = self.network_manager.active_provider
            if active_provider:
                required_confirmations = active_provider.network.required_confirmations

            kwargs["required_confirmations"] = required_confirmations

        if isinstance(kwargs.get("chainId"), str):
            kwargs["chainId"] = int(kwargs["chainId"], 16)

        if "hash" in kwargs:
            kwargs["data"] = kwargs.pop("hash")

        if all(field in kwargs for field in ("v", "r", "s")):
            kwargs["signature"] = TransactionSignature(
                v=kwargs["v"],
                r=bytes(kwargs["r"]),
                s=bytes(kwargs["s"]),
            )

        return txn_class.parse_obj(kwargs)

    def get_transaction_type(self, _type: Optional[Union[int, str, bytes]]) -> TransactionType:
        if _type is None:
            version = TransactionType.STATIC
        elif not isinstance(_type, int):
            version = TransactionType(self.conversion_manager.convert(_type, int))
        else:
            version = TransactionType(_type)
        return version


def _get_transaction_cls(transaction_type: TransactionType) -> Type[TransactionAPI]:
    transaction_types: Dict[TransactionType, Type[TransactionAPI]] = {
        TransactionType.STATIC: StaticFeeTransaction,
        TransactionType.DYNAMIC: DynamicFeeTransaction,
        TransactionType.ACCESS_LIST: AccessListTransaction,
    }
    if transaction_type not in transaction_types:
        raise ApeOptimismError(f"Transaction type '{transaction_type}' not supported.")

    return transaction_types[transaction_type]
