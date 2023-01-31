EXPECTED_OUTPUT = """
optimism
├── mainnet
│   └── geth  (default)
├── goerli
│   └── geth  (default)
└── local  (default)
    └── test  (default)
""".strip()


def assert_rich_text(actual: str, expected: str):
    """
    The output from `rich` causes a bunch of extra spaces to
    appear at the end of each line. For easier testing, we remove those here.
    Also, we ignore whether the expected line is at the end or in the middle
    of the output to handle cases when the test-runner has additional plugins
    installed.
    """
    expected_lines = [
        x.replace("└", "").replace("├", "").replace("│", "").strip()
        for x in expected.strip().split("\n")
    ]
    actual_lines = [
        x.replace("└", "").replace("├", "").replace("│", "").strip()
        for x in actual.strip().split("\n")
    ]

    for expected_line in expected_lines:
        assert expected_line in actual_lines


def test_networks(runner, cli):
    result = runner.invoke(cli, ["networks", "list"])
    assert_rich_text(result.output, EXPECTED_OUTPUT)
