"""Cerclic, Español. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} archivo', '{n} archivos'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": 'Guardado en «{where}»: la carpeta de origen está protegida.',
    # cerclic/app.py:92
    'Téléchargements': 'Descargas',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'Windows u otra aplicación ya lo usa. Elige otro en Cerclic.',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'clic derecho y luego «Cerclic»',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": 'No se encuentra la carpeta elegida: guardado junto al original.',
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'Abrir Cerclic',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'Salir de Cerclic',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'Windows u otra aplicación ya lo usa. Elige otro en Cerclic; el clic derecho «Cerclic» sigue funcionando.',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'macOS u otra aplicación ya lo usa. Elige otro en Cerclic.',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'clic derecho, Acciones rápidas y luego «Cerclic»',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'clic derecho, «Mostrar más opciones» y luego «Cerclic»',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'Permite que Cerclic lea tu selección',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': 'Ajustes del Sistema, Privacidad y seguridad, Automatización: marca «Finder» debajo de Cerclic. El clic derecho, Acciones rápidas, «Cerclic» funciona sin esto.',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Haz clic en una imagen, un PDF, un vídeo o un audio en el Finder o en el escritorio y pulsa {combo}.',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Haz clic en una imagen, un PDF, un vídeo o un audio en el Explorador de archivos o en el escritorio y pulsa {combo}.',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'O bien: clic derecho, Acciones rápidas y luego «Cerclic».',
    # cerclic/app.py:919
    'Image copiée': 'Imagen copiada',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'Pégala donde quieras con {key} + V.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'Aceptar',
    # cerclic/app.py:1253
    'Menu complet activé': 'Menú completo activado',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'Se aplica al reiniciar el Explorador de archivos. Las ventanas de carpetas abiertas se cerrarán.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Menú de Windows 11 restaurado',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'Se aplica al reiniciar el Explorador de archivos.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'Hay dos Cerclic instalados',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'La versión de Cerclic instalada sin Microsoft Store sigue ahí. Para tener un solo «Cerclic» en el clic derecho y un solo atajo, quítala: «Mostrar el desinstalador» y luego haz doble clic en «unins000».',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": 'La versión de Cerclic instalada sin Microsoft Store sigue ahí. Para tener un solo «Cerclic», desinstálala en Aplicaciones instaladas: es el Cerclic que no tiene «Opciones avanzadas» en su menú.',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'macOS u otra aplicación ya lo usa. Elige otro en Cerclic; el clic derecho «Cerclic» sigue funcionando.',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'O bien: clic derecho, «Mostrar más opciones» y luego «Cerclic».',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'O bien: clic derecho y luego «Cerclic».',
    # cerclic/app.py:915
    'Copie impossible': 'No se ha podido copiar',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'Desbloquear',
    # cerclic/app.py:966
    'Continuer': 'Continuar',
    # cerclic/app.py:971
    '« {name} » est protégé.': '«{name}» está protegido.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'Contraseña del PDF',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'Inicio con Windows bloqueado',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': 'Tu organización no permite que las aplicaciones se abran al iniciar Windows.',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': 'Inicio con Windows desactivado en Windows',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'Se desactivó en el Administrador de tareas: solo Windows puede volver a activarlo. En Configuración, Aplicaciones, Inicio, activa «Cerclic».',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'Atajo {combo} no disponible',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Cerclic ha tenido un problema',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'Los detalles están en {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': 'Archivo inaccesible',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'Este archivo no está en una carpeta normal (archivo ZIP, móvil…). Cópialo en una carpeta y vuelve a intentarlo.',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': 'Imagen ilegible.',
    # cerclic/app.py:1224
    'Réessayer': 'Reintentar',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': 'macOS u otra aplicación ya usa {refused}. Tu atajo sigue siendo {kept}.',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': 'Windows u otra aplicación ya usa {refused}. Tu atajo sigue siendo {kept}.',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'Más tarde',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'Abrir los ajustes',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'No hay acciones para este tipo de archivo',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'Cerclic trabaja con imágenes, PDF, vídeos y audios.',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'Primero selecciona un archivo',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': 'Contraseña incorrecta para «{name}». Vuelve a intentarlo.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Recortar solo conservaría la primera. Usa «A PDF» para conservarlas todas y luego {action} en el PDF.',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['«{name}» tiene {n} página', '«{name}» tiene {n} páginas'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': '¿Dónde guardar el resultado?',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'Reiniciar el Explorador',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'Mostrar el desinstalador',
    # cerclic/app.py:602
    'Ouvrir les applications': 'Abrir las aplicaciones',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'macOS u otra aplicación ya lo usa. Tu atajo sigue siendo {kept}.',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'Windows u otra aplicación ya lo usa. Tu atajo sigue siendo {kept}.',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'Contraseña incorrecta',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'No se ha creado nada.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Comprimir solo conservaría la primera. Usa «A PDF» para conservarlas todas y luego {action} en el PDF.',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'Solo la primera se adaptaría al formato. Usa «A PDF» para conservarlas todas.',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'Abrir',
    # cerclic/app.py:707
    'Changer de raccourci': 'Cambiar de atajo',
    # cerclic/app.py:1081
    'Texte du filigrane': 'Texto de la marca de agua',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'Se escribirá en diagonal en cada página.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'CONFIDENCIAL',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'Nueva contraseña',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": 'Se pedirá para abrir el PDF. El original sigue sin contraseña.',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'Proteger',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'Error inesperado. Vuelve a intentarlo; si vuelve a pasar, los detalles están en el registro de Cerclic (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'Acceso denegado: puede que el archivo esté abierto en otra aplicación o que la carpeta esté protegida.',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'Nombre o ruta demasiado largos para Windows: ponle al archivo un nombre más corto o muévelo a una carpeta menos profunda.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'No se encuentra el archivo: puede que se haya movido o eliminado.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'Archivo demasiado pesado para la memoria disponible.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'El disco está lleno.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': 'Imagen ilegible o formato no compatible.',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF dañado o ilegible.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: se necesita al menos {n} archivo.', '{action}: se necesitan al menos {n} archivos.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'Cancelado',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '«{name}» ya no está: se ha movido, renombrado o eliminado (o se ha retirado la memoria USB).',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} archivo ya no está: se ha movido, renombrado o eliminado.', '{n} archivos ya no están: se han movido, renombrado o eliminado.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'Este PDF está protegido con contraseña.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": 'El proceso se ha detenido de golpe: probablemente el archivo esté dañado.',
    # cerclic/paths.py:235
    'compressé': 'comprimido',
    # cerclic/paths.py:235
    'redimensionné': 'redimensionado',
    # cerclic/paths.py:236
    'pivoté': 'girado',
    # cerclic/paths.py:236
    'rogné': 'recortado',
    # cerclic/paths.py:236
    'miroir': 'espejo',
    # cerclic/paths.py:237
    'anonymisé': 'anonimizado',
    # cerclic/paths.py:237
    'assemblé': 'combinado',
    # cerclic/paths.py:237
    'fusionné': 'fusionado',
    # cerclic/paths.py:238
    'réorganisé': 'reorganizado',
    # cerclic/paths.py:238
    'extrait': 'extracto',
    # cerclic/paths.py:238
    'texte': 'texto',
    # cerclic/paths.py:239
    'filigrane': 'marca de agua',
    # cerclic/paths.py:239
    'numéroté': 'numerado',
    # cerclic/paths.py:239
    'signé': 'firmado',
    # cerclic/paths.py:240
    'protégé': 'protegido',
    # cerclic/paths.py:240
    'déverrouillé': 'desbloqueado',
    # cerclic/paths.py:240
    'son': 'audio',
    # cerclic/paths.py:241
    'raccourci': 'acortado',
    # cerclic/paths.py:241
    'sans son': 'sin audio',
    # cerclic/paths.py:241
    'images': 'imágenes',
    # cerclic/paths.py:242
    'pages': 'páginas',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': 'mismo tamaño',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'De {before} a {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} byte', '{n} bytes'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '{pct} % menos',
    # cerclic/sizes.py:64
    '{pct} % de plus': '{pct} % más',
    # cerclic/system.py:17
    'Cmd': 'Cmd',
    # cerclic/system.py:17
    'Ctrl': 'Ctrl',
    # cerclic/system.py:18
    'Suppr': 'Supr',
    # cerclic/system.py:19
    'Retour': 'Retorno',
    # cerclic/system.py:19
    'Entrée': 'Intro',
    # contexte : touche Mac | cerclic/mac/hotkey.py:168
    'touche Mac\x04Touche {code}': 'Tecla {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'Cmd + Espacio abre Spotlight.',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'Opción + Cmd + Espacio abre la búsqueda del Finder.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'Ctrl + Espacio cambia el idioma del teclado.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'Ctrl + Opción + Espacio cambia el idioma del teclado.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'Ctrl + Cmd + Espacio abre los emojis.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'Cmd + Tab cambia de una aplicación a otra.',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'Mayús + Cmd + Tab cambia de una aplicación a otra.',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'Opción + Cmd + Esc fuerza la salida de una aplicación.',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Mayús + Cmd + 3 hace una captura de pantalla.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Mayús + Cmd + 4 hace una captura de pantalla.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Mayús + Cmd + 5 abre la herramienta de captura de pantalla.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'Mayús + Cmd + 6 hace una captura de la Touch Bar.',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'Ctrl + Cmd + Q bloquea la pantalla.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Mayús + Cmd + Q cierra la sesión.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'Ctrl + Cmd + F activa la pantalla completa.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'Opción + Cmd + D oculta el Dock.',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'Opción + Cmd + C copia la ruta de un archivo en el Finder.',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'Opción + Cmd + H oculta las demás aplicaciones.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'Opción + Cmd + M minimiza todas las ventanas.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'Opción + Cmd + W cierra todas las ventanas.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'Opción + Cmd + V mueve un archivo copiado en el Finder.',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Espacio',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'Retorno',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'Intro',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'Tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': 'Supr',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Échap': 'Esc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Début': 'Inicio',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Fin': 'Fin',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page préc.': 'Re Pág',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page suiv.': 'Av Pág',
    # contexte : touche Mac | cerclic/mac/hotkey.py:73
    'touche Mac\x04Aide': 'Ayuda',
    # contexte : touche Mac | cerclic/mac/hotkey.py:156, cerclic/mac/hotkey.py:163
    'touche Mac\x04Pavé {key}': 'Teclado num. {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'Añade una tecla después de Cmd, Ctrl, Opción o Mayús.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} ya es un atajo de macOS (Ajustes del Sistema, Teclado, Funciones rápidas de teclado). Elige otro.',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'Mayús + Cmd + {key} ya se usa en el Finder. Elige otra letra o Mayús + Cmd + Espacio.',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": 'La combinación necesita Cmd o Ctrl: macOS rechaza los atajos hechos solo con Opción o Mayús.',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Cmd + una sola tecla ya se usa en todas las aplicaciones (copiar, pegar, guardar…). Añade Mayús, Opción o Ctrl, por ejemplo Mayús + Cmd + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'Ctrl + las flechas cambian de un escritorio a otro (Mission Control).',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Ctrl',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Opción',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Mayús',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Cmd',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'Cancelar',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'Mostrar la contraseña',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'Ocultar la contraseña',
    # cerclic/ui/cards.py:238
    'Fermer': 'Cerrar',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'Escritorio',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'Descargas',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'Imágenes',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'Vídeos',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'Películas',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'Música',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'Documentos',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'Detener',
    # cerclic/ui/cards.py:299
    'En cours': 'En curso',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'Deteniendo…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['Archivo eliminado', 'Archivos eliminados'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": 'Tu archivo original sigue intacto.',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} archivo creado', '{n} archivos creados'],
    # cerclic/ui/cards.py:366
    'Dossier': 'Carpeta',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'Eliminar',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'Elimina lo que Cerclic acaba de crear (tu archivo original no se toca)',
    # cerclic/ui/cards.py:417
    'Suppression impossible': 'No se ha podido eliminar',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'Seguramente el archivo está abierto en otra aplicación: ciérrala y vuelve a intentarlo.',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent} %',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': 'En\xa0«{folder}»',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} archivo omitido, por ejemplo: {example}', '{n} archivos omitidos, por ejemplo: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'Detenido: no se ha creado nada.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '{size} en total · en\xa0«{folder}»',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · en\xa0«{folder}»',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title} imposible',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'Error desconocido.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'Ligera',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'Media',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'Fuerte',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'Máxima',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent} % · {n} color', '{percent} % · {n} colores'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': 'Imágenes a 220 ppp: muy nítidas, incluso impresas',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": 'Imágenes a 150 ppp: nítidas en pantalla y al imprimir',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": 'Imágenes a 110 ppp: para la pantalla',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': 'Imágenes a 80 ppp: lo más ligero, imágenes menos nítidas',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": 'Hasta 1080p, muy buena calidad',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": 'Hasta 1080p, buena calidad',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p: para un móvil o un mensaje',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p: lo más ligero',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbit/s: música, muy buena calidad',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbit/s: música',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbit/s: voz, y música en un móvil',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbit/s: voz',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent} % · sin pérdida',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'Cargando…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': 'en lugar de {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'Sin ahorro',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'sin ahorro',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'Imposible',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'imposible',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'calculando…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'Elige la calidad · {key} para comprimir',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': 'Elige la intensidad · {key} para comprimir',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'Comprimir',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'Calidad',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'Compresión',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'Pasa el puntero por la imagen: detalle al 100 %',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'Pasa el puntero por la imagen: detalle',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: sin ajustes',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['Vista previa: {name} · total para {n} imagen, estimado con {sampled}', 'Vista previa: {name} · total para {n} imágenes, estimado con {sampled}'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['Vista previa: {name} · total para {n} imagen', 'Vista previa: {name} · total para {n} imágenes'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'No pesa menos',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'No se ha podido comprimir.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} omitida', '{n} omitidas'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'Prueba una compresión más fuerte.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'Original: {size} · baja la calidad',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'Original: {size} · comprime más',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'Libre',
    # cerclic/ui/crop_editor.py:27
    'Original': 'Original',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'Arrastra las esquinas · {key} para recortar',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'Recortar',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'Todas las páginas',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'Imagen completa',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": 'Volver a toda la imagen',
    # cerclic/ui/crop_editor.py:589
    '{width} × {height} cm': '{width} × {height} cm',
    # cerclic/ui/crop_editor.py:593, cerclic/ui/crop_editor.py:448, cerclic/ui/social_editor.py:43
    '{width} × {height} px': '{width} × {height} px',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:103
    'touche du Mac\x04Retour': 'Retorno',
    # contexte : touche | cerclic/ui/editor_base.py:103
    'touche\x04Entrée': 'Intro',
    # contexte : touche | cerclic/ui/editor_base.py:108
    'touche\x04Suppr': 'Supr',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:113
    'touche du Mac\x04Cmd': 'Cmd',
    # contexte : touche | cerclic/ui/editor_base.py:113
    'touche\x04Ctrl': 'Ctrl',
    # cerclic/ui/editor_base.py:205
    'Fermer (Échap)': 'Cerrar (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'Arrastra para ordenar · {key} para quitar',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'Girar a la izquierda',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'Girar a la derecha ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': 'Hacia el principio ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'Hacia el final ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'Extraer la selección',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'Un PDF nuevo solo con las páginas elegidas',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'Restablecer',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'Guardar',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{n} seleccionada de {count}', '{n} seleccionadas de {count}'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} página', '{n} páginas'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'Más',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ Atrás',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'Otras herramientas',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'General',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'Atajo de teclado',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'Clic derecho',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'Archivos creados',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'Firma',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'Acerca de',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'Versión {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Selecciona uno o varios archivos en el Explorador de archivos o en el escritorio y pulsa {combo}.',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'Modificar',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'Por defecto',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'Pulsa tu combinación…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'Comprobando…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'Versión {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Selecciona uno o varios archivos en el Finder o en el escritorio y pulsa {combo}.',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'Abrir la rueda',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'Clic derecho en el archivo, Acciones rápidas y luego «Cerclic». O bien: Abrir con y luego Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'Inicio',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'Detiene Cerclic. Para volver a iniciarlo, ábrelo desde la carpeta Aplicaciones.',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'Idioma',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": 'Automático (idioma del ordenador)',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'Desinstalar Cerclic',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": '¿Quitar Cerclic del clic derecho y del inicio de sesión y después cerrarlo?',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'Desinstalar',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'Una combinación de teclas abre la rueda con los archivos seleccionados.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'Abrir la rueda con el teclado',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '«Cerclic» en el menú del clic derecho de tus archivos.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '«Cerclic» en el clic derecho',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'Tu archivo original nunca se modifica: cada acción crea un archivo nuevo.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'Dónde guardarlos',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'Junto al archivo original',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'En la misma carpeta, por ejemplo en el escritorio si la foto está allí. Recomendado.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'En una carpeta que yo elija',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'Todos los archivos creados en el mismo sitio.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'Preguntarme cada vez',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'Cerclic te pregunta la carpeta antes de crear el archivo.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'Elegir…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'Carpeta de los archivos creados',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'Para firmar tus PDF con un solo gesto. Se queda en este ordenador.',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'Dibujar…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'Importar una foto…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'Borrar',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'El punto justo entre el peso de los archivos y su nitidez.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value} %',
    # cerclic/ui/settings_window.py:993
    'Voir': 'Ver',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'Elegir una foto de tu firma',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'Atajo sin cambios.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'Ejemplos: Mayús + Cmd + Espacio, Ctrl + Opción + X. Esc para cancelar.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'Ejemplos: Ctrl + Alt + Espacio, Ctrl + Mayús + X, Win + Mayús + C. Esc para cancelar.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'Más ligero',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'Más nítido',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'Te damos la bienvenida a Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'Los cambios se aplican al momento.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'Dos formas de abrir la rueda, el inicio y el idioma.',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'Tres formas de abrir la rueda, el inicio y el idioma.',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'Con el teclado',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Mayús + clic derecho en el archivo y luego «Cerclic». Sin Mayús, pasa por «Mostrar más opciones».',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'Clic derecho en el archivo y luego «Cerclic».',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'Con el ratón',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'Abrir Cerclic al iniciar el Mac',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'Iniciar Cerclic con Windows',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'Recomendado: la rueda está lista en cuanto la necesitas.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'Detiene Cerclic. Para volver a iniciarlo, ábrelo desde el menú Inicio.',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'Detiene Cerclic. Para volver a iniciarlo, ábrelo desde el escritorio o el menú Inicio.',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'Detener Cerclic',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": 'La rueda no se abrirá hasta la próxima vez que lo inicies.',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'El de los menús, las ventanas y los mensajes de Cerclic.',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": '«Modificar» y luego pulsa tu combinación. Si macOS u otra aplicación ya la usa, Cerclic te lo dice y conserva la anterior.',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': '¿Tienes un ratón con botones programables? Asigna a un botón una tecla de F13 a F20 y elígela aquí: un clic en ese botón abrirá la rueda.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": '«Modificar» y luego pulsa tu combinación. Si Windows u otra aplicación ya la usa, Cerclic te lo dice y conserva la anterior.',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': '¿Tienes un ratón con botones programables? Asigna a un botón una tecla de F13 a F24 y elígela aquí: un clic en ese botón abrirá la rueda.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'Permiso',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'Ajustes…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'Menú completo del clic derecho',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': '¿No aparece en Acciones rápidas? Clic derecho en un archivo, Acciones rápidas, luego Personalizar, y marca «Cerclic». También está siempre en Abrir con.',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'Compresión de las imágenes',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': 'Ajuste que propone «Comprimir», que muestra el tamaño resultante y recuerda tu última elección.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'JPG creados por las demás acciones',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': 'Recortar, girar, convertir… Al 90 %, la pérdida no se nota.',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'Recortar, firmar, comprimir, convertir, adaptar al formato de las redes sociales… con un solo gesto, sin abrir otra aplicación.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'Registro',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'Si hay algún problema, este archivo ayuda a entender qué ha pasado.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'Licencias',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'Los componentes libres que usa Cerclic y sus licencias.',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'Desinstalar…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'Todavía no hay ninguna firma: dibújala o importa una foto. Si no, se te pedirá la primera vez que firmes.',
    # cerclic/ui/settings_window.py:1130
    'Images': 'Imágenes',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'Ajustar: con el teclado',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'Ajustar: con el ratón',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'Arrastrando',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'Abrir Cerclic al iniciar sesión',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'Con los archivos seleccionados en el Finder o en el escritorio.',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'Con los archivos seleccionados en el Explorador de archivos o en el escritorio.',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Leer la selección del Finder',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': 'La primera vez, macOS pregunta si Cerclic puede controlar el Finder: acepta. Cerclic solo lee ahí los archivos seleccionados.',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '«Cerclic» en el clic derecho del Finder',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'En el menú Acciones rápidas de tus archivos, en el Finder y en el escritorio.',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": 'Muestra el menú completo sin pasar por «Mostrar más opciones». Cerclic te propondrá reiniciar el Explorador de archivos.',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'Truco: sin cambiar nada, Mayús + clic derecho en un archivo abre directamente el menú completo, con «Cerclic».',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'No has elegido ninguna carpeta.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": 'Quita «Cerclic» del clic derecho y del inicio de sesión, y después se cierra. Solo quedará mover Cerclic.app a la Papelera.',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'Atajo desactivado: el clic derecho «Cerclic» sigue disponible.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'Atajo desactivado.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic ya funciona en segundo plano: su icono está en la barra de menús, en la parte superior de la pantalla. Elige abajo tu forma preferida de abrir la rueda.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic ya funciona en segundo plano: su icono está junto al reloj (a veces oculto tras la pequeña flecha ^). Elige abajo tu forma preferida de abrir la rueda.',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": 'Arrastra archivos al icono de Cerclic (en Aplicaciones o en el Dock).',
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": 'Arrastra archivos al icono de Cerclic.',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '«Cerclic» en el clic derecho de los archivos',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'Arriba del todo en el menú de imágenes, PDF, vídeos y audios, en el Explorador de archivos y en el escritorio.',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'En imágenes, PDF, vídeos y audios, en el Explorador de archivos, en el escritorio y en las ventanas Abrir y Guardar.',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'Su nombre: el nombre original más lo que ha cambiado, por ejemplo foto (comprimido).jpg junto a foto.jpg. Si ese nombre ya existe, Cerclic añade un número: nunca se sobrescribe nada.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": '¿No te gusta un resultado? «Eliminar» en su tarjeta lo borra al instante.',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'Carpeta elegida: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'Carpeta elegida: ninguna por ahora.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": 'Basta con una foto de tu firma sobre papel blanco: Cerclic hace transparente el papel y conserva la tinta.',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': 'Para firmar: clic derecho o atajo en un PDF y luego «Firmar». Coloca la firma y pulsa {key}.',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': '¿Lo rechazaste por error? En Automatización, marca «Finder» debajo de Cerclic.',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ Activo en todo el Mac.',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ Activo en todo Windows.',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'macOS u otra aplicación ya usa esta combinación. Elige otra con «Modificar».',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'Windows u otra aplicación ya usa esta combinación. Elige otra con «Modificar».',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'No se ha encontrado ningún trazo de firma en esta imagen.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'Tu firma',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'Se guarda para las próximas veces',
    # cerclic/ui/signature.py:200
    'Importer…': 'Importar…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'Una foto de tu firma sobre papel blanco',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'Arrastra la firma · tira de una esquina · {key} para firmar',
    # cerclic/ui/signature.py:413
    'Changer': 'Cambiar',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': 'Dibujar o importar otra firma',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'Firmar',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'Página {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'Firma aquí',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': 'Elegir una imagen de tu firma',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'Imágenes ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'Rellenar',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": 'La imagen cubre todo el marco y lo que sobra se recorta.\nArrástrala para elegir la parte que se conserva; rueda del ratón para hacer zoom.',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'Fondo borroso',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": 'Toda la imagen, sin recortar nada.\nAlrededor: la misma imagen, desenfocada.',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'Fondo blanco',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": 'Toda la imagen, sin recortar nada.\nAlrededor: blanco.',
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'Fondo negro',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": 'Toda la imagen, sin recortar nada.\nAlrededor: negro.',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'Archivo anterior',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'Archivo siguiente',
    # cerclic/ui/social_editor.py:448
    'Créer': 'Crear',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'Arrastra y haz zoom · {key} para crear',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'No se recorta nada · {key} para crear',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': 'La parte conservada es más pequeña que el formato: al ampliarla, quedará algo menos nítida.',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'El vídeo es más pequeño que el formato: al ampliarlo, quedará algo menos nítido.',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": 'La imagen es más pequeña que el formato: al ampliarla, quedará algo menos nítida.',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'Duración desconocida',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'Arrastra los tiradores · {key} para acortar',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'Acortar',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'Duración {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': 'Duración ilegible: ¿archivo dañado?',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'Inicio {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'Fin {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['«{name}» tiene {n} página: solo se conservaría la primera. Usa «{action}» para conservarlas todas.', '«{name}» tiene {n} páginas: solo se conservaría la primera. Usa «{action}» para conservarlas todas.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'Ya es un {format}.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'Esta imagen ya está bien comprimida.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'La zona que recortar está vacía.',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": 'El marco cubre toda la imagen: no hay nada que recortar.',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'Se necesitan al menos dos imágenes.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'Combinación',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'Esta imagen no contiene ninguna información privada.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'Imagen {i} de {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'A PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": 'La imagen ya mide {size} px o menos.',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': 'Imagen ilegible: {name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '«{name}» está protegido con contraseña.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'Contraseña incorrecta.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'Conversión a Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'Este archivo no es un PDF: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'No hay ninguna imagen.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'Se necesitan al menos dos PDF para fusionar.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'No hay ninguna página que conservar.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": 'No hay texto en este PDF: seguramente es un escaneo (una imagen).',
    # cerclic/actions/pdf.py:570
    'Vérification': 'Comprobación',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'Este PDF ya está bien comprimido.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'El marco cubre toda la página: no hay nada que recortar.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': 'El texto de la marca de agua está vacío.',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'No hay ninguna firma guardada.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'La contraseña está vacía.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": 'Este PDF ya tiene contraseña. Para poner otra, quita primero esta ({more} y luego {action}).',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'Este PDF no está protegido.',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF dañado o ilegible: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'Página {i} de {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i} de {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'Este PDF solo tiene una página.',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'No se encuentra la página en este PDF.',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'Las páginas no han cambiado.',
    # cerclic/actions/registry.py:34
    'Image': 'Imagen',
    # cerclic/actions/registry.py:36
    'Vidéo': 'Vídeo',
    # cerclic/actions/registry.py:37
    'Son': 'Audio',
    # cerclic/actions/registry.py:136
    'Droite': 'Derecha',
    # cerclic/actions/registry.py:137
    'Gauche': 'Izquierda',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'Redes',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'Girar',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'Redimensionar',
    # cerclic/actions/registry.py:213
    'Convertir': 'Convertir',
    # cerclic/actions/registry.py:223
    'Copier': 'Copiar',
    # cerclic/actions/registry.py:226
    'Assembler': 'Combinar',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'Anonimizar',
    # cerclic/actions/registry.py:256
    'Fusionner': 'Fusionar',
    # cerclic/actions/registry.py:260
    'Pages': 'Páginas',
    # cerclic/actions/registry.py:266
    'En Word': 'A Word',
    # cerclic/actions/registry.py:270
    'En images': 'A imágenes',
    # cerclic/actions/registry.py:276
    'Diviser': 'Dividir',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': 'Marca de agua',
    # cerclic/actions/registry.py:290
    'Numéroter': 'Numerar',
    # cerclic/actions/registry.py:295
    'En texte': 'A texto',
    # cerclic/actions/registry.py:326
    'En MP4': 'A MP4',
    # cerclic/actions/registry.py:329
    'En GIF': 'A GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'Extraer audio',
    # cerclic/actions/registry.py:336
    'Couper le son': 'Silenciar',
    # cerclic/actions/registry.py:352
    'En MP3': 'A MP3',
    # cerclic/actions/registry.py:141
    'Miroir': 'Espejo',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'Conservar una parte',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'Recorte',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta, historias, móvil, PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'Formato para redes sociales',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'Girar o voltear',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'Rotación',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'Menos píxeles',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'Redimensionamiento',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'Más ligero, mismo tamaño',
    # cerclic/actions/registry.py:216
    'Changer de format': 'Cambiar de formato',
    # cerclic/actions/registry.py:216
    'Conversion': 'Conversión',
    # cerclic/actions/registry.py:222
    'Une page par image': 'Una página por imagen',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'Creación del PDF',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'Para pegar donde quieras',
    # cerclic/actions/registry.py:225
    'Copie': 'Copia',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'Varias en una',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'Quita GPS, cámara, fecha',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'Anonimización',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'Colocar tu firma',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'Quitar los márgenes',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'Más ligero para enviar',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'Un solo PDF',
    # cerclic/actions/registry.py:259
    'Fusion': 'Fusión',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'Ordenar, girar, eliminar',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'Organización de páginas',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'Editable en Word',
    # cerclic/actions/registry.py:273
    'Une image par page': 'Una imagen por página',
    # cerclic/actions/registry.py:273
    'Conversion en images': 'Conversión a imágenes',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'Un PDF por página',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'División en páginas',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'Un texto en diagonal',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'Números al pie de página',
    # cerclic/actions/registry.py:294
    'Numérotation': 'Numeración',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'El texto en .txt',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'Extracción del texto',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'Con una contraseña',
    # cerclic/actions/registry.py:304
    'Protection': 'Protección',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'Quitar la contraseña',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'Desbloqueo',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'Conservar un fragmento',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'Corte',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels, TikTok, Shorts, PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'Más ligero, en MP4',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'Compatible con todo',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'Conversión a MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': 'Una animación sin sonido',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'Creación del GIF',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'El audio en MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': 'Extracción del audio',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'El vídeo sin sonido',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': 'Supresión del audio',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'Enderezar el vídeo',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'Conversión a MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'Más ligero, en MP3',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'Archivo {i} de {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '«{name}»: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '50 %',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'Lado a lado',
    # cerclic/actions/registry.py:231
    'En colonne': 'En columna',
    # cerclic/actions/registry.py:232
    'En grille': 'En cuadrícula',
    # cerclic/actions/social.py:46
    'Carré': 'Cuadrado',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Publicación de Instagram, Facebook o LinkedIn',
    # cerclic/actions/social.py:47
    'carré': 'cuadrado',
    # cerclic/actions/social.py:48
    'Portrait': 'Vertical',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Publicación de Instagram o Facebook, la más grande del feed',
    # cerclic/actions/social.py:50
    'portrait': 'vertical',
    # cerclic/actions/social.py:51
    'Grille': 'Cuadrícula',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram, con la forma exacta de la cuadrícula del perfil',
    # cerclic/actions/social.py:52
    'grille': 'cuadrícula',
    # cerclic/actions/social.py:53
    'Story': 'Historia',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'Pantalla completa del móvil: historias, Reels, TikTok, YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'historia',
    # cerclic/actions/social.py:56
    'Paysage': 'Horizontal',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'Pantalla de ordenador: YouTube, presentación, X',
    # cerclic/actions/social.py:57
    'paysage': 'horizontal',
    # cerclic/actions/social.py:58
    'Bannière': 'Banner',
    # cerclic/actions/social.py:58
    '1,91:1': '1,91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Enlace compartido o imagen ancha en Facebook, LinkedIn o X',
    # cerclic/actions/social.py:59
    'bannière': 'banner',
    # cerclic/actions/social.py:239
    'Format {name}': 'Formato {name}',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'Esta imagen ya mide {size}.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'Tamaño del vídeo ilegible: ¿archivo dañado?',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'Este vídeo ya mide {size}.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': 'El proceso ha fallado: puede que el archivo esté dañado o en un formato poco habitual.',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': 'No se encuentra ffmpeg: vuelve a instalar Cerclic.',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'Vídeo dañado o formato no compatible.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'Acceso denegado: puede que el archivo esté abierto en otra aplicación.',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'Corte',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'No hay imagen de vídeo en este archivo.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'Este vídeo ya está bien comprimido: prueba una compresión más fuerte.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'Vídeo demasiado largo para un GIF (más de 2 minutos: pesaría cientos de MB). Conserva primero un fragmento con «{action}».',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'Conversión a GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'Este vídeo no tiene sonido.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'El fragmento que conservar es demasiado corto.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': 'El fragmento elegido es el archivo entero.',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'No hay audio en este archivo.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'No se puede mostrar la vista previa.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'Este audio ya es ligero: prueba una compresión más fuerte.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'Este archivo solo contiene audio, sin imagen: usa «{action}» para convertirlo en MP3.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'La vista previa tarda demasiado en prepararse.',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 cierra las ventanas.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab cambia de ventana.',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc cambia de ventana.',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Espacio abre el menú de la ventana.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc abre el menú Inicio.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Ctrl + Alt + Supr está reservado para Windows.',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Ctrl + Mayús + Esc abre el Administrador de tareas.',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'Tecla {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'Espacio',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Tab': 'Tab',
    # contexte : touche Windows | cerclic/win/hotkey.py:40
    'touche Windows\x04Entrée': 'Intro',
    # contexte : touche Windows | cerclic/win/hotkey.py:41
    'touche Windows\x04Retour': 'Retroceso',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Échap': 'Esc',
    # contexte : touche Windows | cerclic/win/hotkey.py:42
    'touche Windows\x04Inser': 'Insert',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Suppr': 'Supr',
    # contexte : touche Windows | cerclic/win/hotkey.py:43
    'touche Windows\x04Origine': 'Inicio',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Fin': 'Fin',
    # contexte : touche Windows | cerclic/win/hotkey.py:44
    'touche Windows\x04Page préc.': 'Re Pág',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Page suiv.': 'Av Pág',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Pause': 'Pausa',
    # contexte : touche Windows | cerclic/win/hotkey.py:46
    'touche Windows\x04Impr. écran': 'Impr Pant',
    # contexte : touche Windows | cerclic/win/hotkey.py:82, cerclic/win/hotkey.py:84
    'touche Windows\x04Pavé {key}': 'Teclado num. {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Añade una tecla después de Ctrl, Alt, Mayús o Win.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} ya se usa en Windows y en las aplicaciones (ayuda, cambiar nombre, actualizar, ortografía…). Añade, por ejemplo, Ctrl + Alt: Ctrl + Alt + {key}.',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt con el teclado numérico sirve para escribir caracteres (Alt + 0201 = É). Elige otra combinación.',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'La combinación necesita Ctrl, Alt o Win (si no, esta tecla ya no escribiría).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Mayús',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt + una sola tecla ya se usa en muchas aplicaciones (sus menús). Añade Mayús o Ctrl, por ejemplo Alt + Mayús + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'Esta combinación sirve para escribir caracteres (@, €, #, [ ]…) con AltGr. Elige otra.',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl + una sola tecla ya se usa en muchas aplicaciones (negrita, copiar, pegar, guardar…). Añade Mayús o Alt, por ejemplo Ctrl + Mayús + {key}.',
    # cerclic/ui/settings_window.py (À propos)
    'Code source': 'Código fuente',
    'Tout le code de Cerclic est public, sur GitHub.': 'Todo el código de Cerclic es público, en GitHub.',
}
