# Cerclic

Une roue d'actions rapides sur tes fichiers, sous Windows 10 et 11 et sur Mac
(macOS 12 ou plus récent) : rogner, signer, compresser, convertir, raccourcir
une vidéo… en un geste, sans ouvrir d'autre application.

![Aperçu de la roue](docs/preview_image.png)

## Ouvrir la roue

- **Ton raccourci clavier** sur les fichiers sélectionnés dans l'Explorateur,
  le Finder ou sur le Bureau : Ctrl + Alt + Espace sur Windows, Maj + Cmd +
  Espace sur Mac au départ. Tu choisis la combinaison que tu veux dans Cerclic.
- **Clic droit sur un fichier, puis « Cerclic »**.
  - Windows : tout en haut du menu, dans l'Explorateur, sur le Bureau et dans
    les fenêtres Ouvrir/Enregistrer, avec un ou plusieurs fichiers (jusqu'à
    100 d'un coup). Sous Windows 11, l'entrée est dans « Afficher d'autres
    options » (ou Maj + clic droit) ; Cerclic peut remettre le menu complet.
  - Mac : dans Actions rapides, et dans Ouvrir avec.
- **Glisse des fichiers sur l'icône de Cerclic.**

La roue s'ouvre sous ta souris, avec un aperçu du fichier au centre. Passe sur
une action pour voir ce qu'elle fait, clique pour la lancer, clique au centre
pour revenir, Échap pour fermer. Au clavier : les touches 1 à 8 (depuis le
haut, dans le sens des aiguilles d'une montre), ou les flèches puis Entrée.

## Ce que Cerclic sait faire

Tout se passe dans de petites fenêtres qui s'ouvrent là où était la roue. Ton
fichier d'origine n'est jamais modifié : chaque résultat est un nouveau
fichier, par exemple `photo (compressé).jpg`, à côté de l'original ou dans le
dossier de ton choix. « Supprimer » sur la carte de résultat l'efface si tu
n'en veux pas.

**Images** (JPG, PNG, WEBP, HEIC d'iPhone, AVIF, GIF, BMP, TIFF) : rogner
(formats 1:1, 4:5, 16:9…), pivoter ou retourner en miroir, redimensionner,
compresser, convertir en JPG, PNG ou WEBP, copier pour coller où tu veux,
réunir en un PDF, assembler plusieurs images en une, anonymiser (retirer la
position GPS, le modèle du téléphone, la date… sans perte de qualité).

**PDF** : signer (tu dessines ta signature une fois, puis tu la poses à la
souris), rogner, compresser, fusionner, organiser les pages (trier, tourner,
supprimer, extraire), convertir en Word, en images ou en texte, diviser,
pivoter, filigrane, numéros de page, protéger par mot de passe, déverrouiller.

**Vidéo** : raccourcir, compresser, convertir en MP4 ou en GIF, extraire le
son, couper le son, pivoter.

**Son** (MP3, M4A, WAV, notes vocales OPUS/OGG, FLAC…) : raccourcir,
convertir en MP3, compresser.

## Installer

**Windows.** Lance `CerclicSetup-x.y.z.exe` : pas de droits administrateur,
rien à configurer. Cerclic démarre avec Windows et se range près de l'horloge.
Une mise à jour s'installe par-dessus et garde tes réglages. Tant que Cerclic
n'est pas signé numériquement, Windows peut afficher « Windows a protégé votre
ordinateur » : « Informations complémentaires », puis « Exécuter quand même ».

Version portable (`Cerclic-x.y.z-portable.zip`) : décompresse-la où tu veux et
double-clique sur `Cerclic.exe`. Elle n'ajoute rien à Windows tant que tu ne
l'actives pas dans ses réglages ; ses données restent dans « Données Cerclic »,
à côté.

**Mac.** Cerclic se construit sur le Mac lui-même, en une commande (voir
`LISEZ-MOI-MAC.txt`) : `bash scripts/build_mac.sh`. Le script installe ce
qu'il faut, construit `Cerclic.app`, le vérifie, le copie dans Applications et
l'ouvre ; il produit aussi `dist/Cerclic-x.y.z-mac-<puce>.dmg` à partager.
Cerclic vit dans la barre des menus. La première fois que tu utilises le
raccourci, macOS demande si Cerclic peut contrôler le Finder : accepte, Cerclic
y lit seulement les fichiers sélectionnés.

## Réglages

Ouvre Cerclic depuis son icône (menu Démarrer, Bureau, Applications) ou depuis
son icône près de l'horloge ou dans la barre des menus. Sept sections : Général,
Raccourci clavier, Clic droit, Fichiers créés (à côté de l'original ou dans un
dossier de ton choix), Signature, Qualité, À propos. Tout s'applique aussitôt.

En cas de souci, le journal `cerclic.log` se trouve dans `%APPDATA%\Cerclic`
(Windows) ou `~/Library/Application Support/Cerclic` (Mac) ; « À propos »,
« Journal », l'ouvre.

## Désinstaller

Windows : Paramètres, Applications, Cerclic, Désinstaller. Tout ce que Cerclic
a ajouté est retiré (clic droit, démarrage, menu complet, réglages).

Mac : Cerclic, À propos, « Désinstaller… » (retire l'action rapide et
l'ouverture de session), puis mets Cerclic.app à la corbeille.

## Pour les développeurs

```
python -m venv .venv
.venv\Scripts\activate          (Mac : source .venv/bin/activate)
pip install -r requirements-dev.txt
pytest                          # 240+ tests : actions, interface, Windows, Mac
python run_cerclic.py           # lancer depuis le code
```

`Cerclic --selftest` vérifie une application construite (bibliothèques,
ffmpeg, vraies actions) et écrit `selftest.txt` à côté du journal.

Construire : `scripts/build_windows.sh` (depuis Linux, avec Wine) ou le
workflow GitHub pour Windows ; `scripts/build_mac.sh` sur un Mac (ou le job
macOS du workflow). Licences des composants : `assets/LICENCES.txt`. Détails
dans `docs/ARCHITECTURE.md`.
