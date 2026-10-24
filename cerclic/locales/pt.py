"""Cerclic, Português. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} arquivo', '{n} arquivos'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": 'Salvo em “{where}”: a pasta original está protegida.',
    # cerclic/app.py:92
    'Téléchargements': 'Downloads',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'O Windows ou outro aplicativo já usa esse atalho. Escolha outro no Cerclic.',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'clique com o botão direito e escolha “Cerclic”',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": 'A pasta escolhida não foi encontrada: salvo ao lado do original.',
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'Abrir o Cerclic',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'Encerrar o Cerclic',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'O Windows ou outro aplicativo já usa esse atalho. Escolha outro no Cerclic; o “Cerclic” no menu do botão direito continua funcionando.',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'O macOS ou outro aplicativo já usa esse atalho. Escolha outro no Cerclic.',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'clique com o botão direito, Ações Rápidas e depois “Cerclic”',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'clique com o botão direito, “Mostrar mais opções” e depois “Cerclic”',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'Permita que o Cerclic leia sua seleção',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': 'Ajustes do Sistema, Privacidade e Segurança, Automação: marque “Finder” abaixo de Cerclic. O clique com o botão direito, Ações Rápidas, “Cerclic” funciona sem isso.',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Clique em uma imagem, um PDF, um vídeo ou um áudio no Finder ou na Mesa e pressione {combo}.',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Clique em uma imagem, um PDF, um vídeo ou um áudio no Explorador de Arquivos ou na Área de Trabalho e pressione {combo}.',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'Ou: clique com o botão direito, Ações Rápidas e depois “Cerclic”.',
    # cerclic/app.py:919
    'Image copiée': 'Imagem copiada',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'Cole onde quiser com {key} + V.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'OK',
    # cerclic/app.py:1253
    'Menu complet activé': 'Menu completo ativado',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'Ele passa a valer quando o Explorador de Arquivos reiniciar. As janelas de pastas abertas serão fechadas.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Menu do Windows 11 restaurado',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'Ele passa a valer quando o Explorador de Arquivos reiniciar.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'Dois Cerclic instalados',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'A versão do Cerclic instalada sem a Microsoft Store ainda está aqui. Para ter só um “Cerclic” no menu do botão direito e um só atalho, remova-a: “Mostrar o desinstalador” e depois clique duas vezes em “unins000”.',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": 'A versão do Cerclic instalada sem a Microsoft Store ainda está aqui. Para ter só um “Cerclic”, desinstale-a em Aplicativos instalados: é o Cerclic que não tem “Opções avançadas” no menu.',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'O macOS ou outro aplicativo já usa esse atalho. Escolha outro no Cerclic; o “Cerclic” no menu do botão direito continua funcionando.',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'Ou: clique com o botão direito, “Mostrar mais opções” e depois “Cerclic”.',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'Ou: clique com o botão direito e escolha “Cerclic”.',
    # cerclic/app.py:915
    'Copie impossible': 'Não foi possível copiar',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'Desbloquear',
    # cerclic/app.py:966
    'Continuer': 'Continuar',
    # cerclic/app.py:971
    '« {name} » est protégé.': '“{name}” está protegido.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'Senha do PDF',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'Inicialização com o Windows bloqueada',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': 'Sua organização não permite que aplicativos sejam iniciados com o Windows.',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': 'Inicialização com o Windows desativada no Windows',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'Ela foi desativada no Gerenciador de Tarefas: só o Windows pode reativá-la. Em Configurações, Aplicativos, Inicialização, ative “Cerclic”.',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'Atalho {combo} indisponível',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'O Cerclic encontrou um problema',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'Os detalhes estão em {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': 'Arquivo inacessível',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'Este arquivo não está em uma pasta comum (arquivo ZIP, celular…). Copie-o para uma pasta e tente de novo.',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': 'Imagem ilegível.',
    # cerclic/app.py:1224
    'Réessayer': 'Tentar de novo',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': '{refused} já é usado pelo macOS ou por outro aplicativo. Seu atalho continua sendo {kept}.',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': '{refused} já é usado pelo Windows ou por outro aplicativo. Seu atalho continua sendo {kept}.',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'Mais tarde',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'Abrir os Ajustes',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'Nenhuma ação para este tipo de arquivo',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'O Cerclic trabalha com imagens, PDFs, vídeos e áudios.',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'Selecione um arquivo primeiro',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': 'Senha incorreta para “{name}”. Tente de novo.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Recortar manteria só a primeira. Use “Para PDF” para manter todas e depois {action} no PDF.',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['“{name}” tem {n} página', '“{name}” tem {n} páginas'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': 'Onde salvar o resultado?',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'Reiniciar o Explorador de Arquivos',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'Mostrar o desinstalador',
    # cerclic/app.py:602
    'Ouvrir les applications': 'Abrir Aplicativos instalados',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'O macOS ou outro aplicativo já usa essa combinação. Seu atalho continua sendo {kept}.',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'O Windows ou outro aplicativo já usa essa combinação. Seu atalho continua sendo {kept}.',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'Senha incorreta',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'Nada foi criado.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'Comprimir manteria só a primeira. Use “Para PDF” para manter todas e depois {action} no PDF.',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'Só a primeira seria ajustada ao formato. Use “Para PDF” para manter todas.',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'Abrir',
    # cerclic/app.py:707
    'Changer de raccourci': 'Mudar o atalho',
    # cerclic/app.py:1081
    'Texte du filigrane': "Texto da marca d'água",
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'Ele será escrito na diagonal em cada página.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'CONFIDENCIAL',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'Senha a definir',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": 'Ela será pedida para abrir o PDF. O original continua sem senha.',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'Proteger',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'Erro inesperado. Tente de novo; se acontecer outra vez, os detalhes estão no registro do Cerclic (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'Acesso negado: talvez o arquivo esteja aberto em outro aplicativo, ou a pasta está protegida.',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'Nome ou caminho longo demais para o Windows: dê um nome mais curto ao arquivo ou mova-o para uma pasta menos profunda.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'Arquivo não encontrado: talvez tenha sido movido ou excluído.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'Arquivo grande demais para a memória disponível.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'O disco está cheio.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': 'Imagem ilegível ou formato não compatível.',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF danificado ou ilegível.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: é necessário pelo menos {n} arquivo.', '{action}: são necessários pelo menos {n} arquivos.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'Cancelado',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '“{name}” não está mais aqui: foi movido, renomeado ou excluído (ou o pen drive foi removido).',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} arquivo não está mais aqui: foi movido, renomeado ou excluído.', '{n} arquivos não estão mais aqui: foram movidos, renomeados ou excluídos.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'Este PDF está protegido por senha.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": 'O processamento parou de repente: o arquivo provavelmente está danificado.',
    # cerclic/paths.py:235
    'compressé': 'comprimido',
    # cerclic/paths.py:235
    'redimensionné': 'redimensionado',
    # cerclic/paths.py:236
    'pivoté': 'girado',
    # cerclic/paths.py:236
    'rogné': 'recortado',
    # cerclic/paths.py:236
    'miroir': 'espelhado',
    # cerclic/paths.py:237
    'anonymisé': 'anonimizado',
    # cerclic/paths.py:237
    'assemblé': 'combinado',
    # cerclic/paths.py:237
    'fusionné': 'mesclado',
    # cerclic/paths.py:238
    'réorganisé': 'reorganizado',
    # cerclic/paths.py:238
    'extrait': 'extraído',
    # cerclic/paths.py:238
    'texte': 'texto',
    # cerclic/paths.py:239
    'filigrane': "marca d'água",
    # cerclic/paths.py:239
    'numéroté': 'numerado',
    # cerclic/paths.py:239
    'signé': 'assinado',
    # cerclic/paths.py:240
    'protégé': 'protegido',
    # cerclic/paths.py:240
    'déverrouillé': 'desbloqueado',
    # cerclic/paths.py:240
    'son': 'áudio',
    # cerclic/paths.py:241
    'raccourci': 'aparado',
    # cerclic/paths.py:241
    'sans son': 'sem som',
    # cerclic/paths.py:241
    'images': 'imagens',
    # cerclic/paths.py:242
    'pages': 'páginas',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': 'mesmo tamanho',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'De {before} para {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} byte', '{n} bytes'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '{pct}% a menos',
    # cerclic/sizes.py:64
    '{pct} % de plus': '{pct}% a mais',
    # cerclic/system.py:17
    'Cmd': 'Cmd',
    # cerclic/system.py:17
    'Ctrl': 'Ctrl',
    # cerclic/system.py:18
    'Suppr': 'Delete',
    # cerclic/system.py:19
    'Retour': 'Return',
    # cerclic/system.py:19
    'Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:168
    'touche Mac\x04Touche {code}': 'Tecla {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'Cmd + Espaço abre o Spotlight.',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'Option + Cmd + Espaço abre a busca do Finder.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'Ctrl + Espaço muda o idioma do teclado.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'Ctrl + Option + Espaço muda o idioma do teclado.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'Ctrl + Cmd + Espaço abre os emojis.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'Cmd + Tab alterna entre os aplicativos.',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'Shift + Cmd + Tab alterna entre os aplicativos.',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'Option + Cmd + Esc força o encerramento de um aplicativo.',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Shift + Cmd + 3 faz uma captura de tela.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Shift + Cmd + 4 faz uma captura de tela.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Shift + Cmd + 5 abre a ferramenta de captura de tela.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'Shift + Cmd + 6 faz uma captura da Touch Bar.',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'Ctrl + Cmd + Q bloqueia a tela.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Shift + Cmd + Q encerra a sessão.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'Ctrl + Cmd + F ativa a tela cheia.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'Option + Cmd + D oculta o Dock.',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'Option + Cmd + C copia o caminho de um arquivo no Finder.',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'Option + Cmd + H oculta os outros aplicativos.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'Option + Cmd + M minimiza todas as janelas.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'Option + Cmd + W fecha todas as janelas.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'Option + Cmd + V move um arquivo copiado no Finder.',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Espaço',
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
    'touche Mac\x04Pavé {key}': 'Num {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'Adicione uma tecla depois de Cmd, Ctrl, Option ou Shift.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} já é um atalho do macOS (Ajustes do Sistema, Teclado, Atalhos de Teclado). Escolha outro.',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'Shift + Cmd + {key} já é usado no Finder. Escolha outra letra, ou Shift + Cmd + Espaço.',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": 'A combinação precisa ter Cmd ou Ctrl: o macOS não aceita atalhos feitos só com Option ou Shift.',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Cmd + uma única tecla já é usado em todos os aplicativos (copiar, colar, salvar…). Adicione Shift, Option ou Ctrl, por exemplo Shift + Cmd + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'Ctrl + as setas passam de uma mesa para outra (Mission Control).',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Ctrl',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Shift',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Cmd',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'Cancelar',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'Mostrar a senha',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'Ocultar a senha',
    # cerclic/ui/cards.py:238
    'Fermer': 'Fechar',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'Área de Trabalho',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'Downloads',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'Imagens',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'Vídeos',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'Filmes',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'Músicas',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'Documentos',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'Parar',
    # cerclic/ui/cards.py:299
    'En cours': 'Em andamento',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'Parando…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['Arquivo excluído', 'Arquivos excluídos'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": 'Seu arquivo original continua no lugar.',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} arquivo criado', '{n} arquivos criados'],
    # cerclic/ui/cards.py:366
    'Dossier': 'Pasta',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'Excluir',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'Exclui o que o Cerclic acabou de criar (seu arquivo original continua no lugar)',
    # cerclic/ui/cards.py:417
    'Suppression impossible': 'Não foi possível excluir',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'O arquivo provavelmente está aberto em outro aplicativo: feche-o e tente de novo.',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': 'Em\xa0“{folder}”',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} arquivo deixado de lado, por exemplo: {example}', '{n} arquivos deixados de lado, por exemplo: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'Interrompido: nada foi criado.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '{size} no total · em\xa0“{folder}”',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · em\xa0“{folder}”',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title} falhou',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'Erro desconhecido.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'Leve',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'Média',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'Forte',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'Máxima',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}% · {n} cor', '{percent}% · {n} cores'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': 'Imagens a 220 ppp: muito nítidas, mesmo impressas',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": 'Imagens a 150 ppp: nítidas na tela e na impressão',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": 'Imagens a 110 ppp: para a tela',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': 'Imagens a 80 ppp: o mais leve, imagens menos nítidas',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": 'Até 1080p, qualidade muito boa',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": 'Até 1080p, boa qualidade',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p: para celular ou mensagem',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p: o mais leve',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbit/s: música, qualidade muito boa',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbit/s: música',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbit/s: voz, e música no celular',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbit/s: voz',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}% · sem perda',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'Carregando…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': 'em vez de {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'Sem ganho',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'sem ganho',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'Impossível',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'impossível',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'calculando…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'Escolha a qualidade · {key} para comprimir',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': 'Escolha a intensidade · {key} para comprimir',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'Comprimir',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'Qualidade',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'Compressão',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'Passe o mouse sobre a imagem: detalhe a 100%',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'Passe o mouse sobre a imagem: detalhe',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: sem ajuste',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['Prévia: {name} · total de {n} imagem, estimado a partir de {sampled}', 'Prévia: {name} · total de {n} imagens, estimado a partir de {sampled}'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['Prévia: {name} · total de {n} imagem', 'Prévia: {name} · total de {n} imagens'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'Não ficou mais leve',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'Não foi possível comprimir.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} deixada de lado', '{n} deixadas de lado'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'Tente uma compressão mais forte.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'Original: {size} · reduza a qualidade',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'Original: {size} · aumente a compressão',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'Livre',
    # cerclic/ui/crop_editor.py:27
    'Original': 'Original',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'Arraste os cantos · {key} para recortar',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'Recortar',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'Todas as páginas',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'Imagem inteira',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": 'Voltar à imagem inteira',
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
    'touche du Mac\x04Cmd': 'Cmd',
    # contexte : touche | cerclic/ui/editor_base.py:113
    'touche\x04Ctrl': 'Ctrl',
    # cerclic/ui/editor_base.py:205
    'Fermer (Échap)': 'Fechar (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'Arraste para ordenar · {key} para remover',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'Girar para a esquerda',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'Girar para a direita ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': 'Para o início ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'Para o fim ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'Extrair a seleção',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'Um novo PDF só com as páginas escolhidas',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'Redefinir',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'Salvar',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{n} selecionada de {count}', '{n} selecionadas de {count}'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} página', '{n} páginas'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'Mais',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ Voltar',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'Outras ferramentas',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'Geral',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'Atalho de teclado',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'Botão direito',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'Arquivos criados',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'Assinatura',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'Sobre',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'Versão {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'Selecione um ou mais arquivos no Explorador de Arquivos ou na Área de Trabalho e pressione {combo}.',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'Alterar',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'Padrão',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'Pressione sua combinação…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'Verificando…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'Versão {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Selecione um ou mais arquivos no Finder ou na Mesa e pressione {combo}.',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'Abrir a roda',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'Clique com o botão direito no arquivo, Ações Rápidas e depois “Cerclic”. Ou: Abrir Com e depois Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'Inicialização',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'Encerra o Cerclic. Para abri-lo de novo, use a pasta Aplicativos.',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'Idioma',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": 'Automático (idioma do computador)',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'Desinstalar o Cerclic',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": 'Remover o Cerclic do menu do botão direito e do início de sessão e depois encerrá-lo?',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'Desinstalar',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'Uma combinação de teclas abre a roda nos arquivos selecionados.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'Abrir a roda pelo teclado',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '“Cerclic” no menu do botão direito dos seus arquivos.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '“Cerclic” no menu do botão direito',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'Seu arquivo original nunca é alterado: cada ação cria um novo arquivo.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'Onde salvá-los',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'Ao lado do arquivo original',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'Na mesma pasta, por exemplo na Área de Trabalho, se a foto estiver lá. Recomendado.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'Em uma pasta que eu escolher',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'Todos os arquivos criados no mesmo lugar.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'Perguntar sempre',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'O Cerclic pergunta a pasta antes de criar o arquivo.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'Escolher…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'Pasta dos arquivos criados',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'Para assinar seus PDFs com um gesto. Ela fica neste computador.',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'Desenhar…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'Importar uma foto…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'Apagar',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'O equilíbrio entre o tamanho dos arquivos e a nitidez.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}%',
    # cerclic/ui/settings_window.py:993
    'Voir': 'Ver',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'Escolher uma foto da sua assinatura',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'Atalho mantido.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'Exemplos: Shift + Cmd + Espaço, Ctrl + Option + X. Esc para cancelar.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'Exemplos: Ctrl + Alt + Espaço, Ctrl + Shift + X, Win + Shift + C. Esc para cancelar.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'Mais leve',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'Mais nítido',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'Boas-vindas ao Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'As alterações são aplicadas na hora.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'Duas formas de abrir a roda, a inicialização e o idioma.',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'Três formas de abrir a roda, a inicialização e o idioma.',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'Pelo teclado',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Shift + clique com o botão direito no arquivo e depois “Cerclic”. Sem Shift, passe por “Mostrar mais opções”.',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'Clique com o botão direito no arquivo e escolha “Cerclic”.',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'Pelo mouse',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'Iniciar o Cerclic com o Mac',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'Iniciar o Cerclic com o Windows',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'Recomendado: a roda fica pronta assim que você precisar.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'Encerra o Cerclic. Para abri-lo de novo, use o menu Iniciar.',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'Encerra o Cerclic. Para abri-lo de novo, use a Área de Trabalho ou o menu Iniciar.',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'Parar o Cerclic',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": 'A roda não vai mais abrir até a próxima vez que o Cerclic for iniciado.',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'O dos menus, das janelas e das mensagens do Cerclic.',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": '“Alterar” e depois pressione sua combinação. Se o macOS ou outro aplicativo já a usar, o Cerclic avisa e mantém a anterior.',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Tem um mouse com botões programáveis? Configure um botão como uma tecla de F13 a F20 e escolha-a aqui: um clique nesse botão abrirá a roda.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": '“Alterar” e depois pressione sua combinação. Se o Windows ou outro aplicativo já a usar, o Cerclic avisa e mantém a anterior.',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Tem um mouse com botões programáveis? Configure um botão como uma tecla de F13 a F24 e escolha-a aqui: um clique nesse botão abrirá a roda.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'Permissão',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'Ajustes…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'Menu completo do botão direito',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': 'Não aparece em Ações Rápidas? Clique com o botão direito em um arquivo, Ações Rápidas e depois Personalizar, e marque “Cerclic”. Ele também está sempre em Abrir Com.',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'Compressão das imagens',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': 'Ajuste sugerido por “Comprimir”, que mostra o tamanho obtido e lembra sua última escolha.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'JPG criados pelas outras ações',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': 'Recortar, girar, converter… A 90%, a perda não é visível.',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'Recortar, assinar, comprimir, converter, ajustar ao formato das redes sociais… com um gesto, sem abrir outro aplicativo.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'Registro',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'Se algo der errado, este arquivo ajuda a entender o que aconteceu.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'Licenças',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'Os componentes livres que o Cerclic usa e suas licenças.',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'Desinstalar…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'Nenhuma assinatura por enquanto: desenhe-a ou importe uma foto. Se não, ela será pedida na primeira vez que você assinar.',
    # cerclic/ui/settings_window.py:1130
    'Images': 'Imagens',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'Ajustar: pelo teclado',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'Ajustar: pelo mouse',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'Arrastando',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'Abrir o Cerclic ao iniciar a sessão',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'Nos arquivos selecionados no Finder ou na Mesa.',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'Nos arquivos selecionados no Explorador de Arquivos ou na Área de Trabalho.',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Ler a seleção do Finder',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': 'Na primeira vez, o macOS pergunta se o Cerclic pode controlar o Finder: aceite. O Cerclic só lê ali os arquivos selecionados.',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '“Cerclic” no menu do botão direito do Finder',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'No menu Ações Rápidas dos seus arquivos, no Finder e na Mesa.',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": 'Mostra o menu completo sem passar por “Mostrar mais opções”. O Cerclic vai sugerir reiniciar o Explorador de Arquivos.',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'Dica: sem mudar nada, Shift + clique com o botão direito em um arquivo abre direto o menu completo, com “Cerclic”.',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'Nenhuma pasta escolhida.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": 'Remove o “Cerclic” do menu do botão direito e do início de sessão e depois encerra. Depois, só falta mover o Cerclic.app para o Lixo.',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'Atalho desativado: o “Cerclic” no menu do botão direito continua disponível.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'Atalho desativado.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'O Cerclic agora funciona em segundo plano: o ícone dele fica na barra de menus, no alto da tela. Escolha abaixo sua forma preferida de abrir a roda.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'O Cerclic agora funciona em segundo plano: o ícone dele fica perto do relógio (às vezes escondido sob a pequena seta ^). Escolha abaixo sua forma preferida de abrir a roda.',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": 'Arraste arquivos até o ícone do Cerclic (em Aplicativos ou no Dock).',
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": 'Arraste arquivos até o ícone do Cerclic.',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '“Cerclic” no menu do botão direito dos arquivos',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'No alto do menu de imagens, PDFs, vídeos e áudios, no Explorador de Arquivos e na Área de Trabalho.',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'Em imagens, PDFs, vídeos e áudios, no Explorador de Arquivos, na Área de Trabalho e nas janelas Abrir e Salvar.',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'O nome deles: o nome original mais o que mudou, por exemplo foto (comprimido).jpg ao lado de foto.jpg. Se esse nome já existir, o Cerclic adiciona um número: nada nunca é sobrescrito.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": 'Não gostou de um resultado? “Excluir” no cartão dele o apaga na hora.',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'Pasta escolhida: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'Pasta escolhida: nenhuma por enquanto.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": 'Basta uma foto da sua assinatura em papel branco: o Cerclic deixa o papel transparente e mantém a tinta.',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': 'Para assinar: botão direito ou atalho em um PDF e depois “Assinar”. Posicione a assinatura e pressione {key}.',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': 'Recusou por engano? Em Automação, marque “Finder” abaixo de Cerclic.',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ Ativo em todo o Mac.',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ Ativo em todo o Windows.',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'O macOS ou outro aplicativo já usa essa combinação. Escolha outra com “Alterar”.',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'O Windows ou outro aplicativo já usa essa combinação. Escolha outra com “Alterar”.',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'Nenhum traço de assinatura encontrado nesta imagem.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'Sua assinatura',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'Guardada para as próximas vezes',
    # cerclic/ui/signature.py:200
    'Importer…': 'Importar…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'Uma foto da sua assinatura em papel branco',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'Arraste a assinatura · puxe um canto · {key} para assinar',
    # cerclic/ui/signature.py:413
    'Changer': 'Trocar',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': 'Desenhar ou importar outra assinatura',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'Assinar',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'Página {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'Assine aqui',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': 'Escolher uma imagem da sua assinatura',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'Imagens ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'Preencher',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": 'A imagem cobre todo o quadro, o que sobra é cortado.\nArraste-a para escolher a parte mantida; role o mouse para dar zoom.',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'Fundo desfocado',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": 'A imagem inteira, nada é cortado.\nEm volta: a mesma imagem, desfocada.',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'Fundo branco',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": 'A imagem inteira, nada é cortado.\nEm volta: branco.',
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'Fundo preto',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": 'A imagem inteira, nada é cortado.\nEm volta: preto.',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'Arquivo anterior',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'Próximo arquivo',
    # cerclic/ui/social_editor.py:448
    'Créer': 'Criar',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'Arraste e dê zoom · {key} para criar',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'Nada é cortado · {key} para criar',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': 'A parte mantida é menor que o formato: ampliada, ficará um pouco menos nítida.',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'O vídeo é menor que o formato: ampliado, ficará um pouco menos nítido.',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": 'A imagem é menor que o formato: ampliada, ficará um pouco menos nítida.',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'Duração desconhecida',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'Puxe as alças · {key} para aparar',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'Aparar',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'Duração {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': 'Duração ilegível: arquivo danificado?',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'Início {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'Fim {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['“{name}” tem {n} página: só a primeira seria mantida. Use “{action}” para manter todas.', '“{name}” tem {n} páginas: só a primeira seria mantida. Use “{action}” para manter todas.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'Já é um {format}.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'Esta imagem já está bem comprimida.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'A área de recorte está vazia.',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": 'O quadro cobre a imagem inteira: nada para recortar.',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'São necessárias pelo menos duas imagens.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'Combinação',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'Esta imagem não contém nenhuma informação privada.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'Imagem {i} de {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'Para PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": 'A imagem já tem {size} px ou menos.',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': 'Imagem ilegível: {name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '“{name}” está protegido por senha.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'Senha incorreta.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'Conversão para Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'Este arquivo não é um PDF: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'Nenhuma imagem.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'São necessários pelo menos dois PDFs para mesclar.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'Nenhuma página para manter.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": 'Nenhum texto neste PDF: provavelmente é uma digitalização (uma imagem).',
    # cerclic/actions/pdf.py:570
    'Vérification': 'Verificação',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'Este PDF já está bem comprimido.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'O quadro cobre a página inteira: nada para recortar.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': "O texto da marca d'água está vazio.",
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'Nenhuma assinatura salva.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'A senha está vazia.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": 'Este PDF já tem senha. Para definir outra, remova esta primeiro ({more} e depois {action}).',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'Este PDF não está protegido.',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF danificado ou ilegível: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'Página {i} de {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i} de {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'Este PDF tem só uma página.',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'Página não encontrada neste PDF.',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'As páginas não mudaram.',
    # cerclic/actions/registry.py:34
    'Image': 'Imagem',
    # cerclic/actions/registry.py:36
    'Vidéo': 'Vídeo',
    # cerclic/actions/registry.py:37
    'Son': 'Áudio',
    # cerclic/actions/registry.py:136
    'Droite': 'Direita',
    # cerclic/actions/registry.py:137
    'Gauche': 'Esquerda',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'Redes',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'Girar',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'Redimensionar',
    # cerclic/actions/registry.py:213
    'Convertir': 'Converter',
    # cerclic/actions/registry.py:223
    'Copier': 'Copiar',
    # cerclic/actions/registry.py:226
    'Assembler': 'Combinar',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'Anonimizar',
    # cerclic/actions/registry.py:256
    'Fusionner': 'Mesclar',
    # cerclic/actions/registry.py:260
    'Pages': 'Páginas',
    # cerclic/actions/registry.py:266
    'En Word': 'Para Word',
    # cerclic/actions/registry.py:270
    'En images': 'Para imagens',
    # cerclic/actions/registry.py:276
    'Diviser': 'Dividir',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': "Marca d'água",
    # cerclic/actions/registry.py:290
    'Numéroter': 'Numerar',
    # cerclic/actions/registry.py:295
    'En texte': 'Para texto',
    # cerclic/actions/registry.py:326
    'En MP4': 'Para MP4',
    # cerclic/actions/registry.py:329
    'En GIF': 'Para GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'Extrair áudio',
    # cerclic/actions/registry.py:336
    'Couper le son': 'Silenciar',
    # cerclic/actions/registry.py:352
    'En MP3': 'Para MP3',
    # cerclic/actions/registry.py:141
    'Miroir': 'Espelhar',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'Manter uma parte',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'Recorte',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta, Story, celular, PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'Formato para redes sociais',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'Girar ou espelhar',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'Rotação',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'Menos pixels',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'Redimensionamento',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'Mais leve, mesmo tamanho',
    # cerclic/actions/registry.py:216
    'Changer de format': 'Mudar o formato',
    # cerclic/actions/registry.py:216
    'Conversion': 'Conversão',
    # cerclic/actions/registry.py:222
    'Une page par image': 'Uma página por imagem',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'Criação do PDF',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'Para colar onde quiser',
    # cerclic/actions/registry.py:225
    'Copie': 'Cópia',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'Várias em uma',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'Remove GPS, câmera, data',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'Anonimização',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'Colocar sua assinatura',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'Cortar as margens',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'Mais leve para enviar',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'Um só PDF',
    # cerclic/actions/registry.py:259
    'Fusion': 'Mesclagem',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'Ordenar, girar, excluir',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'Organização das páginas',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'Editável no Word',
    # cerclic/actions/registry.py:273
    'Une image par page': 'Uma imagem por página',
    # cerclic/actions/registry.py:273
    'Conversion en images': 'Conversão para imagens',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'Um PDF por página',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'Divisão em páginas',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'Um texto na diagonal',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'Números no rodapé',
    # cerclic/actions/registry.py:294
    'Numérotation': 'Numeração',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'O texto em .txt',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'Extração do texto',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'Com uma senha',
    # cerclic/actions/registry.py:304
    'Protection': 'Proteção',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'Remover a senha',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'Desbloqueio',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'Manter um trecho',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'Corte',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels, TikTok, Shorts, PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'Mais leve, em MP4',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'Toca em qualquer lugar',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'Conversão para MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': 'Uma animação sem som',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'Criação do GIF',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'O áudio em MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': 'Extração do áudio',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'O vídeo sem som',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': 'Remoção do áudio',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'Endireitar o vídeo',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'Conversão para MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'Mais leve, em MP3',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'Arquivo {i} de {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '“{name}”: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '50%',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'Lado a lado',
    # cerclic/actions/registry.py:231
    'En colonne': 'Em coluna',
    # cerclic/actions/registry.py:232
    'En grille': 'Em grade',
    # cerclic/actions/social.py:46
    'Carré': 'Quadrado',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Post do Instagram, Facebook ou LinkedIn',
    # cerclic/actions/social.py:47
    'carré': 'quadrado',
    # cerclic/actions/social.py:48
    'Portrait': 'Retrato',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Post do Instagram ou Facebook, o maior no feed',
    # cerclic/actions/social.py:50
    'portrait': 'retrato',
    # cerclic/actions/social.py:51
    'Grille': 'Grade',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram, no formato exato da grade do perfil',
    # cerclic/actions/social.py:52
    'grille': 'grade',
    # cerclic/actions/social.py:53
    'Story': 'Story',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'Tela cheia do celular: Story, Reels, TikTok, YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'story',
    # cerclic/actions/social.py:56
    'Paysage': 'Paisagem',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'Tela de computador: YouTube, apresentação, X',
    # cerclic/actions/social.py:57
    'paysage': 'paisagem',
    # cerclic/actions/social.py:58
    'Bannière': 'Banner',
    # cerclic/actions/social.py:58
    '1,91:1': '1,91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Link compartilhado ou imagem larga no Facebook, LinkedIn ou X',
    # cerclic/actions/social.py:59
    'bannière': 'banner',
    # cerclic/actions/social.py:239
    'Format {name}': 'Formato {name}',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'Esta imagem já está em {size}.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'Tamanho do vídeo ilegível: arquivo danificado?',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'Este vídeo já está em {size}.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': 'O processamento falhou: talvez o arquivo esteja danificado ou em um formato incomum.',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': 'ffmpeg não encontrado: reinstale o Cerclic.',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'Vídeo danificado ou formato não compatível.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'Acesso negado: talvez o arquivo esteja aberto em outro aplicativo.',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'Corte',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'Nenhuma imagem de vídeo neste arquivo.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'Este vídeo já está bem comprimido: tente uma compressão mais forte.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'Vídeo longo demais para um GIF (mais de 2 minutos: ele teria centenas de MB). Primeiro mantenha só um trecho com “{action}”.',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'Conversão para GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'Este vídeo não tem som.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'O trecho a manter é curto demais.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': 'O trecho escolhido é o arquivo inteiro.',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'Nenhum áudio neste arquivo.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'Prévia indisponível.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'Este áudio já está leve: tente uma compressão mais forte.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'Este arquivo só tem áudio, sem imagem: use “{action}” para transformá-lo em MP3.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'A prévia demora demais para ficar pronta.',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 fecha as janelas.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab alterna entre as janelas.',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc alterna entre as janelas.',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Espaço abre o menu da janela.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc abre o menu Iniciar.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Ctrl + Alt + Delete é reservado ao Windows.',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Ctrl + Shift + Esc abre o Gerenciador de Tarefas.',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'Tecla {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'Espaço',
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
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Adicione uma tecla depois de Ctrl, Alt, Shift ou Win.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} já é usado no Windows e nos aplicativos (ajuda, renomear, atualizar, ortografia…). Adicione, por exemplo, Ctrl + Alt: Ctrl + Alt + {key}.',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt com o teclado numérico serve para digitar caracteres (Alt + 0201 = É). Escolha outra combinação.',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'A combinação precisa ter Ctrl, Alt ou Win (senão essa tecla não digitaria mais nada).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Shift',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt + uma única tecla já é usado em muitos aplicativos (os menus dos aplicativos). Adicione Shift ou Ctrl, por exemplo Alt + Shift + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'Essa combinação serve para digitar caracteres (§, ª, º, °…) com AltGr. Escolha outra.',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl + uma única tecla já é usado em muitos aplicativos (negrito, copiar, colar, salvar…). Adicione Shift ou Alt, por exemplo Ctrl + Shift + {key}.',
}
