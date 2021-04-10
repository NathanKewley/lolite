import yaml
import json
import os

from lib import subproc
from lib import output


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
    output.print_info(f"Using Subscription: {subscription_name}")
    subscriptions = json.loads(subproc.run_command("az account list"))
    for subscription in subscriptions:
        if subscription['name'] == subscription_name:
            subscription_id = subscription['id']
            azure_cli_command = f"az account set --subscription {subscription_id}"
            subproc.run_command(azure_cli_command)
            return
    output.print_error("SUBSCRIPTION NOT FOUND")
    exit()

def resource_group_exists(resource_group):
    groups = subproc.run_command("az group list")
    if f"\"name\": \"{resource_group}\"" in groups:
        return True
    return False

def create_resource_group(resource_group, location):
    output.print_command(f"Creating resource group: '{resource_group}' in {location}")
    azure_cli_command = f"az group create --location {location} --name {resource_group}"
    subproc.run_command(azure_cli_command)

def get_stack_deployment(deployment_name, resource_group):
    azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group}"
    result = subproc.run_command(azure_cli_command)
    if "\"provisioningState\": \"Succeeded\"" in result:
        return True
    return False

def get_stack_output(deployment_name, output_name, resource_group):
    azure_cli_command = f"az deployment group show --name {deployment_name} --resource-group {resource_group}"
    print(f"Getting stack output: {azure_cli_command}")
    result = json.loads(subproc.run_command(azure_cli_command))
    return(result["properties"]["outputs"][output_name]["value"])

def get_stack_output_param(value):
    deployment_name = value.split(":")[1]
    output_name = value.split(":")[2]
    resource_group = value.split(":")[1][1:].split(".")[1]

    # Deploy dependant stack
    if not get_stack_deployment(deployment_name, resource_group):
        deployment_config_path = deployment_name.replace(".","/") + ".yaml"
        output.print_info("Dependant stack not deployed. deploying: {deployment_config_path}")
        deploy(deployment_config_path)

    value = get_stack_output(deployment_name, output_name, resource_group)
    return value

def build_param_string(params):
    param_string = ""
    for param, value in params.items():
        if value.startswith("Ref:"):
            value = get_stack_output_param(value)
        param_string = param_string + f"{param}={value} "
    return param_string[:-1]

def deploy_bicep(params, bicep, resource_group, location, deployment_name, subscription):
    if not resource_group_exists(resource_group):
        create_resource_group(resource_group, location)
    
    output.print_command(f"Deployment Name: {deployment_name}")
    parameters = build_param_string(params)
    set_subscription(subscription)
    azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Incremental --name {deployment_name} --parameters {parameters}"
    deploy_result = subproc.run_command(azure_cli_command)
    if "\"provisioningState\": \"Succeeded\"" in deploy_result:
        output.print_info("Deploy Complete\n")
        return
    output.print_error(deploy_result)

# python3 lolite.py deploy lolite-test/rg-deploy-me-01/lolite_automation_account.yaml
def deploy(configuration):
    config = load_config(configuration)
    location = load_location(configuration)
    deployment_name = get_deployment_name(configuration)
    subscription = get_subscription(configuration)
    resource_group = get_resource_group(configuration)
    output.print_command(f"Deploying: {configuration}")
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
