def pytest_configure(config):
    config.addinivalue_line("markers", "wip: WORK IN PROGRESS")