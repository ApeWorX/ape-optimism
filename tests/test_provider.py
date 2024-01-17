def test_use_provider(accounts, networks):
    with networks.optimism.local.use_provider("test"):
        account = accounts.test_accounts[0]
        receipt = account.transfer(account, 100)

        assert not receipt.failed
        assert receipt.value == 100
        assert receipt.type == 2
