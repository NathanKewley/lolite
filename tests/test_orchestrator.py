from lib.orchestrator import Orchestrator


orchestrator = Orchestrator()

def test_get_deployment_name():
    config_path = "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml"
    result = orchestrator.get_deployment_name(config_path)
    assert result == "lolite-test.rg-lolite-test-01.lolite_automation_account"

def test_get_resource_group():
    config_path = "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml"
    result = orchestrator.get_resource_group(config_path)
    assert result == "rg-lolite-test-01"

def test_get_subscription():
    config_path = "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml"
    result = orchestrator.get_subscription(config_path)
    assert result == "lolite-test"

def get_child_items():
    path = "lolite-test/rg-lolite-deploy-me-01"
    result = orchestrator.get_child_items(path)
    assert "rg-lolite-test-01" in result
    assert "rg-lolite-test-02" in result
    assert result.len() == 2
