# Quick Start

Ecosystem Plugin for Optimism support in Ape.

## Dependencies

- [python3](https://www.python.org/downloads) version 3.9 up to 3.12.

## Installation

### via `ape`

You can install this plugin using `ape`:

```bash
ape plugins install optimism
```

or via config file:

```yaml
# ape-config.yaml
plugins:
  - name: optimism
```

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-optimism
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-optimism.git
cd ape-optimism
python3 setup.py install
```

## Quick Usage

Installing this plugin adds support for the Optimism ecosystem:

```bash
ape console --network optimism:sepolia
```

### OP Stack

Use the `optimism` base-class in any custom networks using the OP stack.
For example, to configure a custom network for Fraxtal network, add the following to your `pyproject.toml`

```toml
[[tool.ape.networks.custom]]
name = "mainnet"
ecosystem = "fraxtal"
# Tell Ape to use optimism as the base plugin, instead of ethereum.
base_ecosystem_plugin = "optimism"
chain_id = 252

# (optional): Configure an RPC. Else, Ape will select a random one automatically.
[tool.ape.node.fraxtal.mainnet]
uri = "https://rpc.frax.com"
```

Or equivalent `ape-config.yaml`:

```yaml
networks:
  custom:
    - name: mainnet
      ecosystem: fraxtal
      base_ecosystem_plugin: optimism
```

There are two main benefits of using Optimism as the base-class instead of Ethereum for networks using the OP stack:

1. **Closer defaults**: The block time default is `2` for Optimism networks, which may be a better default value than Ethereum's higher block time parameters.
2. **Existence of System Transactions**: The Optimism base-class is aware of system transactions, which are transactions invoked by the sequencer.

## Development

Comments, questions, criticisms and pull requests are welcomed.
