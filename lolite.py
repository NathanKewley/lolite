import sys

from lib import output
from lib import deploy


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        output.print_error("Unexpected Arguments")

    elif(sys.argv[1] == "help"):
        output.print_help()

    elif(len(sys.argv) != 3):
        output.print_error("Unexpected Arguments")

    elif(sys.argv[1] == "deploy"):
        deploy.deploy(sys.argv[2])

    elif(sys.argv[1] == "deploy-resource-group"):
        deploy.deploy_resource_group(sys.argv[2])

    elif(sys.argv[1] == "deploy-subscription"):
        deploy.deploy_subscription(sys.argv[2])

    elif(sys.argv[1] == "deploy-account"):
        print("not yet implemented")

    else:
        output.print_error("Unexpected Arguments")
