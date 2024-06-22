$regRoot = "HKLM:\Software\Microsoft\"

function Get-Devices
{
    $regKey = $regRoot + "\Windows\CurrentVersion\MMDevices\Audio\Render\"
    Write-Output "Active Sound devices:"
    Get-ChildItem $regKey | Where-Object { $_.GetValue("DeviceState") -eq 1} |
        Foreach-Object {
            $subKey = $_.OpenSubKey("Properties")
            Write-Output ("  " + $subKey.GetValue("{a45c254e-df1c-4efd-8020-67d146a850e0},2"))
            Write-Output ("    " + $_.Name.Substring($_.Name.LastIndexOf("\")))
        }
}

Get-Devices