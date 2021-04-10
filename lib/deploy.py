import yaml
import json
import os

from lib import subproc
from lib.logger import Logger as logger

logger = logger.get_logger()
logger.propagate = False


def load_config(config):
    with open(f"configuration/{config}") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def load_location(config):
    location_path = "configuration/" + config.split("/")[0] + "/" + config.split("/")[1] + "/location.yaml"
    with open(location_path) as file:
        location = yaml.load(file, Loader=yaml.FullLoader)        
        return(location['location'])

def get_deployment_name(configuration):
    return configuration.replace("/",".")[:-5]

def get_resource_group(configuration):
    return configuration.split('/')[1]

def get_child_items(path):
    return(os.listdir(path))

def get_subscription(configuration):
    return configuration.split('/')[0]

def set_subscription(subscription_name):
    subscriptions = json.loads(subproc.run_command("az account list --output json"))
    for subscription in subscriptions:
        if subscription['name'] == subscription_name:
            subscription_id = subscription['id']
            azure_cli_command = f"az account set --subscription {subscription_id} --output json"
            subproc.run_command(azure_cli_command)
            return
    logger.error("SUBSCRIPTION NOT FOUND")
    exit()

def resource_group_exists(resource_group):
    groups = subproc.run_command("az group list --output json")
    if f"\"name\": \"{resource_group}\"" in groups:
        return True
    return False

def create_resource_group(resource_group, location):
    logger.warning(f"Creating resource group: '{resource_group}' in {location}")
    azure_cli_command = f"az group create --location {location} --name {resource_group} --output json"
    subproc.run_command(azure_cli_command)

def get_deployment_deployment(deployment_name, resource_group):
    azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group}"
    result = subproc.run_command(azure_cli_command)
    if "\"provisioningState\": \"Succeeded\"" in result:
        return True
    return False

def get_deployment_output(deployment_name, output_name, resource_group):
    azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group} --output json"
    logger.info(f"Getting Deployment Output: {deployment_name}:{output_name}")
    result = json.loads(subproc.run_command(azure_cli_command))
    if "could not be found" in result:
        logger.error("DEPLOYMENT NOT FOUND: {deployment_name}")
        exit()
    if not "outputs" in result["properties"]:
        logger.error("Deployment output not found: {deployment_name}:{output_name}")
        exit()        
    if not output_name in result["properties"]["outputs"]:
        logger.error("Deployment output not found: {deployment_name}:{output_name}")
        exit()                
    return(result["properties"]["outputs"][output_name]["value"])

def get_deployment_output_param(value, subscription):
    deployment_name = value.split(":")[1]
    output_name = value.split(":")[2]
    resource_group = value.split(":")[1][1:].split(".")[1]
    parameter_subscription = value.split(":")[1].split(".")[0]
    set_subscription(parameter_subscription)

    # Deploy dependant deployment
    if not get_deployment_deployment(deployment_name, resource_group):
        deployment_config_path = deployment_name.replace(".","/") + ".yaml"
        logger.warning("Dependant deployment not deployed. deploying: {deployment_config_path}")
        deploy(deployment_config_path)

    value = get_deployment_output(deployment_name, output_name, resource_group)
    set_subscription(subscription)
    return value

def build_param_string(params, subscription):
    param_string = ""
    for param, value in params.items():
        if value.startswith("Ref:"):
            value = get_deployment_output_param(value, subscription)
        param_string = param_string + f"{param}={value} "
    return param_string[:-1]

def deploy_bicep(params, bicep, resource_group, location, deployment_name, subscription):
    set_subscription(subscription)  
    if not resource_group_exists(resource_group):
        create_resource_group(resource_group, location)
      
    logger.info(f"Deployment Name: {deployment_name}")
    parameters = build_param_string(params, subscription)
    azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Incremental --name {deployment_name} --parameters {parameters} --output json"
    deploy_result = subproc.run_command(azure_cli_command)
    if "\"provisioningState\": \"Succeeded\"" in deploy_result:
        logger.info("Deploy Complete\n")
        return
    logger.error(deploy_result)

# python3 lolite.py deploy lolite-test/rg-deploy-me-01/lolite_automation_account.yaml
def deploy(configuration):
    config = load_config(configuration)
    location = load_location(configuration)
    deployment_name = get_deployment_name(configuration)
    subscription = get_subscription(configuration)
    resource_group = get_resource_group(configuration)
    logger.warning(f"Deploying: {configuration} to {subscription}")
    deploy_bicep(config['params'], config['bicep_path'], resource_group, location, deployment_name, subscription)

# python3 lolite.py deploy-resource-group lolite-test/rg-deploy-me-01
def deploy_resource_group(configuration):
    subscription = get_subscription(configuration)
    resource_group = get_resource_group(configuration)
    deployments = get_child_items(f"configuration/{configuration}/")
    for deployment in deployments:
        if deployment != "location.yaml":
            deploy(f"{subscription}/{resource_group}/{deployment}")

# python3 lolite.py deploy-subscription lolite-test
def deploy_subscription(configuration):
    subscription = get_subscription(configuration)
    resource_groups = get_child_items(f"configuration/{configuration}/")
    for resource_group in resource_groups:
        deploy_resource_group(f"{configuration}/{resource_group}")

# python3 lolite.py deploy-account
def deploy_account():
    subscriptions = get_child_items("configuration/")
    for subscription in subscriptions:
        deploy_subscription(subscription)
