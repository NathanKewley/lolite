import subprocess
import sys

from lolite.lib.logger import Logger as logger

class Subproc():

    def __init__(self):
        self.logger = logger.get_logger()
        self.logger.propagate = False

    def run_command(self, command):
        result = subprocess.run(command.split(' '), capture_output=True, check=False)
        if result.stdout is not False:
            if type(result.stdout) == bytes:
                return result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
            else:
                return result.stdout + result.stderr
        else:
            return result.stderr

    def get_resource_groups(self, resource_group):
        return self.run_command("az group list --output json")        

    def create_resource_group(self, resource_group, location):
        self.logger.info(f"Creating resource group: '{resource_group}' in {location}")
        azure_cli_command = f"az group create --location {location} --name {resource_group} --output json"
        self.run_command(azure_cli_command)        

    def deploy_group_create(self, bicep, resource_group, deployment_name, parameters):
        azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Incremental --name {deployment_name} --parameters {parameters} --output json"
        self.logger.debug(f"command: {azure_cli_command}")
        return self.run_command(azure_cli_command)    

    def get_deployment_output(self, deployment_name, resource_group):
        azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group} --output json"
        self.logger.debug(f"Getting Deployment Output: {deployment_name}:{output_name}")
        self.logger.debug(f"Azure Command: {azure_cli_command}")
        return self.run_command(azure_cli_command)
