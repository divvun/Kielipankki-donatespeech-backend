using './main.bicep'

param location = 'northeurope'
param acrName = 'acrjietnasiellarecprod'
param storageAccountName = 'strecorderprod001'
param storageContainerName = 'recorder-content'
param containerAppsEnvironmentName = 'cae-jietnasiella-recorder-prod'
param containerAppName = 'ca-recorder-backend-prod'
param containerImageTag = 'prod-latest'

param yleClientId = readEnvironmentVariable('YLE_CLIENT_ID', '')
param yleClientKey = readEnvironmentVariable('YLE_CLIENT_KEY', '')
