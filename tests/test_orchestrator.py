from lolite.lib.orchestrator import Orchestrator


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

def test_get_child_items():
    path = "configuration/lolite-test/"
    result = orchestrator.get_child_items(path)
    assert "rg-lolite-test-01" in result
    assert "rg-lolite-test-02" in result
    assert len(result) == 2

def test_deploy():
    configuration = "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml"
    result = orchestrator.deploy(configuration, dry_run=True)
    print(result)
    assert len(result[0]) == 3
    assert result[0].items() == {('location', 'Ref:lolite-test.rg-lolite-test-01.lolite_automation_storage:storageLocation'), ('appName', 'loliteAutomation'), ('skuName', 'Free')}
    assert result[1] == "automation/automation_account.bicep"
    assert result[2] == "rg-lolite-test-01"
    assert result[3] == "australiaeast"
    assert result[4] == "lolite-test.rg-lolite-test-01.lolite_automation_account"
    assert result[5] == "lolite-test"

def test_deploy_resource_group():
    configuration = "lolite-test/rg-lolite-test-01"
    result = orchestrator.deploy_resource_group(configuration, dry_run=True)
    assert len(result) == 2
    assert "lolite-test/rg-lolite-test-01/lolite_automation_account.yaml" in result
    assert "lolite-test/rg-lolite-test-01/lolite_automation_storage.yaml" in result

def test_deploy_subscription():
    configuration = "lolite-test"
    result = orchestrator.deploy_subscription(configuration, dry_run=True)
    assert len(result) == 2
    assert "lolite-test/rg-lolite-test-01" in result
    assert "lolite-test/rg-lolite-test-02" in result

def test_deploy_account():
    result = orchestrator.deploy_account(dry_run=True)
    assert len(result) == 1
    assert "lolite-test" in result
