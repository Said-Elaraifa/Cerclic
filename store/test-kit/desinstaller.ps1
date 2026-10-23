# Retire « Cerclic (test) ». À faire avant d'installer Cerclic depuis le Microsoft Store.
$ErrorActionPreference = 'Stop'
function Fin([int]$code) {
    Read-Host "`nAppuie sur Entrée pour fermer" | Out-Null
    exit $code
}
function EnAdministrateur {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $admin = (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $admin) {
        $script = $MyInvocation.PSCommandPath
        if (-not $script) { $script = $PSCommandPath }
        Start-Process -FilePath powershell.exe -Verb RunAs -ArgumentList @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$script`"")
        exit 0
    }
}

EnAdministrateur
try {
    $paquets = @(Get-AppxPackage -Name 'Cerclic.Test')
    if ($paquets.Count -eq 0) {
        Write-Host "Cerclic (test) n'est pas installé."
    } else {
        $paquets | Remove-AppxPackage
        Write-Host "Cerclic (test) est désinstallé."
    }
    Fin 0
} catch {
    Write-Host "La désinstallation a échoué :"
    Write-Host $_.Exception.Message
    Fin 1
}
