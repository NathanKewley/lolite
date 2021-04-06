def print_help():
    help_text = """
        Lolite Usage:
        - help: show this message
        - deploy: deploy a single configuration
        - deploy-rg: deploy all config in a specific resource group
        - deploy-sub: deploy all config in a specific subscription
        - deploy-account: deploy all config in the account / lolite project 
    """
    print(help_text)

def print_error(error):
    print(error)
    print_help()
