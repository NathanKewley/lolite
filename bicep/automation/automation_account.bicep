param location string
param appName string
param skuName string

resource AutomationAccount 'Microsoft.Automation/automationAccounts@2015-10-31' = {
  name: appName
  properties: {
    sku: {
      name: skuName
    }
  }
  location: location
  tags: {}
}
