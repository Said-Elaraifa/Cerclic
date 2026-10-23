# Architecture de Cerclic

## Vue d'ensemble

```
run_cerclic.py            point d'entrée de Cerclic.exe, de Cerclic.app (et de python)
native/cerclic_open.c     CerclicOpen.exe, le petit programme du clic droit (C, 50 ko)
cerclic/
  launcher.py             instance unique, transmission des demandes (bibliothèque standard seule)
  system.py               ce qui change entre Windows et macOS (module du raccourci, mots)
  selftest.py             « Cerclic --selftest » : vérifie une application construite
  app.py                  l'instance résidente : icône, serveur de demandes, roue, éditeurs, tâches
  engine.py               lance une action, renvoie un résultat, ne lève jamais d'exception
  jobs.py                 sur un thread, ou dans un processus à part pour les PDF lourds
  journal.py              fichiers inachevés (coupure, plantage) retirés au démarrage suivant
  sysenv.py               environnement et dossier de travail des programmes lancés pour l'utilisateur
  errors.py               erreurs prévues (mot de passe, rien à faire, annulation)
  paths.py                noms de sortie réservés atomiquement, jamais d'écrasement
  settings.py  log.py     réglages JSON et journal (%APPDATA%\Cerclic, ~/Library/Application Support/Cerclic)
  actions/                traitements purs, testés partout
    images.py  pdf.py  video.py  registry.py  common.py
  win/                    Windows uniquement
    shell.py              entrée du clic droit, démarrage avec Windows, menu complet de Windows 11
    hotkey.py             raccourci clavier choisi par l'utilisateur (RegisterHotKey) et ses règles
    selection.py          fichiers sélectionnés dans la fenêtre au premier plan (Shell.Application)
    foreground.py         mise au premier plan (sur Mac : mac/foreground.py)
  mac/                    macOS uniquement (s'importe partout, ne touche macOS qu'à l'appel)
    hotkey.py             raccourci clavier (RegisterEventHotKey de Carbon) et ses règles
    selection.py          fichiers sélectionnés dans le Finder (AppleScript)
    integration.py        action rapide « Cerclic » du Finder, ouverture à la connexion
    foreground.py         passe Cerclic au premier plan (NSApplication)
  ui/                     PySide6
    radial.py             la roue (catégories, actions, « Plus », variantes, aperçu au centre)
    dismiss.py            fermeture de la roue, des bulles et des popups quand on va ailleurs
    bubble.py             saisie d'un mot de passe ou d'un texte à la place de la roue
    editor_base.py        le popup compact commun, ouvert là où était la roue
    crop_editor.py        rognage (image et PDF)
    signature.py          dessin de la signature et placement sur la page
    pages_editor.py       organisation des pages d'un PDF
    trim_editor.py        découpe d'une vidéo ou d'un son
    cards.py              progression puis résultat, en bas à droite
    settings_window.py    la fenêtre de Cerclic : raccourci (enregistreur), clic droit, signature...
    glass.py              verre givré : fond pastel, cartes, interrupteurs, barre latérale
    theme.py  logo.py  icons.py  trayicon.py
installer/cerclic.iss     installateur Inno Setup (par utilisateur, sans droits administrateur)
cerclic_mac.spec          Cerclic.app (application de la barre des menus, LSUIElement)
scripts/build_mac.sh      construit, vérifie et installe Cerclic.app sur un Mac, fait le .dmg
```

## Comment la roue s'ouvre

1. **Clic droit, « Cerclic »**. L'entrée est déclarée par utilisateur sous
   `HKCU\Software\Classes\SystemFileAssociations\<ext>\shell\Cerclic` pour
   chaque type pris en charge. L'Explorateur lance `CerclicOpen.exe "<fichier>"`,
   une fois par fichier sélectionné (`MultiSelectModel=Player`, jusqu'à 100).
   Chaque copie envoie son chemin à l'instance résidente par le canal nommé
   `\\.\pipe\Cerclic-<session>`, autorise Cerclic à passer au premier plan
   (`AllowSetForegroundWindow`) et se termine en quelques millisecondes. Les
   chemins qui arrivent dans la même seconde rejoignent la roue déjà ouverte.
   Si Cerclic ne tourne pas, une seule copie le démarre (mutex
   `Local\Cerclic.Launch`, dossier de travail : celui de Cerclic), toutes
   attendent puis transmettent ; tant que Cerclic démarre visiblement (mutex
   `Local\Cerclic.Resident`), l'attente continue jusqu'à deux minutes. S'il
   ne répond jamais, la copie qui l'a lancé le dit dans une fenêtre de message
   plutôt que de rester muette. Des chemins arrivés en retard parce que
   Cerclic était occupé rejoignent encore la roue tant qu'on n'y a pas touché.
2. **Le raccourci clavier** (Ctrl+Alt+Espace au départ, modifiable dans la
   fenêtre de Cerclic). `RegisterHotKey` : Windows ne prévient Cerclic que pour
   cette combinaison. Cerclic lit alors la sélection de la fenêtre de
   l'Explorateur au premier plan (onglets de Windows 11 compris) ou du Bureau.
   Pendant l'enregistrement d'une nouvelle combinaison, l'ancienne est libérée ;
   `hotkey.check()` refuse celles qui gêneraient la frappe (lettres seules,
   Ctrl+C/V..., AltGr+chiffres qui tapent @ # €) ou Windows (Alt+F4...).
3. **Fichiers glissés sur l'icône**, ou `Cerclic.exe --open <fichiers>` :
   même transmission, faite en Python par `launcher.py`.

Cerclic n'écoute ni la souris ni le clavier en dehors de cela. La roue se
ferme quand on clique ailleurs (perte du premier plan), sur Échap, ou si le
pointeur s'éloigne alors que Windows a refusé de la mettre au premier plan.
Les popups (rogner, signer, pages, découpe) s'ouvrent au même endroit, à la
taille de ce qu'ils montrent, et restent dans l'écran ; une fois qu'on a
travaillé dedans, un clic ailleurs ne les ferme plus (Échap ou Annuler).

Lancer Cerclic depuis son icône (Bureau, menu Démarrer) ou cliquer sur son
icône près de l'horloge ouvre sa fenêtre de réglages.

## Sur Mac

- **Application de la barre des menus** (`LSUIElement`), sans icône dans le
  Dock. Réglages dans `~/Library/Application Support/Cerclic`.
- **Clic droit** : une action rapide Automator, `~/Library/Services/
  Cerclic.workflow`, réécrite à chaque démarrage pour pointer vers l'endroit
  où se trouve Cerclic.app. Elle lance `open -a Cerclic.app <fichiers>` :
  macOS envoie les fichiers à Cerclic comme des documents à ouvrir
  (`QFileOpenEvent`, un par fichier), regroupés en une seule roue. « Ouvrir
  avec » et les fichiers glissés sur l'icône passent par le même chemin
  (`CFBundleDocumentTypes`, rang `Alternate` : jamais l'application par défaut).
- **Raccourci clavier** : `RegisterEventHotKey`, l'équivalent de
  `RegisterHotKey` ; macOS ne prévient Cerclic que pour cette combinaison, sans
  autorisation d'accessibilité. Cerclic demande ensuite au Finder sa sélection
  (AppleScript), seulement si le Finder est au premier plan ; macOS demande
  une fois l'autorisation (Automatisation).
- **Ouverture à la connexion** : `~/Library/LaunchAgents/
  com.jannahmarketing.cerclic.plist` (`open -g -a … --args --background`).
- **Construire** : sur le Mac lui-même, `scripts/build_mac.sh` (outils
  d'Apple, uv, Python 3.12, PyInstaller, signature ad hoc, vérification
  `--selftest`, image disque). Les versions de pikepdf et OpenCV s'adaptent à
  la version de macOS (`requirements-mac.txt`).

Instance unique : un mutex `Local\Cerclic.Resident` par session ; deux comptes
Windows ouverts en même temps ont chacun leur Cerclic.

## Principes

- **Rien n'écrase l'original.** Toute sortie est un nouveau fichier voisin,
  réservé atomiquement (création exclusive) : deux actions simultanées ne
  peuvent pas prendre le même nom. Si une action échoue ou est arrêtée, tout
  ce qu'elle avait réservé est supprimé.
- **Le moteur ne dépend pas de l'interface.** `actions/` et `engine.py` se
  testent sur n'importe quel système ; les éditeurs travaillent en unités de
  la source (pixels de l'image redressée, points de la page PDF visible).
- **Une action = métadonnées + fonction** (`registry.ACTIONS`) : libellé,
  description courte (affichée au centre de la roue), catégorie, ce qu'il
  faut demander (`needs`), variantes (`choices`).
- **Programmes lancés pour l'utilisateur** (Explorateur redémarré, application
  qui ouvre un résultat) : sans les variables que l'empaquetage ajoute pour
  Cerclic (plugins Qt, son dossier en tête du PATH), et Cerclic lui-même
  travaille depuis un dossier neutre (une clé USB reste éjectable).
- **PDF lourds** : PyMuPDF garde la main pendant tout un rendu. Dessiner toutes
  les pages ou recompresser les images d'un PDF moyen se fait donc dans un
  processus à part, et la roue ne montre pas l'aperçu d'une première page trop
  chargée (un plan détaillé).
- **Threads et Qt** : le ramasse-miettes cyclique de Python ne tourne que sur
  le thread de l'interface (désactivé, puis lancé régulièrement), sinon il
  pourrait détruire une fenêtre Qt depuis un thread de travail. Les
  chargements en arrière-plan rendent leur résultat par un relais qui vit
  aussi longtemps que l'application, jamais à un popup déjà fermé.
- **PDF tournés ou recadrés** : les coordonnées « vues par le lecteur » sont
  converties pour PyMuPDF ; filigrane et numéros sont posés via une page
  intermédiaire. Des tests vérifient le rendu sur des pages tournées de
  0 à 270° avec une zone de recadrage décalée.

## Tests

`pytest` : chaque action sur de vrais fichiers (EXIF, HEIC, GIF animés, PDF
protégés, vidéos aux dimensions impaires, annulation...), la roue, les
bulles, les éditeurs et le parcours complet demande, roue, action, carte,
hors écran ; le protocole de transmission ; les parties macOS (règles du
raccourci, fichiers de l'action rapide et de la connexion, fichiers envoyés
par macOS, réglages tels qu'ils s'affichent sur Mac). Le build Windows est en
plus essayé sous Wine : roue, rognage, signature, fusion, filigrane,
installation, et `--selftest`.

## Construire

Sur Windows (ou GitHub Actions) : `pip install -r requirements-dev.txt`,
compiler `native/cerclic_open.c` avec mingw-w64, copier `ffmpeg.exe` dans
`assets/ffmpeg/`, `pyinstaller cerclic.spec`, copier `CerclicOpen.exe` dans
`dist/Cerclic/`, puis `ISCC installer/cerclic.iss`. Depuis Linux :
`scripts/build_windows.sh` (Wine, mingw-w64).

Le programme de démarrage de PyInstaller (bootloader) est recompilé depuis ses
sources à chaque version de PyInstaller (mingw-w64 depuis Linux, MSVC dans le
workflow) : les antivirus connaissent celui livré tout fait, que des logiciels
malveillants utilisent aussi. Pas d'UPX, informations de version et manifeste
renseignés. Seule une signature de code supprime l'avertissement SmartScreen.

Sur Mac : `bash scripts/build_mac.sh` (voir « Sur Mac »).

Après un changement de la liste des extensions prises en charge :
`python scripts/gen_installer_registry.py` (un test le vérifie).
