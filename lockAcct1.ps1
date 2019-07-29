param ([string]$addr)
Import-Module ActiveDirectory
write-host "made it to lock acct"
#Disable account until further notice
Get-ADuser -filter {emailaddress -eq $addr} | disable-adaccount
write-host "locked out $addr"
