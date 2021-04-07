# lolite

lolite is an Azure Bicep deployment helper. The main goal is to seperate environment configuration from templates. This is inspired by the AWS Sceptre tool.

## Goals

* Seperation of Bicep configuration and templates
* Deploy individual config / template combinations
* Bulk deploy at different hirachys: Resource Group, Subscription or Account.
* Automated Resource Group Creation

## Not Goals

* Support for anything other than Bicep on Azure
* Support for multiple accounts
