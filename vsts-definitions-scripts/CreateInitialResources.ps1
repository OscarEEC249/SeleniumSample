param(
  # Getting the control percentage as an argument
    [Parameter(Mandatory=$true)] [string] $SubscriptionId,
    [Parameter(Mandatory=$true)] [string] $ResourceGroupName,
    [Parameter(Mandatory=$true)] [string] $VmName,
    [Parameter(Mandatory=$true)] [string] $VmAdminUser,
    [Parameter(Mandatory=$true)] [string] $VmAdminPassword,
    [Parameter(Mandatory=$true)] [string] $VstsAccount,
    [Parameter(Mandatory=$true)] [string] $VstsAgentToken,
    [Parameter(Mandatory=$true)] [string] $VstsAgentPool
)

#
# PowerShell configurations
#

# NOTE: Because the $ErrorActionPreference is "Stop", this script will stop on first failure.
#       This is necessary to ensure we capture errors inside the try-catch-finally block.
$ErrorActionPreference = "Stop"

############################################################### MAIN PROCESS ###############################################################

try{
    ####################################### Azure Login ######################################

    Connect-AzureRmAccount

    ####################################### Move to selected Subscription ######################################

    Select-AzureRmSubscription -SubscriptionId $SubscriptionId

    ####################################### Create Resource Group ######################################

    Write-Host("Creating Resource Group...") -ForegroundColor Magenta
    New-AzureRmResourceGroup -Name $ResourceGroupName -Location "Central US"
    Write-Host("Resource Group created") -ForegroundColor Green
    Write-Host("")

    ####################################### Create Storage Account ######################################

    Write-Host("Creating Storage Account...") -ForegroundColor Magenta
    $StorageAccountInfo = New-AzureRMStorageAccount -ResourceGroupName $ResourceGroupName -AccountName "demojavastorage1x" -Location "Central US" -Type "Standard_LRS"
    Write-Host("")
    Write-Host("Storage Account created") -ForegroundColor Green
    Write-Host("")

    ####################################### Create VM ######################################

    # Create a new clean VM
    Write-Host("Creating and Configuring Virtual Machine...") -ForegroundColor Magenta
    $TemplatePath = $PSScriptRoot + "\VM_Template.json"
    $AzureParams = @{
        ResourceGroupName = $ResourceGroupName
        virtualMachineName = $VmName
        adminUsername = $VmAdminUser
        adminPassword = $VmAdminPassword
        diagnosticsStorageAccountName = $StorageAccountInfo.StorageAccountName
        diagnosticsStorageAccountId = $StorageAccountInfo.Id
    }

    New-AzureRmResourceGroupDeployment -ResourceGroupName $ResourceGroupName -ResourceGroupNameFromTemplate $ResourceGroupName -TemplateFile $TemplatePath -TemplateParameterObject $AzureParams
    Start-Sleep 30
    Write-Host("Virtual Machine created")

    # Enable Remote Powershell
    Write-Host("Enabling RemotePS...")
    Invoke-AzureRmVMRunCommand -ResourceGroupName $ResourceGroupName -Name $VmName -CommandId "EnableRemotePS"
    Write-Host("RemotePS enabled")

    # Enable Admin Account
    Write-Host("Enabling Admin Account...")
    Invoke-AzureRmVMRunCommand -ResourceGroupName $ResourceGroupName -Name $VmName -CommandId "EnableAdminAccount"
    Write-Host("Admin Account enabled")

    # Install .NetFramework 3.5
    Write-Host("Installing .NetFramework 3.5...")
    $ScriptPath = $PSScriptRoot + "\NetFrameworkInstall.ps1"
    Invoke-AzureRmVMRunCommand -ResourceGroupName $ResourceGroupName -Name $VmName -CommandId "RunPowerShellScript" -ScriptPath $ScriptPath
    Write-Host("VSTS Agent installed")
    Write-Host(".NetFramework 3.5 installed")
    Start-Sleep 10

    # Run Agent installation on VM
    Write-Host("Installing VSTS Agent...")
    $ScriptPath = $PSScriptRoot + "\VstsAgentInstall.ps1"
    $AgentParams = @{
        vstsAccount = $VstsAccount
        vstsUserPassword = $VstsAgentToken
        agentName = $VmName
        poolName = $VstsAgentPool
        windowsLogonAccount = $VmAdminUser
        windowsLogonPassword = $VmAdminPassword
        driveLetter = "C"
        workDirectory = "_work"
        runMode = "Service"
    }

    Invoke-AzureRmVMRunCommand -ResourceGroupName $ResourceGroupName -Name $VmName -CommandId "RunPowerShellScript" -ScriptPath $ScriptPath -Parameter $AgentParams
    Write-Host("VSTS Agent installed")

    Write-Host("Virtual Machine created and configured complete") -ForegroundColor Green
    Write-Host("")
}
finally
{
    popd
}