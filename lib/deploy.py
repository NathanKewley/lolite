import yaml

from lib import subproc


def load_config(config):
    with open(f"configuration/{config}") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def load_location(config):
    location_path = "configuration/" + config.split("/")[0] + "/" + config.split("/")[1] + "/location.yaml"
    with open(location_path) as file:
        location = yaml.load(file, Loader=yaml.FullLoader)        
        return(location['location'])

def resource_group_exists(resource_group):
    groups = subproc.run_command("az group list")
    if f"\"name\": \"{resource_group}\"" in groups:
        return True
    return False

def create_resource_group(resource_group, location):
    print(f"Creating resource group: {resource_group}")
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
    azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Complete --parameters {parameters}"
    print(f"Running: {azure_cli_command}")
    deploy_result = subproc.run_command(azure_cli_command)
    if "\"provisioningState\": \"Succeeded\"" in deploy_result:
        print("Deploy Complete")
        return
    print(deploy_result)

def deploy(configuration):
    config = load_config(configuration)
    location = load_location(configuration)
    print(f"Deploying: {configuration}")
    deploy_bicep(config['params'], config['bicep_path'], configuration.split('/')[1], location)

# def deployRg(rg):
#     return 0

# def deploySub(sub):
#     return 0

# def deployAccount(account):
#     return 0
