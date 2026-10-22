@echo off
rem Lance Cerclic depuis ce dossier. Au premier lancement, installe les dependances.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Premier lancement : installation des dependances, une a deux minutes...
  python -m venv .venv || goto :nopython
  ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements.txt || goto :fail
)
echo Cerclic demarre. Laisse cette fenetre ouverte pendant le test.
".venv\Scripts\python.exe" -m cerclic
if errorlevel 1 goto :fail
goto :eof

:nopython
echo Python est introuvable. Installe-le depuis python.org en cochant "Add python.exe to PATH".
pause
goto :eof

:fail
echo Une erreur s'est produite. Copie le texte ci-dessus et envoie-le a Claude.
pause
