from ape import plugins
from ape.api import NetworkAPI, create_network_type
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_geth import GethProvider
from ape_test import LocalProvider

from .ecosystem import NETWORKS, Optimism, OptimismConfig


@plugins.register(plugins.Config)
def config_class():
    return OptimismConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    yield Optimism


@plugins.register(plugins.NetworkPlugin)
def networks():
    for network_name, network_params in NETWORKS.items():
        yield "optimism", network_name, create_network_type(*network_params)

    # NOTE: This works for development providers, as they get chain_id from themselves
    yield "optimism", LOCAL_NETWORK_NAME, NetworkAPI
    yield "optimism", "mainnet-fork", NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "optimism", network_name, GethProvider

    yield "optimism", LOCAL_NETWORK_NAME, LocalProvider
