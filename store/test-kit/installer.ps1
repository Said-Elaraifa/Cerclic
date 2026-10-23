# Installe « Cerclic (test) » : le paquet du Microsoft Store, non signé, pour
# l'essayer avant de le publier. Windows 11 seulement, avec les droits
# d'administrateur (Windows le demande pour un paquet non signé).
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

if ([Environment]::OSVersion.Version.Build -lt 22000) {
    Write-Host "Ce test demande Windows 11 : Windows 10 n'installe pas un paquet non signé."
    Write-Host "La version publiée sur le Microsoft Store marchera aussi sous Windows 10."
    Fin 1
}
EnAdministrateur
$ici = Split-Path -Parent $PSCommandPath
$paquet = Get-ChildItem -Path $ici -Filter 'Cerclic-*-test.msix' | Select-Object -First 1
if (-not $paquet) {
    Write-Host "Le fichier Cerclic-...-test.msix doit être dans le même dossier que ce script."
    Fin 1
}
try {
    Get-AppxPackage -Name 'Cerclic.Test' | Remove-AppxPackage
    Write-Host "Installation de $($paquet.Name) ..."
    Add-AppxPackage -Path $paquet.FullName -AllowUnsigned
    Write-Host ""
    Write-Host "Cerclic (test) est installé."
    Write-Host "Ouvre-le une fois depuis le menu Démarrer, puis fais un clic droit sur une image."
    Fin 0
} catch {
    Write-Host ""
    Write-Host "L'installation a échoué :"
    Write-Host $_.Exception.Message
    Write-Host ""
    Write-Host "Envoie ce message à Claude : il dit ce que Windows reproche au paquet."
    Fin 1
}
