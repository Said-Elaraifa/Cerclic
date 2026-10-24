"""Cerclic, 日本語. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} 個のファイル'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": '元のフォルダは保護されているため、「{where}」に保存しました。',
    # cerclic/app.py:92
    'Téléchargements': 'ダウンロード',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'Windows または別のアプリがすでに使用しています。Cerclic で別のショートカットを選んでください。',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': '右クリックして「Cerclic」を選択',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": '選択したフォルダが見つからないため、元のファイルと同じ場所に保存しました。',
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'Cerclic を開く',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'Cerclic を終了',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'Windows または別のアプリがすでに使用しています。Cerclic で別のショートカットを選んでください。右クリックの「Cerclic」は引き続き使えます。',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'macOS または別のアプリがすでに使用しています。Cerclic で別のショートカットを選んでください。',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': '右クリックして「クイックアクション」から「Cerclic」を選択',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": '右クリックして「その他のオプションを確認」から「Cerclic」を選択',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'Cerclic に選択項目の読み取りを許可してください',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': '「システム設定」>「プライバシーとセキュリティ」>「オートメーション」で、Cerclic の下にある「Finder」をオンにしてください。右クリックの「クイックアクション」>「Cerclic」は、この設定なしでも使えます。',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Finder またはデスクトップで画像、PDF、ビデオ、オーディオのいずれかをクリックしてから、{combo} を押してください。',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'エクスプローラーまたはデスクトップで画像、PDF、ビデオ、オーディオのいずれかをクリックしてから、{combo} を押してください。',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'または：右クリックして「クイックアクション」から「Cerclic」を選択します。',
    # cerclic/app.py:919
    'Image copiée': '画像をコピーしました',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': '{key} + V で好きな場所に貼り付けられます。',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'OK',
    # cerclic/app.py:1253
    'Menu complet activé': '完全なメニューを有効にしました',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'エクスプローラーを再起動すると反映されます。開いているフォルダのウィンドウは閉じられます。',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Windows 11 のメニューに戻しました',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'エクスプローラーを再起動すると反映されます。',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'Cerclic が 2 つインストールされています',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'Microsoft Store 以外からインストールした Cerclic がまだ残っています。右クリックの「Cerclic」とショートカットを 1 つだけにするには、それを削除してください：「アンインストーラーを表示」をクリックし、「unins000」をダブルクリックします。',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": 'Microsoft Store 以外からインストールした Cerclic がまだ残っています。「Cerclic」を 1 つだけにするには、「インストールされているアプリ」でアンインストールしてください：メニューに「詳細オプション」がないほうの Cerclic です。',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'macOS または別のアプリがすでに使用しています。Cerclic で別のショートカットを選んでください。右クリックの「Cerclic」は引き続き使えます。',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'または：右クリックして「その他のオプションを確認」から「Cerclic」を選択します。',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'または：右クリックして「Cerclic」を選択します。',
    # cerclic/app.py:915
    'Copie impossible': 'コピーできませんでした',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'ロック解除',
    # cerclic/app.py:966
    'Continuer': '続ける',
    # cerclic/app.py:971
    '« {name} » est protégé.': '「{name}」は保護されています。',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'PDF のパスワード',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': '自動起動がブロックされています',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': '組織の設定により、Windows の起動時にアプリを自動で起動することはできません。',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': '自動起動が Windows で無効になっています',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'タスク マネージャーで無効にされているため、Windows 側でしか有効に戻せません。「設定」>「アプリ」>「スタートアップ」で「Cerclic」をオンにしてください。',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'ショートカット {combo} は使用できません',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Cerclic で問題が発生しました',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': '詳細は {path} にあります',
    # cerclic/app.py:851
    'Fichier inaccessible': 'ファイルにアクセスできません',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'このファイルは通常のフォルダにありません（ZIP アーカイブ、スマートフォンなど）。フォルダにコピーしてから、もう一度お試しください。',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': '画像を読み込めません。',
    # cerclic/app.py:1224
    'Réessayer': '再試行',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': '{refused} は macOS または別のアプリですでに使用されています。ショートカットは {kept} のままです。',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': '{refused} は Windows または別のアプリですでに使用されています。ショートカットは {kept} のままです。',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': '後で',
    # cerclic/app.py:810
    'Ouvrir les réglages': '設定を開く',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'この種類のファイルに使えるアクションはありません',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'Cerclic は画像、PDF、ビデオ、オーディオを扱います。',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": '先にファイルを選択してください',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': '「{name}」のパスワードが正しくありません。もう一度お試しください。',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'トリミングすると最初のページしか残りません。すべてのページを残すには「PDF に変換」を使い、その PDF で「{action}」を使ってください。',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['「{name}」には {n} ページあります'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': '結果をどこに保存しますか？',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'エクスプローラーを再起動',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'アンインストーラーを表示',
    # cerclic/app.py:602
    'Ouvrir les applications': 'アプリの設定を開く',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'macOS または別のアプリがすでに使用しています。ショートカットは {kept} のままです。',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'Windows または別のアプリがすでに使用しています。ショートカットは {kept} のままです。',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'パスワードが正しくありません',
    # cerclic/app.py:975
    "Rien n'a été créé.": '何も作成されていません。',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": '圧縮すると最初のページしか残りません。すべてのページを残すには「PDF に変換」を使い、その PDF で「{action}」を使ってください。',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'SNS 用のサイズになるのは最初のページだけです。すべてのページを残すには「PDF に変換」を使ってください。',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': '開く',
    # cerclic/app.py:707
    'Changer de raccourci': 'ショートカットを変更',
    # cerclic/app.py:1081
    'Texte du filigrane': '透かしのテキスト',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': '各ページに斜めに表示されます。',
    # cerclic/app.py:1083
    'CONFIDENTIEL': '社外秘',
    # cerclic/app.py:1088
    'Mot de passe à mettre': '設定するパスワード',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": 'PDF を開くときに必要になります。元のファイルにはパスワードは設定されません。',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': '保護',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': '予期しないエラーが発生しました。もう一度お試しください。繰り返し発生する場合は、Cerclic のログ（cerclic.log）に詳細があります。',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'アクセスが拒否されました：ファイルが別のアプリで開かれているか、フォルダが保護されている可能性があります。',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': '名前またはパスが Windows には長すぎます：ファイル名を短くするか、階層の浅いフォルダに移動してください。',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'ファイルが見つかりません：移動または削除された可能性があります。',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'ファイルが大きすぎて、使用可能なメモリでは処理できません。',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'ディスクがいっぱいです。',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': '画像を読み込めないか、対応していない形式です。',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF が破損しているか、読み込めません。',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['「{action}」には {n} 個以上のファイルが必要です。'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'キャンセルされました',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '「{name}」が見つかりません：移動、名前の変更、削除のいずれかが行われたか、USB メモリが取り外された可能性があります。',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} 個のファイルが見つかりません：移動、名前の変更、削除のいずれかが行われた可能性があります。'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'この PDF はパスワードで保護されています。',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": '処理が突然停止しました：ファイルが破損している可能性があります。',
    # cerclic/paths.py:235
    'compressé': '圧縮',
    # cerclic/paths.py:235
    'redimensionné': 'サイズ変更',
    # cerclic/paths.py:236
    'pivoté': '回転',
    # cerclic/paths.py:236
    'rogné': 'トリミング',
    # cerclic/paths.py:236
    'miroir': '反転',
    # cerclic/paths.py:237
    'anonymisé': '匿名化',
    # cerclic/paths.py:237
    'assemblé': '結合',
    # cerclic/paths.py:237
    'fusionné': '結合',
    # cerclic/paths.py:238
    'réorganisé': '整理',
    # cerclic/paths.py:238
    'extrait': '抽出',
    # cerclic/paths.py:238
    'texte': 'テキスト',
    # cerclic/paths.py:239
    'filigrane': '透かし',
    # cerclic/paths.py:239
    'numéroté': 'ページ番号',
    # cerclic/paths.py:239
    'signé': '署名',
    # cerclic/paths.py:240
    'protégé': '保護',
    # cerclic/paths.py:240
    'déverrouillé': 'ロック解除',
    # cerclic/paths.py:240
    'son': '音声',
    # cerclic/paths.py:241
    'raccourci': 'カット',
    # cerclic/paths.py:241
    'sans son': '無音',
    # cerclic/paths.py:241
    'images': '画像',
    # cerclic/paths.py:242
    'pages': 'ページ',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': '同じサイズ',
    # cerclic/sizes.py:71
    'De {before} à {after}': '{before} から {after} に',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} バイト'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '{pct}% 減',
    # cerclic/sizes.py:64
    '{pct} % de plus': '{pct}% 増',
    # cerclic/system.py:17
    'Cmd': 'command',
    # cerclic/system.py:17
    'Ctrl': 'Ctrl',
    # cerclic/system.py:18
    'Suppr': 'Delete',
    # cerclic/system.py:19
    'Retour': 'return',
    # cerclic/system.py:19
    'Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:168
    'touche Mac\x04Touche {code}': 'キー {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'command + space で Spotlight が開きます。',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'option + command + space で Finder の検索が開きます。',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'control + space で入力ソースが切り替わります。',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'control + option + space で入力ソースが切り替わります。',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'control + command + space で絵文字と記号が開きます。',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'command + tab でアプリを切り替えます。',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'shift + command + tab でアプリを切り替えます。',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'option + command + esc でアプリを強制終了します。',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'shift + command + 3 でスクリーンショットを撮ります。',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'shift + command + 4 でスクリーンショットを撮ります。',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'shift + command + 5 でスクリーンショットのツールが開きます。',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'shift + command + 6 で Touch Bar のスクリーンショットを撮ります。',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'control + command + Q で画面をロックします。',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'shift + command + Q でログアウトします。',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'control + command + F でフルスクリーンにします。',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'option + command + D で Dock を非表示にします。',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'option + command + C で Finder のファイルのパス名をコピーします。',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'option + command + H でほかのアプリを非表示にします。',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'option + command + M ですべてのウインドウを Dock にしまいます。',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'option + command + W ですべてのウインドウを閉じます。',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'option + command + V で Finder でコピーしたファイルを移動します。',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'space',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'return',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': 'delete ⌦',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Échap': 'esc',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Début': 'home',
    # contexte : touche Mac | cerclic/mac/hotkey.py:71
    'touche Mac\x04Fin': 'end',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page préc.': 'page up',
    # contexte : touche Mac | cerclic/mac/hotkey.py:72
    'touche Mac\x04Page suiv.': 'page down',
    # contexte : touche Mac | cerclic/mac/hotkey.py:73
    'touche Mac\x04Aide': 'help',
    # contexte : touche Mac | cerclic/mac/hotkey.py:156, cerclic/mac/hotkey.py:163
    'touche Mac\x04Pavé {key}': 'テンキー {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'command、control、option、shift のあとに別のキーを追加してください。',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} はすでに macOS のショートカットとして使われています（「システム設定」>「キーボード」>「キーボードショートカット」）。別の組み合わせを選んでください。',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'shift + command + {key} は Finder ですでに使われています。別の文字を選ぶか、shift + command + space にしてください。',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": '組み合わせには command か control が必要です：option や shift だけのショートカットは macOS で使えません。',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'command と 1 つのキーの組み合わせは、すでにすべてのアプリで使われています（コピー、ペースト、保存など）。shift、option、control のいずれかを追加してください。例：shift + command + {key}',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'control + 矢印キーで操作スペースを切り替えます（Mission Control）。',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'control',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'shift',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'command',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'キャンセル',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'パスワードを表示',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'パスワードを非表示',
    # cerclic/ui/cards.py:238
    'Fermer': '閉じる',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'デスクトップ',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'ダウンロード',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'ピクチャ',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'ビデオ',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'ムービー',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'ミュージック',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'ドキュメント',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': '停止',
    # cerclic/ui/cards.py:299
    'En cours': '処理中',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': '停止しています…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['ファイルを削除しました'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": '元のファイルはそのままです。',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} 個のファイルを作成しました'],
    # cerclic/ui/cards.py:366
    'Dossier': 'フォルダ',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': '削除',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'Cerclic が作成したファイルを削除します（元のファイルはそのままです）',
    # cerclic/ui/cards.py:417
    'Suppression impossible': '削除できませんでした',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'ファイルが別のアプリで開かれている可能性があります：そのアプリを閉じてから、もう一度お試しください。',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': '「{folder}」に保存',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} 個のファイルをスキップしました。例：{example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": '停止しました：何も作成されていません。',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '合計 {size} · 「{folder}」に保存',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · 「{folder}」に保存',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title}に失敗しました',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': '不明なエラーです。',
    # cerclic/ui/compress_editor.py:36
    'Légère': '弱め',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': '標準',
    # cerclic/ui/compress_editor.py:36
    'Forte': '強め',
    # cerclic/ui/compress_editor.py:37
    'Maximale': '最大',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}% · {n} 色'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': '画像を 220 dpi に：印刷してもとても鮮明',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": '画像を 150 dpi に：画面でも印刷でも鮮明',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": '画像を 110 dpi に：画面表示向け',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': '画像を 80 dpi に：最も軽量、画像はやや粗くなります',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": '最大 1080p、非常に高画質',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": '最大 1080p、高画質',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p：スマートフォンやメッセージ向け',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p：最も軽量',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbps：音楽、非常に高音質',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbps：音楽',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbps：音声、スマートフォンで聴く音楽',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbps：音声',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}% · ロスレス',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': '読み込み中…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': '元は {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': '効果なし',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': '効果なし',
    # cerclic/ui/compress_editor.py:203
    'Impossible': '不可',
    # cerclic/ui/compress_editor.py:203
    'impossible': '不可',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': '計算中…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': '画質を選択 · {key} で圧縮',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': '圧縮の強さを選択 · {key} で圧縮',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': '圧縮',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': '画質',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': '圧縮',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'ポインタを画像に置くと 100% で表示',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'ポインタを画像に置くと拡大表示',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF：設定なし',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['プレビュー：{name} · {n} 枚の合計（{sampled} 枚から推定）'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['プレビュー：{name} · {n} 枚の合計'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': '軽くなりません',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': '圧縮できません。',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} 枚をスキップ'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'もっと強い圧縮を試してください。',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': '元のサイズ：{size} · 画質を下げてください',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': '元のサイズ：{size} · もっと強く圧縮してください',
    # cerclic/ui/crop_editor.py:27
    'Libre': '自由',
    # cerclic/ui/crop_editor.py:27
    'Original': '元の比率',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': '角をドラッグ · {key} でトリミング',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'トリミング',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'すべてのページ',
    # cerclic/ui/crop_editor.py:469
    'Image entière': '画像全体',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": '画像全体に戻す',
    # cerclic/ui/crop_editor.py:589
    '{width} × {height} cm': '{width} × {height} cm',
    # cerclic/ui/crop_editor.py:593, cerclic/ui/crop_editor.py:448, cerclic/ui/social_editor.py:43
    '{width} × {height} px': '{width} × {height} px',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:103
    'touche du Mac\x04Retour': 'return',
    # contexte : touche | cerclic/ui/editor_base.py:103
    'touche\x04Entrée': 'Enter',
    # contexte : touche | cerclic/ui/editor_base.py:108
    'touche\x04Suppr': 'Delete',
    # contexte : touche du Mac | cerclic/ui/editor_base.py:113
    'touche du Mac\x04Cmd': 'command',
    # contexte : touche | cerclic/ui/editor_base.py:113
    'touche\x04Ctrl': 'Ctrl',
    # cerclic/ui/editor_base.py:205
    'Fermer (Échap)': '閉じる（Esc）',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'ドラッグで並べ替え · {key} で削除',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': '左に回転',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': '右に回転（{key} + R）',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': '前へ移動（{key} + {arrow}）',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': '後ろへ移動（{key} + {arrow}）',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': '選択したページを抽出',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': '選択したページだけの新しい PDF を作成します',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'リセット',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': '保存',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{n} / {count} ページを選択'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} ページ'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'その他',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ 戻る',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category}（{n}）',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'その他のツール',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': '一般',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'キーボードショートカット',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': '右クリック',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': '作成したファイル',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': '署名',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': '情報',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'バージョン {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'エクスプローラーまたはデスクトップでファイルを 1 つ以上選択してから、{combo} を押してください。',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': '変更',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'デフォルト',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'キーの組み合わせを押してください…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': '確認中…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'バージョン {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'Finder またはデスクトップでファイルを 1 つ以上選択してから、{combo} を押してください。',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'ホイールを開く',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'ファイルを右クリックして「クイックアクション」から「Cerclic」を選択します。または「このアプリケーションで開く」から Cerclic を選択します。',
    # cerclic/ui/settings_window.py:642
    'Démarrage': '起動',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'Cerclic を終了します。再度起動するには、「アプリケーション」フォルダから開いてください。',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': '言語',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": '自動（システムの言語）',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'Cerclic をアンインストール',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": '右クリックメニューとログイン項目から Cerclic を削除して、終了しますか？',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'アンインストール',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'キーの組み合わせで、選択したファイルのホイールを開きます。',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'キーボードでホイールを開く',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': 'ファイルの右クリックメニューに「Cerclic」を表示します。',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '右クリックに「Cerclic」を表示',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": '元のファイルが変更されることはありません：アクションごとに新しいファイルが作成されます。',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': '保存先',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": '元のファイルと同じ場所',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': '同じフォルダに保存します。たとえば写真がデスクトップにあれば、デスクトップに保存されます。おすすめの設定です。',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': '指定したフォルダ',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': '作成したファイルをすべて同じ場所に保存します。',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': '毎回確認する',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'ファイルを作成する前に、Cerclic が保存先のフォルダを確認します。',
    # cerclic/ui/settings_window.py:828
    'Choisir…': '選択…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': '作成したファイルの保存先',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'PDF にワンステップで署名できます。署名はこのコンピュータ内にだけ保存されます。',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': '手書き…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': '写真を読み込む…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': '消去',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'ファイルサイズと鮮明さのバランスを決めます。',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}%',
    # cerclic/ui/settings_window.py:993
    'Voir': '表示',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': '署名の写真を選択',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'ショートカットは変更されていません。',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': '例：shift + command + space、control + option + X。esc でキャンセルします。',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': '例：Ctrl + Alt + Space、Ctrl + Shift + X、Win + Shift + C。Esc でキャンセルします。',
    # cerclic/ui/settings_window.py:313
    'Plus léger': '軽量',
    # cerclic/ui/settings_window.py:315
    'Plus net': '高画質',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'Cerclic へようこそ',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": '変更はすぐに適用されます。',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'ホイールを開く 2 つの方法、起動、言語。',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'ホイールを開く 3 つの方法、起動、言語。',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'キーボードで',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Shift キーを押しながらファイルを右クリックして、「Cerclic」を選択します。Shift なしの場合は「その他のオプションを確認」から選びます。',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'ファイルを右クリックして「Cerclic」を選択します。',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'マウスで',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'Mac の起動時に Cerclic を開く',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'Windows の起動時に Cerclic を開く',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'おすすめ：必要なときにすぐホイールを使えます。',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'Cerclic を終了します。再度起動するには、スタート メニューから開いてください。',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'Cerclic を終了します。再度起動するには、デスクトップまたはスタート メニューから開いてください。',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'Cerclic を停止',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": '次に起動するまで、ホイールは開かなくなります。',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'Cerclic のメニュー、ウィンドウ、メッセージの言語です。',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": '「変更」をクリックして、キーの組み合わせを押してください。macOS または別のアプリですでに使われている場合は、Cerclic がお知らせし、前のショートカットをそのまま使います。',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'プログラム可能なボタン付きのマウスをお使いですか？ボタンに F13～F20 のいずれかのキーを割り当ててから、ここでそのキーを選んでください：そのボタンをクリックするとホイールが開きます。',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": '「変更」をクリックして、キーの組み合わせを押してください。Windows または別のアプリですでに使われている場合は、Cerclic がお知らせし、前のショートカットをそのまま使います。',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'プログラム可能なボタン付きのマウスをお使いですか？ボタンに F13～F24 のいずれかのキーを割り当ててから、ここでそのキーを選んでください：そのボタンをクリックするとホイールが開きます。',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'アクセス許可',
    # cerclic/ui/settings_window.py:745
    'Réglages…': '設定…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': '完全な右クリックメニュー',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': '「クイックアクション」に表示されない場合は、ファイルを右クリックして「クイックアクション」>「カスタマイズ」を選び、「Cerclic」にチェックを入れてください。「このアプリケーションで開く」からもいつでも使えます。',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': '画像の圧縮',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': '「圧縮」で最初に選ばれる設定です。「圧縮」では仕上がりのサイズが表示され、最後に選んだ設定が記憶されます。',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'ほかのアクションで作成される JPG',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': 'トリミング、回転、変換など。90% なら画質の劣化は目立ちません。',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'トリミング、署名、圧縮、変換、SNS 用のサイズ変更などを、ほかのアプリを開かずにワンステップで。',
    # cerclic/ui/settings_window.py:991
    'Journal': 'ログ',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": '問題が起きたときに、このファイルで原因を調べられます。',
    # cerclic/ui/settings_window.py:995
    'Licences': 'ライセンス',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'Cerclic が使用しているオープンソースのコンポーネントとそのライセンス。',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'アンインストール…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'まだ署名がありません：手書きするか、写真を読み込んでください。ここで設定しなくても、初めて署名するときに求められます。',
    # cerclic/ui/settings_window.py:1130
    'Images': '画像',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': '設定：キーボード',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': '設定：マウス',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'ドラッグで',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'ログイン時に Cerclic を開く',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'Finder またはデスクトップで選択したファイルに使えます。',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'エクスプローラーまたはデスクトップで選択したファイルに使えます。',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Finder の選択項目を読み取る',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': '初回は、Cerclic に Finder の制御を許可するか macOS が確認します：許可してください。Cerclic が読み取るのは選択したファイルだけです。',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': 'Finder の右クリックに「Cerclic」を表示',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'Finder とデスクトップで、ファイルの「クイックアクション」メニューに表示します。',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": '「その他のオプションを確認」を経由せずに、完全なメニューを表示します。Cerclic がエクスプローラーの再起動を提案します。',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'ヒント：設定を変えなくても、Shift キーを押しながらファイルを右クリックすると、「Cerclic」を含む完全なメニューが直接開きます。',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'フォルダが選択されていません。',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": '右クリックメニューとログイン項目から「Cerclic」を削除して終了します。そのあと、Cerclic.app をゴミ箱に入れてください。',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'ショートカットはオフです：右クリックの「Cerclic」は引き続き使えます。',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'ショートカットはオフです。',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic はバックグラウンドで動作しています：アイコンは画面上部のメニューバーにあります。ホイールを開くお好みの方法を下で選んでください。',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic はバックグラウンドで動作しています：アイコンは時計の近くにあります（小さな矢印 ^ の中に隠れていることもあります）。ホイールを開くお好みの方法を下で選んでください。',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": 'Cerclic のアイコン（「アプリケーション」フォルダまたは Dock 内）にファイルをドラッグします。',
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": 'Cerclic のアイコンにファイルをドラッグします。',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': 'ファイルの右クリックに「Cerclic」を表示',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'エクスプローラーとデスクトップで、画像、PDF、ビデオ、オーディオのメニューの一番上に表示します。',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'エクスプローラー、デスクトップ、「開く」と「保存」のウィンドウで、画像、PDF、ビデオ、オーディオに表示します。',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'ファイル名は、元の名前に変更内容を付けたものです。たとえば photo.jpg の横に photo (圧縮).jpg が作成されます。同じ名前がすでにある場合は Cerclic が番号を付けるため、上書きされることはありません。',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": '結果が気に入らない場合は、カードの「削除」ですぐに消せます。',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': '指定したフォルダ：{folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": '指定したフォルダ：まだ選択されていません。',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": '白い紙に書いた署名の写真があれば十分です：Cerclic が紙の部分を透明にし、インクだけを残します。',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': '署名するには：PDF を右クリックするかショートカットを使い、「署名」を選びます。署名を配置して {key} を押してください。',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': '誤って拒否した場合は、「オートメーション」で Cerclic の下にある「Finder」をオンにしてください。',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ Mac 全体で有効です。',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ Windows 全体で有効です。',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'macOS または別のアプリがこの組み合わせをすでに使用しています。「変更」で別の組み合わせを選んでください。',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'Windows または別のアプリがこの組み合わせをすでに使用しています。「変更」で別の組み合わせを選んでください。',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'この画像に署名の線が見つかりません。',
    # cerclic/ui/signature.py:196
    'Ta signature': 'あなたの署名',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': '次回以降のために保存されます',
    # cerclic/ui/signature.py:200
    'Importer…': '読み込む…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': '白い紙に書いた署名の写真',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': '署名をドラッグ · 角を引いてサイズ変更 · {key} で署名',
    # cerclic/ui/signature.py:413
    'Changer': '変更',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': '別の署名を手書きするか読み込みます',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': '署名',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'ページ {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'ここに署名',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': '署名の画像を選択',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': '画像 ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': '枠いっぱい',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": '画像で枠全体を埋め、はみ出た部分はカットされます。\nドラッグで残す部分を選び、スクロールでズームします。',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'ぼかし背景',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": '画像全体を表示し、何もカットしません。\n周囲：同じ画像をぼかして表示。',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': '白背景',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": '画像全体を表示し、何もカットしません。\n周囲：白。',
    # cerclic/ui/social_editor.py:37
    'Fond noir': '黒背景',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": '画像全体を表示し、何もカットしません。\n周囲：黒。',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': '前のファイル',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': '次のファイル',
    # cerclic/ui/social_editor.py:448
    'Créer': '作成',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'ドラッグしてズーム · {key} で作成',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'カットなし · {key} で作成',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': '残す部分が指定のサイズより小さいため、拡大されて少しぼやけます。',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'ビデオが指定のサイズより小さいため、拡大されて少しぼやけます。',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": '画像が指定のサイズより小さいため、拡大されて少しぼやけます。',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': '長さ不明',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'ハンドルをドラッグ · {key} で短くする',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': '短くする',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': '長さ {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': '長さを読み取れません：ファイルが破損していませんか？',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': '開始 {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': '終了 {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['「{name}」には {n} ページあります：最初のページしか残りません。すべてのページを残すには「{action}」を使ってください。'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'すでに {format} です。',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'この画像はすでに十分に圧縮されています。',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'トリミングする範囲が空です。',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": '枠が画像全体を覆っているため、トリミングするものがありません。',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': '画像が 2 枚以上必要です。',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': '画像の結合',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'この画像には個人情報が含まれていません。',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': '画像 {i} / {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'PDF に変換',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": '画像はすでに {size} px 以下です。',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': '画像を読み込めません：{name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '「{name}」はパスワードで保護されています。',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'パスワードが正しくありません。',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'Word への変換',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'このファイルは PDF ではありません：{name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': '画像がありません。',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': '結合するには PDF が 2 つ以上必要です。',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': '残すページがありません。',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": 'この PDF にはテキストがありません：スキャンした画像の可能性があります。',
    # cerclic/actions/pdf.py:570
    'Vérification': '確認中',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'この PDF はすでに十分に圧縮されています。',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': '枠がページ全体を覆っているため、トリミングするものがありません。',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': '透かしのテキストが空です。',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': '保存された署名がありません。',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'パスワードが空です。',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": 'この PDF にはすでにパスワードがあります。別のパスワードを設定するには、先に今のパスワードを解除してください（「{more}」>「{action}」）。',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'この PDF は保護されていません。',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF が破損しているか、読み込めません：{name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'ページ {i} / {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i} / {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'この PDF は 1 ページしかありません。',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'この PDF にそのページが見つかりません。',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'ページは変更されていません。',
    # cerclic/actions/registry.py:34
    'Image': '画像',
    # cerclic/actions/registry.py:36
    'Vidéo': 'ビデオ',
    # cerclic/actions/registry.py:37
    'Son': 'オーディオ',
    # cerclic/actions/registry.py:136
    'Droite': '右回り',
    # cerclic/actions/registry.py:137
    'Gauche': '左回り',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'SNS',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': '回転',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'サイズ変更',
    # cerclic/actions/registry.py:213
    'Convertir': '変換',
    # cerclic/actions/registry.py:223
    'Copier': 'コピー',
    # cerclic/actions/registry.py:226
    'Assembler': '並べる',
    # cerclic/actions/registry.py:233
    'Anonymiser': '匿名化',
    # cerclic/actions/registry.py:256
    'Fusionner': '結合',
    # cerclic/actions/registry.py:260
    'Pages': 'ページ',
    # cerclic/actions/registry.py:266
    'En Word': 'Word に変換',
    # cerclic/actions/registry.py:270
    'En images': '画像に変換',
    # cerclic/actions/registry.py:276
    'Diviser': '分割',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': '透かし',
    # cerclic/actions/registry.py:290
    'Numéroter': 'ページ番号',
    # cerclic/actions/registry.py:295
    'En texte': 'テキストに変換',
    # cerclic/actions/registry.py:326
    'En MP4': 'MP4 に変換',
    # cerclic/actions/registry.py:329
    'En GIF': 'GIF に変換',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': '音声を抽出',
    # cerclic/actions/registry.py:336
    'Couper le son': '消音',
    # cerclic/actions/registry.py:352
    'En MP3': 'MP3 に変換',
    # cerclic/actions/registry.py:141
    'Miroir': '左右反転',
    # cerclic/actions/registry.py:191
    'Garder une partie': '一部を残す',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'トリミング',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'インスタ、ストーリーズ、スマホ、PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'SNS サイズ変換',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': '回転・反転',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': '回転',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'ピクセル数を減らす',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'サイズ変更',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': '画素数はそのまま軽量化',
    # cerclic/actions/registry.py:216
    'Changer de format': '形式を変更',
    # cerclic/actions/registry.py:216
    'Conversion': '変換',
    # cerclic/actions/registry.py:222
    'Une page par image': '1 画像につき 1 ページ',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'PDF の作成',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': '好きな場所に貼り付け',
    # cerclic/actions/registry.py:225
    'Copie': 'コピー',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': '複数を 1 枚に',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'GPS・カメラ・日時を削除',
    # cerclic/actions/registry.py:237
    'Anonymisation': '匿名化',
    # cerclic/actions/registry.py:245
    'Placer ta signature': '署名を配置',
    # cerclic/actions/registry.py:250
    'Couper les marges': '余白をカット',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': '送りやすく軽量化',
    # cerclic/actions/registry.py:259
    'Un seul PDF': '1 つの PDF に',
    # cerclic/actions/registry.py:259
    'Fusion': 'PDF の結合',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': '並べ替え・回転・削除',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'ページの整理',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'Word で編集可能',
    # cerclic/actions/registry.py:273
    'Une image par page': '1 ページにつき 1 画像',
    # cerclic/actions/registry.py:273
    'Conversion en images': '画像への変換',
    # cerclic/actions/registry.py:279
    'Un PDF par page': '1 ページにつき 1 PDF',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'ページ分割',
    # cerclic/actions/registry.py:289
    'Un texte en travers': '斜めにテキストを入れる',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'ページ下部に番号',
    # cerclic/actions/registry.py:294
    'Numérotation': 'ページ番号の追加',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'テキストを .txt に',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'テキストの抽出',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'パスワードを設定',
    # cerclic/actions/registry.py:304
    'Protection': 'PDF の保護',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'パスワードを解除',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'ロック解除',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': '一部分を残す',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'カット',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'リール、TikTok、ショート、PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'MP4 で軽量化',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'どこでも再生可能',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'MP4 への変換',
    # cerclic/actions/registry.py:331
    'Une animation sans son': '音声なしのアニメーション',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'GIF の作成',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': '音声を MP3 で',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': '音声の抽出',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': '音声なしのビデオ',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': '音声の削除',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": '向きを直す',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'MP3 への変換',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'MP3 で軽量化',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'ファイル {i} / {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '「{name}」：{error}',
    # cerclic/actions/registry.py:204
    '50 %': '50%',
    # cerclic/actions/registry.py:230
    'Côte à côte': '横に並べる',
    # cerclic/actions/registry.py:231
    'En colonne': '縦に並べる',
    # cerclic/actions/registry.py:232
    'En grille': 'グリッド',
    # cerclic/actions/social.py:46
    'Carré': '正方形',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Instagram、Facebook、LinkedIn の投稿',
    # cerclic/actions/social.py:47
    'carré': '正方形',
    # cerclic/actions/social.py:48
    'Portrait': '縦長',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Instagram、Facebook の投稿（フィードで最も大きく表示）',
    # cerclic/actions/social.py:50
    'portrait': '縦長',
    # cerclic/actions/social.py:51
    'Grille': 'グリッド',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram のプロフィールグリッドにぴったりの形',
    # cerclic/actions/social.py:52
    'grille': 'グリッド',
    # cerclic/actions/social.py:53
    'Story': 'ストーリーズ',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'スマホの全画面：ストーリーズ、リール、TikTok、YouTube ショート',
    # cerclic/actions/social.py:55
    'story': 'ストーリーズ',
    # cerclic/actions/social.py:56
    'Paysage': '横長',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'パソコンの画面：YouTube、プレゼン、X',
    # cerclic/actions/social.py:57
    'paysage': '横長',
    # cerclic/actions/social.py:58
    'Bannière': 'バナー',
    # cerclic/actions/social.py:58
    '1,91:1': '1.91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'Facebook、LinkedIn、X で共有するリンクや横長の画像',
    # cerclic/actions/social.py:59
    'bannière': 'バナー',
    # cerclic/actions/social.py:239
    'Format {name}': '{name}に変換',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'この画像はすでに {size} です。',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'ビデオのサイズを読み取れません：ファイルが破損していませんか？',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'このビデオはすでに {size} です。',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': '処理に失敗しました：ファイルが破損しているか、一般的でない形式の可能性があります。',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': 'ffmpeg が見つかりません：Cerclic を再インストールしてください。',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'ビデオが破損しているか、対応していない形式です。',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'アクセスが拒否されました：ファイルが別のアプリで開かれている可能性があります。',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'カット中',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'このファイルには映像がありません。',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'このビデオはすでに十分に圧縮されています：もっと強い圧縮を試してください。',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'GIF にするにはビデオが長すぎます（2 分を超えると数百 MB になります）。まず「{action}」で一部分だけ残してください。',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'GIF への変換',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'このビデオには音声がありません。',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': '残す部分が短すぎます。',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': '選択した部分がファイル全体になっています。',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'このファイルには音声がありません。',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'プレビューできません。',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'このオーディオはすでに軽量です：もっと強い圧縮を試してください。',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'このファイルには音声だけで映像がありません：MP3 にするには「{action}」を使ってください。',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'プレビューの準備に時間がかかりすぎています。',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4 でウィンドウを閉じます。',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab でウィンドウを切り替えます。',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc でウィンドウを切り替えます。',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Space でウィンドウ メニューが開きます。',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc でスタート メニューが開きます。',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'Ctrl + Alt + Delete は Windows 専用です。',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'Ctrl + Shift + Esc でタスク マネージャーが開きます。',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'キー {code}',
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
    'touche Windows\x04Page préc.': 'PgUp',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Page suiv.': 'PgDn',
    # contexte : touche Windows | cerclic/win/hotkey.py:45
    'touche Windows\x04Pause': 'Pause',
    # contexte : touche Windows | cerclic/win/hotkey.py:46
    'touche Windows\x04Impr. écran': 'PrtSc',
    # contexte : touche Windows | cerclic/win/hotkey.py:82, cerclic/win/hotkey.py:84
    'touche Windows\x04Pavé {key}': 'テンキー {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Ctrl、Alt、Shift、Win のあとに別のキーを追加してください。',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': '{key} は Windows やアプリですでに使われています（ヘルプ、名前の変更、最新の情報に更新、スペルチェックなど）。たとえば Ctrl + Alt を追加して、Ctrl + Alt + {key} にしてください。',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt とテンキーの組み合わせは文字の入力に使われます（Alt + 0201 = É）。別の組み合わせを選んでください。',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": '組み合わせには Ctrl、Alt、Win のいずれかが必要です（そうしないと、このキーで文字を入力できなくなります）。',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Shift',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt と 1 つのキーの組み合わせは、多くのアプリですでに使われています（アプリのメニュー）。Shift か Ctrl を追加してください。例：Alt + Shift + {key}',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'この組み合わせは AltGr で文字（@、€、#、œ など）を入力するのに使われます。別の組み合わせを選んでください。',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl と 1 つのキーの組み合わせは、多くのアプリですでに使われています（太字、コピー、貼り付け、保存など）。Shift か Alt を追加してください。例：Ctrl + Shift + {key}',
}
