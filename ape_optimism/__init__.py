from typing import Any

from ape import plugins


@plugins.register(plugins.Config)
def config_class():
    from ape_optimism.ecosystem import OptimismConfig

    return OptimismConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    from ape_optimism.ecosystem import Optimism

    yield Optimism


@plugins.register(plugins.NetworkPlugin)
def networks():
    from ape.api.networks import (
        LOCAL_NETWORK_NAME,
        ForkedNetworkAPI,
        NetworkAPI,
        create_network_type,
    )

    from ape_optimism.ecosystem import NETWORKS

    for network_name, network_params in NETWORKS.items():
        yield "optimism", network_name, create_network_type(*network_params)
        yield "optimism", f"{network_name}-fork", ForkedNetworkAPI

    # NOTE: This works for local providers, as they get chain_id from themselves
    yield "optimism", LOCAL_NETWORK_NAME, NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    from ape.api.networks import LOCAL_NETWORK_NAME
    from ape_node import Node
    from ape_test import LocalProvider

    from ape_optimism.ecosystem import NETWORKS

    for network_name in NETWORKS:
        yield "optimism", network_name, Node

    yield "optimism", LOCAL_NETWORK_NAME, LocalProvider


def __getattr__(name: str) -> Any:
    if name == "NETWORKS":
        from .ecosystem import NETWORKS

        return NETWORKS

    elif name == "Optimism":
        from .ecosystem import Optimism

        return Optimism

    elif name == "OptimismConfig":
        from .ecosystem import OptimismConfig

        return OptimismConfig

    else:
        raise AttributeError(name)


__all__ = [
    "NETWORKS",
    "Optimism",
    "OptimismConfig",
]
