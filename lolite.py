import sys
import argparse
from argparse import RawTextHelpFormatter

from lib import output
from lib import deploy
from lib.logger import Logger as logger


logger = logger.get_logger()


def _parse_args():
    parser = argparse.ArgumentParser(prog='lolite.py', formatter_class=RawTextHelpFormatter, 
    description="""lolite Usage:
        - deploy: deploy a single configuration
        - deploy-resource-group: deploy all config in a specific resource group
        - deploy-subscription: deploy all config in a specific subscription
        - deploy-account: deploy all config in the account / lolite project
        see GitHub for more details: https://github.com/NathanKewley/lolite """)
    parser.add_argument('operation', nargs='+', help=argparse.SUPPRESS, choices=[ "deploy", "deploy-resource-group", "deploy-subscription", "deploy-account"], metavar="operation")
    parser.add_argument('suboperation', nargs='+', help=argparse.SUPPRESS)
    args = parser.parse_args()
    print(args)
    return args


if __name__ == "__main__":
    args = _parse_args()
    logger.info("test")
    logger.error("test fail")
    logger.info(args)
    try:
        getattr(deploy, f"{args.operation[0]}")(args.suboperation[0])
    except Exception as e:
        logger.error(e)
    
    # if len(sys.argv) <= 1:
    #     output.print_error("Unexpected Arguments")
    #     output.print_help()

    # elif(sys.argv[1] == "help"):
    #     output.print_help()

    # elif(sys.argv[1] == "deploy"):
    #     deploy.deploy(sys.argv[2])

    # elif(sys.argv[1] == "deploy-resource-group"):
    #     deploy.deploy_resource_group(sys.argv[2])

    # elif(sys.argv[1] == "deploy-subscription"):
    #     deploy.deploy_subscription(sys.argv[2])

    # elif(sys.argv[1] == "deploy-account"):
    #     deploy.deploy_account()

    # else:
    #     output.print_error("Unexpected Arguments")
    #     output.print_help()
