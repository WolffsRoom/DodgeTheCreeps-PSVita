# Launch the isolated Vita build from Windows PowerShell.
$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "tools\build.sh"
$linuxScript = (& wsl.exe -d Ubuntu -- wslpath -u $scriptPath.Replace([char]92, [char]47)).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($linuxScript)) {
    throw "Could not resolve WSL path: $scriptPath"
}
& wsl.exe -d Ubuntu -- bash $linuxScript
if ($LASTEXITCODE -ne 0) { throw "Vita VPK build failed ($LASTEXITCODE)" }
