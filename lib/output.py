class print_colors:
    COMMAND = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'

def print_help():
    help_text = """
        lolite Usage:
        - help: show this message
        - deploy: deploy a single configuration
        - deploy-resource-group: deploy all config in a specific resource group
        - deploy-subscription: deploy all config in a specific subscription
        - deploy-account: deploy all config in the account / lolite project 
        see GitHub for more details: https://github.com/NathanKewley/lolite
    """
    print(help_text)

def print_error(error):
    print(f"{print_colors.ERROR}{error}{print_colors.ENDC}")

def print_command(command):
    print(f"{print_colors.COMMAND}{command}{print_colors.ENDC}")

def print_info(info):
    print(info)
