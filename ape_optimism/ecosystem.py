from typing import TYPE_CHECKING, cast

from ape.api import TransactionAPI
from ape.exceptions import ApeException, APINotImplementedError
from ape_ethereum.ecosystem import (
    BaseEthereumConfig,
    Ethereum,
    NetworkConfig,
    create_network_config,
)

if TYPE_CHECKING:
    from eth_pydantic_types import HexBytes

NETWORKS = {
    # chain_id, network_id
    "mainnet": (10, 10),
    "sepolia": (11155420, 11155420),
}
SYSTEM_TRANSACTION = 126


class ApeOptimismError(ApeException):
    """
    Raised in the ape-optimism plugin.
    """


# NOTE: Forked networks automatically are included.
class OptimismConfig(BaseEthereumConfig):
    mainnet: NetworkConfig = create_network_config(block_time=2)
    sepolia: NetworkConfig = create_network_config(block_time=2)


class SystemTransaction(TransactionAPI):
    type: int = SYSTEM_TRANSACTION

    @property
    def txn_hash(self) -> "HexBytes":
        raise APINotImplementedError("Unable to calculate the hash of system transactions.")

    def serialize_transaction(self) -> bytes:
        raise APINotImplementedError("Unable to serialize system transactions.")


class Optimism(Ethereum):
    @property
    def config(self) -> OptimismConfig:  # type: ignore
        return cast(OptimismConfig, self.config_manager.get_config("optimism"))

    def create_transaction(self, **kwargs) -> TransactionAPI:
        if kwargs.get("type") == SYSTEM_TRANSACTION:
            return SystemTransaction.model_validate(kwargs)

        return super().create_transaction(**kwargs)
