 <#
.DESCRIPTION
    Installs Scalyr Agent on a Windows OS
.EXAMPLE
    ./scalyr_install.ps1
#>

#Requires -RunAsAdministrator

[CmdletBinding()]
Param (
    [Parameter(Mandatory=$true)]
    [string] $api_key,
    [Parameter(Mandatory=$false)]
    [string] $version = "2.1.17",
    [Parameter(Mandatory=$false)]
    [string] $install_file = "D:\Temp\ScalyrAgentInstaller.msi",
    [Parameter(Mandatory=$false)]
    [string] $agent_config_dir = "C:\Program Files (x86)\Scalyr\config"
)

# Set variables
$install_url = "https://www.scalyr.com/scalyr-repo/stable/latest/ScalyrAgentInstaller-$version.msi"
$software = "Scalyr Agent 2"

# Checks if software is installed
Function IsInstalled() {
  Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Where-Object DisplayName -eq $software | Sort-Object DisplayName | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize
  (Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Where DisplayName -eq $software ) -ne $null
}

Function Replace_Text_In_File() {
  Param (
    [Parameter(Mandatory = $true)]
    [string] $file,
    [Parameter(Mandatory = $true)]
    [string] $find,
    [Parameter(Mandatory = $true)]
    [string] $replace
  )

  Write-Verbose "Finding '$find' and replacing with '$replace' in $file"
  (Get-Content -path "$file" -Raw) -replace $find,$replace | Set-Content -Path "$file"
}

# TODO: Check if proxy set, if not set and unset
# Downloads from URL ($install_url) and saves to file ($install_file)
Function Download_MSI() {
  Invoke-WebRequest -Uri $install_url -OutFile $install_file 
  Get-ChildItem $install_file
}

# TODO: How to install to the D:\ drive instead of default location?
Function Install_MSI($file) {
  $DataStamp = get-date -Format yyyyMMddTHHmmss
  $logFile = '{0}-{1}.log' -f $file,$DataStamp
  $MSIArguments = @(
      "/I $file",
      "/qn",
      # "/passive"
      "/norestart",
      "/l*v",
      $logFile
  )

  Write-Output "Installing Scalyr Agent"
  Start-Process "msiexec.exe" -ArgumentList $MSIArguments -Wait -NoNewWindow 
}

Function Configure_Agent() {
  # TODO: Can we have a blank {} agent.json and everything in snippets?
  Write-Output "Copying $PSScriptRoot\agent.json to $agent_config_dir"
  Copy-Item -Path "$PSScriptRoot\agent.json" -Destination "$agent_config_dir" -Force
  Replace_Text_In_File -file "$agent_config_dir\agent.json" -find 'api_key: "REPLACE_THIS"' -replace "api_key: `"$api_key`""

  Write-Output "Copying $PSScriptRoot\agent.d\logs.json to $agent_config_dir\agent.d"
  Copy-Item -Path "$PSScriptRoot\agent.d\logs.json" -Destination "$agent_config_dir\agent.d" -Force

  Write-Output "Copying $PSScriptRoot\agent.d\monitors.json to $agent_config_dir\agent.d"
  Copy-Item -Path "$PSScriptRoot\agent.d\monitors.json" -Destination "$agent_config_dir\agent.d" -Force

  Write-Output "Copying $PSScriptRoot\agent.d\proxy.json to $agent_config_dir\agent.d"
  Copy-Item -Path "$PSScriptRoot\agent.d\proxy.json" -Destination "$agent_config_dir\agent.d" -Force

  # Let this be customizable from app teams
  Write-Output "Copying $PSScriptRoot\agent.d\server_attributes.json to $agent_config_dir\agent.d"
  Copy-Item -Path "$PSScriptRoot\agent.d\server_attributes.json" -Destination "$agent_config_dir\agent.d"
}

Function Uninstall_MSI($file) {
  $DataStamp = get-date -Format yyyyMMddTHHmmss
  $logFile = '{0}-{1}.log' -f $file,$DataStamp
  $id = (Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Where-Object DisplayName -eq "Scalyr Agent 2").PSChildName
  $MSIArguments = @(
      "/x",
      $id,
      # "/qb!",
      "/qn!",
      "/norestart",
      "/l*v",
      $logFile
  )
  Write-Output "Uninstalling Scalyr Agent - $id"
  Start-Process "msiexec.exe" -ArgumentList $MSIArguments -Wait -NoNewWindow 
}

Function Start_Scaler() {
  Start-Process "C:\Program Files (x86)\Scalyr\bin\scalyr-agent-2.exe" -ArgumentList start -Wait -NoNewWindow
}

$installed = IsInstalled
If(-Not $installed) {
  Write-Output "'$software' NOT is installed.";
  Download_MSI
  Install_MSI $install_file
}
else {
  Write-Output "'$software' is installed."

  $installed_version = (Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Where-Object DisplayName -eq $software | Select-Object DisplayVersion).DisplayVersion
  if ([version]$version -gt [version]$installed_version) {
    Write-Host "Desired Version ($version) is greater than installed version ($installed_version).  Upgrading Scalyr Agent."
    # Uninstall_MSI $install_file
    Download_MSI
    Install_MSI $install_file
  }
  else {
      Write-Host "$a is less than $b"
  }
}

# Always configure agent and restart
IsInstalled
Configure_Agent
Start_Scaler 
