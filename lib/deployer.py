import yaml
import json
import os

from lib.subproc import Subproc
from lib.logger import Logger as logger
from lib.subscription import Subscription

class Deployer():

    def __init__(self):
        self.logger = logger.get_logger()
        self.logger.propagate = False
        self.subscription = Subscription()
        self.subproc = Subproc()

    def resource_group_exists(self, resource_group):
        groups = self.subproc.run_command("az group list --output json")
        if f"\"name\": \"{resource_group}\"" in groups:
            return True
        return False

    def create_resource_group(self, resource_group, location):
        self.logger.warning(f"Creating resource group: '{resource_group}' in {location}")
        azure_cli_command = f"az group create --location {location} --name {resource_group} --output json"
        self.subproc.run_command(azure_cli_command)

    def get_deployment_output(self, deployment_name, output_name, resource_group):
        azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group} --output json"
        self.logger.info(f"Getting Deployment Output: {deployment_name}:{output_name}")
        result = self.subproc.run_command(azure_cli_command)
        if not result:
            self.logger.error(f"DEPLOYMENT NOT FOUND: {deployment_name}")
            exit()            
        if "could not be found" in result:
            self.logger.error(f"DEPLOYMENT NOT FOUND: {deployment_name}")
            exit()
        if not result["properties"]["outputs"][output_name]:
            self.logger.error(f"Deployment output not found: {deployment_name}:{output_name}")
            exit()                            
        return(result["properties"]["outputs"][output_name]["value"])

    def get_deployment_output_param(self, value, subscription):
        deployment_name = value.split(":")[1]
        output_name = value.split(":")[2]
        resource_group = value.split(":")[1][1:].split(".")[1]
        parameter_subscription = value.split(":")[1].split(".")[0]

        self.subscription.set_subscription(parameter_subscription)
        value = self.get_deployment_output(deployment_name, output_name, resource_group)
        self.subscription.set_subscription(subscription)
        return value

    def build_param_string(self, params, subscription):
        param_string = ""
        for param, value in params.items():
            if value.startswith("Ref:"):
                value = self.get_deployment_output_param(value, subscription)
            param_string = param_string + f"{param}={value} "
        return param_string[:-1]

    def deploy_bicep(self, params, bicep, resource_group, location, deployment_name, subscription):
        self.subscription.set_subscription(subscription)  
        if not self.resource_group_exists(resource_group):
            self.create_resource_group(resource_group, location)
        
        self.logger.info(f"Deployment Name: {deployment_name}")
        parameters = self.build_param_string(params, subscription)
        azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Incremental --name {deployment_name} --parameters {parameters} --output json"
        self.logger.info(f"command: {azure_cli_command}")
        deploy_result = self.subproc.run_command(azure_cli_command)
        if "\"provisioningState\": \"Succeeded\"" in deploy_result:
            self.logger.info("Deploy Complete\n")
            return
        self.logger.error(f"DEPLOYMENT FAILED: {deploy_result}")
        exit()
