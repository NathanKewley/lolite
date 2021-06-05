import json

from lolite.lib.logger import Logger as logger
from lolite.lib.subscription import Subscription

class Deployer():

    def __init__(self, subproc, subscription):
        self.logger = logger.get_logger()
        self.logger.propagate = False
        self.subscription = subscription
        self.subproc = subproc

    def resource_group_exists(self, resource_group):
        groups = self.subproc.get_resource_groups()
        if f"\"name\": \"{resource_group}\"" in groups:
            return True
        return False

    def create_resource_group(self, resource_group, location):
        self.subproc.create_resource_group(resource_group, location)

    def get_deployment_output(self, deployment_name, output_name, resource_group):
        result = json.loads(self.subproc.get_deployment_output(deployment_name, resource_group, output_name))
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
        
        self.logger.debug(f"Deployment Name: {deployment_name}")
        parameters = self.build_param_string(params, subscription)
        deploy_result = self.subproc.deploy_group_create(bicep, resource_group, deployment_name, parameters)
        if "\"provisioningState\": \"Succeeded\"" in deploy_result:
            self.logger.debug("Deploy Complete\n")
            return
        self.logger.error(f"DEPLOYMENT FAILED: {deploy_result}")
        exit()

    def deploy_bicep_subscription(self, params, bicep, location, deployment_name, subscription):
        self.subscription.set_subscription(subscription)       
        self.logger.debug(f"Deployment Name: {deployment_name}")
        parameters = self.build_param_string(params, subscription)
        deploy_result = self.subproc.deploy_subscription_create(bicep, deployment_name, parameters, location)
        if "\"provisioningState\": \"Succeeded\"" in deploy_result:
            self.logger.debug("Deploy Complete\n")
            return
        self.logger.error(f"DEPLOYMENT FAILED: {deploy_result}")
        exit()
