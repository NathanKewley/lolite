from lib import deploy

def test_deploy_load_config():
    config_path = "lolite-test/rg-lolite-deploy-me-01/lolite_automation_account.yaml"
    config_expected_loaded_output = {
        "bicep_path": "automation/automation_account.bicep",
        "params": {
            "location": "Ref:lolite-test.rg-lolite-deploy-me-01.lolite_automation_storage:storageLocation",
            "appName": "loliteAutomation",
            "skuName": "Free"
        }
    }

    config_loaded = deploy.load_config(config_path)
    assert type(config_loaded) == dict
    assert config_loaded["bicep_path"] == "automation/automation_account.bicep"
    assert config_loaded["params"]["location"] == "Ref:lolite-test.rg-lolite-deploy-me-01.lolite_automation_storage:storageLocation"
    assert config_loaded["params"]["appName"] == "loliteAutomation"
    assert config_loaded["params"]["skuName"] == "Free"
    assert config_loaded == config_expected_loaded_output