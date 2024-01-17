from typing import Optional, Type, cast

from ape.api.config import PluginConfig
from ape.api.networks import LOCAL_NETWORK_NAME
from ape.exceptions import ApeException
from ape.utils import DEFAULT_LOCAL_TRANSACTION_ACCEPTANCE_TIMEOUT
from ape_ethereum.ecosystem import Ethereum, ForkedNetworkConfig, NetworkConfig
from ape_ethereum.transactions import TransactionType

NETWORKS = {
    # chain_id, network_id
    "mainnet": (10, 10),
    "goerli": (420, 420),
    "sepolia": (11155420, 11155420),
}


class ApeOptimismError(ApeException):
    """
    Raised in the ape-optimism plugin.
    """


def _create_config(
    required_confirmations: int = 1, block_time: int = 2, cls: Type = NetworkConfig, **kwargs
) -> NetworkConfig:
    return cls(
        required_confirmations=required_confirmations,
        block_time=block_time,
        default_transaction_type=TransactionType.DYNAMIC,
        **kwargs,
    )


def _create_local_config(default_provider: Optional[str] = None, use_fork: bool = False, **kwargs):
    return _create_config(
        block_time=0,
        default_provider=default_provider,
        gas_limit="max",
        required_confirmations=0,
        transaction_acceptance_timeout=DEFAULT_LOCAL_TRANSACTION_ACCEPTANCE_TIMEOUT,
        cls=ForkedNetworkConfig if use_fork else NetworkConfig,
        **kwargs,
    )


class OptimismConfig(PluginConfig):
    mainnet: NetworkConfig = _create_config()
    mainnet_fork: ForkedNetworkConfig = _create_local_config(use_fork=True)
    goerli: NetworkConfig = _create_config()
    goerli_fork: ForkedNetworkConfig = _create_local_config(use_fork=True)
    sepolia: NetworkConfig = _create_config()
    sepolia_fork: ForkedNetworkConfig = _create_local_config(use_fork=True)
    local: NetworkConfig = _create_local_config(default_provider="test")
    default_network: str = LOCAL_NETWORK_NAME


class Optimism(Ethereum):
    @property
    def config(self) -> OptimismConfig:  # type: ignore
        return cast(OptimismConfig, self.config_manager.get_config("optimism"))
