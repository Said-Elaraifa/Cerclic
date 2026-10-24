"""Cerclic, English. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} file', '{n} files'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": 'Saved in “{where}”: the original folder is protected.',
    # cerclic/app.py:92
    'Téléchargements': 'Downloads',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'Windows or another app is already using it. Choose a different one in Cerclic.',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'right-click, then “Cerclic”',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": "The chosen folder can't be found: saved next to the original.",
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'Open Cerclic',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'Quit Cerclic',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'Windows or another app is already using it. Choose a different one in Cerclic; right-click “Cerclic” still works.',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'macOS or another app is already using it. Choose a different one in Cerclic.',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'right-click, Quick Actions, then “Cerclic”',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'right-click, “Show more options”, then “Cerclic”',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'Allow Cerclic to read your selection',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': 'System Settings, Privacy & Security, Automation: turn on “Finder” under Cerclic. Right-click, Quick Actions, “Cerclic” works without it.',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Click an image, PDF, video, or audio file in the Finder or on the desktop, then press {combo}.',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Click an image, PDF, video, or audio file in File Explorer or on the desktop, then press {combo}.',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'Or: right-click, Quick Actions, then “Cerclic”.',
    # cerclic/app.py:919
    'Image copiée': 'Image copied',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'Paste it anywhere with {key} + V.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'OK',
    # cerclic/app.py:1253
    'Menu complet activé': 'Full menu turned on',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'It takes effect when File Explorer restarts. Open folder windows will close.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Windows 11 menu restored',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'It takes effect when File Explorer restarts.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'Two copies of Cerclic installed',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'The version of Cerclic installed without the Microsoft Store is still here. To have only one “Cerclic” in the right-click menu and a single shortcut, remove it: “Show uninstaller”, then double-click “unins000”.',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": "The version of Cerclic installed without the Microsoft Store is still here. To have only one “Cerclic”, uninstall it in Installed apps: it's the Cerclic without “Advanced options” in its menu.",
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'macOS or another app is already using it. Choose a different one in Cerclic; right-click “Cerclic” still works.',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'Or: right-click, “Show more options”, then “Cerclic”.',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'Or: right-click, then “Cerclic”.',
    # cerclic/app.py:915
    'Copie impossible': "Couldn't copy",
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'Unlock',
    # cerclic/app.py:966
    'Continuer': 'Continue',
    # cerclic/app.py:971
    '« {name} » est protégé.': '“{name}” is protected.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'PDF password',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'Starting with Windows is blocked',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': "Your organization doesn't allow apps to start with Windows.",
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': 'Starting with Windows is turned off in Windows',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'It was turned off in Task Manager, and only Windows can turn it back on. In Settings, Apps, Startup, turn on “Cerclic”.',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'Shortcut {combo} unavailable',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Cerclic ran into a problem',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'The details are in {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': "Can't access the file",
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": "This file isn't in a regular folder (ZIP archive, phone…). Copy it to a folder, then try again.",
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': "Can't read the image.",
    # cerclic/app.py:1224
    'Réessayer': 'Try again',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': '{refused} is already used by macOS or another app. Your shortcut stays {kept}.',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': '{refused} is already used by Windows or another app. Your shortcut stays {kept}.',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'Later',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'Open settings',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'No actions for this file type',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'Cerclic works with images, PDFs, videos, and audio files.',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'Select a file first',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': 'Wrong password for “{name}”. Try again.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Cropping would keep only the first page. Use “To PDF” to keep them all, then {action} the PDF.',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['“{name}” has {n} page', '“{name}” has {n} pages'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': 'Where do you want to save the result?',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'Restart File Explorer',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'Show uninstaller',
    # cerclic/app.py:602
    'Ouvrir les applications': 'Open Installed apps',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'macOS or another app is already using it. Your shortcut stays {kept}.',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'Windows or another app is already using it. Your shortcut stays {kept}.',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'Wrong password',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'Nothing was created.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Compressing would keep only the first page. Use “To PDF” to keep them all, then {action} the PDF.',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'Only the first page would be formatted. Use “To PDF” to keep them all.',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'Open',
    # cerclic/app.py:707
    'Changer de raccourci': 'Change shortcut',
    # cerclic/app.py:1081
    'Texte du filigrane': 'Watermark text',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'It will be written diagonally across every page.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'CONFIDENTIAL',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'Password to set',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": 'It will be required to open the PDF. The original stays without a password.',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'Protect',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'Unexpected error. Try again; if it happens again, the details are in the Cerclic log (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'Access denied: the file may be open in another app, or the folder is protected.',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'Name or path too long for Windows: give the file a shorter name, or move it to a less deeply nested folder.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'File not found: it may have been moved or deleted.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'File too large for the available memory.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'The disk is full.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': "Can't read the image, or its format isn't supported.",
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF damaged or unreadable.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: needs at least {n} file.', '{action}: needs at least {n} files.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'Canceled',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '“{name}” is no longer there: it was moved, renamed, or deleted (or the USB drive was removed).',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} file is no longer there: it was moved, renamed, or deleted.', '{n} files are no longer there: they were moved, renamed, or deleted.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'This PDF is password-protected.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": 'Processing stopped abruptly: the file is probably damaged.',
    # cerclic/paths.py:235
    'compressé': 'compressed',
    # cerclic/paths.py:235
    'redimensionné': 'resized',
    # cerclic/paths.py:236
    'pivoté': 'rotated',
    # cerclic/paths.py:236
    'rogné': 'cropped',
    # cerclic/paths.py:236
    'miroir': 'mirrored',
    # cerclic/paths.py:237
    'anonymisé': 'anonymized',
    # cerclic/paths.py:237
    'assemblé': 'combined',
    # cerclic/paths.py:237
    'fusionné': 'merged',
    # cerclic/paths.py:238
    'réorganisé': 'rearranged',
    # cerclic/paths.py:238
    'extrait': 'extracted',
    # cerclic/paths.py:238
    'texte': 'text',
    # cerclic/paths.py:239
    'filigrane': 'watermarked',
    # cerclic/paths.py:239
    'numéroté': 'numbered',
    # cerclic/paths.py:239
    'signé': 'signed',
    # cerclic/paths.py:240
    'protégé': 'protected',
    # cerclic/paths.py:240
    'déverrouillé': 'unlocked',
    # cerclic/paths.py:240
    'son': 'audio',
    # cerclic/paths.py:241
    'raccourci': 'trimmed',
    # cerclic/paths.py:241
    'sans son': 'muted',
    # cerclic/paths.py:241
    'images': 'images',
    # cerclic/paths.py:242
    'pages': 'pages',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': 'same size',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'From {before} to {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} byte', '{n} bytes'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '{pct}% smaller',
    # cerclic/sizes.py:64
    '{pct} % de plus': '{pct}% larger',
    # cerclic/system.py:17
    'Cmd': 'Command',
    # cerclic/system.py:17
    'Ctrl': 'Ctrl',
    # cerclic/system.py:18
    'Suppr': 'Delete',
    # cerclic/system.py:19
    'Retour': 'Return',
    # cerclic/system.py:19
    'Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:168
    'touche Mac\x04Touche {code}': 'Key {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'Command + Space opens Spotlight.',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'Option + Command + Space opens Finder search.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'Control + Space switches the keyboard language.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'Control + Option + Space switches the keyboard language.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'Control + Command + Space opens the emoji picker.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'Command + Tab switches between apps.',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'Shift + Command + Tab switches between apps.',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'Option + Command + Esc force quits an app.',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Shift + Command + 3 takes a screenshot.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Shift + Command + 4 takes a screenshot.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Shift + Command + 5 opens the screenshot tool.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'Shift + Command + 6 takes a screenshot of the Touch Bar.',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'Control + Command + Q locks the screen.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Shift + Command + Q logs out.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'Control + Command + F enters full screen.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'Option + Command + D hides the Dock.',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": "Option + Command + C copies a file's path in the Finder.",
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'Option + Command + H hides the other apps.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'Option + Command + M minimizes all windows.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'Option + Command + W closes all windows.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'Option + Command + V moves a copied file in the Finder.',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Space',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'Return',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'Tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': 'Delete',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Échap': 'Esc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Début': 'Home',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Fin': 'End',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page préc.': 'Page Up',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page suiv.': 'Page Down',
    # contexte : touche Mac | cerclic/mac/hotkey.py:73
    'touche Mac\x04Aide': 'Help',
    # contexte : touche Mac | cerclic/mac/hotkey.py:156, cerclic/mac/hotkey.py:163
    'touche Mac\x04Pavé {key}': 'Keypad {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'Add a key after Command, Control, Option, or Shift.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} is already a macOS shortcut (System Settings, Keyboard, Keyboard Shortcuts). Choose a different one.',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'Shift + Command + {key} is already used in the Finder. Choose another letter, or Shift + Command + Space.',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": "The combination needs Command or Control: macOS doesn't accept shortcuts made only of Option or Shift.",
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Command plus a single key is already used in every app (copy, paste, save…). Add Shift, Option, or Control, for example Shift + Command + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'Control + the arrow keys switch between desktops (Mission Control).',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Control',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Shift',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Command',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'Cancel',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'Show password',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'Hide password',
    # cerclic/ui/cards.py:238
    'Fermer': 'Close',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'Desktop',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'Downloads',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'Pictures',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'Videos',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'Movies',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'Music',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'Documents',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'Stop',
    # cerclic/ui/cards.py:299
    'En cours': 'In progress',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'Stopping…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['File deleted', 'Files deleted'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": "Your original file wasn't touched.",
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} file created', '{n} files created'],
    # cerclic/ui/cards.py:366
    'Dossier': 'Folder',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'Delete',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'Deletes what Cerclic just created (your original file stays as it is)',
    # cerclic/ui/cards.py:417
    'Suppression impossible': "Couldn't delete",
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'The file is probably open in another app: close it, then try again.',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': 'In “{folder}”',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} file skipped, for example: {example}', '{n} files skipped, for example: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'Stopped: nothing was created.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '{size} in total · in “{folder}”',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · in “{folder}”',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title} failed',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'Unknown error.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'Light',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'Medium',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'Strong',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'Maximum',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}% · {n} color', '{percent}% · {n} colors'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': 'Images at 220 dpi: very sharp, even printed',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": 'Images at 150 dpi: sharp on screen and in print',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": 'Images at 110 dpi: for screens',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': 'Images at 80 dpi: smallest file, less sharp images',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": 'Up to 1080p, very good quality',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": 'Up to 1080p, good quality',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p: for a phone or a message',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p: smallest file',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbps: music, very good quality',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbps: music',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbps: voice, and music on a phone',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbps: voice',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}% · lossless',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'Loading…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': 'instead of {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'No gain',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'no gain',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'Failed',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'failed',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'calculating…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'Choose the quality · {key} to compress',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': 'Choose the strength · {key} to compress',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'Compress',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'Quality',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'Compression',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'Hover over the image: detail at 100%',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'Hover over the image: detail',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: no settings',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['Preview: {name} · total for {n} image, estimated from {sampled}', 'Preview: {name} · total for {n} images, estimated from {sampled}'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['Preview: {name} · total for {n} image', 'Preview: {name} · total for {n} images'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'Not smaller',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'Compression failed.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} skipped', '{n} skipped'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'Try a stronger compression.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'Original: {size} · lower the quality',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'Original: {size} · compress more',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'Free',
    # cerclic/ui/crop_editor.py:27
    'Original': 'Original',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'Drag the corners · {key} to crop',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'Crop',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'All pages',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'Whole image',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": 'Select the whole image again',
    # cerclic/ui/crop_editor.py:589
    '{width} × {height} cm': '{width} × {height} cm',
    # cerclic/ui/crop_editor.py:593, cerclic/ui/crop_editor.py:448, cerclic/ui/social_editor.py:43
    '{width} × {height} px': '{width} × {height} px',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:103
    'touche du Mac\x04Retour': 'Return',
    # contexte : touche | cerclic/ui/editor_base.py:103
    'touche\x04Entrée': 'Enter',
    # contexte : touche | cerclic/ui/editor_base.py:108
    'touche\x04Suppr': 'Delete',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:113
    'touche du Mac\x04Cmd': 'Command',
    # contexte : touche | cerclic/ui/editor_base.py:113
    'touche\x04Ctrl': 'Ctrl',
    # cerclic/ui/editor_base.py:205
    'Fermer (Échap)': 'Close (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'Drag to reorder · {key} to remove',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'Rotate left',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'Rotate right ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': 'Move earlier ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'Move later ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'Extract selection',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'A new PDF with only the selected pages',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'Reset',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'Save',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{n} of {count} selected', '{n} of {count} selected'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} page', '{n} pages'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'More',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ Back',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'More tools',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'General',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'Keyboard shortcut',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'Right-click',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'Created files',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'Signature',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'About',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'Version {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Select one or more files in File Explorer or on the desktop, then press {combo}.',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'Change',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'Default',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'Press your key combination…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'Checking…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'Version {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Select one or more files in the Finder or on the desktop, then press {combo}.',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'Open the wheel',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'Right-click the file, Quick Actions, then “Cerclic”. Or: Open With, then Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'Startup',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'Stops Cerclic. To start it again, open it from the Applications folder.',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'Language',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": "Automatic (the computer's language)",
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'Uninstall Cerclic',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": 'Remove Cerclic from the right-click menu and from login items, then quit it?',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'Uninstall',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'A key combination opens the wheel on the selected files.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'Open the wheel from the keyboard',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '“Cerclic” in the right-click menu of your files.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '“Cerclic” in the right-click menu',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'Your original file is never changed: each action creates a new file.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'Where to save them',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'Next to the original file',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'In the same folder, for example on the desktop if the photo is there. Recommended.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'In a folder I choose',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'All created files in one place.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'Ask me every time',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'Cerclic asks you for the folder before creating the file.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'Choose…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'Folder for created files',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'To sign your PDFs in one move. It stays on this computer.',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'Draw…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'Import a photo…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'Clear',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'The right balance between file size and sharpness.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}%',
    # cerclic/ui/settings_window.py:993
    'Voir': 'Show',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'Choose a photo of your signature',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'Shortcut unchanged.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'Examples: Shift + Command + Space, Control + Option + X. Esc to cancel.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'Examples: Ctrl + Alt + Space, Ctrl + Shift + X, Win + Shift + C. Esc to cancel.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'Smaller',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'Sharper',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'Welcome to Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'Changes take effect right away.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'Two ways to open the wheel, startup, and language.',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'Three ways to open the wheel, startup, and language.',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'With the keyboard',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Shift + right-click the file, then “Cerclic”. Without Shift, go through “Show more options”.',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'Right-click the file, then “Cerclic”.',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'With the mouse',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'Start Cerclic with your Mac',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'Start Cerclic with Windows',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'Recommended: the wheel is ready whenever you need it.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'Stops Cerclic. To start it again, open it from the Start menu.',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'Stops Cerclic. To start it again, open it from the desktop or the Start menu.',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'Stop Cerclic',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": "The wheel won't open until Cerclic is started again.",
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': "The language of Cerclic's menus, windows, and messages.",
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": 'Click “Change”, then press your key combination. If macOS or another app already uses it, Cerclic tells you and keeps the old one.',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Have a mouse with programmable buttons? Set a button to a key from F13 to F20, then choose that key here: clicking the button will open the wheel.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": 'Click “Change”, then press your key combination. If Windows or another app already uses it, Cerclic tells you and keeps the old one.',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Have a mouse with programmable buttons? Set a button to a key from F13 to F24, then choose that key here: clicking the button will open the wheel.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'Permission',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'Settings…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'Full right-click menu',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': "Not in Quick Actions? Right-click a file, Quick Actions, then Customize, and select “Cerclic”. It's also always in Open With.",
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'Image compression',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': 'Setting suggested by “Compress”, which shows the resulting size and remembers your last choice.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'JPGs made by other actions',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': "Crop, rotate, convert… At 90%, the loss isn't visible.",
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'Crop, sign, compress, convert, resize for social media… in one move, without opening another app.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'Log',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'If something goes wrong, this file helps figure out what happened.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'Licenses',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'The open-source components Cerclic uses and their licenses.',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'Uninstall…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": "No signature yet: draw it or import a photo. Otherwise, you'll be asked for it the first time you sign.",
    # cerclic/ui/settings_window.py:1130
    'Images': 'Images',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'Set up: keyboard',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'Set up: mouse',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'By dragging',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'Open Cerclic at login',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'On the files selected in the Finder or on the desktop.',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'On the files selected in File Explorer or on the desktop.',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Read the Finder selection',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': 'The first time, macOS asks whether Cerclic can control the Finder: allow it. Cerclic only reads the selected files there.',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '“Cerclic” in the Finder right-click menu',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'In the Quick Actions menu of your files, in the Finder and on the desktop.',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": 'Shows the full menu without going through “Show more options”. Cerclic will offer to restart File Explorer.',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'Tip: without changing anything, Shift + right-click on a file opens the full menu directly, with “Cerclic”.',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'No folder chosen.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": "Removes “Cerclic” from the right-click menu and from login items, then quits. You'll then just need to move Cerclic.app to the Trash.",
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'Shortcut turned off: right-click “Cerclic” is still available.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'Shortcut turned off.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic is now running in the background: its icon is in the menu bar, at the top of the screen. Choose your favorite way to open the wheel below.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic is now running in the background: its icon is near the clock (sometimes hidden under the small ^ arrow). Choose your favorite way to open the wheel below.',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": "Drag files onto Cerclic's icon (in Applications or the Dock).",
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": "Drag files onto Cerclic's icon.",
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '“Cerclic” in the right-click menu of files',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'At the top of the menu for images, PDFs, videos, and audio files, in File Explorer and on the desktop.',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'On images, PDFs, videos, and audio files, in File Explorer, on the desktop, and in Open and Save windows.',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'Their name: the original name plus what changed, for example photo (compressed).jpg next to photo.jpg. If that name is already taken, Cerclic adds a number: nothing is ever overwritten.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": "Don't like a result? “Delete” on its card removes it right away.",
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'Your folder: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'Your folder: none yet.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": 'A photo of your signature on white paper is enough: Cerclic makes the paper transparent and keeps the ink.',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': 'To sign: right-click or use the shortcut on a PDF, then “Sign”. Place the signature and press {key}.',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': 'Denied by mistake? In Automation, turn on “Finder” under Cerclic.',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ Active everywhere on your Mac.',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ Active everywhere in Windows.',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'macOS or another app already uses this combination. Choose a different one with “Change”.',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'Windows or another app already uses this combination. Choose a different one with “Change”.',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'No signature strokes found in this image.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'Your signature',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'Saved for next time',
    # cerclic/ui/signature.py:200
    'Importer…': 'Import…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'A photo of your signature on white paper',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'Drag the signature · pull a corner · {key} to sign',
    # cerclic/ui/signature.py:413
    'Changer': 'Change',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': 'Draw or import another signature',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'Sign',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'Page {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'Sign here',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': 'Choose an image of your signature',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'Images ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'Fill',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": 'The image covers the whole frame; whatever sticks out is cut.\nDrag it to choose the part to keep, scroll to zoom.',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'Blurred edges',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": 'The whole image, nothing is cut.\nAround it: the same image, blurred.',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'White edges',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": 'The whole image, nothing is cut.\nAround it: white.',
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'Black edges',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": 'The whole image, nothing is cut.\nAround it: black.',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'Previous file',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'Next file',
    # cerclic/ui/social_editor.py:448
    'Créer': 'Create',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'Drag and zoom · {key} to create',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'Nothing is cut · {key} to create',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': 'The part you keep is smaller than the format: enlarged, it will be a little less sharp.',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'The video is smaller than the format: enlarged, it will be a little less sharp.',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": 'The image is smaller than the format: enlarged, it will be a little less sharp.',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'Unknown duration',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'Drag the handles · {key} to trim',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'Trim',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'Duration {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': "Can't read the duration: damaged file?",
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'Start {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'End {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['“{name}” has {n} page: only the first would be kept. Use “{action}” to keep them all.', '“{name}” has {n} pages: only the first would be kept. Use “{action}” to keep them all.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'This file is already in {format} format.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'This image is already well compressed.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'The crop area is empty.',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": 'The frame covers the whole image: nothing to crop.',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'You need at least two images.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'Combining',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'This image contains no private information.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'Image {i} of {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'To PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": 'The image is already {size} px or smaller.',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': "Can't read the image: {name}",
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '“{name}” is password-protected.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'Wrong password.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'Conversion to Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'This file is not a PDF: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'No images.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'You need at least two PDFs to merge.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'No pages to keep.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": "No text in this PDF: it's probably a scan (an image).",
    # cerclic/actions/pdf.py:570
    'Vérification': 'Checking',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'This PDF is already well compressed.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'The frame covers the whole page: nothing to crop.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': 'The watermark text is empty.',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'No saved signature.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'The password is empty.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": 'This PDF already has a password. To set a different one, remove this one first ({more}, then {action}).',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": "This PDF isn't protected.",
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF damaged or unreadable: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'Page {i} of {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i} of {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'This PDF has only one page.',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'Page not found in this PDF.',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": "The pages haven't changed.",
    # cerclic/actions/registry.py:34
    'Image': 'Image',
    # cerclic/actions/registry.py:36
    'Vidéo': 'Video',
    # cerclic/actions/registry.py:37
    'Son': 'Audio',
    # cerclic/actions/registry.py:136
    'Droite': 'Right',
    # cerclic/actions/registry.py:137
    'Gauche': 'Left',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'Social',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'Rotate',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'Resize',
    # cerclic/actions/registry.py:213
    'Convertir': 'Convert',
    # cerclic/actions/registry.py:223
    'Copier': 'Copy',
    # cerclic/actions/registry.py:226
    'Assembler': 'Combine',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'Anonymize',
    # cerclic/actions/registry.py:256
    'Fusionner': 'Merge',
    # cerclic/actions/registry.py:260
    'Pages': 'Pages',
    # cerclic/actions/registry.py:266
    'En Word': 'To Word',
    # cerclic/actions/registry.py:270
    'En images': 'To images',
    # cerclic/actions/registry.py:276
    'Diviser': 'Split',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': 'Watermark',
    # cerclic/actions/registry.py:290
    'Numéroter': 'Number pages',
    # cerclic/actions/registry.py:295
    'En texte': 'To text',
    # cerclic/actions/registry.py:326
    'En MP4': 'To MP4',
    # cerclic/actions/registry.py:329
    'En GIF': 'To GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'Extract audio',
    # cerclic/actions/registry.py:336
    'Couper le son': 'Mute',
    # cerclic/actions/registry.py:352
    'En MP3': 'To MP3',
    # cerclic/actions/registry.py:141
    'Miroir': 'Mirror',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'Keep one part',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'Crop',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta, Story, phone, PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'Social media format',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'Rotate or flip',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'Rotation',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'Fewer pixels',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'Resize',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'Smaller, same dimensions',
    # cerclic/actions/registry.py:216
    'Changer de format': 'Change format',
    # cerclic/actions/registry.py:216
    'Conversion': 'Conversion',
    # cerclic/actions/registry.py:222
    'Une page par image': 'One page per image',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'PDF creation',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'Paste it anywhere',
    # cerclic/actions/registry.py:225
    'Copie': 'Copy',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'Several into one',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'Removes GPS, camera, date',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'Anonymization',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'Place your signature',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'Trim the margins',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'Smaller to send',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'Into one PDF',
    # cerclic/actions/registry.py:259
    'Fusion': 'Merge',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'Sort, rotate, delete',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'Page organization',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'Editable in Word',
    # cerclic/actions/registry.py:273
    'Une image par page': 'One image per page',
    # cerclic/actions/registry.py:273
    'Conversion en images': 'Conversion to images',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'One PDF per page',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'Split into pages',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'Text across the page',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'Numbers at the bottom',
    # cerclic/actions/registry.py:294
    'Numérotation': 'Page numbering',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'The text as .txt',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'Text extraction',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'With a password',
    # cerclic/actions/registry.py:304
    'Protection': 'Protection',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'Remove the password',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'Unlock',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'Keep a section',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'Trim',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels, TikTok, Shorts, PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'Smaller, as MP4',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'Plays everywhere',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'Conversion to MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': 'A silent animation',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'GIF creation',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'The soundtrack as MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': 'Audio extraction',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'The video without sound',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': 'Audio removal',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'Turn it upright',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'Conversion to MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'Smaller, as MP3',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'File {i} of {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '“{name}”: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '50%',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'Side by side',
    # cerclic/actions/registry.py:231
    'En colonne': 'In a column',
    # cerclic/actions/registry.py:232
    'En grille': 'In a grid',
    # cerclic/actions/social.py:46
    'Carré': 'Square',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Instagram, Facebook, or LinkedIn post',
    # cerclic/actions/social.py:47
    'carré': 'square',
    # cerclic/actions/social.py:48
    'Portrait': 'Portrait',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Instagram or Facebook post, the largest in the feed',
    # cerclic/actions/social.py:50
    'portrait': 'portrait',
    # cerclic/actions/social.py:51
    'Grille': 'Grid',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram, the exact shape of the profile grid',
    # cerclic/actions/social.py:52
    'grille': 'grid',
    # cerclic/actions/social.py:53
    'Story': 'Story',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'Full phone screen: Story, Reels, TikTok, YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'story',
    # cerclic/actions/social.py:56
    'Paysage': 'Landscape',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'Computer screen: YouTube, presentation, X',
    # cerclic/actions/social.py:57
    'paysage': 'landscape',
    # cerclic/actions/social.py:58
    'Bannière': 'Banner',
    # cerclic/actions/social.py:58
    '1,91:1': '1.91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Shared link or wide image on Facebook, LinkedIn, or X',
    # cerclic/actions/social.py:59
    'bannière': 'banner',
    # cerclic/actions/social.py:239
    'Format {name}': 'Format: {name}',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'This image is already {size}.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': "Can't read the video size: damaged file?",
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'This video is already {size}.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': 'Processing failed: the file may be damaged or in an unusual format.',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': "ffmpeg can't be found: reinstall Cerclic.",
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'Video damaged or format not supported.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'Access denied: the file may be open in another app.',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'Trimming',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'No video frames in this file.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'This video is already well compressed: try a stronger compression.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'Video too long for a GIF (over 2 minutes, it would be hundreds of MB). First keep a section with “{action}”.',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'Conversion to GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'This video has no sound.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'The section to keep is too short.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': 'The chosen section is the whole file.',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'No audio in this file.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'Preview unavailable.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'This audio file is already small: try a stronger compression.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'This file only contains audio, no picture: use “{action}” to make it an MP3.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'The preview takes too long to prepare.',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 closes windows.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab switches windows.',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc switches windows.',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Space opens the window menu.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc opens the Start menu.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Ctrl + Alt + Delete is reserved for Windows.',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Ctrl + Shift + Esc opens Task Manager.',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'Key {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'Space',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Tab': 'Tab',
    # contexte : touche Windows | cerclic/win/hotkey.py:40
    'touche Windows\x04Entrée': 'Enter',
    # contexte : touche Windows | cerclic/win/hotkey.py:41
    'touche Windows\x04Retour': 'Backspace',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Échap': 'Esc',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Inser': 'Insert',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Suppr': 'Delete',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Origine': 'Home',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Fin': 'End',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Page préc.': 'Page Up',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Page suiv.': 'Page Down',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Pause': 'Pause',
    # contexte : touche Windows | cerclic/win/hotkey.py:46
    'touche Windows\x04Impr. écran': 'Print Screen',
    # contexte : touche Windows | cerclic/win/hotkey.py:82, cerclic/win/hotkey.py:84
    'touche Windows\x04Pavé {key}': 'Num {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Add a key after Ctrl, Alt, Shift, or Win.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} is already used by Windows and apps (help, rename, refresh, spelling…). Add Ctrl + Alt, for example: Ctrl + Alt + {key}.',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt with the numeric keypad is used to type characters (Alt + 0201 = É). Choose a different combination.',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'The combination needs Ctrl, Alt, or Win (otherwise this key could no longer be typed).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Shift',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt plus a single key is already used in many apps (app menus). Add Shift or Ctrl, for example Alt + Shift + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'This combination is used to type characters (@, €, #, œ…) with AltGr. Choose a different one.',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl plus a single key is already used in many apps (bold, copy, paste, save…). Add Shift or Alt, for example Ctrl + Shift + {key}.',
}
