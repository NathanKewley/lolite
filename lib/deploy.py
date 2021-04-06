import yaml

def load_config(config):
    with open(f"configuration/{config}") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# def create_resource_group(rg):
#     return 0

def build_bicep_deployment(configuration, bicep):
    # need to validate and generate a final bicep template here
    return 0

def deploy_bicep(configuration, bicep):
    build_bicep_deployment(configuration, bicep)
    # os.deploy(az cli here)

def deploy(configuration):
    print(f"Deploying: {configuration}")
    config = load_config(configuration)
    print(config)

# def deployRg(rg):
#     return 0

# def deploySub(sub):
#     return 0

# def deployAccount(account):
#     return 0
