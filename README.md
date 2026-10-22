# Cerclic

Une roue d'actions rapides sur tes fichiers, sous Windows 10 et 11.

![Aperçu de la roue](docs/preview_image.png)

## Ouvrir la roue

- **Clic droit sur un fichier, puis « Cerclic »** (tout en haut du menu). La
  roue s'ouvre sous ta souris. Ça marche dans l'Explorateur, sur le Bureau et
  dans les fenêtres Ouvrir/Enregistrer de toutes les applications, avec un ou
  plusieurs fichiers (jusqu'à 100 d'un coup).
- **Ctrl+Alt+Espace** sur les fichiers sélectionnés dans l'Explorateur ou sur
  le Bureau.
- **Glisse des fichiers sur l'icône Cerclic** du Bureau.

Sous Windows 11, l'entrée se trouve dans « Afficher d'autres options » (ou
Maj + clic droit). Pour l'avoir en un clic : Paramètres de Cerclic, « Menu clic
droit complet ».

Dans la roue : clic sur une action, clic au centre pour revenir, Échap pour
fermer. Les touches 1 à 9 et les flèches marchent aussi.

## Ce que Cerclic sait faire

Tout se passe dans Cerclic, sans ouvrir d'autre application. Ton fichier
d'origine n'est jamais modifié : chaque résultat est un nouveau fichier à côté,
par exemple `photo (compressed).jpg`, et « Annuler » le supprime.

**Images** (JPG, PNG, WEBP, HEIC d'iPhone, AVIF, GIF, BMP, TIFF) : rogner dans
un éditeur plein écran (formats 1:1, 4:5, 16:9...), convertir en JPG, PNG ou
WEBP, compresser, redimensionner (50 %, 1920, 1280 ou 800 px), pivoter, réunir
en un PDF. Les GIF animés gardent leur animation, les couleurs et les infos
EXIF sont conservées.

**PDF** : signer (tu dessines ta signature une fois, puis tu la poses à la
souris sur la page), rogner, compresser, fusionner, convertir en images ou en
Word, diviser, pivoter, filigrane, numéros de page, protéger par mot de passe,
déverrouiller. Un PDF protégé demande son mot de passe dans une petite bulle.

**Vidéo** : compresser, convertir en MP4 lisible partout, en GIF, extraire le
son en MP3. Une barre montre l'avancement, « Arrêter » interrompt proprement.

## Installer

Télécharge `CerclicSetup-x.y.z.exe` et lance-le : pas de droits
administrateur, pas de Python à installer, rien à configurer. Cerclic démarre
avec Windows et se range près de l'horloge.

Windows peut afficher « Windows a protégé votre ordinateur » car l'application
n'est pas encore signée numériquement : clique sur « Informations
complémentaires », puis « Exécuter quand même ».

Une version portable (`Cerclic-x.y.z-portable.zip`) est aussi fournie :
décompresse-la où tu veux et double-clique sur `Cerclic.exe`.

## Réglages

Clic droit sur l'icône près de l'horloge, puis « Paramètres » : entrée du clic
droit, menu complet de Windows 11, raccourci clavier, signature (dessiner,
importer une photo de ta signature), qualité de compression, démarrage avec
Windows.

En cas de souci, le journal `cerclic.log` se trouve dans
`%APPDATA%\Cerclic`.

## Désinstaller

Paramètres Windows, Applications, Cerclic, Désinstaller. Tout ce que Cerclic a
ajouté (entrée du clic droit, démarrage automatique) est retiré.

## Pour les développeurs

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest                      # 70+ tests : actions, interface, communication
pythonw run_cerclic.py      # lancer depuis le code
```

Construire l'application : le workflow GitHub (`.github/workflows/build.yml`)
fabrique l'exécutable, l'installateur et la version portable sur Windows ;
`scripts/build_windows.sh` fait la même chose depuis Linux avec Wine. Détails
dans `docs/ARCHITECTURE.md`.
