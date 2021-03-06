import json

from lolite.lib.orchestrator import Orchestrator


orchestrator = Orchestrator()

def test_deploy_load_config2():
    config_path = "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml"
    config_expected_loaded_output = json.loads(open('tests/test_output/test_deploy_load_config.json', 'r').read())

    config_loaded = orchestrator.load_config(config_path)
    assert type(config_loaded) == dict
    assert config_loaded["bicep_path"] == "automation/automation_account.bicep"
    assert config_loaded["params"]["location"] == "Ref:lolite-test.rg-lolite-test-01.lolite_automation_storage:storageLocation"
    assert config_loaded["params"]["appName"] == "loliteAutomation"
    assert config_loaded["params"]["skuName"] == "Free"
    assert config_loaded == config_expected_loaded_output

def test_deploy_load_location2():
    config_path = "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml"
    config_expected_loaded_location = "australiaeast"

    location_config_loaded = orchestrator.load_location(config_path)
    assert type(location_config_loaded) == str
    assert location_config_loaded == config_expected_loaded_location
