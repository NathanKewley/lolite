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
    parser.add_argument('operation', nargs=1, help=argparse.SUPPRESS, choices=[ "deploy", "deploy-resource-group", "deploy-subscription", "deploy-account"], metavar="operation")
    parser.add_argument('suboperation', nargs='?', default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.operation[0] = args.operation[0].replace("-", "_")
    print(args)
    return args


if __name__ == "__main__":
    args = _parse_args()
    logger.info(args)
    try:
        if args.suboperation is None:
            getattr(deploy, f"{args.operation[0]}")()
        else:
            logger.info(args.suboperation)
            getattr(deploy, f"{args.operation[0]}")(args.suboperation)
    except Exception as e:
        logger.error(e)