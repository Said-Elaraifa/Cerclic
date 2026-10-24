"""Cerclic, Deutsch. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} Datei', '{n} Dateien'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": 'In „{where}“ gespeichert: Der Originalordner ist geschützt.',
    # cerclic/app.py:92
    'Téléchargements': 'Downloads',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'Windows oder eine andere App verwendet es bereits. Wähle in Cerclic ein anderes.',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'Rechtsklick, dann „Cerclic“',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": 'Der gewählte Ordner wurde nicht gefunden: neben dem Original gespeichert.',
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'Cerclic öffnen',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'Cerclic beenden',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'Windows oder eine andere App verwendet es bereits. Wähle in Cerclic ein anderes; „Cerclic“ im Rechtsklickmenü funktioniert weiterhin.',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'macOS oder eine andere App verwendet es bereits. Wähle in Cerclic ein anderes.',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'Rechtsklick, Schnellaktionen, dann „Cerclic“',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'Rechtsklick, „Weitere Optionen anzeigen“, dann „Cerclic“',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'Erlaube Cerclic, deine Auswahl zu lesen',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': 'Systemeinstellungen, Datenschutz & Sicherheit, Automation: Aktiviere „Finder“ unter Cerclic. Rechtsklick, Schnellaktionen, „Cerclic“ funktioniert auch ohne das.',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Klicke im Finder oder auf dem Schreibtisch auf ein Bild, ein PDF, ein Video oder eine Audiodatei und drücke dann {combo}.',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Klicke im Datei-Explorer oder auf dem Desktop auf ein Bild, ein PDF, ein Video oder eine Audiodatei und drücke dann {combo}.',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'Oder: Rechtsklick, Schnellaktionen, dann „Cerclic“.',
    # cerclic/app.py:919
    'Image copiée': 'Bild kopiert',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'Füge es mit {key} + V ein, wo du willst.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'OK',
    # cerclic/app.py:1253
    'Menu complet activé': 'Vollständiges Menü aktiviert',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'Es wird nach einem Neustart des Datei-Explorers wirksam. Geöffnete Ordnerfenster werden dabei geschlossen.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Windows-11-Menü wiederhergestellt',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'Es wird nach einem Neustart des Datei-Explorers wirksam.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'Cerclic ist doppelt installiert',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'Die ohne Microsoft Store installierte Version von Cerclic ist noch vorhanden. Damit es nur ein „Cerclic“ im Rechtsklickmenü und nur ein Tastenkürzel gibt, entferne sie: „Deinstallationsprogramm zeigen“, dann Doppelklick auf „unins000“.',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": 'Die ohne Microsoft Store installierte Version von Cerclic ist noch vorhanden. Damit es nur ein „Cerclic“ gibt, deinstalliere sie unter „Installierte Apps“: Es ist das Cerclic ohne „Erweiterte Optionen“ in seinem Menü.',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'macOS oder eine andere App verwendet es bereits. Wähle in Cerclic ein anderes; „Cerclic“ im Rechtsklickmenü funktioniert weiterhin.',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'Oder: Rechtsklick, „Weitere Optionen anzeigen“, dann „Cerclic“.',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'Oder: Rechtsklick, dann „Cerclic“.',
    # cerclic/app.py:915
    'Copie impossible': 'Kopieren nicht möglich',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'Entsperren',
    # cerclic/app.py:966
    'Continuer': 'Weiter',
    # cerclic/app.py:971
    '« {name} » est protégé.': '„{name}“ ist geschützt.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'PDF-Passwort',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'Start mit Windows blockiert',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': 'Deine Organisation erlaubt Apps nicht, mit Windows zu starten.',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': 'Start mit Windows in Windows deaktiviert',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'Er wurde im Task-Manager deaktiviert: Nur Windows kann ihn wieder aktivieren. Aktiviere „Cerclic“ unter Einstellungen, Apps, Autostart.',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'Tastenkürzel {combo} nicht verfügbar',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Bei Cerclic ist ein Problem aufgetreten',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'Details findest du in {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': 'Kein Zugriff auf die Datei',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'Diese Datei liegt nicht in einem normalen Ordner (ZIP-Archiv, Smartphone usw.). Kopiere sie in einen Ordner und versuche es dann erneut.',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': 'Bild nicht lesbar.',
    # cerclic/app.py:1224
    'Réessayer': 'Erneut versuchen',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': '{refused} wird bereits von macOS oder einer anderen App verwendet. Dein Tastenkürzel bleibt {kept}.',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': '{refused} wird bereits von Windows oder einer anderen App verwendet. Dein Tastenkürzel bleibt {kept}.',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'Später',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'Einstellungen öffnen',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'Keine Aktion für diesen Dateityp',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'Cerclic arbeitet mit Bildern, PDFs, Videos und Audiodateien.',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'Wähle zuerst eine Datei aus',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': 'Falsches Passwort für „{name}“. Versuche es erneut.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Beim Zuschneiden bliebe nur die erste Seite erhalten. Nutze „Als PDF“, um alle zu behalten, und dann „{action}“ für das PDF.',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['„{name}“ hat {n} Seite', '„{name}“ hat {n} Seiten'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': 'Wo soll das Ergebnis gespeichert werden?',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'Datei-Explorer neu starten',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'Deinstallationsprogramm zeigen',
    # cerclic/app.py:602
    'Ouvrir les applications': 'Installierte Apps öffnen',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'macOS oder eine andere App verwendet es bereits. Dein Tastenkürzel bleibt {kept}.',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'Windows oder eine andere App verwendet es bereits. Dein Tastenkürzel bleibt {kept}.',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'Falsches Passwort',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'Es wurde nichts erstellt.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Beim Komprimieren bliebe nur die erste Seite erhalten. Nutze „Als PDF“, um alle zu behalten, und dann „{action}“ für das PDF.',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'Nur die erste Seite würde ins Format gebracht. Nutze „Als PDF“, um alle zu behalten.',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'Öffnen',
    # cerclic/app.py:707
    'Changer de raccourci': 'Tastenkürzel ändern',
    # cerclic/app.py:1081
    'Texte du filigrane': 'Text des Wasserzeichens',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'Er wird diagonal auf jede Seite geschrieben.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'VERTRAULICH',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'Neues Passwort',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": 'Es wird zum Öffnen des PDFs abgefragt. Das Original bleibt ohne Passwort.',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'Schützen',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'Unerwarteter Fehler. Versuche es erneut; falls es wieder passiert, stehen die Details im Protokoll von Cerclic (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'Zugriff verweigert: Die Datei ist vielleicht in einer anderen App geöffnet oder der Ordner ist geschützt.',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'Name oder Pfad ist zu lang für Windows: Gib der Datei einen kürzeren Namen oder verschiebe sie in einen weniger tief verschachtelten Ordner.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'Datei nicht gefunden: Sie wurde vielleicht verschoben oder gelöscht.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'Die Datei ist zu groß für den verfügbaren Speicher.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'Der Datenträger ist voll.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': 'Bild nicht lesbar oder Format nicht unterstützt.',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF beschädigt oder nicht lesbar.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: Mindestens {n} Datei erforderlich.', '{action}: Mindestens {n} Dateien erforderlich.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'Abgebrochen',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '„{name}“ ist nicht mehr da: Die Datei wurde verschoben, umbenannt oder gelöscht (oder der USB-Stick entfernt).',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} Datei ist nicht mehr da: Sie wurde verschoben, umbenannt oder gelöscht.', '{n} Dateien sind nicht mehr da: Sie wurden verschoben, umbenannt oder gelöscht.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'Dieses PDF ist passwortgeschützt.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": 'Die Verarbeitung wurde abrupt beendet: Die Datei ist wahrscheinlich beschädigt.',
    # cerclic/paths.py:235
    'compressé': 'komprimiert',
    # cerclic/paths.py:235
    'redimensionné': 'verkleinert',
    # cerclic/paths.py:236
    'pivoté': 'gedreht',
    # cerclic/paths.py:236
    'rogné': 'zugeschnitten',
    # cerclic/paths.py:236
    'miroir': 'gespiegelt',
    # cerclic/paths.py:237
    'anonymisé': 'anonymisiert',
    # cerclic/paths.py:237
    'assemblé': 'kombiniert',
    # cerclic/paths.py:237
    'fusionné': 'zusammengefügt',
    # cerclic/paths.py:238
    'réorganisé': 'neu geordnet',
    # cerclic/paths.py:238
    'extrait': 'extrahiert',
    # cerclic/paths.py:238
    'texte': 'Text',
    # cerclic/paths.py:239
    'filigrane': 'Wasserzeichen',
    # cerclic/paths.py:239
    'numéroté': 'nummeriert',
    # cerclic/paths.py:239
    'signé': 'signiert',
    # cerclic/paths.py:240
    'protégé': 'geschützt',
    # cerclic/paths.py:240
    'déverrouillé': 'entsperrt',
    # cerclic/paths.py:240
    'son': 'Ton',
    # cerclic/paths.py:241
    'raccourci': 'gekürzt',
    # cerclic/paths.py:241
    'sans son': 'ohne Ton',
    # cerclic/paths.py:241
    'images': 'Bilder',
    # cerclic/paths.py:242
    'pages': 'Seiten',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': 'gleiche Größe',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'Von {before} auf {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} Byte', '{n} Byte'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '{pct}\xa0% kleiner',
    # cerclic/sizes.py:64
    '{pct} % de plus': '{pct}\xa0% größer',
    # cerclic/system.py:17
    'Cmd': 'Befehl',
    # cerclic/system.py:17
    'Ctrl': 'Strg',
    # cerclic/system.py:18
    'Suppr': 'Entf',
    # cerclic/system.py:19
    'Retour': 'Zeilenschalter',
    # cerclic/system.py:19
    'Entrée': 'Eingabe',
    # contexte : touche Mac | cerclic/mac/hotkey.py:168
    'touche Mac\x04Touche {code}': 'Taste {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'Befehl + Leertaste öffnet Spotlight.',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'option + Befehl + Leertaste öffnet die Finder-Suche.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'control + Leertaste wechselt die Tastatursprache.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'control + option + Leertaste wechselt die Tastatursprache.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'control + Befehl + Leertaste öffnet die Emojis.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'Befehl + Tab wechselt zwischen Apps.',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'Umschalt + Befehl + Tab wechselt zwischen Apps.',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'option + Befehl + Esc erzwingt das Beenden einer App.',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Umschalt + Befehl + 3 erstellt ein Bildschirmfoto.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Umschalt + Befehl + 4 erstellt ein Bildschirmfoto.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Umschalt + Befehl + 5 öffnet die App „Bildschirmfoto“.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'Umschalt + Befehl + 6 erstellt ein Bildschirmfoto der Touch Bar.',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'control + Befehl + Q sperrt den Bildschirm.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Umschalt + Befehl + Q meldet dich ab.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'control + Befehl + F wechselt in den Vollbildmodus.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'option + Befehl + D blendet das Dock aus.',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'option + Befehl + C kopiert im Finder den Pfad einer Datei.',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'option + Befehl + H blendet die anderen Apps aus.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'option + Befehl + M minimiert alle Fenster.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'option + Befehl + W schließt alle Fenster.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'option + Befehl + V bewegt im Finder eine kopierte Datei.',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Leertaste',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'Zeilenschalter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'Tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': 'Entf',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Échap': 'Esc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Début': 'Pos1',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Fin': 'Ende',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page préc.': 'Bild auf',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page suiv.': 'Bild ab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:73
    'touche Mac\x04Aide': 'Hilfe',
    # contexte : touche Mac | cerclic/mac/hotkey.py:156, cerclic/mac/hotkey.py:163
    'touche Mac\x04Pavé {key}': 'Num {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'Füge nach Befehl, control, option oder Umschalt eine Taste hinzu.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} ist bereits ein Tastaturkurzbefehl von macOS (Systemeinstellungen, Tastatur, Tastaturkurzbefehle). Wähle einen anderen.',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'Umschalt + Befehl + {key} wird bereits im Finder verwendet. Wähle einen anderen Buchstaben oder Umschalt + Befehl + Leertaste.',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": 'Die Kombination braucht Befehl oder control: macOS lehnt Tastenkürzel nur aus option oder Umschalt ab.',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Befehl + eine einzelne Taste wird bereits in allen Apps verwendet (Kopieren, Einsetzen, Sichern …). Füge Umschalt, option oder control hinzu, zum Beispiel Umschalt + Befehl + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'control + Pfeiltasten wechseln zwischen Schreibtischen (Mission Control).',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'control',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Umschalt',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Befehl',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'Abbrechen',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'Passwort anzeigen',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'Passwort ausblenden',
    # cerclic/ui/cards.py:238
    'Fermer': 'Schließen',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'Desktop',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'Downloads',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'Bilder',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'Videos',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'Filme',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'Musik',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'Dokumente',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'Stoppen',
    # cerclic/ui/cards.py:299
    'En cours': 'Läuft',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'Wird gestoppt…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['Datei gelöscht', 'Dateien gelöscht'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": 'Deine Originaldatei ist unverändert.',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} Datei erstellt', '{n} Dateien erstellt'],
    # cerclic/ui/cards.py:366
    'Dossier': 'Ordner',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'Löschen',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'Löscht, was Cerclic gerade erstellt hat (deine Originaldatei bleibt unverändert)',
    # cerclic/ui/cards.py:417
    'Suppression impossible': 'Löschen nicht möglich',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'Die Datei ist wahrscheinlich in einer anderen App geöffnet: Schließe diese App und versuche es dann erneut.',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}\xa0%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': 'In\xa0„{folder}“',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} Datei übersprungen, zum Beispiel: {example}', '{n} Dateien übersprungen, zum Beispiel: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'Gestoppt: Es wurde nichts erstellt.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '{size} insgesamt · in\xa0„{folder}“',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · in\xa0„{folder}“',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title} nicht möglich',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'Unbekannter Fehler.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'Leicht',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'Mittel',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'Stark',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'Maximal',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}\xa0% · {n} Farbe', '{percent}\xa0% · {n} Farben'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': 'Bilder mit 220 dpi: sehr scharf, auch gedruckt',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": 'Bilder mit 150 dpi: scharf auf dem Bildschirm und im Druck',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": 'Bilder mit 110 dpi: für den Bildschirm',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': 'Bilder mit 80 dpi: am kleinsten, Bilder weniger scharf',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": 'Bis 1080p, sehr gute Qualität',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": 'Bis 1080p, gute Qualität',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p: für ein Smartphone oder eine Nachricht',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p: am kleinsten',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbit/s: Musik, sehr gute Qualität',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbit/s: Musik',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbit/s: Sprache, und Musik auf dem Smartphone',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbit/s: Sprache',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}\xa0% · verlustfrei',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'Wird geladen…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': 'statt {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'Keine Ersparnis',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'keine Ersparnis',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'Nicht möglich',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'nicht möglich',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'wird berechnet…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'Wähle die Qualität · {key} zum Komprimieren',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': 'Wähle die Stärke · {key} zum Komprimieren',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'Komprimieren',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'Qualität',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'Komprimierung',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'Fahre mit der Maus über das Bild: Details bei 100\xa0%',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'Fahre mit der Maus über das Bild: Details',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: ohne Einstellung',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['Vorschau: {name} · gesamt für {n} Bild, geschätzt anhand von {sampled}', 'Vorschau: {name} · gesamt für {n} Bilder, geschätzt anhand von {sampled}'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['Vorschau: {name} · gesamt für {n} Bild', 'Vorschau: {name} · gesamt für {n} Bilder'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'Nicht kleiner',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'Komprimieren nicht möglich.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} übersprungen', '{n} übersprungen'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'Versuche eine stärkere Komprimierung.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'Original: {size} · senke die Qualität',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'Original: {size} · komprimiere stärker',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'Frei',
    # cerclic/ui/crop_editor.py:27
    'Original': 'Original',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'Ziehe die Ecken · {key} zum Zuschneiden',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'Zuschneiden',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'Alle Seiten',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'Ganzes Bild',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": 'Auf das ganze Bild zurücksetzen',
    # cerclic/ui/crop_editor.py:589
    '{width} × {height} cm': '{width} × {height} cm',
    # cerclic/ui/crop_editor.py:593, cerclic/ui/crop_editor.py:448, cerclic/ui/social_editor.py:43
    '{width} × {height} px': '{width} × {height} px',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:103
    'touche du Mac\x04Retour': 'Zeilenschalter',
    # contexte : touche | cerclic/ui/editor_base.py:103
    'touche\x04Entrée': 'Eingabe',
    # contexte : touche | cerclic/ui/editor_base.py:108
    'touche\x04Suppr': 'Entf',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:113
    'touche du Mac\x04Cmd': 'Befehl',
    # contexte : touche | cerclic/ui/editor_base.py:113
    'touche\x04Ctrl': 'Strg',
    # cerclic/ui/editor_base.py:205
    'Fermer (Échap)': 'Schließen (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'Ziehe zum Sortieren · {key} zum Entfernen',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'Nach links drehen',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'Nach rechts drehen ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': 'Nach vorne ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'Nach hinten ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'Auswahl extrahieren',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'Ein neues PDF nur mit den ausgewählten Seiten',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'Zurücksetzen',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'Speichern',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{n} von {count} ausgewählt', '{n} von {count} ausgewählt'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} Seite', '{n} Seiten'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'Mehr',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ Zurück',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'Weitere Werkzeuge',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'Allgemein',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'Tastenkürzel',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'Rechtsklick',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'Erstellte Dateien',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'Unterschrift',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'Info',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'Version {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Wähle eine oder mehrere Dateien im Datei-Explorer oder auf dem Desktop aus und drücke dann {combo}.',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'Ändern',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'Standard',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'Drücke deine Tastenkombination…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'Wird geprüft…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'Version {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Wähle eine oder mehrere Dateien im Finder oder auf dem Schreibtisch aus und drücke dann {combo}.',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'Rad öffnen',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'Rechtsklick auf die Datei, Schnellaktionen, dann „Cerclic“. Oder: Öffnen mit, dann Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'Start',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'Beendet Cerclic. Zum erneuten Starten öffne es aus dem Ordner „Programme“.',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'Sprache',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": 'Automatisch (Sprache des Computers)',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'Cerclic deinstallieren',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": 'Cerclic aus dem Rechtsklickmenü und den Anmeldeobjekten entfernen und dann beenden?',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'Deinstallieren',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'Eine Tastenkombination öffnet das Rad für die ausgewählten Dateien.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'Rad per Tastatur öffnen',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '„Cerclic“ im Rechtsklickmenü deiner Dateien.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '„Cerclic“ im Rechtsklickmenü',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'Deine Originaldatei wird nie verändert: Jede Aktion erstellt eine neue Datei.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'Speicherort',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'Neben der Originaldatei',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'Im selben Ordner, zum Beispiel auf dem Desktop, wenn das Foto dort liegt. Empfohlen.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'In einem Ordner meiner Wahl',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'Alle erstellten Dateien am selben Ort.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'Jedes Mal fragen',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'Cerclic fragt dich vor dem Erstellen der Datei nach dem Ordner.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'Auswählen…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'Ordner für erstellte Dateien',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'Um deine PDFs mit einem Klick zu signieren. Sie bleibt auf diesem Computer.',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'Zeichnen…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'Foto importieren…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'Löschen',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'Der goldene Mittelweg zwischen Dateigröße und Schärfe.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}\xa0%',
    # cerclic/ui/settings_window.py:993
    'Voir': 'Anzeigen',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'Foto deiner Unterschrift auswählen',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'Tastenkürzel unverändert.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'Beispiele: Umschalt + Befehl + Leertaste, control + option + X. Esc zum Abbrechen.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'Beispiele: Strg + Alt + Leertaste, Strg + Umschalt + X, Win + Umschalt + C. Esc zum Abbrechen.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'Kleiner',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'Schärfer',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'Willkommen bei Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'Änderungen werden sofort übernommen.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'Zwei Wege, das Rad zu öffnen, Start und Sprache.',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'Drei Wege, das Rad zu öffnen, Start und Sprache.',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'Per Tastatur',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Umschalt + Rechtsklick auf die Datei, dann „Cerclic“. Ohne Umschalt über „Weitere Optionen anzeigen“.',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'Rechtsklick auf die Datei, dann „Cerclic“.',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'Per Maus',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'Cerclic mit dem Mac starten',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'Cerclic mit Windows starten',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'Empfohlen: Das Rad ist sofort bereit, wenn du es brauchst.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'Beendet Cerclic. Zum erneuten Starten öffne es über das Startmenü.',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'Beendet Cerclic. Zum erneuten Starten öffne es über den Desktop oder das Startmenü.',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'Cerclic stoppen',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": 'Das Rad öffnet sich bis zum nächsten Start nicht mehr.',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'Die Sprache der Menüs, Fenster und Meldungen von Cerclic.',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": '„Ändern“, dann drücke deine Tastenkombination. Wenn macOS oder eine andere App sie schon verwendet, sagt Cerclic dir das und behält die alte.',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Eine Maus mit programmierbaren Tasten? Lege eine Maustaste auf eine der Tasten F13 bis F20 und wähle diese dann hier: Ein Klick auf die Maustaste öffnet das Rad.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": '„Ändern“, dann drücke deine Tastenkombination. Wenn Windows oder eine andere App sie schon verwendet, sagt Cerclic dir das und behält die alte.',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Eine Maus mit programmierbaren Tasten? Lege eine Maustaste auf eine der Tasten F13 bis F24 und wähle diese dann hier: Ein Klick auf die Maustaste öffnet das Rad.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'Berechtigung',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'Einstellungen…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'Vollständiges Rechtsklickmenü',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': 'Nicht in den Schnellaktionen? Rechtsklick auf eine Datei, Schnellaktionen, dann Anpassen, und aktiviere „Cerclic“. Es ist auch immer unter „Öffnen mit“ zu finden.',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'Bildkomprimierung',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': 'Voreinstellung für „Komprimieren“, das die erzielte Größe zeigt und sich deine letzte Wahl merkt.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'Von anderen Aktionen erstellte JPGs',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': 'Zuschneiden, Drehen, Konvertieren und mehr. Bei 90\xa0% ist kein Verlust sichtbar.',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'Zuschneiden, Signieren, Komprimieren, Konvertieren, für Social Media formatieren und mehr: mit einem Klick, ohne eine andere App zu öffnen.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'Protokoll',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'Bei Problemen hilft diese Datei zu verstehen, was passiert ist.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'Lizenzen',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'Die freien Komponenten, die Cerclic nutzt, und ihre Lizenzen.',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'Deinstallieren…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'Noch keine Unterschrift: Zeichne sie oder importiere ein Foto. Sonst wirst du beim ersten Signieren danach gefragt.',
    # cerclic/ui/settings_window.py:1130
    'Images': 'Bilder',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'Einstellen: per Tastatur',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'Einstellen: per Maus',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'Per Drag & Drop',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'Cerclic beim Anmelden öffnen',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'Für die ausgewählten Dateien im Finder oder auf dem Schreibtisch.',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'Für die ausgewählten Dateien im Datei-Explorer oder auf dem Desktop.',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Finder-Auswahl lesen',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': 'Beim ersten Mal fragt macOS, ob Cerclic den Finder steuern darf: Erlaube es. Cerclic liest dort nur die ausgewählten Dateien.',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '„Cerclic“ im Rechtsklickmenü des Finders',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'Im Menü „Schnellaktionen“ deiner Dateien, im Finder und auf dem Schreibtisch.',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": 'Zeigt das vollständige Menü ohne den Umweg über „Weitere Optionen anzeigen“. Cerclic bietet dann an, den Datei-Explorer neu zu starten.',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'Tipp: Auch ohne Änderung öffnet Umschalt + Rechtsklick auf eine Datei direkt das vollständige Menü mit „Cerclic“.',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'Kein Ordner ausgewählt.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": 'Entfernt „Cerclic“ aus dem Rechtsklickmenü und den Anmeldeobjekten und beendet es. Danach musst du nur noch Cerclic.app in den Papierkorb legen.',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'Tastenkürzel deaktiviert: „Cerclic“ im Rechtsklickmenü bleibt verfügbar.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'Tastenkürzel deaktiviert.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic läuft jetzt im Hintergrund: Sein Symbol ist in der Menüleiste oben auf dem Bildschirm. Wähle unten, wie du das Rad am liebsten öffnest.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic läuft jetzt im Hintergrund: Sein Symbol ist neben der Uhr (manchmal unter dem kleinen Pfeil ^ versteckt). Wähle unten, wie du das Rad am liebsten öffnest.',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": 'Ziehe Dateien auf das Symbol von Cerclic (im Ordner „Programme“ oder im Dock).',
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": 'Ziehe Dateien auf das Symbol von Cerclic.',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '„Cerclic“ im Rechtsklickmenü von Dateien',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'Oben im Menü von Bildern, PDFs, Videos und Audiodateien, im Datei-Explorer und auf dem Desktop.',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'Für Bilder, PDFs, Videos und Audiodateien, im Datei-Explorer, auf dem Desktop und in den Fenstern „Öffnen“ und „Speichern“.',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'Ihr Name: der Originalname plus die Änderung, zum Beispiel Foto (komprimiert).jpg neben Foto.jpg. Ist der Name schon vergeben, fügt Cerclic eine Nummer hinzu: Nichts wird je überschrieben.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": 'Gefällt dir ein Ergebnis nicht? „Löschen“ auf seiner Karte entfernt es sofort.',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'Ordner deiner Wahl: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'Ordner deiner Wahl: noch keiner.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": 'Ein Foto deiner Unterschrift auf weißem Papier genügt: Cerclic macht das Papier transparent und behält die Tinte.',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': 'Zum Signieren: Rechtsklick oder Tastenkürzel auf einem PDF, dann „Signieren“. Platziere die Unterschrift und drücke {key}.',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': 'Versehentlich abgelehnt? Aktiviere unter Automation „Finder“ bei Cerclic.',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ Überall auf dem Mac aktiv.',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ Überall in Windows aktiv.',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'macOS oder eine andere App verwendet diese Kombination bereits. Wähle mit „Ändern“ eine andere.',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'Windows oder eine andere App verwendet diese Kombination bereits. Wähle mit „Ändern“ eine andere.',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'In diesem Bild wurde keine Unterschrift erkannt.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'Deine Unterschrift',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'Wird für die nächsten Male gespeichert',
    # cerclic/ui/signature.py:200
    'Importer…': 'Importieren…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'Ein Foto deiner Unterschrift auf weißem Papier',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'Verschiebe die Unterschrift · ziehe an einer Ecke · {key} zum Signieren',
    # cerclic/ui/signature.py:413
    'Changer': 'Ändern',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': 'Eine andere Unterschrift zeichnen oder importieren',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'Signieren',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'Seite {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'Hier unterschreiben',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': 'Bild deiner Unterschrift auswählen',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'Bilder ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'Füllen',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": 'Das Bild füllt den ganzen Rahmen, Überstehendes wird abgeschnitten.\nZiehe es, um den sichtbaren Teil zu wählen, Mausrad zum Zoomen.',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'Unscharf',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": 'Das ganze Bild, nichts wird abgeschnitten.\nDrumherum: dasselbe Bild, unscharf.',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'Weiß',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": 'Das ganze Bild, nichts wird abgeschnitten.\nDrumherum: Weiß.',
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'Schwarz',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": 'Das ganze Bild, nichts wird abgeschnitten.\nDrumherum: Schwarz.',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'Vorherige Datei',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'Nächste Datei',
    # cerclic/ui/social_editor.py:448
    'Créer': 'Erstellen',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'Ziehe und zoome · {key} zum Erstellen',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'Nichts wird abgeschnitten · {key} zum Erstellen',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': 'Der gewählte Ausschnitt ist kleiner als das Format: Vergrößert wird er etwas unschärfer.',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'Das Video ist kleiner als das Format: Vergrößert wird es etwas unschärfer.',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": 'Das Bild ist kleiner als das Format: Vergrößert wird es etwas unschärfer.',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'Dauer unbekannt',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'Ziehe an den Griffen · {key} zum Kürzen',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'Kürzen',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'Dauer {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': 'Dauer nicht lesbar: Datei beschädigt?',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'Anfang {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'Ende {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['„{name}“ hat {n} Seite: Nur die erste bliebe erhalten. Nutze „{action}“, um alle zu behalten.', '„{name}“ hat {n} Seiten: Nur die erste bliebe erhalten. Nutze „{action}“, um alle zu behalten.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'Das ist bereits ein {format}.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'Dieses Bild ist bereits gut komprimiert.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'Der Zuschneidebereich ist leer.',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": 'Der Rahmen umfasst das ganze Bild: Es gibt nichts zuzuschneiden.',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'Es sind mindestens zwei Bilder nötig.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'Kombinieren',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'Dieses Bild enthält keine privaten Informationen.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'Bild {i} von {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'Als PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": 'Das Bild hat bereits {size} px oder weniger.',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': 'Bild nicht lesbar: {name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '„{name}“ ist passwortgeschützt.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'Falsches Passwort.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'Umwandlung in Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'Diese Datei ist kein PDF: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'Keine Bilder.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'Zum Zusammenfügen sind mindestens zwei PDFs nötig.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'Keine Seite zum Behalten.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": 'Kein Text in diesem PDF: Es ist wohl ein Scan (ein Bild).',
    # cerclic/actions/pdf.py:570
    'Vérification': 'Prüfung',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'Dieses PDF ist bereits gut komprimiert.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'Der Rahmen umfasst die ganze Seite: Es gibt nichts zuzuschneiden.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': 'Der Text des Wasserzeichens ist leer.',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'Keine Unterschrift gespeichert.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'Das Passwort ist leer.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": 'Dieses PDF hat bereits ein Passwort. Um ein anderes festzulegen, entferne zuerst dieses ({more}, dann {action}).',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'Dieses PDF ist nicht geschützt.',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF beschädigt oder nicht lesbar: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'Seite {i} von {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i} von {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'Dieses PDF hat nur eine Seite.',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'Seite in diesem PDF nicht gefunden.',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'Die Seiten wurden nicht geändert.',
    # cerclic/actions/registry.py:34
    'Image': 'Bild',
    # cerclic/actions/registry.py:36
    'Vidéo': 'Video',
    # cerclic/actions/registry.py:37
    'Son': 'Audio',
    # cerclic/actions/registry.py:136
    'Droite': 'Rechts',
    # cerclic/actions/registry.py:137
    'Gauche': 'Links',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'Social Media',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'Drehen',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'Größe ändern',
    # cerclic/actions/registry.py:213
    'Convertir': 'Konvertieren',
    # cerclic/actions/registry.py:223
    'Copier': 'Kopieren',
    # cerclic/actions/registry.py:226
    'Assembler': 'Kombinieren',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'Anonymisieren',
    # cerclic/actions/registry.py:256
    'Fusionner': 'Zusammenfügen',
    # cerclic/actions/registry.py:260
    'Pages': 'Seiten',
    # cerclic/actions/registry.py:266
    'En Word': 'Als Word',
    # cerclic/actions/registry.py:270
    'En images': 'Als Bilder',
    # cerclic/actions/registry.py:276
    'Diviser': 'Aufteilen',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': 'Wasserzeichen',
    # cerclic/actions/registry.py:290
    'Numéroter': 'Nummerieren',
    # cerclic/actions/registry.py:295
    'En texte': 'Als Text',
    # cerclic/actions/registry.py:326
    'En MP4': 'Als MP4',
    # cerclic/actions/registry.py:329
    'En GIF': 'Als GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'Ton extrahieren',
    # cerclic/actions/registry.py:336
    'Couper le son': 'Ton entfernen',
    # cerclic/actions/registry.py:352
    'En MP3': 'Als MP3',
    # cerclic/actions/registry.py:141
    'Miroir': 'Spiegeln',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'Einen Teil behalten',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'Zuschneiden',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta, Story, Handy, PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'Social-Media-Format',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'Drehen oder spiegeln',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'Drehen',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'Weniger Pixel',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'Größenänderung',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'Kleinere Datei, gleiche Maße',
    # cerclic/actions/registry.py:216
    'Changer de format': 'Format ändern',
    # cerclic/actions/registry.py:216
    'Conversion': 'Umwandlung',
    # cerclic/actions/registry.py:222
    'Une page par image': 'Eine Seite pro Bild',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'PDF-Erstellung',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'Zum Einfügen, wo du willst',
    # cerclic/actions/registry.py:225
    'Copie': 'Kopieren',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'Mehrere zu einem Bild',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'Entfernt GPS, Kamera, Datum',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'Anonymisierung',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'Deine Unterschrift platzieren',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'Ränder abschneiden',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'Kleiner zum Versenden',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'Ein einziges PDF',
    # cerclic/actions/registry.py:259
    'Fusion': 'Zusammenfügen',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'Sortieren, drehen, löschen',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'Seiten ordnen',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'In Word bearbeitbar',
    # cerclic/actions/registry.py:273
    'Une image par page': 'Ein Bild pro Seite',
    # cerclic/actions/registry.py:273
    'Conversion en images': 'Umwandlung in Bilder',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'Ein PDF pro Seite',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'Aufteilung in Seiten',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'Ein Text quer darüber',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'Seitenzahlen unten',
    # cerclic/actions/registry.py:294
    'Numérotation': 'Nummerierung',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'Der Text als .txt',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'Textextraktion',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'Mit einem Passwort',
    # cerclic/actions/registry.py:304
    'Protection': 'Passwortschutz',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'Passwort entfernen',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'Entsperren',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'Einen Abschnitt behalten',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'Kürzen',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels, TikTok, Shorts, PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'Kleiner, als MP4',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'Überall abspielbar',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'Umwandlung in MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': 'Eine Animation ohne Ton',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'GIF-Erstellung',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'Die Tonspur als MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': 'Tonextraktion',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'Das Video ohne Ton',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': 'Ton entfernen',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'Richtig herum drehen',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'Umwandlung in MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'Kleiner, als MP3',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'Datei {i} von {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '„{name}“: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '50\xa0%',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'Nebeneinander',
    # cerclic/actions/registry.py:231
    'En colonne': 'Untereinander',
    # cerclic/actions/registry.py:232
    'En grille': 'Als Raster',
    # cerclic/actions/social.py:46
    'Carré': 'Quadrat',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Beitrag für Instagram, Facebook oder LinkedIn',
    # cerclic/actions/social.py:47
    'carré': 'quadratisch',
    # cerclic/actions/social.py:48
    'Portrait': 'Hochformat',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Beitrag für Instagram oder Facebook, am größten im Feed',
    # cerclic/actions/social.py:50
    'portrait': 'Hochformat',
    # cerclic/actions/social.py:51
    'Grille': 'Raster',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram, genau im Format des Profilrasters',
    # cerclic/actions/social.py:52
    'grille': 'Raster',
    # cerclic/actions/social.py:53
    'Story': 'Story',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'Smartphone-Vollbild: Story, Reels, TikTok, YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'Story',
    # cerclic/actions/social.py:56
    'Paysage': 'Querformat',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'Computerbildschirm: YouTube, Präsentation, X',
    # cerclic/actions/social.py:57
    'paysage': 'Querformat',
    # cerclic/actions/social.py:58
    'Bannière': 'Banner',
    # cerclic/actions/social.py:58
    '1,91:1': '1,91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Geteilter Link oder breites Bild auf Facebook, LinkedIn oder X',
    # cerclic/actions/social.py:59
    'bannière': 'Banner',
    # cerclic/actions/social.py:239
    'Format {name}': 'Format: {name}',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'Dieses Bild hat bereits {size}.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'Videogröße nicht lesbar: Datei beschädigt?',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'Dieses Video hat bereits {size}.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': 'Die Verarbeitung ist fehlgeschlagen: Die Datei ist vielleicht beschädigt oder in einem ungewöhnlichen Format.',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': 'ffmpeg wurde nicht gefunden: Installiere Cerclic neu.',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'Video beschädigt oder Format nicht unterstützt.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'Zugriff verweigert: Die Datei ist vielleicht in einer anderen App geöffnet.',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'Kürzen',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'Keine Videobilder in dieser Datei.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'Dieses Video ist bereits gut komprimiert: Versuche eine stärkere Komprimierung.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'Video zu lang für ein GIF (über 2 Minuten: Es wäre Hunderte MB groß). Behalte zuerst einen Abschnitt mit „{action}“.',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'Umwandlung in GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'Dieses Video hat keinen Ton.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'Der zu behaltende Abschnitt ist zu kurz.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': 'Der gewählte Abschnitt umfasst die ganze Datei.',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'Kein Ton in dieser Datei.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'Vorschau nicht möglich.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'Diese Audiodatei ist bereits klein: Versuche eine stärkere Komprimierung.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'Diese Datei enthält nur Ton, kein Bild: Nutze „{action}“, um daraus ein MP3 zu machen.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'Die Vorschau braucht zu lange.',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 schließt Fenster.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab wechselt zwischen Fenstern.',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc wechselt zwischen Fenstern.',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Leertaste öffnet das Fenstermenü.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Strg + Esc öffnet das Startmenü.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Strg + Alt + Entf ist für Windows reserviert.',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Strg + Umschalt + Esc öffnet den Task-Manager.',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'Taste {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'Leertaste',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Tab': 'Tab',
    # contexte : touche Windows | cerclic/win/hotkey.py:40
    'touche Windows\x04Entrée': 'Eingabe',
    # contexte : touche Windows | cerclic/win/hotkey.py:41
    'touche Windows\x04Retour': 'Rücktaste',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Échap': 'Esc',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Inser': 'Einfg',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Suppr': 'Entf',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Origine': 'Pos1',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Fin': 'Ende',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Page préc.': 'Bild auf',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Page suiv.': 'Bild ab',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Pause': 'Pause',
    # contexte : touche Windows | cerclic/win/hotkey.py:46
    'touche Windows\x04Impr. écran': 'Druck',
    # contexte : touche Windows | cerclic/win/hotkey.py:82, cerclic/win/hotkey.py:84
    'touche Windows\x04Pavé {key}': 'Num {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Füge nach Strg, Alt, Umschalt oder Win eine Taste hinzu.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} wird bereits von Windows und Apps verwendet (Hilfe, Umbenennen, Aktualisieren, Rechtschreibung …). Füge zum Beispiel Strg + Alt hinzu: Strg + Alt + {key}.',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt mit dem Ziffernblock dient zum Eingeben von Zeichen (Alt + 0201 = É). Wähle eine andere Kombination.',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'Die Kombination braucht Strg, Alt oder Win (sonst ließe sich diese Taste nicht mehr tippen).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Strg',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Umschalt',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt + eine einzelne Taste wird bereits in vielen Apps verwendet (für die Menüs der Apps). Füge Umschalt oder Strg hinzu, zum Beispiel Alt + Umschalt + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'Diese Kombination dient zum Eingeben von Zeichen mit AltGr (@, €, µ …). Wähle eine andere.',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Strg + eine einzelne Taste wird bereits in vielen Apps verwendet (Fett, Kopieren, Einfügen, Speichern …). Füge Umschalt oder Alt hinzu, zum Beispiel Strg + Umschalt + {key}.',
    # cerclic/ui/settings_window.py (À propos)
    'Code source': 'Quellcode',
    'Tout le code de Cerclic est public, sur GitHub.': 'Der gesamte Code von Cerclic ist öffentlich, auf GitHub.',
}
