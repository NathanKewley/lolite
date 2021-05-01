from unittest.mock import patch
import json

from lolite.lib.subproc import Subproc
from lolite.lib.deployer import Deployer
from lolite.lib.subscription import Subscription


def test_resource_group_exists():
    sample_azure_response = open('tests/test_output/test_subproc_get_resource_groups.json', 'r').read()
    with patch.object(Subproc, 'get_resource_groups', return_value = sample_azure_response):
        subproc = Subproc()
        subscription = Subscription(subproc)
        deployer = Deployer(subproc, subscription)

        assert deployer.resource_group_exists("rg-lolite-test-01")
        assert not deployer.resource_group_exists("rg-lolite-test-02")

def test_get_deployment_output():
    sample_azure_response = open('tests/test_output/test_subproc_get_deployment_output.json', 'r').read()
    with patch.object(Subproc, 'get_deployment_output', return_value = sample_azure_response):
        subproc = Subproc()
        subscription = Subscription(subproc)
        deployer = Deployer(subproc, subscription)
        assert deployer.get_deployment_output("lolite-test.rg-lolite-test-01.lolite_automation_storage", "storageLocation","rg-lolite-test-01") == "australiaeast"

def test_get_deployment_output_param():
    sample_azure_response = open('tests/test_output/test_subproc_get_deployment_output.json', 'r').read()
    with patch.object(Subproc, 'get_deployment_output', return_value = sample_azure_response):
        with patch.object(Subproc, 'set_subscription', return_value = True):
            with patch.object(Subscription, 'set_subscription', return_value = True):
                subproc = Subproc()
                subscription = Subscription(subproc)
                deployer = Deployer(subproc, subscription)
                assert deployer.get_deployment_output_param("Ref:lolite-test.rg-lolite-test-01.lolite_automation_storage:storageLocation", "lolite-test")
                assert True

def test_build_param_string():
    sample_azure_response = open('tests/test_output/test_subproc_get_deployment_output.json', 'r').read()
    with patch.object(Subproc, 'get_deployment_output', return_value = sample_azure_response):
        with patch.object(Subproc, 'set_subscription', return_value = True):
            with patch.object(Subscription, 'set_subscription', return_value = True):
                subproc = Subproc()
                subscription = Subscription(subproc)
                deployer = Deployer(subproc, subscription)    
                params = {'location': 'australiaeast', 'storageName': 'lolitestorekew', 'containerName': 'loliteautomation', 'skuName': 'Standard_LRS'}
                assert deployer.build_param_string(params, "lolite-test") == "location=australiaeast storageName=lolitestorekew containerName=loliteautomation skuName=Standard_LRS"
                assert True
