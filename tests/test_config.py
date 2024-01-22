from ape_optimism.ecosystem import OptimismConfig


def test_mainnet_fork_not_configured():
    obj = OptimismConfig.model_validate({})
    assert obj.mainnet_fork.required_confirmations == 0


def test_mainnet_fork_configured():
    data = {"mainnet_fork": {"required_confirmations": 555}}
    obj = OptimismConfig.model_validate(data)
    assert obj.mainnet_fork.required_confirmations == 555
