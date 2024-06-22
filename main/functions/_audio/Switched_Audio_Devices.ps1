$cSharpSourceCode = @"
using System;
using System.Runtime.InteropServices;

using System.Collections.Generic;
internal enum ERole : uint
{
    eConsole         = 0,
    eMultimedia      = 1,
    eCommunications  = 2,
    ERole_enum_count = 3
}
[Guid("F8679F50-850A-41CF-9C72-430F290290C8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
internal interface IPolicyConfig
{
    [PreserveSig]
    int GetMixFormat();
    [PreserveSig]
    int GetDeviceFormat();
    [PreserveSig]
    int ResetDeviceFormat();
    [PreserveSig]
    int SetDeviceFormat();
    [PreserveSig]
    int GetProcessingPeriod();
    [PreserveSig]
    int SetProcessingPeriod();
    [PreserveSig]
    int GetShareMode();
    [PreserveSig]
    int SetShareMode();
    [PreserveSig]
    int GetPropertyValue();
    [PreserveSig]
    int SetPropertyValue();
    [PreserveSig]
    int SetDefaultEndpoint(
        [In] [MarshalAs(UnmanagedType.LPWStr)] string deviceId, 
        [In] [MarshalAs(UnmanagedType.U4)] ERole role);
    [PreserveSig]
    int SetEndpointVisibility();
}
[ComImport, Guid("870AF99C-171D-4F9E-AF0D-E63DF40C2BC9")]
internal class _CPolicyConfigClient
{
}
public class PolicyConfigClient
{
    public static int SetDefaultDevice(string deviceID)
    {
        IPolicyConfig _policyConfigClient = (new _CPolicyConfigClient() as IPolicyConfig);
        try {
            Marshal.ThrowExceptionForHR(_policyConfigClient.SetDefaultEndpoint(deviceID, ERole.eConsole));
            Marshal.ThrowExceptionForHR(_policyConfigClient.SetDefaultEndpoint(deviceID, ERole.eMultimedia));
            Marshal.ThrowExceptionForHR(_policyConfigClient.SetDefaultEndpoint(deviceID, ERole.eCommunications));
            return 0;
        } catch {
            return 1;
        }
    }
}
"@

add-type -TypeDefinition $cSharpSourceCode

function Set-DefaultAudioDevice
{
    Param
    (
        [parameter(Mandatory=$true)]
        [string[]]
        $deviceId
    )

    If ([PolicyConfigClient]::SetDefaultDevice("{0.0.0.00000000}.$deviceId") -eq 0)
    {
        Write-Host "SUCCESS: The default audio device has been set."
    }
    Else
    {
        Write-Host "ERROR: There has been a problem setting the default audio device." -ForegroundColor Red
    }
}

$id = $args[0]
Set-DefaultAudioDevice $id