from typing import cast

from ape.exceptions import ApeException
from ape_ethereum.ecosystem import (
    BaseEthereumConfig,
    Ethereum,
    NetworkConfig,
    create_network_config,
)

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


# NOTE: Forked networks automatically are included.
class OptimismConfig(BaseEthereumConfig):
    mainnet: NetworkConfig = create_network_config(block_time=2)
    goerli: NetworkConfig = create_network_config(block_time=2)
    sepolia: NetworkConfig = create_network_config(block_time=2)


class Optimism(Ethereum):
    @property
    def config(self) -> OptimismConfig:  # type: ignore
        return cast(OptimismConfig, self.config_manager.get_config("optimism"))
