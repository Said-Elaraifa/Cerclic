"""Cerclic, العربية. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} ملف', 'ملف واحد', 'ملفان', '{n} ملفات', '{n} ملفًا', '{n} ملف'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": 'تم الحفظ في «{where}»: المجلد الأصلي محمي.',
    # cerclic/app.py:92
    'Téléchargements': 'التنزيلات',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'يستخدمه Windows أو تطبيق آخر بالفعل. اختر اختصارًا آخر في Cerclic.',
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'انقر بزر الماوس الأيمن، ثم «Cerclic»',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": 'تعذّر العثور على المجلد المختار: تم الحفظ بجانب الملف الأصلي.',
    # cerclic/app.py:459
    'Ouvrir Cerclic': 'فتح Cerclic',
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': 'إنهاء Cerclic',
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'يستخدمه Windows أو تطبيق آخر بالفعل. اختر اختصارًا آخر في Cerclic؛ لا يزال «Cerclic» يعمل من قائمة النقر بالزر الأيمن.',
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": 'يستخدمه macOS أو تطبيق آخر بالفعل. اختر اختصارًا آخر في Cerclic.',
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'انقر بزر الماوس الأيمن، ثم الإجراءات السريعة، ثم «Cerclic»',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'انقر بزر الماوس الأيمن، ثم «إظهار المزيد من الخيارات»، ثم «Cerclic»',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': 'اسمح لـ Cerclic بقراءة العناصر المحددة',
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': 'إعدادات النظام، ثم الخصوصية والأمن، ثم الأتمتة: حدد «Finder» أسفل Cerclic. يعمل النقر بزر الماوس الأيمن، ثم الإجراءات السريعة، ثم «Cerclic» من دون ذلك.',
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'انقر على صورة أو ملف PDF أو فيديو أو ملف صوتي في Finder أو على سطح المكتب، ثم اضغط على {combo}.',
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'انقر على صورة أو ملف PDF أو فيديو أو ملف صوتي في مستكشف الملفات أو على سطح المكتب، ثم اضغط على {combo}.',
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'أو: انقر بزر الماوس الأيمن، ثم الإجراءات السريعة، ثم «Cerclic».',
    # cerclic/app.py:919
    'Image copiée': 'تم نسخ الصورة',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'الصقها حيث تريد باستخدام {key} + V.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'حسنًا',
    # cerclic/app.py:1253
    'Menu complet activé': 'تم تفعيل القائمة الكاملة',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'يُطبَّق عند إعادة تشغيل مستكشف الملفات. ستُغلق نوافذ المجلدات المفتوحة.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'تمت استعادة قائمة Windows 11',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'يُطبَّق عند إعادة تشغيل مستكشف الملفات.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'نسختان مثبتتان من Cerclic',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": 'لا تزال نسخة Cerclic المثبتة من خارج Microsoft Store موجودة. لكي يظهر «Cerclic» مرة واحدة فقط في قائمة النقر بالزر الأيمن ويكون لديك اختصار واحد، أزلها: «إظهار برنامج إلغاء التثبيت»، ثم انقر نقرًا مزدوجًا على «unins000».',
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": 'لا تزال نسخة Cerclic المثبتة من خارج Microsoft Store موجودة. لكي يكون لديك «Cerclic» واحد فقط، ألغِ تثبيتها من التطبيقات المثبتة: إنها نسخة Cerclic التي لا تحتوي قائمتها على «خيارات متقدمة».',
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": 'يستخدمه macOS أو تطبيق آخر بالفعل. اختر اختصارًا آخر في Cerclic؛ لا يزال «Cerclic» يعمل من قائمة النقر بالزر الأيمن.',
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'أو: انقر بزر الماوس الأيمن، ثم «إظهار المزيد من الخيارات»، ثم «Cerclic».',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'أو: انقر بزر الماوس الأيمن، ثم «Cerclic».',
    # cerclic/app.py:915
    'Copie impossible': 'تعذّر النسخ',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'إلغاء القفل',
    # cerclic/app.py:966
    'Continuer': 'متابعة',
    # cerclic/app.py:971
    '« {name} » est protégé.': '«{name}» محمي.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'كلمة سر ملف PDF',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'التشغيل مع Windows محظور',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': 'لا تسمح مؤسستك للتطبيقات بالتشغيل مع بدء Windows.',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': 'التشغيل مع Windows معطّل في Windows',
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': 'تم تعطيله في إدارة المهام: لا يمكن إعادة تفعيله إلا من Windows. في الإعدادات، ثم التطبيقات، ثم بدء التشغيل، فعّل «Cerclic».',
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': 'الاختصار {combo} غير متاح',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'واجه Cerclic مشكلة',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'التفاصيل في {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': 'تعذّر الوصول إلى الملف',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'هذا الملف ليس في مجلد عادي (أرشيف ZIP، هاتف…). انسخه إلى مجلد، ثم أعد المحاولة.',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': 'تعذّرت قراءة الصورة.',
    # cerclic/app.py:1224
    'Réessayer': 'إعادة المحاولة',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': 'الاختصار {refused} مستخدم بالفعل من قِبل macOS أو تطبيق آخر. يبقى اختصارك {kept}.',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': 'الاختصار {refused} مستخدم بالفعل من قِبل Windows أو تطبيق آخر. يبقى اختصارك {kept}.',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'لاحقًا',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'فتح الإعدادات',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'لا توجد إجراءات لهذا النوع من الملفات',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': 'يعمل Cerclic على الصور وملفات PDF ومقاطع الفيديو والملفات الصوتية.',
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'حدد ملفًا أولًا',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': 'كلمة السر غير صحيحة لـ «{name}». أعد المحاولة.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'لن يحتفظ الاقتصاص إلا بالأولى. استخدم «إلى PDF» للاحتفاظ بها كلها، ثم «{action}» على ملف PDF.',
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['يحتوي «{name}» على {n} صفحة', 'يحتوي «{name}» على صفحة واحدة', 'يحتوي «{name}» على صفحتين', 'يحتوي «{name}» على {n} صفحات', 'يحتوي «{name}» على {n} صفحة', 'يحتوي «{name}» على {n} صفحة'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': 'أين تريد حفظ النتيجة؟',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": 'إعادة تشغيل مستكشف الملفات',
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'إظهار برنامج إلغاء التثبيت',
    # cerclic/app.py:602
    'Ouvrir les applications': 'فتح التطبيقات',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'يستخدمه macOS أو تطبيق آخر بالفعل. يبقى اختصارك {kept}.',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'يستخدمه Windows أو تطبيق آخر بالفعل. يبقى اختصارك {kept}.',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'كلمة السر غير صحيحة',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'لم يتم إنشاء أي شيء.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": 'لن يحتفظ الضغط إلا بالأولى. استخدم «إلى PDF» للاحتفاظ بها كلها، ثم «{action}» على ملف PDF.',
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': 'لن يُطبَّق المقاس إلا على الأولى. استخدم «إلى PDF» للاحتفاظ بها كلها.',
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'فتح',
    # cerclic/app.py:707
    'Changer de raccourci': 'تغيير الاختصار',
    # cerclic/app.py:1081
    'Texte du filigrane': 'نص العلامة المائية',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'سيُكتب بشكل قُطري على كل صفحة.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'سري',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'كلمة السر الجديدة',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": 'ستُطلب لفتح ملف PDF. يبقى الملف الأصلي بلا كلمة سر.',
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'حماية',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'خطأ غير متوقع. أعد المحاولة؛ وإذا تكرر ذلك، فالتفاصيل في سجل Cerclic (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'تم رفض الوصول: ربما الملف مفتوح في تطبيق آخر، أو المجلد محمي.',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'الاسم أو المسار طويل جدًا بالنسبة لـ Windows: أعد تسمية الملف باسم أقصر، أو انقله إلى مجلد أقل عمقًا.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'تعذّر العثور على الملف: ربما تم نقله أو حذفه.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'الملف كبير جدًا بالنسبة للذاكرة المتاحة.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'القرص ممتلئ.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': 'صورة غير قابلة للقراءة أو تنسيق غير مدعوم.',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'ملف PDF تالف أو غير قابل للقراءة.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: يلزم {n} ملف على الأقل.', '{action}: يلزم ملف واحد على الأقل.', '{action}: يلزم ملفان على الأقل.', '{action}: يلزم {n} ملفات على الأقل.', '{action}: يلزم {n} ملفًا على الأقل.', '{action}: يلزم {n} ملف على الأقل.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'تم الإلغاء',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": 'لم يعد «{name}» موجودًا: تم نقله أو تغيير اسمه أو حذفه (أو فُصلت ذاكرة USB).',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['لم يعد {n} ملف موجودًا: تم نقلها أو تغيير أسمائها أو حذفها.', 'لم يعد ملف واحد موجودًا: تم نقله أو تغيير اسمه أو حذفه.', 'لم يعد ملفان موجودين: تم نقلهما أو تغيير اسميهما أو حذفهما.', 'لم تعد {n} ملفات موجودة: تم نقلها أو تغيير أسمائها أو حذفها.', 'لم يعد {n} ملفًا موجودًا: تم نقلها أو تغيير أسمائها أو حذفها.', 'لم يعد {n} ملف موجودًا: تم نقلها أو تغيير أسمائها أو حذفها.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'ملف PDF هذا محمي بكلمة سر.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": 'توقفت المعالجة فجأة: ربما الملف تالف.',
    # cerclic/paths.py:235
    'compressé': 'مضغوط',
    # cerclic/paths.py:235
    'redimensionné': 'معدل الحجم',
    # cerclic/paths.py:236
    'pivoté': 'مدور',
    # cerclic/paths.py:236
    'rogné': 'مقتطع',
    # cerclic/paths.py:236
    'miroir': 'معكوس',
    # cerclic/paths.py:237
    'anonymisé': 'مخفي الهوية',
    # cerclic/paths.py:237
    'assemblé': 'مجمع',
    # cerclic/paths.py:237
    'fusionné': 'مدمج',
    # cerclic/paths.py:238
    'réorganisé': 'معاد ترتيبه',
    # cerclic/paths.py:238
    'extrait': 'مستخرج',
    # cerclic/paths.py:238
    'texte': 'نص',
    # cerclic/paths.py:239
    'filigrane': 'علامة مائية',
    # cerclic/paths.py:239
    'numéroté': 'مرقم',
    # cerclic/paths.py:239
    'signé': 'موقّع',
    # cerclic/paths.py:240
    'protégé': 'محمي',
    # cerclic/paths.py:240
    'déverrouillé': 'غير مقفل',
    # cerclic/paths.py:240
    'son': 'صوت',
    # cerclic/paths.py:241
    'raccourci': 'مختصر',
    # cerclic/paths.py:241
    'sans son': 'بلا صوت',
    # cerclic/paths.py:241
    'images': 'صور',
    # cerclic/paths.py:242
    'pages': 'صفحات',
    # cerclic/sizes.py:21
    '{size} To': '{size} ت.ب',
    # cerclic/sizes.py:65
    'même taille': 'الحجم نفسه',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'من {before} إلى {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} ك.ب',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} م.ب',
    # cerclic/sizes.py:20
    '{size} Go': '{size} غ.ب',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} بايت', '{n} بايت', '{n} بايت', '{n} بايت', '{n} بايت', '{n} بايت'],
    # cerclic/sizes.py:62
    '{pct} % de moins': 'أصغر بنسبة {pct}%',
    # cerclic/sizes.py:64
    '{pct} % de plus': 'أكبر بنسبة {pct}%',
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
    'touche Mac\x04Touche {code}': 'المفتاح {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': 'الاختصار Cmd + مسافة يفتح Spotlight.',
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'الاختصار Option + Cmd + مسافة يفتح البحث في Finder.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'الاختصار Ctrl + مسافة يغيّر لغة لوحة المفاتيح.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'الاختصار Ctrl + Option + مسافة يغيّر لغة لوحة المفاتيح.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'الاختصار Ctrl + Cmd + مسافة يفتح الرموز التعبيرية.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'الاختصار Cmd + Tab ينتقل من تطبيق إلى آخر.',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'الاختصار Shift + Cmd + Tab ينتقل من تطبيق إلى آخر.',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'الاختصار Option + Cmd + Esc يفرض إنهاء تطبيق.',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'الاختصار Shift + Cmd + 3 يلتقط لقطة شاشة.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'الاختصار Shift + Cmd + 4 يلتقط لقطة شاشة.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'الاختصار Shift + Cmd + 5 يفتح أداة لقطة الشاشة.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': 'الاختصار Shift + Cmd + 6 يلتقط لقطة لشريط Touch Bar.',
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'الاختصار Ctrl + Cmd + Q يقفل الشاشة.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'الاختصار Shift + Cmd + Q يسجّل الخروج.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'الاختصار Ctrl + Cmd + F ينتقل إلى ملء الشاشة.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': 'الاختصار Option + Cmd + D يُخفي Dock.',
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": 'الاختصار Option + Cmd + C ينسخ مسار ملف في Finder.',
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'الاختصار Option + Cmd + H يُخفي التطبيقات الأخرى.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'الاختصار Option + Cmd + M يصغّر كل النوافذ.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'الاختصار Option + Cmd + W يغلق كل النوافذ.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': 'الاختصار Option + Cmd + V ينقل ملفًا منسوخًا في Finder.',
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'مسافة',
    # contexte : touche Mac | cerclic/mac/hotkey.py:68
    'touche Mac\x04Retour': 'Return',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Entrée': 'Enter',
    # contexte : touche Mac | cerclic/mac/hotkey.py:69
    'touche Mac\x04Tab': 'Tab',
    # contexte : touche Mac | cerclic/mac/hotkey.py:70
    'touche Mac\x04Suppr': '⌦',
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
    'touche Mac\x04Pavé {key}': 'لوحة الأرقام {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'أضف مفتاحًا بعد Cmd أو Ctrl أو Option أو Shift.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': 'الاختصار {shortcut} مستخدم بالفعل في macOS (إعدادات النظام، لوحة المفاتيح، اختصارات لوحة المفاتيح). اختر اختصارًا آخر.',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': 'الاختصار Shift + Cmd + {key} مستخدم بالفعل في Finder. اختر حرفًا آخر، أو Shift + Cmd + مسافة.',
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": 'يجب أن تتضمن المجموعة Cmd أو Ctrl: لا يقبل macOS الاختصارات المكونة من Option أو Shift فقط.',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'الاختصار Cmd مع مفتاح واحد مستخدم بالفعل في كل التطبيقات (نسخ، لصق، حفظ…). أضف Shift أو Option أو Ctrl، مثلًا Shift + Cmd + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'يُستخدم Ctrl مع مفاتيح الأسهم للتنقل بين أسطح المكتب (Mission Control).',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Ctrl',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Shift',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Cmd',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'إلغاء',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'إظهار كلمة السر',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'إخفاء كلمة السر',
    # cerclic/ui/cards.py:238
    'Fermer': 'إغلاق',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'سطح المكتب',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'التنزيلات',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'الصور',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'مقاطع الفيديو',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'الأفلام',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'الموسيقى',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'المستندات',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'إيقاف',
    # cerclic/ui/cards.py:299
    'En cours': 'قيد التنفيذ',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'جارٍ الإيقاف…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['تم حذف الملفات', 'تم حذف الملف', 'تم حذف الملفين', 'تم حذف الملفات', 'تم حذف الملفات', 'تم حذف الملفات'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": 'لم يتغير ملفك الأصلي.',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['تم إنشاء {n} ملف', 'تم إنشاء ملف واحد', 'تم إنشاء ملفين', 'تم إنشاء {n} ملفات', 'تم إنشاء {n} ملفًا', 'تم إنشاء {n} ملف'],
    # cerclic/ui/cards.py:366
    'Dossier': 'المجلد',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'حذف',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": 'احذف ما أنشأه Cerclic للتو (يبقى ملفك الأصلي كما هو)',
    # cerclic/ui/cards.py:417
    'Suppression impossible': 'تعذّر الحذف',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'ربما الملف مفتوح في تطبيق آخر: أغلق ذلك التطبيق، ثم أعد المحاولة.',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '{percent}%',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': 'في «{folder}»',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['تم تخطي {n} ملف، مثلًا: {example}', 'تم تخطي ملف واحد: {example}', 'تم تخطي ملفين، مثلًا: {example}', 'تم تخطي {n} ملفات، مثلًا: {example}', 'تم تخطي {n} ملفًا، مثلًا: {example}', 'تم تخطي {n} ملف، مثلًا: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'تم الإيقاف: لم يتم إنشاء أي شيء.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': '{size} إجمالًا · في «{folder}»',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · في «{folder}»',
    # cerclic/ui/cards.py:394
    '{title} impossible': 'تعذّر {title}',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'خطأ غير معروف.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'خفيف',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'متوسط',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'قوي',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'أقصى',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['{percent}% · {n} لون', '{percent}% · لون واحد', '{percent}% · لونان', '{percent}% · {n} ألوان', '{percent}% · {n} لونًا', '{percent}% · {n} لون'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': 'الصور بدقة 220 نقطة لكل بوصة: واضحة جدًا، حتى عند طباعتها',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": 'الصور بدقة 150 نقطة لكل بوصة: واضحة على الشاشة وعند الطباعة',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": 'الصور بدقة 110 نقطة لكل بوصة: للشاشة',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': 'الصور بدقة 80 نقطة لكل بوصة: الأخف حجمًا، صور أقل وضوحًا',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": 'حتى 1080p، جودة عالية جدًا',
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": 'حتى 1080p، جودة جيدة',
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': 'دقة 720p: للهاتف أو للرسائل',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': 'دقة 480p: الأخف حجمًا',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'ملف MP3 بمعدل 192 كيلوبت/ث: للموسيقى، جودة عالية جدًا',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'ملف MP3 بمعدل 128 كيلوبت/ث: للموسيقى',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'ملف MP3 بمعدل 96 كيلوبت/ث: للكلام، وللموسيقى على الهاتف',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'ملف MP3 بمعدل 64 كيلوبت/ث: للكلام',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '{percent}% · بدون فقدان',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'جارٍ التحميل…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': 'بدلًا من {size} · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'لا توفير',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'لا توفير',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'غير ممكن',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'غير ممكن',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'جارٍ الحساب…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'اختر الجودة · {key} للضغط',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': 'اختر المستوى · {key} للضغط',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'ضغط',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'الجودة',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'الضغط',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'مرّر المؤشر فوق الصورة: التفاصيل بحجم 100%',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'مرّر المؤشر فوق الصورة: التفاصيل',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: بدون إعدادات',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['معاينة: {name} · المجموع لـ {n} صورة، تقديرًا من {sampled} منها', 'معاينة: {name} · المجموع لصورة واحدة، تقديرًا من {sampled} منها', 'معاينة: {name} · المجموع لصورتين، تقديرًا من {sampled} منها', 'معاينة: {name} · المجموع لـ {n} صور، تقديرًا من {sampled} منها', 'معاينة: {name} · المجموع لـ {n} صورة، تقديرًا من {sampled} منها', 'معاينة: {name} · المجموع لـ {n} صورة، تقديرًا من {sampled} منها'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['معاينة: {name} · المجموع لـ {n} صورة', 'معاينة: {name} · المجموع لصورة واحدة', 'معاينة: {name} · المجموع لصورتين', 'معاينة: {name} · المجموع لـ {n} صور', 'معاينة: {name} · المجموع لـ {n} صورة', 'معاينة: {name} · المجموع لـ {n} صورة'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'ليس أخف حجمًا',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'تعذّر الضغط.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['تم تخطي {n} صورة', 'تم تخطي صورة واحدة', 'تم تخطي صورتين', 'تم تخطي {n} صور', 'تم تخطي {n} صورة', 'تم تخطي {n} صورة'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'جرّب ضغطًا أقوى.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'الأصلي: {size} · اخفض الجودة',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'الأصلي: {size} · اضغط بقوة أكبر',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'حر',
    # cerclic/ui/crop_editor.py:27
    'Original': 'الأصلي',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'اسحب الزوايا · {key} للاقتصاص',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'اقتصاص',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} من {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'كل الصفحات',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'الصورة كاملة',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": 'استعادة الصورة بأكملها',
    # cerclic/ui/crop_editor.py:589
    '{width} × {height} cm': '{width} × {height} سم',
    # cerclic/ui/crop_editor.py:593, cerclic/ui/crop_editor.py:448, cerclic/ui/social_editor.py:43
    '{width} × {height} px': '{width} × {height} بكسل',
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
    'Fermer (Échap)': 'إغلاق (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'اسحب للترتيب · {key} للإزالة',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'تدوير لليسار',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'تدوير لليمين ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': 'نحو البداية ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'نحو النهاية ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'استخراج المحدد',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'ملف PDF جديد يضم الصفحات المختارة فقط',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'إعادة تعيين',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'حفظ',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['تم تحديد {n} من {count}', 'تم تحديد {n} من {count}', 'تم تحديد {n} من {count}', 'تم تحديد {n} من {count}', 'تم تحديد {n} من {count}', 'تم تحديد {n} من {count}'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} صفحة', 'صفحة واحدة', 'صفحتان', '{n} صفحات', '{n} صفحة', '{n} صفحة'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'المزيد',
    # cerclic/ui/radial.py:479
    '‹ Retour': '› رجوع',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'أدوات أخرى',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'عام',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'اختصار لوحة المفاتيح',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'النقر بالزر الأيمن',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'الملفات المُنشأة',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'التوقيع',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'حول',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'الإصدار {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": 'حدد ملفًا أو أكثر في مستكشف الملفات أو على سطح المكتب، ثم اضغط على {combo}.',
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'تغيير',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'الافتراضي',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'اضغط على مجموعة المفاتيح…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'جارٍ التحقق…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'الإصدار {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': 'حدد ملفًا أو أكثر في Finder أو على سطح المكتب، ثم اضغط على {combo}.',
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'فتح العجلة',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'انقر بزر الماوس الأيمن على الملف، ثم الإجراءات السريعة، ثم «Cerclic». أو: فتح باستخدام، ثم Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'بدء التشغيل',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': 'يوقف Cerclic. لإعادة تشغيله، افتحه من مجلد التطبيقات.',
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'اللغة',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": 'تلقائي (لغة الكمبيوتر)',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': 'إلغاء تثبيت Cerclic',
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": 'هل تريد إزالة Cerclic من قائمة النقر بالزر الأيمن ومن التشغيل عند تسجيل الدخول، ثم إنهاءه؟',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'إلغاء التثبيت',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'مجموعة مفاتيح تفتح العجلة على الملفات المحددة.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'فتح العجلة من لوحة المفاتيح',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': '«Cerclic» في قائمة النقر بالزر الأيمن لملفاتك.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': '«Cerclic» في قائمة النقر بالزر الأيمن',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'لا يُعدَّل ملفك الأصلي أبدًا: كل إجراء ينشئ ملفًا جديدًا.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'مكان الحفظ',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'بجانب الملف الأصلي',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'في المجلد نفسه، مثلًا على سطح المكتب إذا كانت الصورة هناك. موصى به.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'في مجلد أختاره',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'كل الملفات المُنشأة في المكان نفسه.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'السؤال في كل مرة',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'يسألك Cerclic عن المجلد قبل إنشاء الملف.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'اختيار…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'مجلد الملفات المُنشأة',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': 'لتوقيع ملفات PDF بحركة واحدة. يبقى التوقيع على هذا الكمبيوتر.',
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'رسم…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'استيراد صورة…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'مسح',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'التوازن المناسب بين حجم الملفات ووضوحها.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '{value}%',
    # cerclic/ui/settings_window.py:993
    'Voir': 'عرض',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'اختيار صورة لتوقيعك',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'لم يتغير الاختصار.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'أمثلة: Shift + Cmd + مسافة أو Ctrl + Option + X. اضغط Esc للإلغاء.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'أمثلة: Ctrl + Alt + مسافة أو Ctrl + Shift + X أو Win + Shift + C. اضغط Esc للإلغاء.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'أخف',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'أوضح',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': 'مرحبًا بك في Cerclic',
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'تُطبَّق التغييرات فورًا.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'طريقتان لفتح العجلة، وبدء التشغيل، واللغة.',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'ثلاث طرق لفتح العجلة، وبدء التشغيل، واللغة.',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'بلوحة المفاتيح',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'اضغط Shift مع النقر بزر الماوس الأيمن على الملف، ثم «Cerclic». بدون Shift، مرّ عبر «إظهار المزيد من الخيارات».',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'انقر بزر الماوس الأيمن على الملف، ثم «Cerclic».',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'بالماوس',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': 'تشغيل Cerclic مع بدء تشغيل Mac',
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': 'تشغيل Cerclic مع Windows',
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'موصى به: تكون العجلة جاهزة متى احتجت إليها.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': 'يوقف Cerclic. لإعادة تشغيله، افتحه من قائمة ابدأ.',
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': 'يوقف Cerclic. لإعادة تشغيله، افتحه من سطح المكتب أو من قائمة ابدأ.',
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': 'إيقاف Cerclic',
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": 'لن تُفتح العجلة حتى التشغيل التالي.',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': 'لغة القوائم والنوافذ والرسائل في Cerclic.',
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": 'انقر على «تغيير»، ثم اضغط على مجموعة المفاتيح. إذا كانت مستخدمة بالفعل من قِبل macOS أو تطبيق آخر، يخبرك Cerclic بذلك ويحتفظ بالمجموعة السابقة.',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'هل لديك ماوس بأزرار قابلة للبرمجة؟ اضبط زرًا على أحد المفاتيح من F13 إلى F20، ثم اختره هنا: النقر على هذا الزر سيفتح العجلة.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": 'انقر على «تغيير»، ثم اضغط على مجموعة المفاتيح. إذا كانت مستخدمة بالفعل من قِبل Windows أو تطبيق آخر، يخبرك Cerclic بذلك ويحتفظ بالمجموعة السابقة.',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'هل لديك ماوس بأزرار قابلة للبرمجة؟ اضبط زرًا على أحد المفاتيح من F13 إلى F24، ثم اختره هنا: النقر على هذا الزر سيفتح العجلة.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'الإذن',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'الإعدادات…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'قائمة النقر بالزر الأيمن الكاملة',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': 'ليس في الإجراءات السريعة؟ انقر بزر الماوس الأيمن على ملف، ثم الإجراءات السريعة ثم تخصيص، وحدد «Cerclic». وهو موجود دائمًا أيضًا في فتح باستخدام.',
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'ضغط الصور',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': 'الإعداد الذي يقترحه «ضغط»، الذي يعرض الحجم الناتج ويتذكر اختيارك الأخير.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': 'ملفات JPG التي تنشئها الإجراءات الأخرى',
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': 'الاقتصاص، التدوير، التحويل… عند 90%، لا يظهر الفقد في الجودة.',
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'اقتصاص، توقيع، ضغط، تحويل، ملاءمة لمقاسات وسائل التواصل… بحركة واحدة، دون فتح تطبيق آخر.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'السجل',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'عند حدوث مشكلة، يساعد هذا الملف على فهم ما حدث.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'التراخيص',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": 'المكونات مفتوحة المصدر التي يستخدمها Cerclic وتراخيصها.',
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'إلغاء التثبيت…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'لا يوجد توقيع حتى الآن: ارسمه أو استورد صورة. وإلا فسيُطلب منك في أول مرة توقّع فيها.',
    # cerclic/ui/settings_window.py:1130
    'Images': 'الصور',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'الإعداد: لوحة المفاتيح',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'الإعداد: الماوس',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'بالسحب',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": 'فتح Cerclic عند تسجيل الدخول',
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': 'على الملفات المحددة في Finder أو على سطح المكتب.',
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": 'على الملفات المحددة في مستكشف الملفات أو على سطح المكتب.',
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'قراءة العناصر المحددة في Finder',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': 'في المرة الأولى، يسألك macOS هل يمكن لـ Cerclic التحكم في Finder: وافق. لا يقرأ Cerclic فيه سوى الملفات المحددة.',
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': '«Cerclic» في قائمة النقر بالزر الأيمن في Finder',
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': 'في قائمة الإجراءات السريعة لملفاتك، في Finder وعلى سطح المكتب.',
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": 'يعرض القائمة الكاملة دون المرور عبر «إظهار المزيد من الخيارات». سيقترح Cerclic إعادة تشغيل مستكشف الملفات.',
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'تلميح: دون تغيير أي شيء، يؤدي الضغط على Shift مع النقر بزر الماوس الأيمن على ملف إلى فتح القائمة الكاملة مباشرةً، مع «Cerclic».',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'لم يتم اختيار مجلد.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": 'يزيل «Cerclic» من قائمة النقر بالزر الأيمن ومن التشغيل عند تسجيل الدخول، ثم ينهيه. بعد ذلك، انقل Cerclic.app إلى سلة المهملات.',
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'تم تعطيل الاختصار: يبقى «Cerclic» متاحًا في قائمة النقر بالزر الأيمن.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'تم تعطيل الاختصار.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'يعمل Cerclic الآن في الخلفية: أيقونته في شريط القائمة أعلى الشاشة. اختر أدناه طريقتك المفضلة لفتح العجلة.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'يعمل Cerclic الآن في الخلفية: أيقونته بجانب الساعة (مخفية أحيانًا تحت السهم الصغير ^). اختر أدناه طريقتك المفضلة لفتح العجلة.',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": 'اسحب الملفات إلى أيقونة Cerclic (في التطبيقات أو في Dock).',
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": 'اسحب الملفات إلى أيقونة Cerclic.',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': '«Cerclic» في قائمة النقر بالزر الأيمن للملفات',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": 'أعلى قائمة الصور وملفات PDF ومقاطع الفيديو والملفات الصوتية، في مستكشف الملفات وعلى سطح المكتب.',
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": 'على الصور وملفات PDF ومقاطع الفيديو والملفات الصوتية، في مستكشف الملفات وعلى سطح المكتب وفي نافذتي «فتح» و«حفظ».',
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'اسمها: الاسم الأصلي، مع ما تغيّر، مثلًا صورة (مضغوط).jpg بجانب صورة.jpg. إذا كان هذا الاسم مستخدمًا، يضيف Cerclic رقمًا: لا يُستبدل أي ملف أبدًا.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": 'لم تعجبك نتيجة؟ زر «حذف» في بطاقتها يحذفها فورًا.',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'المجلد الذي اخترته: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'المجلد الذي اخترته: لا يوجد حتى الآن.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": 'تكفي صورة لتوقيعك على ورق أبيض: يجعل Cerclic الورق شفافًا ويحتفظ بالحبر.',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': 'للتوقيع: انقر بزر الماوس الأيمن أو استخدم الاختصار على ملف PDF، ثم «توقيع». ضع التوقيع واضغط على {key}.',
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': 'رفضت عن طريق الخطأ؟ في الأتمتة، حدد «Finder» أسفل Cerclic.',
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': '✓ نشط في كل مكان على Mac.',
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': '✓ نشط في كل مكان في Windows.',
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'يستخدم macOS أو تطبيق آخر هذه المجموعة بالفعل. اختر مجموعة أخرى عبر «تغيير».',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'يستخدم Windows أو تطبيق آخر هذه المجموعة بالفعل. اختر مجموعة أخرى عبر «تغيير».',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'لم يُعثر على أي خط توقيع في هذه الصورة.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'توقيعك',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'محفوظ للمرات القادمة',
    # cerclic/ui/signature.py:200
    'Importer…': 'استيراد…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'صورة لتوقيعك على ورق أبيض',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'اسحب التوقيع · اسحب زاوية · {key} للتوقيع',
    # cerclic/ui/signature.py:413
    'Changer': 'تغيير',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': 'رسم توقيع آخر أو استيراده',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'توقيع',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'الصفحة {page} من {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'وقّع هنا',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': 'اختيار صورة لتوقيعك',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'الصور ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'ملء',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": 'تغطي الصورة الإطار كله، ويُقص ما يتجاوزه.\nاسحبها لاختيار الجزء المحفوظ، واستخدم عجلة الماوس للتكبير.',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'خلفية ضبابية',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": 'الصورة كاملة، دون قص أي شيء.\nحولها: الصورة نفسها، ضبابية.',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'خلفية بيضاء',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": 'الصورة كاملة، دون قص أي شيء.\nحولها: لون أبيض.',
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'خلفية سوداء',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": 'الصورة كاملة، دون قص أي شيء.\nحولها: لون أسود.',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'الملف السابق',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'الملف التالي',
    # cerclic/ui/social_editor.py:448
    'Créer': 'إنشاء',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'اسحب وكبّر · {key} للإنشاء',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'لا يُقص أي شيء · {key} للإنشاء',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': 'الجزء المحفوظ أصغر من المقاس: عند تكبيره سيصبح أقل وضوحًا قليلًا.',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'الفيديو أصغر من المقاس: عند تكبيره سيصبح أقل وضوحًا قليلًا.',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": 'الصورة أصغر من المقاس: عند تكبيرها ستصبح أقل وضوحًا قليلًا.',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'المدة غير معروفة',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'اسحب المقبضين · {key} للتقصير',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'تقصير',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  ←  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'المدة {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': 'تعذّرت قراءة المدة: هل الملف تالف؟',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'البداية {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'النهاية {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['يحتوي «{name}» على {n} صفحة: لن يُحتفظ إلا بالأولى. استخدم «{action}» للاحتفاظ بها كلها.', 'يحتوي «{name}» على صفحة واحدة: لن يُحتفظ إلا بالأولى. استخدم «{action}» للاحتفاظ بها كلها.', 'يحتوي «{name}» على صفحتين: لن يُحتفظ إلا بالأولى. استخدم «{action}» للاحتفاظ بهما كلتيهما.', 'يحتوي «{name}» على {n} صفحات: لن يُحتفظ إلا بالأولى. استخدم «{action}» للاحتفاظ بها كلها.', 'يحتوي «{name}» على {n} صفحة: لن يُحتفظ إلا بالأولى. استخدم «{action}» للاحتفاظ بها كلها.', 'يحتوي «{name}» على {n} صفحة: لن يُحتفظ إلا بالأولى. استخدم «{action}» للاحتفاظ بها كلها.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'إنه بالفعل ملف {format}.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'هذه الصورة مضغوطة جيدًا بالفعل.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'منطقة الاقتصاص فارغة.',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": 'الإطار يغطي الصورة كلها: لا شيء لاقتصاصه.',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'يلزم صورتان على الأقل.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'التجميع',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'لا تحتوي هذه الصورة على أي معلومات خاصة.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'الصورة {i} من {n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': 'إلى PDF',
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": 'أبعاد الصورة {size} بكسل أو أقل بالفعل.',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': 'تعذّرت قراءة الصورة: {name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '«{name}» محمي بكلمة سر.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'كلمة السر غير صحيحة.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': 'التحويل إلى Word',
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'هذا الملف ليس PDF: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'لا توجد صور.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'يلزم ملفا PDF على الأقل للدمج.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'لا توجد صفحات للاحتفاظ بها.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": 'لا يوجد نص في ملف PDF هذا: غالبًا هو مستند ممسوح ضوئيًا (صورة).',
    # cerclic/actions/pdf.py:570
    'Vérification': 'جارٍ التحقق',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'ملف PDF هذا مضغوط جيدًا بالفعل.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'الإطار يغطي الصفحة كلها: لا شيء لاقتصاصه.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': 'نص العلامة المائية فارغ.',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'لا يوجد توقيع محفوظ.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'كلمة السر فارغة.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": 'لملف PDF هذا كلمة سر بالفعل. لتعيين كلمة سر أخرى، أزل الحالية أولًا («{more}»، ثم «{action}»).',
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'ملف PDF هذا غير محمي.',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'ملف PDF تالف أو غير قابل للقراءة: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'الصفحة {i} من {n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'ملف PDF رقم {i} من {n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": 'لا يحتوي ملف PDF هذا إلا على صفحة واحدة.',
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': 'الصفحة غير موجودة في ملف PDF هذا.',
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'لم تتغير الصفحات.',
    # cerclic/actions/registry.py:34
    'Image': 'صورة',
    # cerclic/actions/registry.py:36
    'Vidéo': 'فيديو',
    # cerclic/actions/registry.py:37
    'Son': 'صوت',
    # cerclic/actions/registry.py:136
    'Droite': 'لليمين',
    # cerclic/actions/registry.py:137
    'Gauche': 'لليسار',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'وسائل التواصل',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'تدوير',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'تغيير الحجم',
    # cerclic/actions/registry.py:213
    'Convertir': 'تحويل',
    # cerclic/actions/registry.py:223
    'Copier': 'نسخ',
    # cerclic/actions/registry.py:226
    'Assembler': 'تجميع',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'إخفاء الهوية',
    # cerclic/actions/registry.py:256
    'Fusionner': 'دمج',
    # cerclic/actions/registry.py:260
    'Pages': 'الصفحات',
    # cerclic/actions/registry.py:266
    'En Word': 'إلى Word',
    # cerclic/actions/registry.py:270
    'En images': 'إلى صور',
    # cerclic/actions/registry.py:276
    'Diviser': 'تقسيم',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': 'إضافة علامة مائية',
    # cerclic/actions/registry.py:290
    'Numéroter': 'ترقيم',
    # cerclic/actions/registry.py:295
    'En texte': 'إلى نص',
    # cerclic/actions/registry.py:326
    'En MP4': 'إلى MP4',
    # cerclic/actions/registry.py:329
    'En GIF': 'إلى GIF',
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'استخراج الصوت',
    # cerclic/actions/registry.py:336
    'Couper le son': 'كتم الصوت',
    # cerclic/actions/registry.py:352
    'En MP3': 'إلى MP3',
    # cerclic/actions/registry.py:141
    'Miroir': 'عكس',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'الاحتفاظ بجزء',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'الاقتصاص',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'إنستغرام، قصة، جوال، كمبيوتر',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'التحويل لوسائل التواصل',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'تدوير أو عكس',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'التدوير',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'بكسلات أقل',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'تغيير الحجم',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'أخف، بالأبعاد نفسها',
    # cerclic/actions/registry.py:216
    'Changer de format': 'تغيير التنسيق',
    # cerclic/actions/registry.py:216
    'Conversion': 'التحويل',
    # cerclic/actions/registry.py:222
    'Une page par image': 'صفحة لكل صورة',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'إنشاء ملف PDF',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'للصق حيث تريد',
    # cerclic/actions/registry.py:225
    'Copie': 'النسخ',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'عدة صور في صورة واحدة',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'يزيل GPS والجهاز والتاريخ',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'إخفاء الهوية',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'ضع توقيعك',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'قص الهوامش',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'أخف للإرسال',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'ملف PDF واحد',
    # cerclic/actions/registry.py:259
    'Fusion': 'الدمج',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'ترتيب، تدوير، حذف',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'تنظيم الصفحات',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': 'قابل للتحرير في Word',
    # cerclic/actions/registry.py:273
    'Une image par page': 'صورة لكل صفحة',
    # cerclic/actions/registry.py:273
    'Conversion en images': 'التحويل إلى صور',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'ملف PDF لكل صفحة',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'التقسيم إلى صفحات',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'نص مائل عبر الصفحة',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'أرقام أسفل الصفحة',
    # cerclic/actions/registry.py:294
    'Numérotation': 'الترقيم',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'النص بصيغة TXT',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'استخراج النص',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'بكلمة سر',
    # cerclic/actions/registry.py:304
    'Protection': 'الحماية',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'إزالة كلمة السر',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'إلغاء القفل',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'الاحتفاظ بمقطع',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'التقصير',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels وTikTok وShorts وكمبيوتر',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'أخف، بصيغة MP4',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'يعمل في كل مكان',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': 'التحويل إلى MP4',
    # cerclic/actions/registry.py:331
    'Une animation sans son': 'رسم متحرك بلا صوت',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'إنشاء GIF',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'المسار الصوتي بصيغة MP3',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': 'استخراج الصوت',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'الفيديو بلا صوت',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': 'إزالة الصوت',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'تصحيح الاتجاه',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': 'التحويل إلى MP3',
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'أخف، بصيغة MP3',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'الملف {i} من {n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '«{name}»: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '50%',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'جنبًا إلى جنب',
    # cerclic/actions/registry.py:231
    'En colonne': 'في عمود',
    # cerclic/actions/registry.py:232
    'En grille': 'في شبكة',
    # cerclic/actions/social.py:46
    'Carré': 'مربع',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'منشور على Instagram أو Facebook أو LinkedIn',
    # cerclic/actions/social.py:47
    'carré': 'مربع',
    # cerclic/actions/social.py:48
    'Portrait': 'عمودي',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'منشور على Instagram أو Facebook، الأكبر حجمًا في الموجز',
    # cerclic/actions/social.py:50
    'portrait': 'عمودي',
    # cerclic/actions/social.py:51
    'Grille': 'شبكة',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'لشبكة الملف الشخصي على Instagram، بشكلها الدقيق',
    # cerclic/actions/social.py:52
    'grille': 'شبكة',
    # cerclic/actions/social.py:53
    'Story': 'قصة',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'ملء شاشة الهاتف: القصص وReels وTikTok وYouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'قصة',
    # cerclic/actions/social.py:56
    'Paysage': 'أفقي',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'شاشة الكمبيوتر: YouTube والعروض التقديمية وX',
    # cerclic/actions/social.py:57
    'paysage': 'أفقي',
    # cerclic/actions/social.py:58
    'Bannière': 'لافتة',
    # cerclic/actions/social.py:58
    '1,91:1': '1.91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': 'رابط مُشارَك أو صورة عريضة على Facebook أو LinkedIn أو X',
    # cerclic/actions/social.py:59
    'bannière': 'لافتة',
    # cerclic/actions/social.py:239
    'Format {name}': 'مقاس {name}',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'هذه الصورة بمقاس {size} بالفعل.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'تعذّرت قراءة أبعاد الفيديو: هل الملف تالف؟',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'هذا الفيديو بمقاس {size} بالفعل.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': 'فشلت المعالجة: ربما الملف تالف أو بتنسيق غير معتاد.',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': 'لم يُعثر على ffmpeg: أعد تثبيت Cerclic.',
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'فيديو تالف أو تنسيق غير مدعوم.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'تم رفض الوصول: ربما الملف مفتوح في تطبيق آخر.',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'جارٍ التقصير',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'لا يحتوي هذا الملف على صورة فيديو.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'هذا الفيديو مضغوط جيدًا بالفعل: جرّب ضغطًا أقوى.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'الفيديو طويل جدًا لصورة GIF (أكثر من دقيقتين: سيبلغ حجمها مئات الميغابايت). احتفظ أولًا بمقطع باستخدام «{action}».',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': 'التحويل إلى GIF',
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'لا يحتوي هذا الفيديو على صوت.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'المقطع المراد الاحتفاظ به قصير جدًا.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': 'المقطع المختار هو الملف بأكمله.',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'لا يوجد صوت في هذا الملف.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'تعذّرت المعاينة.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'هذا الملف الصوتي خفيف بالفعل: جرّب ضغطًا أقوى.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'يحتوي هذا الملف على صوت فقط، بلا صورة: استخدم «{action}» لتحويله إلى MP3.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'تحضير المعاينة يستغرق وقتًا طويلًا جدًا.',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'الاختصار Alt + F4 يغلق النوافذ.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'الاختصار Alt + Tab ينتقل بين النوافذ.',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'الاختصار Alt + Esc ينتقل بين النوافذ.',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'الاختصار Alt + مسافة يفتح قائمة النافذة.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'الاختصار Ctrl + Esc يفتح قائمة ابدأ.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': 'الاختصار Ctrl + Alt + Delete محجوز لـ Windows.',
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': 'الاختصار Ctrl + Shift + Esc يفتح إدارة المهام.',
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'المفتاح {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'مسافة',
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
    'touche Windows\x04Impr. écran': 'PrtScn',
    # contexte : touche Windows | cerclic/win/hotkey.py:82, cerclic/win/hotkey.py:84
    'touche Windows\x04Pavé {key}': 'لوحة الأرقام {key}',
    # cerclic/win/hotkey.py:147
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'أضف مفتاحًا بعد Ctrl أو Alt أو Shift أو Win.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': 'المفتاح {key} مستخدم بالفعل في Windows والتطبيقات (التعليمات، إعادة التسمية، التحديث، التدقيق الإملائي…). أضف مثلًا Ctrl + Alt لتصبح المجموعة Ctrl + Alt + {key}.',
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'يُستخدم Alt مع لوحة الأرقام لكتابة الأحرف (Alt + 0201 = É). اختر مجموعة أخرى.',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'يجب أن تتضمن المجموعة Ctrl أو Alt أو Win (وإلا فلن يكتب هذا المفتاح حرفه بعد ذلك).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Shift',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'الاختصار Alt مع مفتاح واحد مستخدم بالفعل في كثير من التطبيقات (قوائم التطبيقات). أضف Shift أو Ctrl، مثلًا Alt + Shift + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'تُستخدم هذه المجموعة لكتابة أحرف (@ و€ و# وœ…) باستخدام AltGr. اختر مجموعة أخرى.',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'الاختصار Ctrl مع مفتاح واحد مستخدم بالفعل في كثير من التطبيقات (غامق، نسخ، لصق، حفظ…). أضف Shift أو Alt، مثلًا Ctrl + Shift + {key}.',
    # cerclic/ui/settings_window.py (À propos)
    'Code source': 'الشيفرة المصدرية',
    'Tout le code de Cerclic est public, sur GitHub.': 'كل شيفرة Cerclic متاحة للجميع على GitHub.',
}
