import yaml
import json
import os

from lib import subproc
from lib import output
from lib.logger import Logger as logger


logger = logger.get_logger()


def load_config(config):
    with open(f"configuration/{config}") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def load_location(config):
    location_path = "configuration/" + config.split("/")[0] + "/" + config.split("/")[1] + "/location.yaml"
    with open(location_path) as file:
        location = yaml.load(file, Loader=yaml.FullLoader)        
        return(location['location'])

def get_resource_group(configuration):
    return configuration.split('/')[1]

def get_child_items(path):
    return(os.listdir(path))

def get_subscription(configuration):
    return configuration.split('/')[0]

def set_subscription(subscription_name):
    logger.info(f"Using Subscription: {subscription_name}")
    subscriptions = json.loads(subproc.run_command("az account list"))
    for subscription in subscriptions:
        if subscription['name'] == subscription_name:
            subscription_id = subscription['id']
            azure_cli_command = f"az account set --subscription {subscription_id}"
            subproc.run_command(azure_cli_command)
            return
    logger.error("SUBSCRIPTION NOT FOUND")
    exit()

def resource_group_exists(resource_group):
    groups = subproc.run_command("az group list")
    if f"\"name\": \"{resource_group}\"" in groups:
        return True
    return False

def create_resource_group(resource_group, location):
    output.print_command(f"Creating resource group: {resource_group}")
    azure_cli_command = f"az group create --location {location} --name {resource_group}"
    subproc.run_command(azure_cli_command)

def build_param_string(params):
    param_string = ""
    for param, value in params.items():
        param_string = param_string + f"{param}={value} "
    return param_string[:-1]

def deploy_bicep(params, bicep, resource_group, location):
    if not resource_group_exists(resource_group):
        create_resource_group(resource_group, location)
    
    parameters = build_param_string(params)
    azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Incremental --parameters {parameters}"
    deploy_result = subproc.run_command(azure_cli_command)
    if "\"provisioningState\": \"Succeeded\"" in deploy_result:
        logger.info("Deploy Complete\n")
        return
    logger.info(deploy_result)

# python3 lolite.py deploy lolite-test/rg-deploy-me-01/lolite_automation_account.yaml
def deploy(configuration):
    config = load_config(configuration)
    location = load_location(configuration)
    resource_group = get_resource_group(configuration)
    set_subscription(get_subscription(configuration))
    output.print_command(f"Deploying: {configuration}")
    deploy_bicep(config['params'], config['bicep_path'], resource_group, location)

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
