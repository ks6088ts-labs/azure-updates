import logging

from azure_updates.core import call_azure_updates_api, parse_azure_updates


def test_call_azure_updates_api(caplog):
    with caplog.at_level(logging.DEBUG):
        response_json = call_azure_updates_api(top=5)
    assert response_json is not None


def test_parse_azure_updates(caplog):
    with caplog.at_level(logging.DEBUG):
        response_json = call_azure_updates_api(top=5)
        azure_updates = parse_azure_updates(response_json=response_json)
    assert len(azure_updates) == 5
