# lolite

lolite is an Azure Bicep orchestration tool. The main goal is to separate environment configuration from templates. This is inspired by the AWS Sceptre tool.

`NOTE: lolite is still very much a WIP`

There is a getting started guide on my blog [here](https://nathan.kewley.me/2021-04-20-orchestrate-azure-bicep-deploys-with-lolite/). This is meant to be complementry to the info in this Readme.

## Goals

* Separation of Bicep configuration and templates
* Deploy individual configurations
* Bulk deploy at different hierarchies: Resource Group, Subscription or Account
* Automated Resource Group Creation
* Automated deployment hierarchy based on output bindings.

## Not Goals

* Support for anything other than Bicep on Azure
* Support for multiple accounts

## Requirements

* Python 3.8+
* Azure CLI
* Azure Bicep CLI

## Building From Source

* Clone this repo
* Build the project `python3 -m build`
* Install `pip3 install dist/lolite-0.0.1-py3-none-any.whl`

## Assumptions

* You have a single account with multiple subscriptions
* Each subscription has a unique name
* All deployments are `--mode Incremental`

## Possible Future Features

* pre and post deploy hooks
* Parallel deploys
* configurable deploy mode

## lolite project structure

A lolite project is structured in the following way:

```
- root/
    - bicep/
        - storage_account_and_container.bicep
    - configuration/
        - Subscription_1/
            - Resource_Group_1/
                - location.yaml
                - storage_account_and_container.yaml
                - config_2.yaml
            - Resource_Group_2/
                - location.yaml
                - config_1.yaml
        - Subscription_2/
            - Resource_Group_1/
                - location.yaml
                - config_1.yaml
```

Given the example structure above a few important things to note:

* `bicep` - this folder contains all of your bicep templates.
* `configuration` - this contains your configuration for deployments, the hierarchy is important.
* `Subscription_1` - This is the root level under configuration. `Subscription_1` matched exactly the name of a subscription in Azure.
* `Resource_Group_1` - At the root level of a given subscription. This sets the resource group for a deployment within that subscription.
* `location.yaml` - A special configuration file to set the location of the resource group.
* `storage_account_and_container.yaml` - This is a deployable configuration. It will link to a template in the `bicep` folder and contain the required parameters.

Sample `bicep` and `configuration` folders are included in the root of this repo.

### Bicep files

This is just a standard bicep template, for example when creating a storage account and container you might have a file such as `storage_account_and_container.yaml` that looks something like:

```
param location string
param storageName string
param containerName string
param skuName string

resource StorageAccount 'Microsoft.Storage/storageAccounts@2019-06-01' = {
  name: storageName
  location: location
  kind: 'Storage'
  sku: {
    name: skuName
  }
}

resource StorageContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2019-06-01' = {
  name: '${StorageAccount.name}/default/${containerName}'
  properties: {
    publicAccess: 'None'
  }
}

output storageLocation string = StorageAccount.properties.primaryLocation
```

### Configuration files

Given the configuration file 

`configuration/Subscription_1/Resource_Group_1/storage_account_and_container.yaml`:
This is broken down into sections as such: 

`<discarded>/<Subscription>/<resource_group>/<config_to_deploy>`

in this case `storage_account_and_container.yaml` might look like the following:

```
---
bicep_path: storage_account.bicep

params:
  storageName: storagetestlolit1
  containerName: blog
  skuName: Standard_LRS
  location: Ref:Subscription_1.Resource_Group_1.config2:storageLocation
```

The `bicep_path` here points to the template in the `bicep/` folder of the project. This bicep template is then deployed using the provided `params` block to the subscription and resource group determined by the configuration files path.

#### Referencing Other Deployment Outputs

Any parameter in the config file prefixes with `Ref:` is a reference to an output from a different deployment. The format for referencing an output from a different deployment is:
`<Ref>:<deployment_path>:<output_name>` where the `deployent_path` replaces `/` with `.`.

When referencing the output from a different deployment lolite will first check if the dependent deployment exists then deploy it if required. If the dependent deployment does exist lolite will look up the output value and use it for the deployment. deployment hierarchy can be of an arbitrary depth and span across the whole project.

If the resource group for a deployment does not exist lolite will create it for you using the location specified by the `location.yaml` file.

### location.yaml

This is a super simple file that is required for every resource group. It tells lolite what location to create the resource group in if it does not exist. Each resource deployed into that resource group inherits the location. An example of a location.yaml:

```
---
location: australiaeast

```

## Usage

lolite is designed to be easy to use and allow scoped control of deployments.

### Deploying a single configuration

From the root folder of your repository run the following command:

`lolite deploy Subscription_1/Resource_Group_1/storage_account_and_container.yaml`

This will deploy a single configuration / template

### Deploying at resource group scope

From the root folder of your repository run the following command:

`lolite deploy-resource-group Subscription_1/Resource_Group_1`

This will deploy every configuration file under that resource group

### Deploying at subscription scope

From the root folder of your repository run the following command:

`lolite deploy-subscription Subscription_1`

This will deploy each configuration file for each resource group in the specified subscription

### Deploying at account scope

From the root folder of your repository run the following command:

`lolite deploy-account`

This will deploy every configuration file in the project to the appropriate subscriptions and resource groups
