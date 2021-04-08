# lolite

lolite is an Azure Bicep orchestration tool. The main goal is to seperate environment configuration from templates. This is inspired by the AWS Sceptre tool.

`NOTE: lolite is a MVP and still very much a WIP`

## Goals

* Seperation of Bicep configuration and templates
* Deploy individual configurations
* Bulk deploy at different hirachys: Resource Group, Subscription or Account.
* Automated Resource Group Creation

## Not Goals

* Support for anything other than Bicep on Azure
* Support for multiple accounts

## Requirements

* Python 3.8+
* Azure CLI
* Azure Bicep CLI

## Assumptions

* You have a singlge account with multiple subscriptions
* Each subscription has a unique name
* All deployments are `--mode Incremental`

## Future Features

* Nice output formatting and color
* Stack output/input referencing
* Automatically build deploy dependancy tree based on input/output references
* Paralell deploys
* confgiurable deploy mode

## lolite project structure

A lolite project is structured in the following way:

```
- root/
    - bicep/
        - storage_account_and_container.yaml
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
* `configuration` - this contains your configuration for deployments, the hierachy is important.
* `Subscription_1` - This is the root level under configuration. `Subscription_1` matched exactually the name of a subscription in Azure.
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
  location: australiaeast
  storageName: storagetestlolit1
  containerName: blog
  skuName: Standard_LRS

```

The `bicep_path` here points to the template in the `bicep/` folder of the project. This bicep template is then deployed using the provided `params` block to the subscription and resource group determined by the configuration files path.

If the resource group does not exist lolite will create it for you in the location specified by the `location.yaml` file.

### location.yaml

This is a super simple file that is required for every resource group. It tells lolite what location to create the resource group in if it does not exist. Each resource deployed into that reosurce group inherits the location. An example of a location.yaml:

```
---
location: australiaeast

```

## Usage

lolite is designed to be easy to use and allow scoped control of deployments. At current this is just a python script and not a executatble as such. This is just because I dont know how to do that with python yet lol. 

### Deploying a single configuration

From the root folder of your repository run the following command:

`python3 lolite.py deploy Subscription_1/Resource_Group_1/storage_account_and_container.yaml`

This will deploy a single configuration / template

### Deploying at resource group scope

From the root folder of your repository run the following command:

`python3 lolite.py deploy-resource-group Subscription_1/Resource_Group_1`

This will deploy every configuration file under that resource group

### Deploying at subscription scope

From the root folder of your repository run the following command:

`python3 lolite.py deploy-subscription Subscription_1`

This will deploy each configuration file for each resouce group in the specified subscription

### Deploying at account scope

From the root folder of your repository run the following command:

`python3 lolite.py deploy-account`

This will deploy every configuration file in the project to the appropriate subscriptions and resource groups
