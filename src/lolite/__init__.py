import sys
import argparse
from argparse import RawTextHelpFormatter

from lolite.lib.logger import Logger as logger
from lolite.lib.orchestrator import Orchestrator

logger = logger.get_logger()
orchestrator = Orchestrator()


def _parse_args():
    parser = argparse.ArgumentParser(prog='lolite', formatter_class=RawTextHelpFormatter, 
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
    return args

def lolite():
    args = _parse_args()
    logger.debug(args)
    try:
        if args.suboperation is None:
            getattr(orchestrator, f"{args.operation[0]}")()
        else:
            getattr(orchestrator, f"{args.operation[0]}")(args.suboperation)
    except Exception as e:
        logger.error(e)
