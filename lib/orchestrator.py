import yaml
import json
import os

from lib.subproc import Subproc
from lib.logger import Logger as logger
from lib.deployer import Deployer
from lib.subscription import Subscription

class Orchestrator():

    def __init__(self):
        self.logger = logger.get_logger()
        self.logger.propagate = False
        self.deployer = Deployer()
        self.subscription = Subscription()
        self.subproc = Subproc()

    def get_deployment_name(self, configuration):
        return configuration.replace("/",".")[:-5]

    def get_resource_group(self, configuration):
        return configuration.split('/')[1]

    def get_subscription(self, configuration):
        return configuration.split('/')[0]

    def get_child_items(self, path):
        return(os.listdir(path))

    def load_config(self, config):
        with open(f"configuration/{config}") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def load_location(self, config):
        location_path = "configuration/" + config.split("/")[0] + "/" + config.split("/")[1] + "/location.yaml"
        with open(location_path) as file:
            location = yaml.load(file, Loader=yaml.FullLoader)        
            return(location['location'])

    def get_deployment(self, deployment_name, resource_group):
        azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group}"
        result = ""
        try:
            result = self.subproc.run_command(azure_cli_command)
        except:
            self.logger.error(f"Error running: {azure_cli_command}")
        if "\"provisioningState\": \"Succeeded\"" in result:
            return True
        return False

    def check_deployment_dependancy(self, value, subscription):
        deployment_name = value.split(":")[1]
        output_name = value.split(":")[2]
        resource_group = value.split(":")[1][1:].split(".")[1]
        parameter_subscription = value.split(":")[1].split(".")[0]

        self.subscription.set_subscription(parameter_subscription)
        if not self.get_deployment(deployment_name, resource_group):
            deployment_config_path = deployment_name.replace(".","/") + ".yaml"
            self.logger.warning(f"Dependant deployment not deployed. deploying: {deployment_config_path}")
            self.deploy(deployment_config_path)
        self.subscription.set_subscription(subscription)

    def deploy(self, configuration):
        config = self.load_config(configuration)
        location = self.load_location(configuration)
        deployment_name = self.get_deployment_name(configuration)
        subscription = self.get_subscription(configuration)
        resource_group = self.get_resource_group(configuration)

        # deploy dependant deployments before this one
        for param, value in config['params'].items():
            if "Ref:" in value:
                self.check_deployment_dependancy(value, subscription)

        self.logger.warning(f"Deploying: {configuration} to {subscription}")
        self.deployer.deploy_bicep(config['params'], config['bicep_path'], resource_group, location, deployment_name, subscription)

    def deploy_resource_group(self, configuration):
        subscription = self.get_subscription(configuration)
        resource_group = self.get_resource_group(configuration)
        deployments = self.get_child_items(f"configuration/{configuration}/")
        for deployment in deployments:
            if deployment != "location.yaml":
                self.deploy(f"{subscription}/{resource_group}/{deployment}")

    def deploy_subscription(self, configuration):
        subscription = self.get_subscription(configuration)
        resource_groups = self.get_child_items(f"configuration/{configuration}/")
        for resource_group in resource_groups:
            self.deploy_resource_group(f"{configuration}/{resource_group}")

    def deploy_account(self):
        subscriptions = self.get_child_items("configuration/")
        for subscription in subscriptions:
            self.deploy_subscription(subscription)
