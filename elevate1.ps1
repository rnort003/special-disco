param ([string]$addr)
### Thanks @nimizen for code to load XML config (StackOverflow)
$configFile = ".\configexample.xml"
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

$un = $connSettings["PSusername"]
$SecPass = ConvertTo-SecureString $connSettings["PSpassword"] -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $un, $SecPass
write-host "Grabbed creds and recipient $addr"
#New file path to run with elevated privilages
$path = 'C:\Path\to\lockAcct.ps1'
#Start new powershell session with script and parameters
Start-Process powershell.exe -Credential $Credential -ArgumentList ("-file $path $addr")
