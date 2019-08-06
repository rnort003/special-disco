param ([string]$addr)
Import-Module AzureAD
### Thanks @nimizen for code to load XML config (StackOverflow)
$configFile = ".\config.xml"
    if(Test-Path $configFile) {
        Try {
            #Load config connsettings
            $global:connSettings = @{}
            $config = [xml](get-content $configFile)
            foreach ($addNode in $config.configuration.connsettings.add) {
                if ($addNode.Value.Contains(',')) {
                    # Array case
                    $value = $addNode.Value.Split(',')
                        for ($i = 0; $i -lt $value.length; $i++) {
                            $value[$i] = $value[$i].Trim()
                        }
                }
                else {
                    # Scalar case
                    $value = $addNode.Value
                }
            $global:connSettings[$addNode.Key] = $value
            }
        }
        Catch [system.exception]{
        }
    }
###
$un = $connSettings["username"]
$SecPass = ConvertTo-SecureString $connSettings["password"] -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential ($un, $SecPass)
Connect-AzureAD -Credential $cred
Get-AzureADUser -SearchString $addr | Revoke-AzureADUserAllRefreshToken
