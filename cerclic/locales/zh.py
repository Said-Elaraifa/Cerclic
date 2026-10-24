"""Cerclic, 简体中文. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} 个文件'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": '已保存到“{where}”：原文件夹受保护。',
    # cerclic/app.py:92
    'Téléchargements': '下载',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'Windows 或其他应用已在使用这个快捷键。请在 Cerclic 中另选一个。',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': '右键单击，然后选择“Cerclic”',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": '找不到所选文件夹：已保存在原文件旁边。',
    # cerclic/app.py:459
    'Ouvrir Cerclic': '打开 Cerclic',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': '退出 Cerclic',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'Windows 或其他应用已在使用这个快捷键。请在 Cerclic 中另选一个；右键菜单中的“Cerclic”仍然可用。',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'macOS 或其他应用已在使用这个快捷键。请在 Cerclic 中另选一个。',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': '右键点按，选择“快速操作”，然后选择“Cerclic”',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": '右键单击，选择“显示更多选项”，然后选择“Cerclic”',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': '允许 Cerclic 读取你选中的文件',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': '前往“系统设置”>“隐私与安全性”>“自动化”，勾选 Cerclic 下方的“访达”。不勾选的话，右键点按 >“快速操作”>“Cerclic”也能使用。',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': '在“访达”或桌面上点按图片、PDF、视频或音频文件，然后按 {combo}。',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": '在文件资源管理器或桌面上单击图片、PDF、视频或音频文件，然后按 {combo}。',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': '或者：右键点按，选择“快速操作”，然后选择“Cerclic”。',
    # cerclic/app.py:919
    'Image copiée': '图片已复制',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': '按 {key} + V 即可粘贴到任意位置。',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': '好',
    # cerclic/app.py:1253
    'Menu complet activé': '已启用完整菜单',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": '重启文件资源管理器后生效。已打开的文件夹窗口将会关闭。',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': '已恢复 Windows 11 菜单',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": '重启文件资源管理器后生效。',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': '安装了两个 Cerclic',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": '未通过 Microsoft Store 安装的 Cerclic 版本仍然存在。要让右键菜单中只有一个“Cerclic”、只有一个快捷键，请将其移除：点击“显示卸载程序”，然后双击“unins000”。',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": '未通过 Microsoft Store 安装的 Cerclic 版本仍然存在。要只保留一个“Cerclic”，请在“已安装的应用”中卸载它：就是菜单中没有“高级选项”的那个 Cerclic。',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'macOS 或其他应用已在使用这个快捷键。请在 Cerclic 中另选一个；右键菜单中的“Cerclic”仍然可用。',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": '或者：右键单击，选择“显示更多选项”，然后选择“Cerclic”。',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': '或者：右键单击，然后选择“Cerclic”。',
    # cerclic/app.py:915
    'Copie impossible': '无法复制',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': '解锁',
    # cerclic/app.py:966
    'Continuer': '继续',
    # cerclic/app.py:971
    '« {name} » est protégé.': '“{name}”受密码保护。',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'PDF 密码',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': '随 Windows 启动已被阻止',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': '你的组织不允许应用随 Windows 启动。',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': '随 Windows 启动已在 Windows 中被禁用',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': '它已在任务管理器中被禁用，只能在 Windows 中重新启用：前往“设置”>“应用”>“启动”，打开“Cerclic”。',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': '快捷键 {combo} 不可用',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Cerclic 遇到了问题',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': '详细信息见 {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': '无法访问文件',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": '此文件不在普通文件夹中（如 ZIP 压缩包、手机等）。请将它复制到一个文件夹中，然后重试。',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': '无法读取图片。',
    # cerclic/app.py:1224
    'Réessayer': '重试',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': '{refused} 已被 macOS 或其他应用占用。你的快捷键仍为 {kept}。',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': '{refused} 已被 Windows 或其他应用占用。你的快捷键仍为 {kept}。',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': '稍后',
    # cerclic/app.py:810
    'Ouvrir les réglages': '打开设置',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': '此类文件没有可用的操作',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'Cerclic 可处理图片、PDF、视频和音频。',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": '请先选择一个文件',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': '“{name}”的密码不正确。请重试。',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": '裁剪只会保留第一页。请先用“转为 PDF”保留所有页面，再对 PDF 使用“{action}”。',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['“{name}”有 {n} 页'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': '结果保存到哪里？',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": '重启文件资源管理器',
    # cerclic/app.py:591
    'Montrer le désinstalleur': '显示卸载程序',
    # cerclic/app.py:602
    'Ouvrir les applications': '打开已安装的应用',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'macOS 或其他应用已在使用这个组合键。你的快捷键仍为 {kept}。',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'Windows 或其他应用已在使用这个组合键。你的快捷键仍为 {kept}。',
    # cerclic/app.py:975
    'Mot de passe incorrect': '密码不正确',
    # cerclic/app.py:975
    "Rien n'a été créé.": '未创建任何文件。',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": '压缩只会保留第一页。请先用“转为 PDF”保留所有页面，再对 PDF 使用“{action}”。',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': '只有第一页会被调整为该尺寸。请用“转为 PDF”保留所有页面。',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': '打开',
    # cerclic/app.py:707
    'Changer de raccourci': '更改快捷键',
    # cerclic/app.py:1081
    'Texte du filigrane': '水印文字',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': '将斜向显示在每一页上。',
    # cerclic/app.py:1083
    'CONFIDENTIEL': '机密',
    # cerclic/app.py:1088
    'Mot de passe à mettre': '要设置的密码',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": '打开 PDF 时需要输入此密码。原文件仍不设密码。',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': '加密',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': '发生意外错误。请重试；如果问题再次出现，详细信息见 Cerclic 日志（cerclic.log）。',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': '访问被拒绝：文件可能已在其他应用中打开，或文件夹受保护。',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': '名称或路径对 Windows 来说太长：请缩短文件名，或将文件移到层级较浅的文件夹中。',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': '找不到文件：它可能已被移动或删除。',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': '文件太大，可用内存不足。',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': '磁盘已满。',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': '无法读取图片，或格式不受支持。',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF 已损坏或无法读取。',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}：至少需要 {n} 个文件。'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': '已取消',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '“{name}”已不在原处：它已被移动、重命名或删除（或 U 盘已拔出）。',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} 个文件已不在原处：它们已被移动、重命名或删除。'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': '此 PDF 受密码保护。',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": '处理突然中止：文件可能已损坏。',
    # cerclic/paths.py:235
    'compressé': '已压缩',
    # cerclic/paths.py:235
    'redimensionné': '已调整大小',
    # cerclic/paths.py:236
    'pivoté': '已旋转',
    # cerclic/paths.py:236
    'rogné': '已裁剪',
    # cerclic/paths.py:236
    'miroir': '镜像',
    # cerclic/paths.py:237
    'anonymisé': '已匿名化',
    # cerclic/paths.py:237
    'assemblé': '已拼接',
    # cerclic/paths.py:237
    'fusionné': '已合并',
    # cerclic/paths.py:238
    'réorganisé': '已整理',
    # cerclic/paths.py:238
    'extrait': '提取',
    # cerclic/paths.py:238
    'texte': '文本',
    # cerclic/paths.py:239
    'filigrane': '水印',
    # cerclic/paths.py:239
    'numéroté': '已编页码',
    # cerclic/paths.py:239
    'signé': '已签名',
    # cerclic/paths.py:240
    'protégé': '已加密',
    # cerclic/paths.py:240
    'déverrouillé': '已解锁',
    # cerclic/paths.py:240
    'son': '音频',
    # cerclic/paths.py:241
    'raccourci': '已修剪',
    # cerclic/paths.py:241
    'sans son': '无声',
    # cerclic/paths.py:241
    'images': '图片',
    # cerclic/paths.py:242
    'pages': '页面',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': '大小不变',
    # cerclic/sizes.py:71
    'De {before} à {after}': '从 {before} 到 {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} 字节'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '减小 {pct}%',
    # cerclic/sizes.py:64
    '{pct} % de plus': '增大 {pct}%',
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
    'touche Mac\x04Touche {code}': '按键 {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'Command + Space 用于打开“聚焦”。',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'Option + Command + Space 用于打开“访达”搜索。',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'Control + Space 用于切换输入法。',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'Control + Option + Space 用于切换输入法。',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'Control + Command + Space 用于打开表情符号。',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'Command + Tab 用于在应用之间切换。',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'Shift + Command + Tab 用于在应用之间切换。',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'Option + Command + Esc 用于强制退出应用。',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Shift + Command + 3 用于截屏。',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Shift + Command + 4 用于截屏。',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Shift + Command + 5 用于打开截屏工具。',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'Shift + Command + 6 用于截取触控栏。',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'Control + Command + Q 用于锁定屏幕。',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Shift + Command + Q 用于退出登录。',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'Control + Command + F 用于进入全屏幕。',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'Option + Command + D 用于隐藏程序坞。',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'Option + Command + C 用于在“访达”中复制文件路径。',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'Option + Command + H 用于隐藏其他应用。',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'Option + Command + M 用于最小化所有窗口。',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'Option + Command + W 用于关闭所有窗口。',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'Option + Command + V 用于在“访达”中移动已复制的文件。',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Space',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'Return',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'Tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': 'Delete ⌦',
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
    'touche Mac\x04Pavé {key}': '小键盘 {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': '请在 Command、Control、Option 或 Shift 之后再加一个键。',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} 已是 macOS 的快捷键（“系统设置”>“键盘”>“键盘快捷键”）。请另选一个。',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'Shift + Command + {key} 已用于“访达”。请选择其他字母，或使用 Shift + Command + Space。',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": '组合中需要包含 Command 或 Control：macOS 不接受只用 Option 或 Shift 的快捷键。',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Command 加单个键已在所有应用中使用（复制、粘贴、保存等）。请加上 Shift、Option 或 Control，例如 Shift + Command + {key}。',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'Control + 方向键用于在桌面之间切换（调度中心）。',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Control',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Shift',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Command',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': '取消',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': '显示密码',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': '隐藏密码',
    # cerclic/ui/cards.py:238
    'Fermer': '关闭',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': '桌面',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': '下载',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': '图片',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': '视频',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': '影片',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': '音乐',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': '文档',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': '停止',
    # cerclic/ui/cards.py:299
    'En cours': '处理中',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': '正在停止…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['文件已删除'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": '你的原文件保持不变。',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['已创建 {n} 个文件'],
    # cerclic/ui/cards.py:366
    'Dossier': '文件夹',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': '删除',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": '删除 Cerclic 刚刚创建的文件（你的原文件保持不变）',
    # cerclic/ui/cards.py:417
    'Suppression impossible': '无法删除',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': '文件可能已在其他应用中打开：请关闭该应用，然后重试。',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': '位于“{folder}”',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['跳过了 {n} 个文件，例如：{example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": '已停止：未创建任何文件。',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '共 {size} · 位于“{folder}”',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · 位于“{folder}”',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title}失败',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': '未知错误。',
    # cerclic/ui/compress_editor.py:36
    'Légère': '轻度',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': '中度',
    # cerclic/ui/compress_editor.py:36
    'Forte': '高度',
    # cerclic/ui/compress_editor.py:37
    'Maximale': '最大',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}% · {n} 种颜色'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': '图片 220 ppi：非常清晰，打印也很清晰',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": '图片 150 ppi：屏幕显示和打印都清晰',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": '图片 110 ppi：适合屏幕查看',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': '图片 80 ppi：文件最小，图片不太清晰',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": '最高 1080p，画质很好',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": '最高 1080p，画质良好',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p：适合手机观看或消息发送',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p：文件最小',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbit/s：音乐，音质很好',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbit/s：音乐',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbit/s：人声，或在手机上听音乐',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbit/s：人声',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}% · 无损',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': '正在加载…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': '原为 {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': '未变小',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': '未变小',
    # cerclic/ui/compress_editor.py:203
    'Impossible': '失败',
    # cerclic/ui/compress_editor.py:203
    'impossible': '失败',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': '计算中…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': '选择质量 · 按 {key} 压缩',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': '选择压缩强度 · 按 {key} 压缩',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': '压缩',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': '质量',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': '压缩',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": '将指针悬停在图片上：查看 100% 细节',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": '将指针悬停在图片上：查看细节',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF：无可调设置',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['预览：{name} · {n} 张图片的总大小，基于 {sampled} 张估算'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['预览：{name} · {n} 张图片的总大小'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': '没有变小',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': '无法压缩。',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['跳过 {n} 张'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': '试试更高的压缩强度。',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': '原始大小：{size} · 请降低质量',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': '原始大小：{size} · 请提高压缩强度',
    # cerclic/ui/crop_editor.py:27
    'Libre': '自由',
    # cerclic/ui/crop_editor.py:27
    'Original': '原始比例',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': '拖动边角 · 按 {key} 裁剪',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': '裁剪',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': '所有页面',
    # cerclic/ui/crop_editor.py:469
    'Image entière': '整张图片',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": '恢复为整张图片',
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
    'Fermer (Échap)': '关闭（Esc）',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': '拖动以排序 · 按 {key} 移除',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': '向左旋转',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': '向右旋转（{key} + R）',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': '移到前面（{key} + {arrow}）',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': '移到后面（{key} + {arrow}）',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': '提取所选页面',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': '只包含所选页面的新 PDF',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': '重置',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': '保存',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['已选择 {n} 页，共 {count} 页'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} 页'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': '更多',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ 返回',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category}（{n}）',
    # cerclic/ui/radial.py:215
    "D'autres outils": '更多工具',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': '通用',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': '键盘快捷键',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': '右键菜单',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': '生成的文件',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': '签名',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': '关于',
    # cerclic/ui/settings_window.py:593
    'Version {version}': '版本 {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": '在文件资源管理器或桌面上选择一个或多个文件，然后按 {combo}。',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': '更改',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': '默认',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': '请按下你的组合键…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': '正在检查…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': '版本 {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': '在“访达”或桌面上选择一个或多个文件，然后按 {combo}。',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': '打开轮盘',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': '右键点按文件，选择“快速操作”，然后选择“Cerclic”。或者：选择“打开方式”，然后选择 Cerclic。',
    # cerclic/ui/settings_window.py:642
    'Démarrage': '启动',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': '退出 Cerclic。要重新启动，请从“应用程序”文件夹打开它。',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': '语言',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": '自动（跟随电脑语言）',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': '卸载 Cerclic',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": '从右键菜单和登录项中移除 Cerclic，然后退出？',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': '卸载',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': '按下组合键，即可为所选文件打开轮盘。',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': '用键盘打开轮盘',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '在文件的右键菜单中显示“Cerclic”。',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '右键菜单中的“Cerclic”',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": '你的原文件永远不会被修改：每次操作都会创建一个新文件。',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': '保存位置',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": '原文件旁边',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': '保存在同一文件夹中，例如照片在桌面上，就保存在桌面上。推荐。',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': '我选择的文件夹',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': '所有生成的文件都放在同一个位置。',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': '每次询问我',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'Cerclic 会在创建文件前询问保存到哪个文件夹。',
    # cerclic/ui/settings_window.py:828
    'Choisir…': '选择…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': '生成文件的文件夹',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': '一步即可为 PDF 签名。签名只保存在这台电脑上。',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': '绘制…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': '导入照片…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': '清除',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': '在文件大小与清晰度之间取得平衡。',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}%',
    # cerclic/ui/settings_window.py:993
    'Voir': '查看',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': '选择你的签名照片',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': '快捷键未更改。',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': '例如：Shift + Command + Space、Control + Option + X。按 Esc 取消。',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': '例如：Ctrl + Alt + Space、Ctrl + Shift + X、Win + Shift + C。按 Esc 取消。',
    # cerclic/ui/settings_window.py:313
    'Plus léger': '更小',
    # cerclic/ui/settings_window.py:315
    'Plus net': '更清晰',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': '欢迎使用 Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": '更改会立即生效。',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": '打开轮盘的两种方式、启动和语言。',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": '打开轮盘的三种方式、启动和语言。',
    # cerclic/ui/settings_window.py:620
    'Au clavier': '用键盘',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": '按住 Shift 并右键单击文件，然后选择“Cerclic”。不按 Shift 时，请先选择“显示更多选项”。',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': '右键单击文件，然后选择“Cerclic”。',
    # cerclic/ui/settings_window.py:632
    'À la souris': '用鼠标',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': '随 Mac 启动 Cerclic',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': '随 Windows 启动 Cerclic',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': '推荐：需要时轮盘随时可用。',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': '退出 Cerclic。要重新启动，请从“开始”菜单打开它。',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': '退出 Cerclic。要重新启动，请从桌面或“开始”菜单打开它。',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': '停止 Cerclic',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": '在下次启动前，轮盘将无法打开。',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'Cerclic 菜单、窗口和消息所用的语言。',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": '点按“更改”，然后按下你的组合键。如果它已被 macOS 或其他应用占用，Cerclic 会告诉你，并保留原来的快捷键。',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': '鼠标有可编程按键？将其中一个按键设为 F13 到 F20 中的某个键，然后在这里选择该键：点按这个鼠标按键即可打开轮盘。',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": '点击“更改”，然后按下你的组合键。如果它已被 Windows 或其他应用占用，Cerclic 会告诉你，并保留原来的快捷键。',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': '鼠标有可编程按键？将其中一个按键设为 F13 到 F24 中的某个键，然后在这里选择该键：单击这个鼠标按键即可打开轮盘。',
    # cerclic/ui/settings_window.py:744
    'Autorisation': '权限',
    # cerclic/ui/settings_window.py:745
    'Réglages…': '设置…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': '完整右键菜单',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': '“快速操作”中没有？右键点按文件，选择“快速操作”>“自定”，然后勾选“Cerclic”。它也始终位于“打开方式”中。',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': '图片压缩',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': '“压缩”默认提供的设置；它会显示压缩后的大小，并记住你上次的选择。',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': '其他操作生成的 JPG',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': '用于裁剪、旋转、转换等。设为 90% 时看不出画质损失。',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": '裁剪、签名、压缩、转换、调整为社交媒体尺寸等，一步完成，无需打开其他应用。',
    # cerclic/ui/settings_window.py:991
    'Journal': '日志',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": '出现问题时，这个文件有助于了解发生了什么。',
    # cerclic/ui/settings_window.py:995
    'Licences': '许可证',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'Cerclic 使用的开源组件及其许可证。',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': '卸载…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": '目前还没有签名：请绘制签名或导入照片。否则，第一次签名时会请你提供。',
    # cerclic/ui/settings_window.py:1130
    'Images': '图片',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': '设置：键盘',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': '设置：鼠标',
    # cerclic/ui/settings_window.py:636
    'En glissant': '拖放',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": '登录时打开 Cerclic',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': '作用于在“访达”或桌面上选中的文件。',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": '作用于在文件资源管理器或桌面上选中的文件。',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': '读取“访达”中的所选项',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': '首次使用时，macOS 会询问是否允许 Cerclic 控制“访达”：请选择允许。Cerclic 只会读取其中选中的文件。',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '“访达”右键菜单中的“Cerclic”',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': '位于文件的“快速操作”菜单中，在“访达”和桌面上均可用。',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": '直接显示完整菜单，无需点击“显示更多选项”。Cerclic 会提示你重启文件资源管理器。',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': '提示：无需更改任何设置，按住 Shift 并右键单击文件，即可直接打开包含“Cerclic”的完整菜单。',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': '未选择文件夹。',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": '从右键菜单和登录项中移除“Cerclic”，然后退出。之后只需将 Cerclic.app 移到废纸篓。',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': '快捷键已停用：右键菜单中的“Cerclic”仍然可用。',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': '快捷键已停用。',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic 现在正在后台运行：它的图标位于屏幕顶部的菜单栏中。请在下方选择你喜欢的轮盘打开方式。',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic 现在正在后台运行：它的图标位于时钟旁边（有时隐藏在小箭头 ^ 下）。请在下方选择你喜欢的轮盘打开方式。',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": '将文件拖到 Cerclic 图标上（位于“应用程序”文件夹或程序坞中）。',
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": '将文件拖到 Cerclic 图标上。',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '文件右键菜单中的“Cerclic”',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": '位于图片、PDF、视频和音频的右键菜单顶部，在文件资源管理器和桌面上均可用。',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": '适用于图片、PDF、视频和音频，在文件资源管理器、桌面以及“打开”和“保存”窗口中均可用。',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": '文件名：原文件名加上所做的更改，例如 photo.jpg 旁边的 photo (已压缩).jpg。如果该名称已被占用，Cerclic 会添加编号：绝不会覆盖任何文件。',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": '对结果不满意？点击结果卡片上的“删除”即可立即删除。',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': '你选择的文件夹：{folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": '你选择的文件夹：暂未选择。',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": '只需一张白纸上签名的照片：Cerclic 会让纸张变透明，只保留笔迹。',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': '签名方法：在 PDF 上右键点击或使用快捷键，然后选择“签名”。放好签名后按 {key}。',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': '不小心拒绝了？请在“自动化”中勾选 Cerclic 下方的“访达”。',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ 在 Mac 上任何位置均可用。',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ 在 Windows 中任何位置均可用。',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'macOS 或其他应用已在使用这个组合键。请点按“更改”另选一个。',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'Windows 或其他应用已在使用这个组合键。请点击“更改”另选一个。',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': '在这张图片中未找到签名笔迹。',
    # cerclic/ui/signature.py:196
    'Ta signature': '你的签名',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': '会保存下来供以后使用',
    # cerclic/ui/signature.py:200
    'Importer…': '导入…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': '白纸上签名的照片',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': '拖动签名 · 拖拽边角调整大小 · 按 {key} 签名',
    # cerclic/ui/signature.py:413
    'Changer': '更换',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': '绘制或导入其他签名',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': '签名',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': '第 {page} / {count} 页',
    # cerclic/ui/signature.py:153
    'Signe ici': '在此签名',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': '选择你的签名图片',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': '图片 ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': '填充',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": '图片铺满整个画框，超出部分会被裁掉。\n拖动图片选择要保留的部分，滚动滚轮缩放。',
    # cerclic/ui/social_editor.py:34
    'Fond flou': '模糊背景',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": '完整显示图片，不裁掉任何部分。\n周围：同一张图片的模糊版本。',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': '白色背景',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": '完整显示图片，不裁掉任何部分。\n周围：白色。',
    # cerclic/ui/social_editor.py:37
    'Fond noir': '黑色背景',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": '完整显示图片，不裁掉任何部分。\n周围：黑色。',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': '上一个文件',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': '下一个文件',
    # cerclic/ui/social_editor.py:448
    'Créer': '创建',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': '拖动并缩放 · 按 {key} 创建',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": '不裁掉任何部分 · 按 {key} 创建',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': '保留的部分小于目标尺寸：放大后会稍微模糊一些。',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': '视频小于目标尺寸：放大后会稍微模糊一些。',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": '图片小于目标尺寸：放大后会稍微模糊一些。',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': '时长未知',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': '拖动手柄 · 按 {key} 修剪',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': '修剪',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': '时长 {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': '无法读取时长：文件是否已损坏？',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': '开始 {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': '结束 {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['“{name}”有 {n} 页：只会保留第一页。请使用“{action}”保留所有页面。'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": '已经是 {format} 格式。',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': '这张图片已经充分压缩。',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': '裁剪区域为空。',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": '裁剪框覆盖了整张图片：没有可裁剪的部分。',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': '至少需要两张图片。',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': '拼接',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': '这张图片不包含任何隐私信息。',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': '第 {i} 张图片，共 {n} 张',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': '转为 PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": '图片已经不超过 {size} px。',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': '无法读取图片：{name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '“{name}”受密码保护。',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': '密码不正确。',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': '转换为 Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": '此文件不是 PDF：{name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': '没有图片。',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': '至少需要两个 PDF 才能合并。',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': '没有要保留的页面。',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": '此 PDF 中没有文本：它很可能是扫描件（图片）。',
    # cerclic/actions/pdf.py:570
    'Vérification': '正在检查',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': '此 PDF 已经充分压缩。',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': '裁剪框覆盖了整个页面：没有可裁剪的部分。',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': '水印文字为空。',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': '没有已保存的签名。',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': '密码为空。',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": '此 PDF 已有密码。要设置新密码，请先移除当前密码（先选“{more}”，再选“{action}”）。',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": '此 PDF 未设密码。',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF 已损坏或无法读取：{name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': '第 {i} 页，共 {n} 页',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': '第 {i} 个 PDF，共 {n} 个',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": '此 PDF 只有一页。',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': '在此 PDF 中找不到该页面。',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": '页面没有变化。',
    # cerclic/actions/registry.py:34
    'Image': '图片',
    # cerclic/actions/registry.py:36
    'Vidéo': '视频',
    # cerclic/actions/registry.py:37
    'Son': '音频',
    # cerclic/actions/registry.py:136
    'Droite': '向右',
    # cerclic/actions/registry.py:137
    'Gauche': '向左',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': '社交媒体',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': '旋转',
    # cerclic/actions/registry.py:200
    'Redimensionner': '调整大小',
    # cerclic/actions/registry.py:213
    'Convertir': '转换',
    # cerclic/actions/registry.py:223
    'Copier': '复制',
    # cerclic/actions/registry.py:226
    'Assembler': '拼接',
    # cerclic/actions/registry.py:233
    'Anonymiser': '匿名化',
    # cerclic/actions/registry.py:256
    'Fusionner': '合并',
    # cerclic/actions/registry.py:260
    'Pages': '页面',
    # cerclic/actions/registry.py:266
    'En Word': '转为 Word',
    # cerclic/actions/registry.py:270
    'En images': '转为图片',
    # cerclic/actions/registry.py:276
    'Diviser': '拆分',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': '水印',
    # cerclic/actions/registry.py:290
    'Numéroter': '添加页码',
    # cerclic/actions/registry.py:295
    'En texte': '转为文本',
    # cerclic/actions/registry.py:326
    'En MP4': '转为 MP4',
    # cerclic/actions/registry.py:329
    'En GIF': '转为 GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': '提取音频',
    # cerclic/actions/registry.py:336
    'Couper le son': '去除声音',
    # cerclic/actions/registry.py:352
    'En MP3': '转为 MP3',
    # cerclic/actions/registry.py:141
    'Miroir': '镜像',
    # cerclic/actions/registry.py:191
    'Garder une partie': '保留一部分',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': '裁剪',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta、快拍、手机、电脑',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': '社交媒体尺寸',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': '旋转或翻转',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': '旋转',
    # cerclic/actions/registry.py:203
    'Moins de pixels': '减少像素',
    # cerclic/actions/registry.py:203
    'Redimensionnement': '调整大小',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': '文件更小，尺寸不变',
    # cerclic/actions/registry.py:216
    'Changer de format': '更改格式',
    # cerclic/actions/registry.py:216
    'Conversion': '转换',
    # cerclic/actions/registry.py:222
    'Une page par image': '每张图片一页',
    # cerclic/actions/registry.py:222
    'Création du PDF': '创建 PDF',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': '随处粘贴',
    # cerclic/actions/registry.py:225
    'Copie': '复制',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': '多张合成一张',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': '移除 GPS、设备、日期',
    # cerclic/actions/registry.py:237
    'Anonymisation': '匿名化',
    # cerclic/actions/registry.py:245
    'Placer ta signature': '放置你的签名',
    # cerclic/actions/registry.py:250
    'Couper les marges': '裁掉边距',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': '更小，方便发送',
    # cerclic/actions/registry.py:259
    'Un seul PDF': '合成一个 PDF',
    # cerclic/actions/registry.py:259
    'Fusion': '合并',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': '排序、旋转、删除',
    # cerclic/actions/registry.py:265
    'Organisation des pages': '整理页面',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': '可在 Word 中编辑',
    # cerclic/actions/registry.py:273
    'Une image par page': '每页一张图片',
    # cerclic/actions/registry.py:273
    'Conversion en images': '转换为图片',
    # cerclic/actions/registry.py:279
    'Un PDF par page': '每页一个 PDF',
    # cerclic/actions/registry.py:279
    'Découpage en pages': '按页拆分',
    # cerclic/actions/registry.py:289
    'Un texte en travers': '斜贯页面的文字',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': '在页面底部添加页码',
    # cerclic/actions/registry.py:294
    'Numérotation': '添加页码',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': '将文本导出为 .txt',
    # cerclic/actions/registry.py:299
    'Extraction du texte': '提取文本',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': '设置密码',
    # cerclic/actions/registry.py:304
    'Protection': '加密',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': '移除密码',
    # cerclic/actions/registry.py:309
    'Déverrouillage': '解锁',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': '保留一段',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': '修剪',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels、TikTok、Shorts、电脑',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': '更小，MP4 格式',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': '随处可播放',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': '转换为 MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': '无声动画',
    # cerclic/actions/registry.py:331
    'Création du GIF': '创建 GIF',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': '将音轨导出为 MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': '提取音频',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': '去掉声音的视频',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': '去除声音',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": '摆正方向',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': '转换为 MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': '更小，MP3 格式',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': '第 {i} 个文件，共 {n} 个',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '“{name}”：{error}',
    # cerclic/actions/registry.py:204
    '50 %': '50%',
    # cerclic/actions/registry.py:230
    'Côte à côte': '并排',
    # cerclic/actions/registry.py:231
    'En colonne': '竖排',
    # cerclic/actions/registry.py:232
    'En grille': '网格',
    # cerclic/actions/social.py:46
    'Carré': '方形',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Instagram、Facebook 或 LinkedIn 帖子',
    # cerclic/actions/social.py:47
    'carré': '方形',
    # cerclic/actions/social.py:48
    'Portrait': '竖版',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Instagram 或 Facebook 帖子，在动态中显示最大',
    # cerclic/actions/social.py:50
    'portrait': '竖版',
    # cerclic/actions/social.py:51
    'Grille': '网格',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram，与主页网格的形状完全一致',
    # cerclic/actions/social.py:52
    'grille': '网格',
    # cerclic/actions/social.py:53
    'Story': '快拍',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': '手机全屏：快拍、Reels、TikTok、YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': '快拍',
    # cerclic/actions/social.py:56
    'Paysage': '横版',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": '电脑屏幕：YouTube、演示文稿、X',
    # cerclic/actions/social.py:57
    'paysage': '横版',
    # cerclic/actions/social.py:58
    'Bannière': '横幅',
    # cerclic/actions/social.py:58
    '1,91:1': '1.91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Facebook、LinkedIn 或 X 上的分享链接或宽幅图片',
    # cerclic/actions/social.py:59
    'bannière': '横幅',
    # cerclic/actions/social.py:239
    'Format {name}': '{name}格式',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': '这张图片已经是 {size}。',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': '无法读取视频尺寸：文件是否已损坏？',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': '这个视频已经是 {size}。',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': '处理失败：文件可能已损坏，或格式不常见。',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': '找不到 ffmpeg：请重新安装 Cerclic。',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': '视频已损坏，或格式不受支持。',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': '访问被拒绝：文件可能已在其他应用中打开。',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': '正在修剪',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': '此文件中没有视频画面。',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': '这个视频已经充分压缩：试试更高的压缩强度。',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": '视频太长，无法转为 GIF（超过 2 分钟，GIF 会有几百 MB）。请先用“{action}”保留一段。',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': '转换为 GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": '这个视频没有声音。',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': '要保留的片段太短。',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': '所选片段就是整个文件。',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': '此文件中没有声音。',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': '无法预览。',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': '这个音频已经很小：试试更高的压缩强度。',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": '此文件只有声音，没有画面：请使用“{action}”将其转为 MP3。',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': '预览准备时间过长。',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 用于关闭窗口。',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab 用于切换窗口。',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc 用于切换窗口。',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Space 用于打开窗口菜单。',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc 用于打开“开始”菜单。',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Ctrl + Alt + Delete 由 Windows 专用。',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Ctrl + Shift + Esc 用于打开任务管理器。',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': '按键 {code}',
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
    'touche Windows\x04Pavé {key}': '小键盘 {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': '请在 Ctrl、Alt、Shift 或 Win 之后再加一个键。',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} 已被 Windows 和各类应用使用（帮助、重命名、刷新、拼写检查等）。可以加上 Ctrl + Alt，例如：Ctrl + Alt + {key}。',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt 加数字小键盘用于输入字符（Alt + 0201 = É）。请另选一个组合键。',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": '组合中需要包含 Ctrl、Alt 或 Win（否则这个键将无法正常输入）。',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Shift',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt 加单个键已被许多应用使用（用于打开应用菜单）。请加上 Shift 或 Ctrl，例如 Alt + Shift + {key}。',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': '这个组合键用于配合 AltGr 输入字符（@、€、#、œ 等）。请另选一个。',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl 加单个键已被许多应用使用（加粗、复制、粘贴、保存等）。请加上 Shift 或 Alt，例如 Ctrl + Shift + {key}。',
    # cerclic/ui/settings_window.py (À propos)
    'Code source': '源代码',
    'Tout le code de Cerclic est public, sur GitHub.': 'Cerclic 的全部代码都公开在 GitHub 上。',
}
