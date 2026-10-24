"""Cerclic, Italiano. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} file', '{n} file'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": 'Salvato in «{where}»: la cartella originale è protetta.',
    # cerclic/app.py:92
    'Téléchargements': 'Download',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": "Windows o un'altra app la usa già. Scegline un'altra in Cerclic.",
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'clic destro, poi «Cerclic»',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": "La cartella scelta non si trova: salvato accanto all'originale.",
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'Apri Cerclic',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'Esci da Cerclic',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": "Windows o un'altra app la usa già. Scegline un'altra in Cerclic; il clic destro «Cerclic» funziona sempre.",
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": "macOS o un'altra app la usa già. Scegline un'altra in Cerclic.",
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'clic destro, Azioni rapide, poi «Cerclic»',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'clic destro, «Mostra altre opzioni», poi «Cerclic»',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'Consenti a Cerclic di leggere la tua selezione',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': 'Impostazioni di Sistema, Privacy e sicurezza, Automazione: attiva «Finder» sotto Cerclic. Il clic destro, Azioni rapide, «Cerclic» funziona anche senza.',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': "Fai clic su un'immagine, un PDF, un video o un file audio nel Finder o sulla Scrivania, poi premi {combo}.",
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": "Fai clic su un'immagine, un PDF, un video o un file audio in Esplora file o sul desktop, poi premi {combo}.",
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'Oppure: clic destro, Azioni rapide, poi «Cerclic».',
    # cerclic/app.py:919
    'Image copiée': 'Immagine copiata',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'Incollala dove vuoi con {key} + V.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'OK',
    # cerclic/app.py:1253
    'Menu complet activé': 'Menu completo attivato',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'Si applica al riavvio di Esplora file. Le finestre delle cartelle aperte si chiuderanno.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Menu di Windows 11 ripristinato',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'Si applica al riavvio di Esplora file.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'Due Cerclic installati',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'La versione di Cerclic installata senza Microsoft Store è ancora presente. Per avere un solo «Cerclic» nel clic destro e un solo collegamento, rimuovila: «Mostra il programma di disinstallazione», poi fai doppio clic su «unins000».',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": 'La versione di Cerclic installata senza Microsoft Store è ancora presente. Per avere un solo «Cerclic», disinstallala in App installate: è il Cerclic che non ha «Opzioni avanzate» nel suo menu.',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": "macOS o un'altra app la usa già. Scegline un'altra in Cerclic; il clic destro «Cerclic» funziona sempre.",
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'Oppure: clic destro, «Mostra altre opzioni», poi «Cerclic».',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'Oppure: clic destro, poi «Cerclic».',
    # cerclic/app.py:915
    'Copie impossible': 'Impossibile copiare',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'Sblocca',
    # cerclic/app.py:966
    'Continuer': 'Continua',
    # cerclic/app.py:971
    '« {name} » est protégé.': '«{name}» è protetto.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'Password del PDF',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'Avvio con Windows bloccato',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': 'La tua organizzazione non consente alle app di avviarsi con Windows.',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': 'Avvio con Windows disattivato in Windows',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'È stato disattivato in Gestione attività: solo Windows può riattivarlo. In Impostazioni, App, Avvio, attiva «Cerclic».',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'Scorciatoia {combo} non disponibile',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Cerclic ha riscontrato un problema',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'I dettagli sono in {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': 'File non accessibile',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'Questo file non è in una cartella normale (archivio ZIP, telefono…). Copialo in una cartella, poi riprova.',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': 'Immagine illeggibile.',
    # cerclic/app.py:1224
    'Réessayer': 'Riprova',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': "macOS o un'altra app usa già {refused}. La tua scorciatoia resta {kept}.",
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': "Windows o un'altra app usa già {refused}. La tua scorciatoia resta {kept}.",
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'Più tardi',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'Apri le impostazioni',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'Nessuna azione per questo tipo di file',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'Cerclic funziona con immagini, PDF, video e file audio.',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'Seleziona prima un file',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': 'Password errata per «{name}». Riprova.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Il ritaglio terrebbe solo la prima. Usa «In PDF» per tenerle tutte, poi {action} sul PDF.',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['«{name}» ha {n} pagina', '«{name}» ha {n} pagine'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': 'Dove salvare il risultato?',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'Riavvia Esplora file',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'Mostra il programma di disinstallazione',
    # cerclic/app.py:602
    'Ouvrir les applications': 'Apri App installate',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": "macOS o un'altra app la usa già. La tua scorciatoia resta {kept}.",
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": "Windows o un'altra app la usa già. La tua scorciatoia resta {kept}.",
    # cerclic/app.py:975
    'Mot de passe incorrect': 'Password errata',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'Non è stato creato nulla.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'La compressione terrebbe solo la prima. Usa «In PDF» per tenerle tutte, poi {action} sul PDF.',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'Solo la prima verrebbe adattata al formato. Usa «In PDF» per tenerle tutte.',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'Apri',
    # cerclic/app.py:707
    'Changer de raccourci': 'Cambia scorciatoia',
    # cerclic/app.py:1081
    'Texte du filigrane': 'Testo della filigrana',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'Verrà scritto in diagonale su ogni pagina.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'RISERVATO',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'Password da impostare',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": "Verrà chiesta per aprire il PDF. L'originale resta senza password.",
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'Proteggi',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'Errore imprevisto. Riprova; se succede di nuovo, i dettagli sono nel registro di Cerclic (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': "Accesso negato: forse il file è aperto in un'altra app, oppure la cartella è protetta.",
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'Nome o percorso troppo lungo per Windows: dai al file un nome più corto, oppure spostalo in una cartella meno profonda.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'File non trovato: forse è stato spostato o eliminato.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'File troppo grande per la memoria disponibile.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'Il disco è pieno.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': 'Immagine illeggibile o formato non supportato.',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF danneggiato o illeggibile.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: serve almeno {n} file.', '{action}: servono almeno {n} file.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'Annullato',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": "«{name}» non c'è più: è stato spostato, rinominato o eliminato (oppure la chiavetta USB è stata rimossa).",
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ["{n} file non c'è più: è stato spostato, rinominato o eliminato.", '{n} file non ci sono più: sono stati spostati, rinominati o eliminati.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'Questo PDF è protetto da password.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": "L'elaborazione si è interrotta di colpo: probabilmente il file è danneggiato.",
    # cerclic/paths.py:235
    'compressé': 'compresso',
    # cerclic/paths.py:235
    'redimensionné': 'ridimensionato',
    # cerclic/paths.py:236
    'pivoté': 'ruotato',
    # cerclic/paths.py:236
    'rogné': 'ritagliato',
    # cerclic/paths.py:236
    'miroir': 'specchiato',
    # cerclic/paths.py:237
    'anonymisé': 'anonimizzato',
    # cerclic/paths.py:237
    'assemblé': 'assemblato',
    # cerclic/paths.py:237
    'fusionné': 'unito',
    # cerclic/paths.py:238
    'réorganisé': 'riordinato',
    # cerclic/paths.py:238
    'extrait': 'estratto',
    # cerclic/paths.py:238
    'texte': 'testo',
    # cerclic/paths.py:239
    'filigrane': 'filigrana',
    # cerclic/paths.py:239
    'numéroté': 'numerato',
    # cerclic/paths.py:239
    'signé': 'firmato',
    # cerclic/paths.py:240
    'protégé': 'protetto',
    # cerclic/paths.py:240
    'déverrouillé': 'sbloccato',
    # cerclic/paths.py:240
    'son': 'audio',
    # cerclic/paths.py:241
    'raccourci': 'accorciato',
    # cerclic/paths.py:241
    'sans son': 'senza audio',
    # cerclic/paths.py:241
    'images': 'immagini',
    # cerclic/paths.py:242
    'pages': 'pagine',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': 'stessa dimensione',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'Da {before} a {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} byte', '{n} byte'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '{pct}% in meno',
    # cerclic/sizes.py:64
    '{pct} % de plus': '{pct}% in più',
    # cerclic/system.py:17
    'Cmd': 'Cmd',
    # cerclic/system.py:17
    'Ctrl': 'Ctrl',
    # cerclic/system.py:18
    'Suppr': 'Canc',
    # cerclic/system.py:19
    'Retour': 'Invio',
    # cerclic/system.py:19
    'Entrée': 'Invio',
    # contexte : touche Mac | cerclic/mac/hotkey.py:168
    'touche Mac\x04Touche {code}': 'Tasto {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'Cmd + Spazio apre Spotlight.',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'Opzione + Cmd + Spazio apre la ricerca del Finder.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'Ctrl + Spazio cambia la lingua della tastiera.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'Ctrl + Opzione + Spazio cambia la lingua della tastiera.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'Ctrl + Cmd + Spazio apre le emoji.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": "Cmd + Tab passa da un'app all'altra.",
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": "Maiusc + Cmd + Tab passa da un'app all'altra.",
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': "Opzione + Cmd + Esc forza l'uscita da un'app.",
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Maiusc + Cmd + 3 fa uno screenshot.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Maiusc + Cmd + 4 fa uno screenshot.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Maiusc + Cmd + 5 apre lo strumento Screenshot.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'Maiusc + Cmd + 6 fa uno screenshot della Touch Bar.',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'Ctrl + Cmd + Q blocca lo schermo.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Maiusc + Cmd + Q chiude la sessione.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'Ctrl + Cmd + F passa a tutto schermo.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'Opzione + Cmd + D nasconde il Dock.',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'Opzione + Cmd + C copia il percorso di un file nel Finder.',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'Opzione + Cmd + H nasconde le altre app.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'Opzione + Cmd + M riduce a icona tutte le finestre.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'Opzione + Cmd + W chiude tutte le finestre.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'Opzione + Cmd + V sposta un file copiato nel Finder.',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Spazio',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'Invio',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'Tastierino Invio',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'Tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': 'Canc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Échap': 'Esc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Début': 'Home',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Fin': 'Fine',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page préc.': 'Pag su',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page suiv.': 'Pag giù',
    # contexte : touche Mac | cerclic/mac/hotkey.py:73
    'touche Mac\x04Aide': 'Aiuto',
    # contexte : touche Mac | cerclic/mac/hotkey.py:156, cerclic/mac/hotkey.py:163
    'touche Mac\x04Pavé {key}': 'Tastierino {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'Aggiungi un tasto dopo Cmd, Ctrl, Opzione o Maiusc.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': "{shortcut} è già una scorciatoia di macOS (Impostazioni di Sistema, Tastiera, Abbreviazioni da tastiera). Scegline un'altra.",
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': "Maiusc + Cmd + {key} è già in uso nel Finder. Scegli un'altra lettera, oppure Maiusc + Cmd + Spazio.",
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": 'Serve Cmd o Ctrl nella combinazione: macOS rifiuta le scorciatoie fatte solo di Opzione o Maiusc.',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Cmd + un solo tasto è già in uso in tutte le app (copia, incolla, salva…). Aggiungi Maiusc, Opzione o Ctrl, ad esempio Maiusc + Cmd + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": "Ctrl + le frecce passano da una scrivania all'altra (Mission Control).",
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Ctrl',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Opzione',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Maiusc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Cmd',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'Annulla',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'Mostra la password',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'Nascondi la password',
    # cerclic/ui/cards.py:238
    'Fermer': 'Chiudi',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'Desktop',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'Download',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'Immagini',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'Video',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'Filmati',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'Musica',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'Documenti',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'Interrompi',
    # cerclic/ui/cards.py:299
    'En cours': 'In corso',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'Interruzione in corso…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['File eliminato', 'File eliminati'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": 'Il tuo file originale non è stato toccato.',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} file creato', '{n} file creati'],
    # cerclic/ui/cards.py:366
    'Dossier': 'Cartella',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'Elimina',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'Elimina ciò che Cerclic ha appena creato (il tuo file originale non viene toccato)',
    # cerclic/ui/cards.py:417
    'Suppression impossible': 'Impossibile eliminare',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': "Probabilmente il file è aperto in un'altra app: chiudila, poi riprova.",
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': 'In «{folder}»',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} file escluso, ad esempio: {example}', '{n} file esclusi, ad esempio: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'Interrotto: non è stato creato nulla.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '{size} in tutto · in «{folder}»',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · in «{folder}»',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title} impossibile',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'Errore sconosciuto.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'Leggera',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'Media',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'Forte',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'Massima',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}% · {n} colore', '{percent}% · {n} colori'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': 'Immagini a 220 dpi: molto nitide, anche stampate',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": 'Immagini a 150 dpi: nitide a schermo e in stampa',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": 'Immagini a 110 dpi: per lo schermo',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': 'Immagini a 80 dpi: il più leggero, immagini meno nitide',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": 'Fino a 1080p, qualità molto buona',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": 'Fino a 1080p, buona qualità',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p: per un telefono o un messaggio',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p: il più leggero',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbit/s: musica, qualità molto buona',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbit/s: musica',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbit/s: voce, e musica su un telefono',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbit/s: voce',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}% · senza perdita',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'Caricamento…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': 'invece di {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'Nessun risparmio',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'nessun risparmio',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'Impossibile',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'impossibile',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'calcolo…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'Scegli la qualità · {key} per comprimere',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': "Scegli l'intensità · {key} per comprimere",
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'Comprimi',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'Qualità',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'Compressione',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": "Passa sopra l'immagine: dettaglio al 100%",
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": "Passa sopra l'immagine: dettaglio",
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: nessuna regolazione',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['Anteprima: {name} · totale per {n} immagine, stimato su {sampled}', 'Anteprima: {name} · totale per {n} immagini, stimato su {sampled}'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['Anteprima: {name} · totale per {n} immagine', 'Anteprima: {name} · totale per {n} immagini'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'Non più leggero',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'Compressione impossibile.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} esclusa', '{n} escluse'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'Prova una compressione più forte.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'Originale: {size} · abbassa la qualità',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'Originale: {size} · comprimi di più',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'Libero',
    # cerclic/ui/crop_editor.py:27
    'Original': 'Originale',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'Trascina gli angoli · {key} per ritagliare',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'Ritaglia',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'Tutte le pagine',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'Immagine intera',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": "Riprendi tutta l'immagine",
    # cerclic/ui/crop_editor.py:589
    '{width} × {height} cm': '{width} × {height} cm',
    # cerclic/ui/crop_editor.py:593, cerclic/ui/crop_editor.py:448, cerclic/ui/social_editor.py:43
    '{width} × {height} px': '{width} × {height} px',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:103
    'touche du Mac\x04Retour': 'Invio',
    # contexte : touche | cerclic/ui/editor_base.py:103
    'touche\x04Entrée': 'Invio',
    # contexte : touche | cerclic/ui/editor_base.py:108
    'touche\x04Suppr': 'Canc',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:113
    'touche du Mac\x04Cmd': 'Cmd',
    # contexte : touche | cerclic/ui/editor_base.py:113
    'touche\x04Ctrl': 'Ctrl',
    # cerclic/ui/editor_base.py:205
    'Fermer (Échap)': 'Chiudi (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'Trascina per riordinare · {key} per togliere',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'Ruota a sinistra',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'Ruota a destra ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': "Verso l'inizio ({key} + {arrow})",
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'Verso la fine ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'Estrai la selezione',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'Un nuovo PDF con solo le pagine scelte',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'Ripristina',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'Salva',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{n} selezionata su {count}', '{n} selezionate su {count}'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} pagina', '{n} pagine'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'Altro',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ Indietro',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'Altri strumenti',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'Generali',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'Scorciatoia da tastiera',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'Clic destro',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'File creati',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'Firma',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'Info',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'Versione {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Seleziona uno o più file in Esplora file o sul desktop, poi premi {combo}.',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'Modifica',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'Predefinito',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'Premi la tua combinazione…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'Verifica…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'Versione {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Seleziona uno o più file nel Finder o sulla Scrivania, poi premi {combo}.',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'Apri la ruota',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'Clic destro sul file, Azioni rapide, poi «Cerclic». Oppure: Apri con, poi Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'Avvio',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'Chiude Cerclic. Per riaprirlo, avvialo dalla cartella Applicazioni.',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'Lingua',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": 'Automatica (lingua del computer)',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'Disinstalla Cerclic',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": 'Rimuovere Cerclic dal clic destro e dagli elementi di login, poi chiuderlo?',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'Disinstalla',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'Una combinazione di tasti apre la ruota sui file selezionati.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'Apri la ruota dalla tastiera',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '«Cerclic» nel menu del clic destro dei tuoi file.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '«Cerclic» nel clic destro',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'Il tuo file originale non viene mai modificato: ogni azione crea un nuovo file.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'Dove salvarli',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'Accanto al file originale',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'Nella stessa cartella, ad esempio sulla scrivania se la foto è lì. Consigliato.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'In una cartella a mia scelta',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'Tutti i file creati nello stesso posto.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'Chiedimelo ogni volta',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'Cerclic ti chiede la cartella prima di creare il file.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'Scegli…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'Cartella dei file creati',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'Per firmare i tuoi PDF con un gesto. Resta su questo computer.',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'Disegna…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'Importa una foto…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'Cancella',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'Il giusto equilibrio tra peso dei file e nitidezza.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}%',
    # cerclic/ui/settings_window.py:993
    'Voir': 'Mostra',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'Scegli una foto della tua firma',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'Scorciatoia invariata.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'Esempi: Maiusc + Cmd + Spazio, Ctrl + Opzione + X. Esc per annullare.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'Esempi: Ctrl + Alt + Spazio, Ctrl + Maiusc + X, Win + Maiusc + C. Esc per annullare.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'Più leggero',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'Più nitido',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'Ti diamo il benvenuto in Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'Le modifiche si applicano subito.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": "Due modi per aprire la ruota, l'avvio e la lingua.",
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": "Tre modi per aprire la ruota, l'avvio e la lingua.",
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'Con la tastiera',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Maiusc + clic destro sul file, poi «Cerclic». Senza Maiusc, passa da «Mostra altre opzioni».',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'Clic destro sul file, poi «Cerclic».',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'Con il mouse',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'Avvia Cerclic con il Mac',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'Avvia Cerclic con Windows',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'Consigliato: la ruota è pronta appena ti serve.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'Chiude Cerclic. Per riaprirlo, avvialo dal menu Start.',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'Chiude Cerclic. Per riaprirlo, avvialo dal desktop o dal menu Start.',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'Chiudi Cerclic',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": 'La ruota non si aprirà più fino al prossimo avvio.',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'Quella di menu, finestre e messaggi di Cerclic.',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": "«Modifica», poi premi la tua combinazione. Se è già usata da macOS o da un'altra app, Cerclic te lo dice e tiene quella precedente.",
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Hai un mouse con pulsanti programmabili? Imposta un pulsante su un tasto da F13 a F20, poi sceglilo qui: un clic su quel pulsante aprirà la ruota.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": "«Modifica», poi premi la tua combinazione. Se è già usata da Windows o da un'altra app, Cerclic te lo dice e tiene quella precedente.",
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Hai un mouse con pulsanti programmabili? Imposta un pulsante su un tasto da F13 a F24, poi sceglilo qui: un clic su quel pulsante aprirà la ruota.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'Autorizzazione',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'Impostazioni…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'Menu completo del clic destro',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': 'Non è in Azioni rapide? Clic destro su un file, Azioni rapide, poi Personalizza, e seleziona «Cerclic». È anche sempre in Apri con.',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'Compressione delle immagini',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': 'Impostazione proposta da «Comprimi», che mostra la dimensione ottenuta e ricorda la tua ultima scelta.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'JPG creati dalle altre azioni',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': 'Ritagliare, ruotare, convertire… Al 90% la perdita non si vede.',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'Ritagliare, firmare, comprimere, convertire, adattare ai formati dei social… con un gesto, senza aprire altre app.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'Registro',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'In caso di problemi, questo file aiuta a capire cosa è successo.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'Licenze',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'I componenti open source usati da Cerclic e le loro licenze.',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'Disinstalla…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'Nessuna firma per ora: disegnala o importa una foto. Altrimenti ti verrà chiesta la prima volta che firmi.',
    # cerclic/ui/settings_window.py:1130
    'Images': 'Immagini',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'Imposta: con la tastiera',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'Imposta: con il mouse',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'Trascinando',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'Apri Cerclic al login',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'Sui file selezionati nel Finder o sulla Scrivania.',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'Sui file selezionati in Esplora file o sul desktop.',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Leggere la selezione del Finder',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': 'La prima volta, macOS chiede se Cerclic può controllare il Finder: accetta. Cerclic legge solo i file selezionati.',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '«Cerclic» nel clic destro del Finder',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'Nel menu Azioni rapide dei tuoi file, nel Finder e sulla Scrivania.',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": 'Mostra il menu completo senza passare da «Mostra altre opzioni». Cerclic proporrà di riavviare Esplora file.',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'Suggerimento: senza cambiare nulla, Maiusc + clic destro su un file apre direttamente il menu completo, con «Cerclic».',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'Nessuna cartella scelta.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": 'Rimuove «Cerclic» dal clic destro e dagli elementi di login, poi esce. Resterà da spostare Cerclic.app nel Cestino.',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'Scorciatoia disattivata: il clic destro «Cerclic» resta disponibile.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'Scorciatoia disattivata.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Ora Cerclic funziona in background: la sua icona è nella barra dei menu, in alto sullo schermo. Scegli qui sotto il tuo modo preferito per aprire la ruota.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": "Ora Cerclic funziona in background: la sua icona è vicino all'orologio (a volte nascosta sotto la piccola freccia ^). Scegli qui sotto il tuo modo preferito per aprire la ruota.",
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": "Trascina i file sull'icona di Cerclic (in Applicazioni o nel Dock).",
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": "Trascina i file sull'icona di Cerclic.",
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '«Cerclic» nel clic destro dei file',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'In cima al menu di immagini, PDF, video e file audio, in Esplora file e sul desktop.',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'Su immagini, PDF, video e file audio, in Esplora file, sul desktop e nelle finestre Apri e Salva.',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'Il loro nome: il nome originale, più ciò che è cambiato, ad esempio foto (compresso).jpg accanto a foto.jpg. Se quel nome è già usato, Cerclic aggiunge un numero: nulla viene mai sovrascritto.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": 'Un risultato non ti piace? «Elimina» sulla sua scheda lo cancella subito.',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'Cartella a tua scelta: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'Cartella a tua scelta: nessuna per ora.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": "Basta una foto della tua firma su carta bianca: Cerclic rende trasparente la carta e tiene l'inchiostro.",
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': 'Per firmare: clic destro o scorciatoia su un PDF, poi «Firma». Posiziona la firma e premi {key}.',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': 'Rifiutato per errore? In Automazione, attiva «Finder» sotto Cerclic.',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ Attiva ovunque sul Mac.',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ Attiva ovunque in Windows.',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': "macOS o un'altra app usa già questa combinazione. Scegline un'altra con «Modifica».",
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': "Windows o un'altra app usa già questa combinazione. Scegline un'altra con «Modifica».",
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'Nessun tratto di firma trovato in questa immagine.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'La tua firma',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'Conservata per le prossime volte',
    # cerclic/ui/signature.py:200
    'Importer…': 'Importa…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'Una foto della tua firma su carta bianca',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'Trascina la firma · tira un angolo · {key} per firmare',
    # cerclic/ui/signature.py:413
    'Changer': 'Cambia',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': "Disegna o importa un'altra firma",
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'Firma',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'Pagina {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'Firma qui',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': "Scegli un'immagine della tua firma",
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'Immagini ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'Riempi',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": "L'immagine riempie tutto il riquadro, ciò che esce viene tagliato.\nTrascinala per scegliere la parte da tenere, rotellina per lo zoom.",
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'Sfondo sfocato',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": "Tutta l'immagine, nulla viene tagliato.\nIntorno: la stessa immagine, sfocata.",
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'Sfondo bianco',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": "Tutta l'immagine, nulla viene tagliato.\nIntorno: bianco.",
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'Sfondo nero',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": "Tutta l'immagine, nulla viene tagliato.\nIntorno: nero.",
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'File precedente',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'File successivo',
    # cerclic/ui/social_editor.py:448
    'Créer': 'Crea',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'Trascina e ingrandisci · {key} per creare',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'Nulla viene tagliato · {key} per creare',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': "La parte tenuta è più piccola del formato: ingrandita, sarà un po' meno nitida.",
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': "Il video è più piccolo del formato: ingrandito, sarà un po' meno nitido.",
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": "L'immagine è più piccola del formato: ingrandita, sarà un po' meno nitida.",
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'Durata sconosciuta',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'Trascina le maniglie · {key} per accorciare',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'Accorcia',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'Durata {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': 'Durata illeggibile: file danneggiato?',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'Inizio {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'Fine {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['«{name}» ha {n} pagina: verrebbe tenuta solo la prima. Usa «{action}» per tenerle tutte.', '«{name}» ha {n} pagine: verrebbe tenuta solo la prima. Usa «{action}» per tenerle tutte.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'È già un {format}.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'Questa immagine è già ben compressa.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': "L'area da ritagliare è vuota.",
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": "Il riquadro copre tutta l'immagine: niente da ritagliare.",
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'Servono almeno due immagini.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'Assemblaggio',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'Questa immagine non contiene informazioni private.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'Immagine {i} di {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'In PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": "L'immagine misura già {size} px o meno.",
    # cerclic/actions/images.py:704
    'Image illisible : {name}': 'Immagine illeggibile: {name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '«{name}» è protetto da password.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'Password errata.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'Conversione in Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'Questo file non è un PDF: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'Nessuna immagine.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'Servono almeno due PDF da unire.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'Nessuna pagina da tenere.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": "Nessun testo in questo PDF: probabilmente è una scansione (un'immagine).",
    # cerclic/actions/pdf.py:570
    'Vérification': 'Verifica',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'Questo PDF è già ben compresso.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'Il riquadro copre tutta la pagina: niente da ritagliare.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': 'Il testo della filigrana è vuoto.',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'Nessuna firma salvata.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'La password è vuota.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": "Questo PDF ha già una password. Per impostarne un'altra, rimuovi prima questa ({more}, poi {action}).",
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'Questo PDF non è protetto.',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF danneggiato o illeggibile: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'Pagina {i} di {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i} di {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'Questo PDF ha una sola pagina.',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'Pagina non trovata in questo PDF.',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'Le pagine non sono cambiate.',
    # cerclic/actions/registry.py:34
    'Image': 'Immagine',
    # cerclic/actions/registry.py:36
    'Vidéo': 'Video',
    # cerclic/actions/registry.py:37
    'Son': 'Audio',
    # cerclic/actions/registry.py:136
    'Droite': 'Destra',
    # cerclic/actions/registry.py:137
    'Gauche': 'Sinistra',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'Social',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'Ruota',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'Ridimensiona',
    # cerclic/actions/registry.py:213
    'Convertir': 'Converti',
    # cerclic/actions/registry.py:223
    'Copier': 'Copia',
    # cerclic/actions/registry.py:226
    'Assembler': 'Assembla',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'Anonimizza',
    # cerclic/actions/registry.py:256
    'Fusionner': 'Unisci',
    # cerclic/actions/registry.py:260
    'Pages': 'Pagine',
    # cerclic/actions/registry.py:266
    'En Word': 'In Word',
    # cerclic/actions/registry.py:270
    'En images': 'In immagini',
    # cerclic/actions/registry.py:276
    'Diviser': 'Dividi',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': 'Filigrana',
    # cerclic/actions/registry.py:290
    'Numéroter': 'Numera',
    # cerclic/actions/registry.py:295
    'En texte': 'In testo',
    # cerclic/actions/registry.py:326
    'En MP4': 'In MP4',
    # cerclic/actions/registry.py:329
    'En GIF': 'In GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'Estrai audio',
    # cerclic/actions/registry.py:336
    'Couper le son': 'Togli audio',
    # cerclic/actions/registry.py:352
    'En MP3': 'In MP3',
    # cerclic/actions/registry.py:141
    'Miroir': 'Specchia',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'Tieni una parte',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'Ritaglio',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta, Storie, mobile, PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'Formato social',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'Ruota o capovolgi',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'Rotazione',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'Meno pixel',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'Ridimensionamento',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'Più leggero, stesse dimensioni',
    # cerclic/actions/registry.py:216
    'Changer de format': 'Cambia formato',
    # cerclic/actions/registry.py:216
    'Conversion': 'Conversione',
    # cerclic/actions/registry.py:222
    'Une page par image': 'Una pagina per immagine',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'Creazione del PDF',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'Da incollare dove vuoi',
    # cerclic/actions/registry.py:225
    'Copie': 'Copia',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'Più immagini in una',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'Rimuove GPS, fotocamera, data',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'Anonimizzazione',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'Posiziona la tua firma',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'Taglia i margini',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'Più leggero da inviare',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'Un solo PDF',
    # cerclic/actions/registry.py:259
    'Fusion': 'Unione',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'Riordina, ruota, elimina',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'Organizzazione delle pagine',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'Modificabile in Word',
    # cerclic/actions/registry.py:273
    'Une image par page': "Un'immagine per pagina",
    # cerclic/actions/registry.py:273
    'Conversion en images': 'Conversione in immagini',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'Un PDF per pagina',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'Divisione in pagine',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'Un testo di traverso',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'Numeri a piè di pagina',
    # cerclic/actions/registry.py:294
    'Numérotation': 'Numerazione',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'Il testo in .txt',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'Estrazione del testo',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'Con una password',
    # cerclic/actions/registry.py:304
    'Protection': 'Protezione',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'Rimuovi la password',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'Sblocco',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'Tieni un pezzo',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'Taglio',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels, TikTok, Shorts, PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'Più leggero, in MP4',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'Compatibile ovunque',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'Conversione in MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': "Un'animazione senza audio",
    # cerclic/actions/registry.py:331
    'Création du GIF': 'Creazione della GIF',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'La traccia audio in MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': "Estrazione dell'audio",
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'Il video senza audio',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': "Rimozione dell'audio",
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'Raddrizza',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'Conversione in MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'Più leggero, in MP3',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'File {i} di {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '«{name}»: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '50%',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'Affiancate',
    # cerclic/actions/registry.py:231
    'En colonne': 'In colonna',
    # cerclic/actions/registry.py:232
    'En grille': 'In griglia',
    # cerclic/actions/social.py:46
    'Carré': 'Quadrato',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Post Instagram, Facebook o LinkedIn',
    # cerclic/actions/social.py:47
    'carré': 'quadrato',
    # cerclic/actions/social.py:48
    'Portrait': 'Verticale',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Post Instagram o Facebook, il più grande nel feed',
    # cerclic/actions/social.py:50
    'portrait': 'verticale',
    # cerclic/actions/social.py:51
    'Grille': 'Griglia',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram, con la forma esatta della griglia del profilo',
    # cerclic/actions/social.py:52
    'grille': 'griglia',
    # cerclic/actions/social.py:53
    'Story': 'Storia',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'Schermo intero del telefono: Storie, Reels, TikTok, YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'storia',
    # cerclic/actions/social.py:56
    'Paysage': 'Orizzontale',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'Schermo del computer: YouTube, presentazioni, X',
    # cerclic/actions/social.py:57
    'paysage': 'orizzontale',
    # cerclic/actions/social.py:58
    'Bannière': 'Banner',
    # cerclic/actions/social.py:58
    '1,91:1': '1,91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Link condiviso o immagine larga su Facebook, LinkedIn o X',
    # cerclic/actions/social.py:59
    'bannière': 'banner',
    # cerclic/actions/social.py:239
    'Format {name}': 'Formato {name}',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'Questa immagine misura già {size}.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'Dimensioni del video illeggibili: file danneggiato?',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'Questo video misura già {size}.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': "L'elaborazione non è riuscita: forse il file è danneggiato o in un formato insolito.",
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': 'ffmpeg non trovato: reinstalla Cerclic.',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'Video danneggiato o formato non supportato.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': "Accesso negato: forse il file è aperto in un'altra app.",
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'Taglio',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'Nessuna immagine video in questo file.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'Questo video è già ben compresso: prova una compressione più forte.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'Video troppo lungo per una GIF (più di 2 minuti: peserebbe centinaia di MB). Prima tieni un pezzo con «{action}».',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'Conversione in GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'Questo video non ha audio.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'Il pezzo da tenere è troppo corto.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': "Il pezzo scelto è l'intero file.",
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'Nessun audio in questo file.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'Anteprima non disponibile.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'Questo audio è già leggero: prova una compressione più forte.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'Questo file contiene solo audio, senza immagini: usa «{action}» per farne un MP3.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': "L'anteprima richiede troppo tempo.",
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 chiude le finestre.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': "Alt + Tab passa da una finestra all'altra.",
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': "Alt + Esc passa da una finestra all'altra.",
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Spazio apre il menu della finestra.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc apre il menu Start.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Ctrl + Alt + Canc è riservato a Windows.',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Ctrl + Maiusc + Esc apre Gestione attività.',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'Tasto {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'Spazio',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Tab': 'Tab',
    # contexte : touche Windows | cerclic/win/hotkey.py:40
    'touche Windows\x04Entrée': 'Invio',
    # contexte : touche Windows | cerclic/win/hotkey.py:41
    'touche Windows\x04Retour': 'Backspace',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Échap': 'Esc',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Inser': 'Ins',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Suppr': 'Canc',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Origine': 'Home',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Fin': 'Fine',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Page préc.': 'Pag↑',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Page suiv.': 'Pag↓',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Pause': 'Pausa',
    # contexte : touche Windows | cerclic/win/hotkey.py:46
    'touche Windows\x04Impr. écran': 'Stamp',
    # contexte : touche Windows | cerclic/win/hotkey.py:82, cerclic/win/hotkey.py:84
    'touche Windows\x04Pavé {key}': 'Tastierino {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Aggiungi un tasto dopo Ctrl, Alt, Maiusc o Win.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} è già in uso in Windows e nelle app (guida, rinomina, aggiorna, ortografia…). Aggiungi ad esempio Ctrl + Alt: Ctrl + Alt + {key}.',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': "Alt con il tastierino numerico serve a digitare caratteri (Alt + 0201 = É). Scegli un'altra combinazione.",
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'Serve Ctrl, Alt o Win nella combinazione (altrimenti questo tasto non scriverebbe più).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Maiusc',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt + un solo tasto è già in uso in molte app (i menu delle app). Aggiungi Maiusc o Ctrl, ad esempio Alt + Maiusc + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': "Questa combinazione serve a digitare caratteri (@, €, #, œ…) con AltGr. Scegline un'altra.",
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl + un solo tasto è già in uso in molte app (grassetto, copia, incolla, salva…). Aggiungi Maiusc o Alt, ad esempio Ctrl + Maiusc + {key}.',
}
