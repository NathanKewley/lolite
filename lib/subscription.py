import json

from lib.subproc import Subproc
from lib.logger import Logger as logger


class Subscription():

    def __init__(self):
        self.logger = logger.get_logger()
        self.logger.propagate = False
        self.subproc = Subproc()

    def check_if_current(self, subscription_name):
        if subscription_name in self.subproc.run_command("az account show --output json"):
            return True
        return False

    def set_subscription(self, subscription_name):
        if not self.check_if_current(subscription_name):
            self.logger.info(f"Setting Subscription: {subscription_name}")
            subscriptions = json.loads(self.subproc.run_command("az account list --output json"))
            for subscription in subscriptions:
                if subscription['name'] == subscription_name:
                    subscription_id = subscription['id']
                    azure_cli_command = f"az account set --subscription {subscription_id} --output json"
                    result = self.subproc.run_command(azure_cli_command)
                    return
            self.logger.error("SUBSCRIPTION NOT FOUND")
            exit()
