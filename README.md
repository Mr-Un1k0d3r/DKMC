# Don't Kill My Cat (DKMC)
Tool that generate obfuscated shellcode that is stored inside of polyglot images. The image is 100% valid and also 100% valid shellcode. The idea is too avoid sandbox analysis since it's a simple "legit" image. For now the tool rely on PowerShell the execute the final shellcode payload.

# Basic Flow
* Generate shellcode (meterpreter / Beacon)
* Embed the obfuscated shellcode inside the image
* PowerShell download the image and execute the image as shellcode
* Get your shell

# Usage
Launching DKMC
```
python dkmc.py
```

Generate shellcode from a raw file
```
>>> sc
(shellcode)>>> set source shellcode.txt
        [+] source value is set.

(shellcode)>>> run
        [+] Shellcode:
\x41\x41\x41\x41
```

Generate the obfuscated shellcode embedded inside of an image.
```

```

Generate PowerShell payload to execute on the victim system.
```

```

Built-in Web Server to deliver the image
```

```
