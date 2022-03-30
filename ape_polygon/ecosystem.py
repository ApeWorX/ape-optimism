from ape.api.config import PluginConfig
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_ethereum.ecosystem import Ethereum, NetworkConfig

NETWORKS = {
    # chain_id, network_id
    "mainnet": (137, 137),
    "mumbai": (80001, 80001),
}


class PolygonConfig(PluginConfig):
    mainnet: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=2)  # type: ignore
    mumbai: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=2)  # type: ignore
    local: NetworkConfig = NetworkConfig(default_provider="test")  # type: ignore
    default_network: str = LOCAL_NETWORK_NAME


class Polygon(Ethereum):
    @property
    def config(self) -> PolygonConfig:  # type: ignore
        return self.config_manager.get_config("polygon")  # type: ignore
