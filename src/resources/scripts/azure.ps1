#!/usr/bin/env pwsh

# Install PowerShellGet utils
Install-Module -Name PowerShellGet -Verbose -AcceptLicense -Confirm:$false -Force -SkipPublisherCheck

# Install Azure PowerShell
Install-Module -Name Az -Verbose -AcceptLicense -Confirm:$false -Repository PSGallery -Force -SkipPublisherCheck

# Install Azure RM PowerShell
Install-Module -Name AzureRM -Verbose -AcceptLicense -Confirm:$false -AllowClobber -Force -SkipPublisherCheck