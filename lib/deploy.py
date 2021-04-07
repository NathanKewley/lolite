import yaml

def load_config(config):
    with open(f"configuration/{config}") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def build_param_string(params):
    param_string = ""
    for param, value in params.items():
        param_string = param_string + f"{param}={value} "
    return param_string[:-1]

def deploy_bicep(params, bicep, resource_group):
    parameters = build_param_string(params)
    azure_cli_command = f"az deployment group create -f bicep/{bicep} -g {resource_group} --mode Complete --parameters {parameters}"
    print(azure_cli_command)

def deploy(configuration):
    config = load_config(configuration)
    print(f"Deploying: {configuration}")
    deploy_bicep(config['params'], config['bicep_path'], configuration.split('/')[1])

# def create_resource_group(rg):
#     return 0

# def deployRg(rg):
#     return 0

# def deploySub(sub):
#     return 0

# def deployAccount(account):
#     return 0
