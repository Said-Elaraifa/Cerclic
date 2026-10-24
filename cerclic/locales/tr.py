"""Cerclic, Türkçe. Keys: the French text of the code (docs/I18N.md).
Kept up to date by scripts/i18n_messages.py --update."""

T: dict = {
    # pluriel : '{n} fichiers' | cerclic/app.py:51, cerclic/ui/compress_editor.py:343, cerclic/ui/radial.py:204
    '{n} fichier': ['{n} dosya', '{n} dosya'],
    # cerclic/app.py:93
    "Enregistré dans «\xa0{where}\xa0» : le dossier d'origine est protégé.": '“{where}” klasörüne kaydedildi: orijinal klasör korumalı.',
    # cerclic/app.py:92
    'Téléchargements': 'İndirilenler',
    # cerclic/app.py:720
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": "Windows veya başka bir uygulama bunu zaten kullanıyor. Cerclic'te başka bir kısayol seçin.",
    # cerclic/app.py:744
    'clic droit, puis « Cerclic »': 'sağ tık, sonra “Cerclic”',
    # cerclic/app.py:87
    "Le dossier choisi est introuvable : enregistré à côté de l'original.": 'Seçilen klasör bulunamadı: orijinalin yanına kaydedildi.',
    # cerclic/app.py:459
    'Ouvrir Cerclic': "Cerclic'i aç",
    # cerclic/app.py:461, cerclic/ui/settings_window.py:659
    'Quitter Cerclic': "Cerclic'ten çık",
    # cerclic/app.py:715
    "Windows ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": "Windows veya başka bir uygulama bunu zaten kullanıyor. Cerclic'te başka bir kısayol seçin; sağ tık menüsündeki “Cerclic” her zaman çalışır.",
    # cerclic/app.py:718
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic.": "macOS veya başka bir uygulama bunu zaten kullanıyor. Cerclic'te başka bir kısayol seçin.",
    # cerclic/app.py:741
    'clic droit, Actions rapides, puis « Cerclic »': 'sağ tık, Hızlı Eylemler, sonra “Cerclic”',
    # cerclic/app.py:743
    "clic droit, « Afficher d'autres options », puis « Cerclic »": 'sağ tık, “Daha fazla seçenek göster”, sonra “Cerclic”',
    # cerclic/app.py:805
    'Autorise Cerclic à lire ta sélection': "Cerclic'in seçiminizi okumasına izin verin",
    # cerclic/app.py:806
    'Réglages Système, Confidentialité et sécurité, Automatisation : coche « Finder » sous Cerclic. Le clic droit, Actions rapides, « Cerclic » marche sans cela.': "Sistem Ayarları, Gizlilik ve Güvenlik, Otomasyon: Cerclic'in altındaki “Finder” kutusunu işaretleyin. Sağ tık, Hızlı Eylemler, “Cerclic” yolu bu izin olmadan da çalışır.",
    # cerclic/app.py:869
    'Clique sur une image, un PDF, une vidéo ou un son dans le Finder ou sur le Bureau, puis appuie sur {combo}.': "Finder'da veya masaüstünde bir görüntüye, PDF'ye, videoya ya da sese tıklayın, sonra {combo} kısayolunu kullanın.",
    # cerclic/app.py:872
    "Clique sur une image, un PDF, une vidéo ou un son dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": "Dosya Gezgini'nde veya masaüstünde bir görüntüye, PDF'ye, videoya ya da sese tıklayın, sonra {combo} kısayolunu kullanın.",
    # cerclic/app.py:878
    'Ou : clic droit, Actions rapides, puis « Cerclic ».': 'Ya da: sağ tık, Hızlı Eylemler, sonra “Cerclic”.',
    # cerclic/app.py:919
    'Image copiée': 'Görüntü kopyalandı',
    # cerclic/app.py:920
    'Colle-la où tu veux avec {key} + V.': 'İstediğiniz yere {key} + V ile yapıştırın.',
    # cerclic/app.py:1138, cerclic/ui/bubble.py:88
    'OK': 'Tamam',
    # cerclic/app.py:1253
    'Menu complet activé': 'Tam menü etkinleştirildi',
    # cerclic/app.py:1254
    "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de dossiers ouvertes vont se fermer.": 'Dosya Gezgini yeniden başlatıldığında uygulanır. Açık klasör pencereleri kapanacak.',
    # cerclic/app.py:1269
    'Menu de Windows 11 rétabli': 'Windows 11 menüsü geri yüklendi',
    # cerclic/app.py:1270
    "Il s'applique au redémarrage de l'Explorateur.": 'Dosya Gezgini yeniden başlatıldığında uygulanır.',
    # cerclic/app.py:584, cerclic/app.py:595
    'Deux Cerclic installés': 'İki Cerclic yüklü',
    # cerclic/app.py:585
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et un seul raccourci, retire-la : « Montrer le désinstalleur », puis double-clique « unins000 ».": "Cerclic'in Microsoft Store dışından yüklenen sürümü hâlâ duruyor. Sağ tık menüsünde tek bir “Cerclic” ve tek bir kısayol olması için o sürümü kaldırın: “Kaldırıcıyı göster”, sonra “unins000” dosyasına çift tıklayın.",
    # cerclic/app.py:596
    "La version de Cerclic installée sans le Microsoft Store est encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans Applications installées : c'est le Cerclic qui n'a pas « Options avancées » dans son menu.": "Cerclic'in Microsoft Store dışından yüklenen sürümü hâlâ duruyor. Tek bir “Cerclic” olması için o sürümü Yüklü uygulamalar bölümünden kaldırın: menüsünde “Gelişmiş seçenekler” olmayan Cerclic odur.",
    # cerclic/app.py:713
    "macOS ou une autre application l'utilise déjà. Choisis-en un autre dans Cerclic ; le clic droit « Cerclic » marche toujours.": "macOS veya başka bir uygulama bunu zaten kullanıyor. Cerclic'te başka bir kısayol seçin; sağ tık menüsündeki “Cerclic” her zaman çalışır.",
    # cerclic/app.py:880
    "Ou : clic droit, « Afficher d'autres options », puis « Cerclic ».": 'Ya da: sağ tık, “Daha fazla seçenek göster”, sonra “Cerclic”.',
    # cerclic/app.py:882
    'Ou : clic droit, puis « Cerclic ».': 'Ya da: sağ tık, sonra “Cerclic”.',
    # cerclic/app.py:915
    'Copie impossible': 'Kopyalanamadı',
    # cerclic/app.py:966, cerclic/actions/pdf.py:735, cerclic/actions/registry.py:305
    'Déverrouiller': 'Kilidi aç',
    # cerclic/app.py:966
    'Continuer': 'Devam',
    # cerclic/app.py:971
    '« {name} » est protégé.': '“{name}” korumalı.',
    # cerclic/app.py:1223, cerclic/app.py:978
    'Mot de passe du PDF': 'PDF parolası',
    # cerclic/app.py:562
    'Lancement avec Windows bloqué': 'Windows ile başlatma engellendi',
    # cerclic/app.py:563
    'Ton organisation ne permet pas aux applications de se lancer avec Windows.': 'Kuruluşunuz, uygulamaların Windows ile başlatılmasına izin vermiyor.',
    # cerclic/app.py:566
    'Lancement avec Windows désactivé dans Windows': "Windows ile başlatma Windows'ta kapatılmış",
    # cerclic/app.py:567
    'Il a été désactivé dans le Gestionnaire des tâches : seul Windows peut le réactiver. Dans Paramètres, Applications, Démarrage, active « Cerclic ».': "Görev Yöneticisi'nde devre dışı bırakılmış: yalnızca Windows yeniden açabilir. Ayarlar, Uygulamalar, Başlangıç bölümünde “Cerclic” seçeneğini açın.",
    # cerclic/app.py:704, cerclic/app.py:692
    'Raccourci {combo} indisponible': '{combo} kısayolu kullanılamıyor',
    # cerclic/app.py:758, cerclic/app.py:932
    'Cerclic a rencontré un problème': 'Cerclic bir sorunla karşılaştı',
    # cerclic/app.py:759, cerclic/app.py:933
    'Les détails sont dans {path}': 'Ayrıntılar şurada: {path}',
    # cerclic/app.py:851
    'Fichier inaccessible': 'Dosyaya erişilemiyor',
    # cerclic/app.py:852
    "Ce fichier n'est pas dans un dossier normal (archive ZIP, téléphone…). Copie-le dans un dossier, puis réessaie.": 'Bu dosya normal bir klasörde değil (ZIP arşivi, telefon…). Bir klasöre kopyalayıp yeniden deneyin.',
    # cerclic/app.py:915, cerclic/ui/settings_window.py:1139, cerclic/ui/signature.py:247
    'Image illisible.': 'Görüntü okunamıyor.',
    # cerclic/app.py:1224
    'Réessayer': 'Yeniden dene',
    # cerclic/app.py:685
    '{refused} est déjà utilisé par macOS ou une autre application. Ton raccourci reste {kept}.': '{refused} kombinasyonu macOS veya başka bir uygulama tarafından zaten kullanılıyor. Kısayolunuz {kept} olarak kalıyor.',
    # cerclic/app.py:687
    '{refused} est déjà utilisé par Windows ou une autre application. Ton raccourci reste {kept}.': '{refused} kombinasyonu Windows veya başka bir uygulama tarafından zaten kullanılıyor. Kısayolunuz {kept} olarak kalıyor.',
    # cerclic/app.py:809, cerclic/app.py:1256, cerclic/app.py:1271 ...
    'Plus tard': 'Daha sonra',
    # cerclic/app.py:810
    'Ouvrir les réglages': 'Ayarları aç',
    # cerclic/app.py:855
    'Aucune action pour ce type de fichier': 'Bu dosya türü için işlem yok',
    # cerclic/app.py:856
    'Cerclic travaille sur les images, les PDF, les vidéos et les sons.': "Cerclic görüntüler, PDF'ler, videolar ve seslerle çalışır.",
    # cerclic/app.py:859
    "Sélectionne d'abord un fichier": 'Önce bir dosya seçin',
    # cerclic/app.py:986
    'Mot de passe incorrect pour « {name} ». Réessaie.': '“{name}” için parola yanlış. Yeniden deneyin.',
    # cerclic/app.py:999
    "Rogner n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": "Kırpma yalnızca ilk sayfayı tutar. Hepsini tutmak için önce “PDF'ye dönüştür” işlemini, ardından PDF üzerinde “{action}” işlemini kullanın.",
    # pluriel : '« {name} » a {n} pages' | cerclic/app.py:1009
    '« {name} » a {n} page': ['“{name}” dosyasında {n} sayfa var', '“{name}” dosyasında {n} sayfa var'],
    # cerclic/app.py:1126
    'Où enregistrer le résultat ?': 'Sonuç nereye kaydedilsin?',
    # cerclic/app.py:1257, cerclic/app.py:1272
    "Redémarrer l'Explorateur": "Dosya Gezgini'ni yeniden başlat",
    # cerclic/app.py:591
    'Montrer le désinstalleur': 'Kaldırıcıyı göster',
    # cerclic/app.py:602
    'Ouvrir les applications': 'Uygulamaları aç',
    # cerclic/app.py:693
    "macOS ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'macOS veya başka bir uygulama bunu zaten kullanıyor. Kısayolunuz {kept} olarak kalıyor.',
    # cerclic/app.py:695
    "Windows ou une autre application l'utilise déjà. Ton raccourci reste {kept}.": 'Windows veya başka bir uygulama bunu zaten kullanıyor. Kısayolunuz {kept} olarak kalıyor.',
    # cerclic/app.py:975
    'Mot de passe incorrect': 'Parola yanlış',
    # cerclic/app.py:975
    "Rien n'a été créé.": 'Hiçbir şey oluşturulmadı.',
    # cerclic/app.py:1003
    "Compresser n'en garderait que la première. Utilise « En PDF » pour les garder toutes, puis {action} sur le PDF.": "Sıkıştırma yalnızca ilk sayfayı tutar. Hepsini tutmak için önce “PDF'ye dönüştür” işlemini, ardından PDF üzerinde “{action}” işlemini kullanın.",
    # cerclic/app.py:1007
    'Seule la première serait mise au format. Utilise « En PDF » pour les garder toutes.': "Yalnızca ilk sayfa formata uyarlanır. Hepsini tutmak için “PDF'ye dönüştür” işlemini kullanın.",
    # cerclic/app.py:571, cerclic/ui/cards.py:363, cerclic/ui/settings_window.py:830 ...
    'Ouvrir': 'Aç',
    # cerclic/app.py:707
    'Changer de raccourci': 'Kısayolu değiştir',
    # cerclic/app.py:1081
    'Texte du filigrane': 'Filigran metni',
    # cerclic/app.py:1082
    'Il sera écrit en diagonale sur chaque page.': 'Her sayfaya çapraz olarak yazılacak.',
    # cerclic/app.py:1083
    'CONFIDENTIEL': 'GİZLİ',
    # cerclic/app.py:1088
    'Mot de passe à mettre': 'Eklenecek parola',
    # cerclic/app.py:1089
    "Il sera demandé pour ouvrir le PDF. L'original reste sans mot de passe.": "PDF'yi açmak için sorulacak. Orijinal dosya parolasız kalır.",
    # cerclic/app.py:1091, cerclic/actions/registry.py:300
    'Protéger': 'Koru',
    # cerclic/engine.py:102
    'Erreur inattendue. Réessaie ; si cela recommence, le détail est dans le journal de Cerclic (cerclic.log).': 'Beklenmeyen hata. Yeniden deneyin; yine olursa ayrıntılar Cerclic günlüğünde (cerclic.log).',
    # cerclic/engine.py:84
    'Accès refusé : le fichier est peut-être ouvert dans une autre application, ou le dossier est protégé.': 'Erişim reddedildi: dosya başka bir uygulamada açık olabilir ya da klasör korumalı.',
    # cerclic/engine.py:89
    'Nom ou chemin trop long pour Windows : renomme le fichier plus court, ou déplace-le dans un dossier moins profond.': 'Ad veya yol Windows için çok uzun: dosyaya daha kısa bir ad verin ya da daha az iç içe bir klasöre taşıyın.',
    # cerclic/engine.py:92, cerclic/actions/video.py:176
    'Fichier introuvable : il a peut-être été déplacé ou supprimé.': 'Dosya bulunamadı: taşınmış veya silinmiş olabilir.',
    # cerclic/engine.py:94
    'Fichier trop lourd pour la mémoire disponible.': 'Dosya, kullanılabilir bellek için çok büyük.',
    # cerclic/engine.py:96, cerclic/actions/video.py:174
    'Le disque est plein.': 'Disk dolu.',
    # cerclic/engine.py:99, cerclic/ui/compress_editor.py:130, cerclic/actions/images.py:106
    'Image illisible ou format non pris en charge.': 'Görüntü okunamıyor ya da biçimi desteklenmiyor.',
    # cerclic/engine.py:101
    'PDF endommagé ou illisible.': 'PDF hasarlı ya da okunamıyor.',
    # pluriel : '{action} : il faut au moins {n} fichiers.' | cerclic/engine.py:137
    '{action} : il faut au moins {n} fichier.': ['{action}: en az {n} dosya gerekir.', '{action}: en az {n} dosya gerekir.'],
    # cerclic/engine.py:148, cerclic/jobs.py:105
    'Annulé': 'İptal edildi',
    # cerclic/engine.py:129
    "« {name} » n'est plus là : il a été déplacé, renommé ou supprimé (ou la clé USB retirée).": '“{name}” artık yerinde değil: taşınmış, yeniden adlandırılmış ya da silinmiş (veya USB bellek çıkarılmış).',
    # pluriel : '{n} fichiers ne sont plus là : ils ont été déplacés, renommés ou supprimés.' | cerclic/engine.py:132
    "{n} fichier n'est plus là : il a été déplacé, renommé ou supprimé.": ['{n} dosya artık yerinde değil: taşınmış, yeniden adlandırılmış ya da silinmiş.', '{n} dosya artık yerinde değil: taşınmış, yeniden adlandırılmış ya da silinmiş.'],
    # cerclic/errors.py:20
    'Ce PDF est protégé par un mot de passe.': 'Bu PDF parolayla korunuyor.',
    # cerclic/jobs.py:119
    "Le traitement s'est arrêté net : le fichier est probablement endommagé.": 'İşlem aniden durdu: dosya büyük olasılıkla hasarlı.',
    # cerclic/paths.py:235
    'compressé': 'sıkıştırılmış',
    # cerclic/paths.py:235
    'redimensionné': 'yeniden boyutlandırılmış',
    # cerclic/paths.py:236
    'pivoté': 'döndürülmüş',
    # cerclic/paths.py:236
    'rogné': 'kırpılmış',
    # cerclic/paths.py:236
    'miroir': 'aynalanmış',
    # cerclic/paths.py:237
    'anonymisé': 'anonimleştirilmiş',
    # cerclic/paths.py:237
    'assemblé': 'birleştirilmiş',
    # cerclic/paths.py:237
    'fusionné': 'birleştirilmiş',
    # cerclic/paths.py:238
    'réorganisé': 'yeniden düzenlenmiş',
    # cerclic/paths.py:238
    'extrait': 'ayıklanmış',
    # cerclic/paths.py:238
    'texte': 'metin',
    # cerclic/paths.py:239
    'filigrane': 'filigranlı',
    # cerclic/paths.py:239
    'numéroté': 'numaralı',
    # cerclic/paths.py:239
    'signé': 'imzalı',
    # cerclic/paths.py:240
    'protégé': 'korumalı',
    # cerclic/paths.py:240
    'déverrouillé': 'kilidi açılmış',
    # cerclic/paths.py:240
    'son': 'ses',
    # cerclic/paths.py:241
    'raccourci': 'kısaltılmış',
    # cerclic/paths.py:241
    'sans son': 'sessiz',
    # cerclic/paths.py:241
    'images': 'görüntüler',
    # cerclic/paths.py:242
    'pages': 'sayfalar',
    # cerclic/sizes.py:21
    '{size} To': '{size} TB',
    # cerclic/sizes.py:65
    'même taille': 'aynı boyut',
    # cerclic/sizes.py:71
    'De {before} à {after}': 'Önce {before}, şimdi {after}',
    # cerclic/sizes.py:16
    '{size} Ko': '{size} KB',
    # cerclic/sizes.py:18
    '{size} Mo': '{size} MB',
    # cerclic/sizes.py:20
    '{size} Go': '{size} GB',
    # pluriel : '{n} octets' | cerclic/sizes.py:28
    '{n} octet': ['{n} bayt', '{n} bayt'],
    # cerclic/sizes.py:62
    '{pct} % de moins': '%{pct} daha küçük',
    # cerclic/sizes.py:64
    '{pct} % de plus': '%{pct} daha büyük',
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
    'touche Mac\x04Touche {code}': 'Tuş {code}',
    # cerclic/mac/hotkey.py:191
    'Cmd + Espace ouvre Spotlight.': "Cmd + Boşluk, Spotlight'ı açar.",
    # cerclic/mac/hotkey.py:192
    'Option + Cmd + Espace ouvre la recherche du Finder.': 'Option + Cmd + Boşluk, Finder aramasını açar.',
    # cerclic/mac/hotkey.py:193
    'Ctrl + Espace change la langue du clavier.': 'Ctrl + Boşluk, klavye dilini değiştirir.',
    # cerclic/mac/hotkey.py:194
    'Ctrl + Option + Espace change la langue du clavier.': 'Ctrl + Option + Boşluk, klavye dilini değiştirir.',
    # cerclic/mac/hotkey.py:195
    'Ctrl + Cmd + Espace ouvre les emojis.': 'Ctrl + Cmd + Boşluk, emojileri açar.',
    # cerclic/mac/hotkey.py:196
    "Cmd + Tab passe d'une application à l'autre.": 'Cmd + Tab, uygulamalar arasında geçiş yapar.',
    # cerclic/mac/hotkey.py:197
    "Maj + Cmd + Tab passe d'une application à l'autre.": 'Shift + Cmd + Tab, uygulamalar arasında geçiş yapar.',
    # cerclic/mac/hotkey.py:198
    'Option + Cmd + Échap force une application à quitter.': 'Option + Cmd + Esc, bir uygulamayı zorla kapatır.',
    # cerclic/mac/hotkey.py:199
    "Maj + Cmd + 3 fait une capture d'écran.": 'Shift + Cmd + 3, ekran görüntüsü alır.',
    # cerclic/mac/hotkey.py:200
    "Maj + Cmd + 4 fait une capture d'écran.": 'Shift + Cmd + 4, ekran görüntüsü alır.',
    # cerclic/mac/hotkey.py:201
    "Maj + Cmd + 5 ouvre l'outil de capture d'écran.": 'Shift + Cmd + 5, ekran görüntüsü aracını açar.',
    # cerclic/mac/hotkey.py:202
    'Maj + Cmd + 6 fait une capture de la Touch Bar.': "Shift + Cmd + 6, Touch Bar'ın görüntüsünü alır.",
    # cerclic/mac/hotkey.py:205
    "Ctrl + Cmd + Q verrouille l'écran.": 'Ctrl + Cmd + Q, ekranı kilitler.',
    # cerclic/mac/hotkey.py:206
    'Maj + Cmd + Q ferme la session.': 'Shift + Cmd + Q, oturumu kapatır.',
    # cerclic/mac/hotkey.py:207
    'Ctrl + Cmd + F passe en plein écran.': 'Ctrl + Cmd + F, tam ekrana geçer.',
    # cerclic/mac/hotkey.py:208
    'Option + Cmd + D masque le Dock.': "Option + Cmd + D, Dock'u gizler.",
    # cerclic/mac/hotkey.py:209
    "Option + Cmd + C copie le chemin d'un fichier dans le Finder.": "Option + Cmd + C, Finder'da bir dosyanın yolunu kopyalar.",
    # cerclic/mac/hotkey.py:210
    'Option + Cmd + H masque les autres applications.': 'Option + Cmd + H, diğer uygulamaları gizler.',
    # cerclic/mac/hotkey.py:211
    'Option + Cmd + M réduit toutes les fenêtres.': 'Option + Cmd + M, tüm pencereleri küçültür.',
    # cerclic/mac/hotkey.py:212
    'Option + Cmd + W ferme toutes les fenêtres.': 'Option + Cmd + W, tüm pencereleri kapatır.',
    # cerclic/mac/hotkey.py:213
    'Option + Cmd + V déplace un fichier copié dans le Finder.': "Option + Cmd + V, Finder'da kopyalanan bir dosyayı taşır.",
    # contexte : touche Mac | cerclic/mac/hotkey.py:67
    'touche Mac\x04Espace': 'Boşluk',
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
    'touche Mac\x04Pavé {key}': 'Tuş takımı {key}',
    # cerclic/mac/hotkey.py:276
    'Ajoute une touche après Cmd, Ctrl, Option ou Maj.': 'Cmd, Ctrl, Option veya Shift tuşundan sonra bir tuş ekleyin.',
    # cerclic/mac/hotkey.py:280
    '{shortcut} est déjà un raccourci de macOS (Réglages Système, Clavier, Raccourcis clavier). Choisis-en un autre.': '{shortcut} zaten bir macOS kısayolu (Sistem Ayarları, Klavye, Klavye Kestirmeleri). Başka bir kısayol seçin.',
    # cerclic/mac/hotkey.py:287
    'Maj + Cmd + {key} sert déjà dans le Finder. Choisis une autre lettre, ou Maj + Cmd + Espace.': "Shift + Cmd + {key} Finder'da zaten kullanılıyor. Başka bir harf ya da Shift + Cmd + Boşluk seçin.",
    # cerclic/mac/hotkey.py:292
    "Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis faits seulement d'Option ou de Maj.": 'Kombinasyonda Cmd veya Ctrl olmalı: macOS yalnızca Option veya Shift ile yapılan kısayolları kabul etmez.',
    # cerclic/mac/hotkey.py:295
    'Cmd + une seule touche sert déjà dans toutes les applications (copier, coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple Maj + Cmd + {key}.': 'Cmd + tek bir tuş tüm uygulamalarda zaten kullanılıyor (kopyala, yapıştır, kaydet…). Shift, Option veya Ctrl ekleyin, örneğin Shift + Cmd + {key}.',
    # cerclic/mac/hotkey.py:299
    "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control).": 'Ctrl + ok tuşları masaüstleri arasında geçiş yapar (Mission Control).',
    # contexte : touche Mac | cerclic/mac/hotkey.py:176
    'touche Mac\x04Ctrl': 'Ctrl',
    # contexte : touche Mac | cerclic/mac/hotkey.py:178
    'touche Mac\x04Option': 'Option',
    # contexte : touche Mac | cerclic/mac/hotkey.py:180
    'touche Mac\x04Maj': 'Shift',
    # contexte : touche Mac | cerclic/mac/hotkey.py:182
    'touche Mac\x04Cmd': 'Cmd',
    # cerclic/ui/bubble.py:84, cerclic/ui/compress_editor.py:378, cerclic/ui/crop_editor.py:476 ...
    'Annuler': 'Vazgeç',
    # cerclic/ui/bubble.py:72, cerclic/ui/bubble.py:112
    'Afficher le mot de passe': 'Parolayı göster',
    # cerclic/ui/bubble.py:112
    'Masquer le mot de passe': 'Parolayı gizle',
    # cerclic/ui/cards.py:238
    'Fermer': 'Kapat',
    # contexte : dossier | cerclic/ui/cards.py:251
    'dossier\x04Bureau': 'Masaüstü',
    # contexte : dossier | cerclic/ui/cards.py:253
    'dossier\x04Téléchargements': 'İndirilenler',
    # contexte : dossier | cerclic/ui/cards.py:255
    'dossier\x04Images': 'Resimler',
    # contexte : dossier | cerclic/ui/cards.py:257
    'dossier\x04Vidéos': 'Videolar',
    # contexte : dossier du Mac | cerclic/ui/cards.py:259
    'dossier du Mac\x04Vidéos': 'Filmler',
    # contexte : dossier | cerclic/ui/cards.py:261
    'dossier\x04Musique': 'Müzik',
    # contexte : dossier | cerclic/ui/cards.py:263
    'dossier\x04Documents': 'Belgeler',
    # cerclic/ui/cards.py:291
    '{title}…': '{title}…',
    # cerclic/ui/cards.py:293
    'Arrêter': 'Durdur',
    # cerclic/ui/cards.py:299
    'En cours': 'Devam ediyor',
    # cerclic/ui/cards.py:307
    'Arrêt en cours…': 'Durduruluyor…',
    # pluriel : 'Fichiers supprimés' | cerclic/ui/cards.py:428
    'Fichier supprimé': ['Dosya silindi', 'Dosyalar silindi'],
    # cerclic/ui/cards.py:429
    "Ton fichier d'origine n'a pas bougé.": 'Orijinal dosyanız yerinde duruyor.',
    # pluriel : '{n} fichiers créés' | cerclic/ui/cards.py:331
    '{n} fichier créé': ['{n} dosya oluşturuldu', '{n} dosya oluşturuldu'],
    # cerclic/ui/cards.py:366
    'Dossier': 'Klasör',
    # cerclic/ui/cards.py:368, cerclic/ui/pages_editor.py:141
    'Supprimer': 'Sil',
    # cerclic/ui/cards.py:370
    "Supprime ce que Cerclic vient de créer (ton fichier d'origine ne bouge pas)": "Cerclic'in az önce oluşturduğunu siler (orijinal dosyanız yerinde kalır)",
    # cerclic/ui/cards.py:417
    'Suppression impossible': 'Silinemedi',
    # cerclic/ui/cards.py:418
    'Le fichier est sans doute ouvert dans une autre application : ferme-la, puis réessaie.': 'Dosya büyük olasılıkla başka bir uygulamada açık: o uygulamayı kapatıp yeniden deneyin.',
    # cerclic/ui/cards.py:314, cerclic/ui/compress_editor.py:192
    '{percent} %': '%{percent}',
    # cerclic/ui/cards.py:340, cerclic/ui/cards.py:349
    'Dans\xa0«\xa0{folder}\xa0»': '“{folder}” klasöründe',
    # pluriel : '{n} fichiers laissés de côté, par exemple : {example}' | cerclic/ui/cards.py:354
    '{n} fichier laissé de côté, par exemple : {example}': ['{n} dosya atlandı, örneğin: {example}', '{n} dosya atlandı, örneğin: {example}'],
    # cerclic/ui/cards.py:385
    "Arrêté : rien n'a été créé.": 'Durduruldu: hiçbir şey oluşturulmadı.',
    # cerclic/ui/cards.py:343
    '{size} en tout · dans\xa0«\xa0{folder}\xa0»': 'Toplam {size} · “{folder}” klasöründe',
    # cerclic/ui/cards.py:346
    '{size} · dans\xa0«\xa0{folder}\xa0»': '{size} · “{folder}” klasöründe',
    # cerclic/ui/cards.py:394
    '{title} impossible': '{title} başarısız oldu',
    # cerclic/ui/cards.py:395
    'Erreur inconnue.': 'Bilinmeyen hata.',
    # cerclic/ui/compress_editor.py:36
    'Légère': 'Hafif',
    # cerclic/ui/compress_editor.py:36
    'Moyenne': 'Orta',
    # cerclic/ui/compress_editor.py:36
    'Forte': 'Güçlü',
    # cerclic/ui/compress_editor.py:37
    'Maximale': 'En yüksek',
    # pluriel : '{percent} % · {n} couleurs' | cerclic/ui/compress_editor.py:195
    '{percent} % · {n} couleur': ['%{percent} · {n} renk', '%{percent} · {n} renk'],
    # cerclic/ui/compress_editor.py:39
    'Images à 220 ppp : très nettes, même imprimées': '220 dpi görüntüler: baskıda bile çok net',
    # cerclic/ui/compress_editor.py:40
    "Images à 150 ppp : nettes à l'écran et à l'impression": '150 dpi görüntüler: ekranda ve baskıda net',
    # cerclic/ui/compress_editor.py:41
    "Images à 110 ppp : pour l'écran": '110 dpi görüntüler: ekran için',
    # cerclic/ui/compress_editor.py:42
    'Images à 80 ppp : le plus léger, images moins nettes': '80 dpi görüntüler: en hafif, görüntüler daha az net',
    # cerclic/ui/compress_editor.py:43
    "Jusqu'à 1080p, très bonne qualité": "1080p'ye kadar, çok iyi kalite",
    # cerclic/ui/compress_editor.py:44
    "Jusqu'à 1080p, bonne qualité": "1080p'ye kadar, iyi kalite",
    # cerclic/ui/compress_editor.py:45
    '720p : pour un téléphone ou un message': '720p: telefon veya mesaj için',
    # cerclic/ui/compress_editor.py:46
    '480p : le plus léger': '480p: en hafif',
    # cerclic/ui/compress_editor.py:47
    'MP3 192 kbit/s : musique, très bonne qualité': 'MP3 192 kbit/sn: müzik, çok iyi kalite',
    # cerclic/ui/compress_editor.py:48
    'MP3 128 kbit/s : musique': 'MP3 128 kbit/sn: müzik',
    # cerclic/ui/compress_editor.py:49
    'MP3 96 kbit/s : voix, et musique sur un téléphone': 'MP3 96 kbit/sn: konuşma ve telefonda müzik',
    # cerclic/ui/compress_editor.py:50
    'MP3 64 kbit/s : voix': 'MP3 64 kbit/sn: konuşma',
    # cerclic/ui/compress_editor.py:194
    '{percent} % · sans perte': '%{percent} · kayıpsız',
    # cerclic/ui/compress_editor.py:248, cerclic/ui/crop_editor.py:99, cerclic/ui/crop_editor.py:531 ...
    'Chargement…': 'Yükleniyor…',
    # cerclic/ui/compress_editor.py:367, cerclic/ui/compress_editor.py:601
    'au lieu de {size} · {gain}': '{size} yerine · {gain}',
    # cerclic/ui/compress_editor.py:201
    'Pas de gain': 'Kazanç yok',
    # cerclic/ui/compress_editor.py:201
    'pas de gain': 'kazanç yok',
    # cerclic/ui/compress_editor.py:203
    'Impossible': 'Başarısız',
    # cerclic/ui/compress_editor.py:203
    'impossible': 'başarısız',
    # cerclic/ui/compress_editor.py:221, cerclic/ui/compress_editor.py:574, cerclic/ui/compress_editor.py:627
    'calcul…': 'hesaplanıyor…',
    # cerclic/ui/compress_editor.py:344
    'Choisis la qualité · {key} pour compresser': 'Kaliteyi seçin · sıkıştırmak için {key}',
    # cerclic/ui/compress_editor.py:346
    'Choisis la force · {key} pour compresser': 'Sıkıştırma düzeyini seçin · sıkıştırmak için {key}',
    # cerclic/ui/compress_editor.py:382, cerclic/actions/registry.py:208, cerclic/actions/registry.py:251 ...
    'Compresser': 'Sıkıştır',
    # cerclic/ui/compress_editor.py:408, cerclic/ui/settings_window.py:481, cerclic/ui/settings_window.py:923
    'Qualité': 'Kalite',
    # cerclic/ui/compress_editor.py:525, cerclic/actions/registry.py:212, cerclic/actions/registry.py:255 ...
    'Compression': 'Sıkıştırma',
    # cerclic/ui/compress_editor.py:294
    "Survole l'image : détail à 100 %": 'Görüntünün üzerine gelin: %100 ayrıntı',
    # cerclic/ui/compress_editor.py:295
    "Survole l'image : détail": 'Görüntünün üzerine gelin: ayrıntı',
    # cerclic/ui/compress_editor.py:445
    'GIF : sans réglage': 'GIF: ayar yok',
    # pluriel : 'Aperçu : {name} · total pour {n} images, estimé sur {sampled}' | cerclic/ui/compress_editor.py:509
    'Aperçu : {name} · total pour {n} image, estimé sur {sampled}': ['Önizleme: {name} · {n} görüntü için toplam, {sampled} görüntüden tahmin', 'Önizleme: {name} · {n} görüntü için toplam, {sampled} görüntüden tahmin'],
    # pluriel : 'Aperçu : {name} · total pour {n} images' | cerclic/ui/compress_editor.py:513
    'Aperçu : {name} · total pour {n} image': ['Önizleme: {name} · {n} görüntü için toplam', 'Önizleme: {name} · {n} görüntü için toplam'],
    # cerclic/ui/compress_editor.py:605, cerclic/actions/video.py:361
    'Pas plus léger': 'Daha hafif değil',
    # cerclic/ui/compress_editor.py:182
    'Compression impossible.': 'Sıkıştırılamıyor.',
    # pluriel : '{n} laissées de côté' | cerclic/ui/compress_editor.py:516
    '{n} laissée de côté': ['{n} tanesi atlandı', '{n} tanesi atlandı'],
    # cerclic/ui/compress_editor.py:585
    'Essaie une compression plus forte.': 'Daha güçlü bir sıkıştırma deneyin.',
    # cerclic/ui/compress_editor.py:609
    'Original : {size} · baisse la qualité': 'Orijinal: {size} · kaliteyi düşürün',
    # cerclic/ui/compress_editor.py:610
    'Original : {size} · compresse plus fort': 'Orijinal: {size} · daha güçlü sıkıştırın',
    # cerclic/ui/crop_editor.py:27
    'Libre': 'Serbest',
    # cerclic/ui/crop_editor.py:27
    'Original': 'Orijinal',
    # cerclic/ui/crop_editor.py:427
    'Glisse les coins · {key} pour rogner': 'Köşeleri sürükleyin · kırpmak için {key}',
    # cerclic/ui/crop_editor.py:480, cerclic/actions/registry.py:188, cerclic/actions/registry.py:246
    'Rogner': 'Kırp',
    # cerclic/ui/crop_editor.py:557, cerclic/ui/social_editor.py:545
    '{index} / {count}': '{index} / {count}',
    # cerclic/ui/crop_editor.py:461, cerclic/actions/registry.py:284
    'Toutes les pages': 'Tüm sayfalar',
    # cerclic/ui/crop_editor.py:469
    'Image entière': 'Tüm görüntü',
    # cerclic/ui/crop_editor.py:471
    "Reprendre toute l'image": 'Görüntünün tamamını seç',
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
    'Fermer (Échap)': 'Kapat (Esc)',
    # cerclic/ui/pages_editor.py:127
    'Glisse pour trier · {key} pour enlever': 'Sıralamak için sürükleyin · kaldırmak için {key}',
    # cerclic/ui/pages_editor.py:136
    'Pivoter à gauche': 'Sola döndür',
    # cerclic/ui/pages_editor.py:139
    'Pivoter à droite ({key} + R)': 'Sağa döndür ({key} + R)',
    # cerclic/ui/pages_editor.py:147
    'Vers le début ({key} + {arrow})': 'Başa taşı ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:151
    'Vers la fin ({key} + {arrow})': 'Sona taşı ({key} + {arrow})',
    # cerclic/ui/pages_editor.py:162
    'Extraire la sélection': 'Seçimi ayıkla',
    # cerclic/ui/pages_editor.py:164
    'Un nouveau PDF avec seulement les pages choisies': 'Yalnızca seçilen sayfaları içeren yeni bir PDF',
    # cerclic/ui/pages_editor.py:167
    'Réinitialiser': 'Sıfırla',
    # cerclic/ui/pages_editor.py:175, cerclic/ui/signature.py:215
    'Enregistrer': 'Kaydet',
    # pluriel : '{n} sélectionnées sur {count}' | cerclic/ui/pages_editor.py:276
    '{n} sélectionnée sur {count}': ['{count} sayfadan {n} tanesi seçili', '{count} sayfadan {n} tanesi seçili'],
    # pluriel : '{n} pages' | cerclic/ui/pages_editor.py:277
    '{n} page': ['{n} sayfa', '{n} sayfa'],
    # cerclic/ui/radial.py:245, cerclic/ui/radial.py:214, cerclic/actions/pdf.py:735
    'Plus': 'Diğer',
    # cerclic/ui/radial.py:479
    '‹ Retour': '‹ Geri',
    # cerclic/ui/radial.py:202
    '{category} ({n})': '{category} ({n})',
    # cerclic/ui/radial.py:215
    "D'autres outils": 'Diğer araçlar',
    # cerclic/ui/settings_window.py:476, cerclic/ui/settings_window.py:607
    'Général': 'Genel',
    # cerclic/ui/settings_window.py:477, cerclic/ui/settings_window.py:705
    'Raccourci clavier': 'Klavye kısayolu',
    # cerclic/ui/settings_window.py:478, cerclic/ui/settings_window.py:758
    'Clic droit': 'Sağ tık',
    # cerclic/ui/settings_window.py:479, cerclic/ui/settings_window.py:800
    'Fichiers créés': 'Oluşturulan dosyalar',
    # cerclic/ui/settings_window.py:480, cerclic/ui/settings_window.py:890, cerclic/actions/registry.py:245
    'Signature': 'İmza',
    # cerclic/ui/settings_window.py:482, cerclic/ui/settings_window.py:968
    'À propos': 'Hakkında',
    # cerclic/ui/settings_window.py:593
    'Version {version}': 'Sürüm {version}',
    # cerclic/ui/settings_window.py:600
    "Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, puis appuie sur {combo}.": "Dosya Gezgini'nde veya masaüstünde bir ya da birkaç dosya seçin, sonra {combo} kısayolunu kullanın.",
    # cerclic/ui/settings_window.py:164, cerclic/ui/settings_window.py:219, cerclic/ui/settings_window.py:259 ...
    'Modifier': 'Değiştir',
    # cerclic/ui/settings_window.py:167, cerclic/ui/settings_window.py:939
    'Par défaut': 'Varsayılan',
    # cerclic/ui/settings_window.py:205, cerclic/ui/settings_window.py:249, cerclic/ui/settings_window.py:270
    'Appuie sur ta combinaison…': 'Tuş kombinasyonunuza basın…',
    # cerclic/ui/settings_window.py:234, cerclic/ui/settings_window.py:261
    'Vérification…': 'Denetleniyor…',
    # cerclic/ui/settings_window.py:592
    'Version {version} · Microsoft Store': 'Sürüm {version} · Microsoft Store',
    # cerclic/ui/settings_window.py:598
    'Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, puis appuie sur {combo}.': "Finder'da veya masaüstünde bir ya da birkaç dosya seçin, sonra {combo} kısayolunu kullanın.",
    # cerclic/ui/settings_window.py:619
    'Ouvrir la roue': 'Çarkı açmak',
    # cerclic/ui/settings_window.py:625
    'Clic droit sur le fichier, Actions rapides, puis « Cerclic ». Ou : Ouvrir avec, puis Cerclic.': 'Dosyaya sağ tıklayın, Hızlı Eylemler, sonra “Cerclic”. Ya da: Birlikte Aç, sonra Cerclic.',
    # cerclic/ui/settings_window.py:642
    'Démarrage': 'Başlangıç',
    # cerclic/ui/settings_window.py:652
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier Applications.': "Cerclic'i kapatır. Yeniden başlatmak için Uygulamalar klasöründen açın.",
    # cerclic/ui/settings_window.py:667, cerclic/ui/settings_window.py:674
    'Langue': 'Dil',
    # cerclic/ui/settings_window.py:668
    "Automatique (langue de l'ordinateur)": 'Otomatik (bilgisayarın dili)',
    # cerclic/ui/settings_window.py:690, cerclic/ui/settings_window.py:1000
    'Désinstaller Cerclic': "Cerclic'i kaldır",
    # cerclic/ui/settings_window.py:691
    "Retirer Cerclic du clic droit et de l'ouverture de session, puis le quitter ?": 'Cerclic sağ tık menüsünden ve oturum açılışından kaldırılıp kapatılsın mı?',
    # cerclic/ui/settings_window.py:693
    'Désinstaller': 'Kaldır',
    # cerclic/ui/settings_window.py:706
    'Une combinaison de touches ouvre la roue sur les fichiers sélectionnés.': 'Bir tuş kombinasyonu, seçili dosyalarda çarkı açar.',
    # cerclic/ui/settings_window.py:709, cerclic/ui/settings_window.py:712
    'Ouvrir la roue au clavier': 'Çarkı klavyeyle aç',
    # cerclic/ui/settings_window.py:759
    '« Cerclic » dans le menu du clic droit de tes fichiers.': 'Dosyalarınızın sağ tık menüsünde “Cerclic”.',
    # cerclic/ui/settings_window.py:761
    '« Cerclic » dans le clic droit': 'Sağ tık menüsünde “Cerclic”',
    # cerclic/ui/settings_window.py:801
    "Ton fichier d'origine n'est jamais modifié : chaque action crée un nouveau fichier.": 'Orijinal dosyanız hiçbir zaman değiştirilmez: her işlem yeni bir dosya oluşturur.',
    # cerclic/ui/settings_window.py:803
    'Où les enregistrer': 'Nereye kaydedilsin',
    # cerclic/ui/settings_window.py:809
    "À côté du fichier d'origine": 'Orijinal dosyanın yanına',
    # cerclic/ui/settings_window.py:810
    'Dans le même dossier, par exemple sur le Bureau si la photo y est. Recommandé.': 'Aynı klasöre, örneğin fotoğraf masaüstündeyse masaüstüne. Önerilir.',
    # cerclic/ui/settings_window.py:812
    'Dans un dossier de mon choix': 'Seçtiğim bir klasöre',
    # cerclic/ui/settings_window.py:813
    'Tous les fichiers créés au même endroit.': 'Oluşturulan tüm dosyalar aynı yerde.',
    # cerclic/ui/settings_window.py:814
    'Me demander à chaque fois': 'Her seferinde sor',
    # cerclic/ui/settings_window.py:815
    'Cerclic te demande le dossier avant de créer le fichier.': 'Cerclic, dosyayı oluşturmadan önce klasörü size sorar.',
    # cerclic/ui/settings_window.py:828
    'Choisir…': 'Seç…',
    # cerclic/ui/settings_window.py:872
    'Dossier des fichiers créés': 'Oluşturulan dosyaların klasörü',
    # cerclic/ui/settings_window.py:891
    'Pour signer tes PDF en un geste. Elle reste sur cet ordinateur.': "PDF'lerinizi tek hareketle imzalamak için. İmzanız bu bilgisayarda kalır.",
    # cerclic/ui/settings_window.py:902
    'Dessiner…': 'Çiz…',
    # cerclic/ui/settings_window.py:904
    'Importer une photo…': 'Fotoğraf içe aktar…',
    # cerclic/ui/settings_window.py:906, cerclic/ui/signature.py:205
    'Effacer': 'Temizle',
    # cerclic/ui/settings_window.py:924
    'Le juste milieu entre le poids des fichiers et leur netteté.': 'Dosya boyutu ile netlik arasındaki denge.',
    # cerclic/ui/settings_window.py:954, cerclic/ui/settings_window.py:955
    '{value} %': '%{value}',
    # cerclic/ui/settings_window.py:993
    'Voir': 'Göster',
    # cerclic/ui/settings_window.py:1129
    'Choisir une photo de ta signature': 'İmzanızın fotoğrafını seçin',
    # cerclic/ui/settings_window.py:197, cerclic/ui/settings_window.py:244, cerclic/ui/settings_window.py:278
    'Raccourci inchangé.': 'Kısayol değişmedi.',
    # cerclic/ui/settings_window.py:206
    'Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour annuler.': 'Örnekler: Shift + Cmd + Boşluk, Ctrl + Option + X. Vazgeçmek için Esc.',
    # cerclic/ui/settings_window.py:208
    'Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C. Échap pour annuler.': 'Örnekler: Ctrl + Alt + Boşluk, Ctrl + Shift + X, Win + Shift + C. Vazgeçmek için Esc.',
    # cerclic/ui/settings_window.py:313
    'Plus léger': 'Daha hafif',
    # cerclic/ui/settings_window.py:315
    'Plus net': 'Daha net',
    # cerclic/ui/settings_window.py:384
    'Bienvenue dans Cerclic': "Cerclic'e hoş geldiniz",
    # cerclic/ui/settings_window.py:544
    "Les changements s'appliquent aussitôt.": 'Değişiklikler hemen uygulanır.',
    # cerclic/ui/settings_window.py:608
    "Deux façons d'ouvrir la roue, le démarrage et la langue.": 'Çarkı açmanın iki yolu, başlangıç ve dil.',
    # cerclic/ui/settings_window.py:610
    "Trois façons d'ouvrir la roue, le démarrage et la langue.": 'Çarkı açmanın üç yolu, başlangıç ve dil.',
    # cerclic/ui/settings_window.py:620
    'Au clavier': 'Klavyeyle',
    # cerclic/ui/settings_window.py:628
    "Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe par « Afficher d'autres options ».": 'Dosyaya Shift + sağ tıklayın, sonra “Cerclic”. Shift olmadan “Daha fazla seçenek göster” yolunu kullanın.',
    # cerclic/ui/settings_window.py:631
    'Clic droit sur le fichier, puis « Cerclic ».': 'Dosyaya sağ tıklayın, sonra “Cerclic”.',
    # cerclic/ui/settings_window.py:632
    'À la souris': 'Fareyle',
    # cerclic/ui/settings_window.py:643
    'Lancer Cerclic avec le Mac': "Cerclic'i Mac ile başlat",
    # cerclic/ui/settings_window.py:644, cerclic/ui/settings_window.py:648
    'Lancer Cerclic avec Windows': "Cerclic'i Windows ile başlat",
    # cerclic/ui/settings_window.py:649
    'Recommandé : la roue est prête dès que tu en as besoin.': 'Önerilir: çark, ihtiyaç duyduğunuz anda hazır olur.',
    # cerclic/ui/settings_window.py:655
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.': "Cerclic'i kapatır. Yeniden başlatmak için Başlat menüsünden açın.",
    # cerclic/ui/settings_window.py:657
    'Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le menu Démarrer.': "Cerclic'i kapatır. Yeniden başlatmak için masaüstünden veya Başlat menüsünden açın.",
    # cerclic/ui/settings_window.py:661
    'Arrêter Cerclic': "Cerclic'i durdur",
    # cerclic/ui/settings_window.py:661
    "La roue ne s'ouvrira plus jusqu'au prochain lancement.": 'Çark, bir sonraki başlatmaya kadar açılmaz.',
    # cerclic/ui/settings_window.py:674
    'Celle des menus, des fenêtres et des messages de Cerclic.': "Cerclic'in menü, pencere ve mesajlarının dili.",
    # cerclic/ui/settings_window.py:729
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par macOS ou une autre application, Cerclic te le dit et garde l'ancienne.": '“Değiştir” düğmesine tıklayın, sonra tuş kombinasyonunuza basın. macOS veya başka bir uygulama bu kombinasyonu zaten kullanıyorsa Cerclic bunu size söyler ve eskisini korur.',
    # cerclic/ui/settings_window.py:732
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Programlanabilir düğmeli bir fareniz mi var? Bir düğmeyi F13 ile F20 arasındaki bir tuşa atayın, sonra o tuşu burada seçin: bu düğmeye tıklamak çarkı açar.',
    # cerclic/ui/settings_window.py:736
    "« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise par Windows ou une autre application, Cerclic te le dit et garde l'ancienne.": '“Değiştir” düğmesine tıklayın, sonra tuş kombinasyonunuza basın. Windows veya başka bir uygulama bu kombinasyonu zaten kullanıyorsa Cerclic bunu size söyler ve eskisini korur.',
    # cerclic/ui/settings_window.py:739
    'Une souris à boutons programmables ? Règle un bouton sur une touche F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la roue.': 'Programlanabilir düğmeli bir fareniz mi var? Bir düğmeyi F13 ile F24 arasındaki bir tuşa atayın, sonra o tuşu burada seçin: bu düğmeye tıklamak çarkı açar.',
    # cerclic/ui/settings_window.py:744
    'Autorisation': 'İzin',
    # cerclic/ui/settings_window.py:745
    'Réglages…': 'Ayarlar…',
    # cerclic/ui/settings_window.py:779, cerclic/ui/settings_window.py:782
    'Menu clic droit complet': 'Tam sağ tık menüsü',
    # cerclic/ui/settings_window.py:787
    'Pas dans Actions rapides ? Clic droit sur un fichier, Actions rapides puis Personnaliser, et coche « Cerclic ». Il est aussi toujours dans Ouvrir avec.': "Hızlı Eylemler'de yok mu? Bir dosyaya sağ tıklayın, Hızlı Eylemler, sonra Özelleştir'i seçin ve “Cerclic” kutusunu işaretleyin. Cerclic her zaman Birlikte Aç menüsünde de bulunur.",
    # cerclic/ui/settings_window.py:929, cerclic/actions/pdf.py:549, cerclic/actions/pdf.py:474 ...
    'Compression des images': 'Görüntü sıkıştırma',
    # cerclic/ui/settings_window.py:930
    'Réglage proposé par « Compresser », qui montre la taille obtenue et retient ton dernier choix.': '“Sıkıştır” işleminin önerdiği ayar: elde edilen boyutu gösterir ve son seçiminizi hatırlar.',
    # cerclic/ui/settings_window.py:936
    'JPG créés par les autres actions': "Diğer işlemlerin oluşturduğu JPG'ler",
    # cerclic/ui/settings_window.py:937
    'Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas.': "Kırpma, döndürme, dönüştürme… %90'da kayıp fark edilmez.",
    # cerclic/ui/settings_window.py:983
    "Rogner, signer, compresser, convertir, mettre au format des réseaux sociaux… en un geste, sans ouvrir d'autre application.": 'Kırpma, imzalama, sıkıştırma, dönüştürme, sosyal medya formatına uyarlama… tek hareketle, başka bir uygulama açmadan.',
    # cerclic/ui/settings_window.py:991
    'Journal': 'Günlük',
    # cerclic/ui/settings_window.py:991
    "En cas de souci, ce fichier aide à comprendre ce qui s'est passé.": 'Bir sorun olduğunda bu dosya ne olduğunu anlamaya yardımcı olur.',
    # cerclic/ui/settings_window.py:995
    'Licences': 'Lisanslar',
    # cerclic/ui/settings_window.py:996
    "Les composants libres qu'utilise Cerclic et leurs licences.": "Cerclic'in kullandığı açık kaynak bileşenler ve lisansları.",
    # cerclic/ui/settings_window.py:998
    'Désinstaller…': 'Kaldır…',
    # cerclic/ui/settings_window.py:1122
    "Aucune signature pour l'instant : dessine-la ou importe une photo. Sinon, elle te sera demandée la première fois que tu signes.": 'Henüz imza yok: çizin ya da bir fotoğraf içe aktarın. Aksi hâlde ilk kez imzaladığınızda istenecek.',
    # cerclic/ui/settings_window.py:1130
    'Images': 'Görüntüler',
    # cerclic/ui/settings_window.py:622
    'Régler : au clavier': 'Ayarla: klavyeyle',
    # cerclic/ui/settings_window.py:633
    'Régler : à la souris': 'Ayarla: fareyle',
    # cerclic/ui/settings_window.py:636
    'En glissant': 'Sürükleyerek',
    # cerclic/ui/settings_window.py:647
    "Ouvrir Cerclic à l'ouverture de session": "Oturum açıldığında Cerclic'i aç",
    # cerclic/ui/settings_window.py:713
    'Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.': "Finder'da veya masaüstünde seçili dosyalarda.",
    # cerclic/ui/settings_window.py:715
    "Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau.": "Dosya Gezgini'nde veya masaüstünde seçili dosyalarda.",
    # cerclic/ui/settings_window.py:747
    'Lire la sélection du Finder': 'Finder seçimini oku',
    # cerclic/ui/settings_window.py:748
    'La première fois, macOS demande si Cerclic peut contrôler le Finder : accepte. Cerclic y lit seulement les fichiers sélectionnés.': "İlk seferde macOS, Cerclic'in Finder'ı denetleyip denetleyemeyeceğini sorar: izin verin. Cerclic orada yalnızca seçili dosyaları okur.",
    # cerclic/ui/settings_window.py:765
    '« Cerclic » dans le clic droit du Finder': "Finder'ın sağ tık menüsünde “Cerclic”",
    # cerclic/ui/settings_window.py:766
    'Dans le menu Actions rapides de tes fichiers, dans le Finder et sur le Bureau.': "Dosyalarınızın Hızlı Eylemler menüsünde, Finder'da ve masaüstünde.",
    # cerclic/ui/settings_window.py:783
    "Affiche le menu complet sans passer par « Afficher d'autres options ». Cerclic proposera de redémarrer l'Explorateur.": "“Daha fazla seçenek göster” adımına gerek kalmadan tam menüyü gösterir. Cerclic, Dosya Gezgini'ni yeniden başlatmayı önerecek.",
    # cerclic/ui/settings_window.py:791
    'Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre directement le menu complet, avec « Cerclic ».': 'İpucu: hiçbir şeyi değiştirmeden, bir dosyaya Shift + sağ tık doğrudan “Cerclic” içeren tam menüyü açar.',
    # cerclic/ui/settings_window.py:852
    'Aucun dossier choisi.': 'Klasör seçilmedi.',
    # cerclic/ui/settings_window.py:1001
    "Retire « Cerclic » du clic droit et de l'ouverture de session, puis quitte. Il restera à mettre Cerclic.app à la corbeille.": "“Cerclic” öğesini sağ tık menüsünden ve oturum açılışından kaldırır, sonra kapanır. Ardından Cerclic.app uygulamasını Çöp Sepeti'ne taşımanız yeterli.",
    # cerclic/ui/settings_window.py:1077
    'Raccourci désactivé : le clic droit « Cerclic » reste disponible.': 'Kısayol kapalı: sağ tık menüsündeki “Cerclic” kullanılabilir durumda.',
    # cerclic/ui/settings_window.py:1078
    'Raccourci désactivé.': 'Kısayol kapalı.',
    # cerclic/ui/settings_window.py:613
    "Cerclic tourne maintenant en arrière-plan : son icône est dans la barre des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic artık arka planda çalışıyor: simgesi ekranın üstündeki menü çubuğunda. Çarkı açmak için en sevdiğiniz yolu aşağıdan seçin.',
    # cerclic/ui/settings_window.py:616
    "Cerclic tourne maintenant en arrière-plan : son icône est près de l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous ta façon préférée d'ouvrir la roue.": 'Cerclic artık arka planda çalışıyor: simgesi saatin yanında (bazen küçük ^ okunun altında gizli). Çarkı açmak için en sevdiğiniz yolu aşağıdan seçin.',
    # cerclic/ui/settings_window.py:637
    "Glisse des fichiers sur l'icône de Cerclic (dans Applications ou le Dock).": "Dosyaları Cerclic simgesinin üzerine sürükleyin (Uygulamalar klasöründe veya Dock'ta).",
    # cerclic/ui/settings_window.py:639
    "Glisse des fichiers sur l'icône de Cerclic.": 'Dosyaları Cerclic simgesinin üzerine sürükleyin.',
    # cerclic/ui/settings_window.py:769, cerclic/ui/settings_window.py:773
    '« Cerclic » dans le clic droit des fichiers': 'Dosyaların sağ tık menüsünde “Cerclic”',
    # cerclic/ui/settings_window.py:770
    "En haut du menu des images, PDF, vidéos et sons, dans l'Explorateur et sur le Bureau.": "Dosya Gezgini'nde ve masaüstünde; görüntülerin, PDF'lerin, videoların ve seslerin menüsünün en üstünde.",
    # cerclic/ui/settings_window.py:774
    "Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le Bureau et dans les fenêtres Ouvrir et Enregistrer.": "Görüntülerde, PDF'lerde, videolarda ve seslerde; Dosya Gezgini'nde, masaüstünde ve Aç ile Kaydet pencerelerinde.",
    # cerclic/ui/settings_window.py:838
    "Leur nom : le nom d'origine, plus ce qui a changé, par exemple photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic ajoute un numéro : rien n'est jamais écrasé.": 'Adları: orijinal ad ve değişen şey, örneğin foto.jpg dosyasının yanında foto (sıkıştırılmış).jpg. Bu ad zaten kullanılıyorsa Cerclic bir numara ekler: hiçbir şeyin üzerine yazılmaz.',
    # cerclic/ui/settings_window.py:841
    "Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface aussitôt.": 'Bir sonucu beğenmediniz mi? Kartındaki “Sil” düğmesi onu hemen siler.',
    # cerclic/ui/settings_window.py:854
    'Dossier de ton choix : {folder}': 'Seçtiğiniz klasör: {folder}',
    # cerclic/ui/settings_window.py:856
    "Dossier de ton choix : aucun pour l'instant.": 'Seçtiğiniz klasör: henüz yok.',
    # cerclic/ui/settings_window.py:915
    "Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier transparent et garde l'encre.": 'Beyaz kâğıttaki imzanızın bir fotoğrafı yeterli: Cerclic kâğıdı saydam yapar, mürekkebi korur.',
    # cerclic/ui/settings_window.py:917
    'Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la signature et appuie sur {key}.': "İmzalamak için: bir PDF'de sağ tık ya da kısayol, sonra “İmzala”. İmzayı yerleştirip {key} tuşuna basın.",
    # cerclic/ui/settings_window.py:752
    'Refusé par erreur ? Dans Automatisation, coche « Finder » sous Cerclic.': "Yanlışlıkla mı reddettiniz? Otomasyon bölümünde Cerclic'in altındaki “Finder” kutusunu işaretleyin.",
    # cerclic/ui/settings_window.py:1082
    '✓ Actif partout sur le Mac.': "✓ Mac'te her yerde etkin.",
    # cerclic/ui/settings_window.py:1083
    '✓ Actif partout dans Windows.': "✓ Windows'ta her yerde etkin.",
    # cerclic/ui/settings_window.py:1085
    'macOS ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'macOS veya başka bir uygulama bu kombinasyonu zaten kullanıyor. “Değiştir” ile başka bir kombinasyon seçin.',
    # cerclic/ui/settings_window.py:1089
    'Windows ou une autre application utilise déjà cette combinaison. Choisis-en une autre avec « Modifier ».': 'Windows veya başka bir uygulama bu kombinasyonu zaten kullanıyor. “Değiştir” ile başka bir kombinasyon seçin.',
    # cerclic/ui/signature.py:76
    'Aucun trait de signature trouvé dans cette image.': 'Bu görüntüde imza çizgisi bulunamadı.',
    # cerclic/ui/signature.py:196
    'Ta signature': 'İmzanız',
    # cerclic/ui/signature.py:196
    'Gardée pour les prochaines fois': 'Sonraki kullanımlar için saklanır',
    # cerclic/ui/signature.py:200
    'Importer…': 'İçe aktar…',
    # cerclic/ui/signature.py:202
    'Une photo de ta signature sur papier blanc': 'Beyaz kâğıttaki imzanızın fotoğrafı',
    # cerclic/ui/signature.py:405
    'Glisse la signature · tire un coin · {key} pour signer': 'İmzayı sürükleyin · köşesinden çekin · imzalamak için {key}',
    # cerclic/ui/signature.py:413
    'Changer': 'Değiştir',
    # cerclic/ui/signature.py:415
    'Dessiner ou importer une autre signature': 'Başka bir imza çizin veya içe aktarın',
    # cerclic/ui/signature.py:429, cerclic/actions/registry.py:240
    'Signer': 'İmzala',
    # cerclic/ui/signature.py:523
    'Page {page} / {count}': 'Sayfa {page} / {count}',
    # cerclic/ui/signature.py:153
    'Signe ici': 'Buraya imzalayın',
    # cerclic/ui/signature.py:236
    'Choisir une image de ta signature': 'İmzanızın görüntüsünü seçin',
    # cerclic/ui/signature.py:237
    'Images ({patterns})': 'Görüntüler ({patterns})',
    # cerclic/ui/social_editor.py:32
    'Remplir': 'Doldur',
    # cerclic/ui/social_editor.py:32
    "L'image couvre tout le cadre, ce qui dépasse est coupé.\nGlisse-la pour choisir la partie gardée, molette pour zoomer.": 'Görüntü tüm çerçeveyi kaplar, taşan kısım kesilir.\nTutulacak kısmı seçmek için sürükleyin, yakınlaştırmak için kaydırma tekerleğini kullanın.',
    # cerclic/ui/social_editor.py:34
    'Fond flou': 'Bulanık arka plan',
    # cerclic/ui/social_editor.py:34
    "Toute l'image, rien n'est coupé.\nAutour : la même image, floutée.": 'Görüntünün tamamı, hiçbir şey kesilmez.\nÇevresi: aynı görüntü, bulanıklaştırılmış.',
    # cerclic/ui/social_editor.py:36
    'Fond blanc': 'Beyaz arka plan',
    # cerclic/ui/social_editor.py:36
    "Toute l'image, rien n'est coupé.\nAutour : du blanc.": 'Görüntünün tamamı, hiçbir şey kesilmez.\nÇevresi: beyaz.',
    # cerclic/ui/social_editor.py:37
    'Fond noir': 'Siyah arka plan',
    # cerclic/ui/social_editor.py:37
    "Toute l'image, rien n'est coupé.\nAutour : du noir.": 'Görüntünün tamamı, hiçbir şey kesilmez.\nÇevresi: siyah.',
    # cerclic/ui/social_editor.py:433
    'Fichier précédent': 'Önceki dosya',
    # cerclic/ui/social_editor.py:438
    'Fichier suivant': 'Sonraki dosya',
    # cerclic/ui/social_editor.py:448
    'Créer': 'Oluştur',
    # cerclic/ui/social_editor.py:413
    '{format} {ratio}': '{format} {ratio}',
    # cerclic/ui/social_editor.py:553
    'Glisse et zoome · {key} pour créer': 'Sürükleyin ve yakınlaştırın · oluşturmak için {key}',
    # cerclic/ui/social_editor.py:555
    "Rien n'est coupé · {key} pour créer": 'Hiçbir şey kesilmez · oluşturmak için {key}',
    # cerclic/ui/social_editor.py:559
    'La partie gardée est plus petite que le format : agrandie, elle sera un peu moins nette.': 'Tutulan kısım formattan küçük: büyütüleceği için biraz daha az net olacak.',
    # cerclic/ui/social_editor.py:562
    'La vidéo est plus petite que le format : agrandie, elle sera un peu moins nette.': 'Video formattan küçük: büyütüleceği için biraz daha az net olacak.',
    # cerclic/ui/social_editor.py:565
    "L'image est plus petite que le format : agrandie, elle sera un peu moins nette.": 'Görüntü formattan küçük: büyütüleceği için biraz daha az net olacak.',
    # cerclic/ui/trim_editor.py:59
    'Durée inconnue': 'Süre bilinmiyor',
    # cerclic/ui/trim_editor.py:255
    'Tire les poignées · {key} pour raccourcir': 'Tutamaçları çekin · kısaltmak için {key}',
    # cerclic/ui/trim_editor.py:278, cerclic/actions/registry.py:312, cerclic/actions/registry.py:347 ...
    'Raccourcir': 'Kısalt',
    # cerclic/ui/trim_editor.py:386
    '{start}  →  {end}': '{start}  →  {end}',
    # cerclic/ui/trim_editor.py:388
    'Durée {duration}': 'Süre {duration}',
    # cerclic/ui/trim_editor.py:317, cerclic/actions/video.py:352
    'Durée illisible : fichier endommagé ?': 'Süre okunamıyor: dosya hasarlı mı?',
    # cerclic/ui/trim_editor.py:392
    'Début {time}': 'Başlangıç {time}',
    # cerclic/ui/trim_editor.py:393
    'Fin {time}': 'Bitiş {time}',
    # pluriel : '« {name} » a {n} pages : seule la première serait gardée. Utilise « {action} » pour les garder toutes.' | cerclic/actions/images.py:137
    '« {name} » a {n} page : seule la première serait gardée. Utilise « {action} » pour les garder toutes.': ['“{name}” dosyasında {n} sayfa var: yalnızca ilki tutulur. Hepsini tutmak için “{action}” işlemini kullanın.', '“{name}” dosyasında {n} sayfa var: yalnızca ilki tutulur. Hepsini tutmak için “{action}” işlemini kullanın.'],
    # cerclic/actions/images.py:350, cerclic/actions/video.py:652
    "C'est déjà un {format}.": 'Bu zaten bir {format} dosyası.',
    # cerclic/actions/images.py:420
    'Cette image est déjà bien compressée.': 'Bu görüntü zaten iyi sıkıştırılmış.',
    # cerclic/actions/images.py:469, cerclic/actions/pdf.py:599
    'La zone à rogner est vide.': 'Kırpılacak alan boş.',
    # cerclic/actions/images.py:471
    "Le cadre couvre toute l'image : rien à rogner.": 'Çerçeve görüntünün tamamını kaplıyor: kırpılacak bir şey yok.',
    # cerclic/actions/images.py:698
    'Il faut au moins deux images.': 'En az iki görüntü gerekir.',
    # cerclic/actions/images.py:765, cerclic/actions/registry.py:229
    'Assemblage': 'Birleştirme',
    # cerclic/actions/images.py:651
    'Cette image ne contient aucune information privée.': 'Bu görüntü hiçbir özel bilgi içermiyor.',
    # cerclic/actions/images.py:732, cerclic/actions/pdf.py:241
    'Image {i} sur {n}': 'Görüntü {i}/{n}',
    # cerclic/actions/images.py:141, cerclic/actions/registry.py:220
    'En PDF': "PDF'ye dönüştür",
    # cerclic/actions/images.py:437
    "L'image fait déjà {size} px ou moins.": 'Görüntü zaten {size} px veya daha küçük.',
    # cerclic/actions/images.py:704
    'Image illisible : {name}': 'Görüntü okunamıyor: {name}',
    # cerclic/actions/pdf.py:59
    '«\xa0{name}\xa0» est protégé par un mot de passe.': '“{name}” parolayla korunuyor.',
    # cerclic/actions/pdf.py:58
    'Mot de passe incorrect.': 'Parola yanlış.',
    # cerclic/actions/pdf.py:628, cerclic/actions/registry.py:269
    'Conversion en Word': "Word'e dönüştürme",
    # cerclic/actions/pdf.py:47
    "Ce fichier n'est pas un PDF : {name}": 'Bu dosya bir PDF değil: {name}',
    # cerclic/actions/pdf.py:223
    'Aucune image.': 'Görüntü yok.',
    # cerclic/actions/pdf.py:267
    'Il faut au moins deux PDF pour fusionner.': 'Birleştirmek için en az iki PDF gerekir.',
    # cerclic/actions/pdf.py:323
    'Aucune page à garder.': 'Tutulacak sayfa yok.',
    # cerclic/actions/pdf.py:349
    "Aucun texte dans ce PDF : c'est sûrement un scan (une image).": "Bu PDF'de metin yok: büyük olasılıkla taranmış bir belge (görüntü).",
    # cerclic/actions/pdf.py:570
    'Vérification': 'Denetleniyor',
    # cerclic/actions/pdf.py:579
    'Ce PDF est déjà bien compressé.': 'Bu PDF zaten iyi sıkıştırılmış.',
    # cerclic/actions/pdf.py:601
    'Le cadre couvre toute la page : rien à rogner.': 'Çerçeve sayfanın tamamını kaplıyor: kırpılacak bir şey yok.',
    # cerclic/actions/pdf.py:643
    'Le texte du filigrane est vide.': 'Filigran metni boş.',
    # cerclic/actions/pdf.py:705
    'Aucune signature enregistrée.': 'Kayıtlı imza yok.',
    # cerclic/actions/pdf.py:731
    'Le mot de passe est vide.': 'Parola boş.',
    # cerclic/actions/pdf.py:733
    "Ce PDF a déjà un mot de passe. Pour en mettre un autre, retire d'abord celui-ci ({more}, puis {action}).": "Bu PDF'nin zaten bir parolası var. Başka bir parola koymak için önce bunu kaldırın ({more}, sonra {action}).",
    # cerclic/actions/pdf.py:745
    "Ce PDF n'est pas protégé.": 'Bu PDF korumalı değil.',
    # cerclic/actions/pdf.py:43
    'PDF endommagé ou illisible : {name}': 'PDF hasarlı ya da okunamıyor: {name}',
    # cerclic/actions/pdf.py:205, cerclic/actions/pdf.py:297, cerclic/actions/pdf.py:346 ...
    'Page {i} sur {n}': 'Sayfa {i}/{n}',
    # cerclic/actions/pdf.py:273
    'PDF {i} sur {n}': 'PDF {i}/{n}',
    # cerclic/actions/pdf.py:290
    "Ce PDF n'a qu'une page.": "Bu PDF'de yalnızca bir sayfa var.",
    # cerclic/actions/pdf.py:327
    'Page introuvable dans ce PDF.': "Sayfa bu PDF'de bulunamadı.",
    # cerclic/actions/pdf.py:329
    "Les pages n'ont pas changé.": 'Sayfalar değişmedi.',
    # cerclic/actions/registry.py:34
    'Image': 'Görüntü',
    # cerclic/actions/registry.py:36
    'Vidéo': 'Video',
    # cerclic/actions/registry.py:37
    'Son': 'Ses',
    # cerclic/actions/registry.py:136
    'Droite': 'Sağa',
    # cerclic/actions/registry.py:137
    'Gauche': 'Sola',
    # cerclic/actions/registry.py:192, cerclic/actions/registry.py:317
    'Réseaux': 'Sosyal medya',
    # cerclic/actions/registry.py:196, cerclic/actions/registry.py:280, cerclic/actions/registry.py:340
    'Pivoter': 'Döndür',
    # cerclic/actions/registry.py:200
    'Redimensionner': 'Yeniden boyutlandır',
    # cerclic/actions/registry.py:213
    'Convertir': 'Dönüştür',
    # cerclic/actions/registry.py:223
    'Copier': 'Kopyala',
    # cerclic/actions/registry.py:226
    'Assembler': 'Birleştir',
    # cerclic/actions/registry.py:233
    'Anonymiser': 'Anonimleştir',
    # cerclic/actions/registry.py:256
    'Fusionner': 'Birleştir',
    # cerclic/actions/registry.py:260
    'Pages': 'Sayfalar',
    # cerclic/actions/registry.py:266
    'En Word': "Word'e dönüştür",
    # cerclic/actions/registry.py:270
    'En images': 'Görüntülere dönüştür',
    # cerclic/actions/registry.py:276
    'Diviser': 'Böl',
    # cerclic/actions/registry.py:285, cerclic/actions/registry.py:289
    'Filigrane': 'Filigran',
    # cerclic/actions/registry.py:290
    'Numéroter': 'Numaralandır',
    # cerclic/actions/registry.py:295
    'En texte': 'Metne dönüştür',
    # cerclic/actions/registry.py:326
    'En MP4': "MP4'e dönüştür",
    # cerclic/actions/registry.py:329
    'En GIF': "GIF'e dönüştür",
    # cerclic/actions/registry.py:332, cerclic/actions/video.py:236
    'Extraire le son': 'Sesi ayıkla',
    # cerclic/actions/registry.py:336
    'Couper le son': 'Sesi kaldır',
    # cerclic/actions/registry.py:352
    'En MP3': "MP3'e dönüştür",
    # cerclic/actions/registry.py:141
    'Miroir': 'Ayna',
    # cerclic/actions/registry.py:191
    'Garder une partie': 'Bir kısmını tut',
    # cerclic/actions/registry.py:191, cerclic/actions/registry.py:250
    'Rognage': 'Kırpma',
    # cerclic/actions/registry.py:194
    'Insta, Story, mobile, PC': 'Insta, Hikaye, mobil, PC',
    # cerclic/actions/registry.py:195, cerclic/actions/registry.py:320
    'Format réseaux sociaux': 'Sosyal medya formatı',
    # cerclic/actions/registry.py:199
    'Tourner ou retourner': 'Döndür veya çevir',
    # cerclic/actions/registry.py:199, cerclic/actions/registry.py:284, cerclic/actions/registry.py:344 ...
    'Rotation': 'Döndürme',
    # cerclic/actions/registry.py:203
    'Moins de pixels': 'Daha az piksel',
    # cerclic/actions/registry.py:203
    'Redimensionnement': 'Yeniden boyutlandırma',
    # cerclic/actions/registry.py:211
    'Plus léger, même taille': 'Daha hafif, aynı ölçüler',
    # cerclic/actions/registry.py:216
    'Changer de format': 'Biçimi değiştir',
    # cerclic/actions/registry.py:216
    'Conversion': 'Dönüştürme',
    # cerclic/actions/registry.py:222
    'Une page par image': 'Görüntü başına bir sayfa',
    # cerclic/actions/registry.py:222
    'Création du PDF': 'PDF oluşturma',
    # cerclic/actions/registry.py:225
    'À coller où tu veux': 'İstediğiniz yere yapıştırın',
    # cerclic/actions/registry.py:225
    'Copie': 'Kopyalama',
    # cerclic/actions/registry.py:229
    'Plusieurs en une': 'Birkaçı tek görüntüde',
    # cerclic/actions/registry.py:236
    'Retire GPS, appareil, date': 'GPS, cihaz ve tarihi siler',
    # cerclic/actions/registry.py:237
    'Anonymisation': 'Anonimleştirme',
    # cerclic/actions/registry.py:245
    'Placer ta signature': 'İmzanızı yerleştirin',
    # cerclic/actions/registry.py:250
    'Couper les marges': 'Kenar boşluklarını kes',
    # cerclic/actions/registry.py:254
    'Plus léger à envoyer': 'Göndermek için daha hafif',
    # cerclic/actions/registry.py:259
    'Un seul PDF': 'Tek bir PDF',
    # cerclic/actions/registry.py:259
    'Fusion': 'Birleştirme',
    # cerclic/actions/registry.py:265
    'Trier, tourner, supprimer': 'Sırala, döndür, sil',
    # cerclic/actions/registry.py:265
    'Organisation des pages': 'Sayfaları düzenleme',
    # cerclic/actions/registry.py:269
    'Modifiable dans Word': "Word'de düzenlenebilir",
    # cerclic/actions/registry.py:273
    'Une image par page': 'Sayfa başına bir görüntü',
    # cerclic/actions/registry.py:273
    'Conversion en images': 'Görüntülere dönüştürme',
    # cerclic/actions/registry.py:279
    'Un PDF par page': 'Sayfa başına bir PDF',
    # cerclic/actions/registry.py:279
    'Découpage en pages': 'Sayfalara bölme',
    # cerclic/actions/registry.py:289
    'Un texte en travers': 'Çapraz bir metin',
    # cerclic/actions/registry.py:294
    'Numéros en bas de page': 'Sayfa altına numaralar',
    # cerclic/actions/registry.py:294
    'Numérotation': 'Numaralandırma',
    # cerclic/actions/registry.py:299
    'Le texte en .txt': 'Metni .txt olarak',
    # cerclic/actions/registry.py:299
    'Extraction du texte': 'Metin ayıklama',
    # cerclic/actions/registry.py:304
    'Avec un mot de passe': 'Parolayla',
    # cerclic/actions/registry.py:304
    'Protection': 'Koruma',
    # cerclic/actions/registry.py:309
    'Retirer le mot de passe': 'Parolayı kaldır',
    # cerclic/actions/registry.py:309
    'Déverrouillage': 'Kilit açma',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Garder un passage': 'Bir bölümü tut',
    # cerclic/actions/registry.py:316, cerclic/actions/registry.py:351
    'Découpe': 'Kısaltma',
    # cerclic/actions/registry.py:319
    'Reels, TikTok, Shorts, PC': 'Reels, TikTok, Shorts, PC',
    # cerclic/actions/registry.py:324
    'Plus légère, en MP4': 'Daha hafif, MP4 olarak',
    # cerclic/actions/registry.py:328, cerclic/actions/registry.py:355
    'Lisible partout': 'Her yerde oynatılır',
    # cerclic/actions/registry.py:328, cerclic/actions/video.py:487
    'Conversion en MP4': "MP4'e dönüştürme",
    # cerclic/actions/registry.py:331
    'Une animation sans son': 'Sessiz bir animasyon',
    # cerclic/actions/registry.py:331
    'Création du GIF': 'GIF oluşturma',
    # cerclic/actions/registry.py:335
    'La bande son en MP3': 'Ses MP3 olarak',
    # cerclic/actions/registry.py:335, cerclic/actions/video.py:544
    'Extraction du son': 'Ses ayıklama',
    # cerclic/actions/registry.py:339
    'La vidéo sans son': 'Sessiz video',
    # cerclic/actions/registry.py:339, cerclic/actions/video.py:623, cerclic/actions/video.py:613
    'Suppression du son': 'Sesi kaldırma',
    # cerclic/actions/registry.py:344
    "Remettre à l'endroit": 'Doğru yöne çevir',
    # cerclic/actions/registry.py:355, cerclic/actions/video.py:658
    'Conversion en MP3': "MP3'e dönüştürme",
    # cerclic/actions/registry.py:359
    'Plus léger, en MP3': 'Daha hafif, MP3 olarak',
    # cerclic/actions/registry.py:88
    'Fichier {i} sur {n}': 'Dosya {i}/{n}',
    # cerclic/actions/registry.py:104
    '« {name} » : {error}': '“{name}”: {error}',
    # cerclic/actions/registry.py:204
    '50 %': '%50',
    # cerclic/actions/registry.py:230
    'Côte à côte': 'Yan yana',
    # cerclic/actions/registry.py:231
    'En colonne': 'Alt alta',
    # cerclic/actions/registry.py:232
    'En grille': 'Izgara',
    # cerclic/actions/social.py:46
    'Carré': 'Kare',
    # cerclic/actions/social.py:47
    'Publication Instagram, Facebook ou LinkedIn': 'Instagram, Facebook veya LinkedIn gönderisi',
    # cerclic/actions/social.py:47
    'carré': 'kare',
    # cerclic/actions/social.py:48
    'Portrait': 'Dikey',
    # cerclic/actions/social.py:49
    'Publication Instagram ou Facebook, la plus grande dans le fil': 'Instagram veya Facebook gönderisi, akışta en büyük olan',
    # cerclic/actions/social.py:50
    'portrait': 'dikey',
    # cerclic/actions/social.py:51
    'Grille': 'Izgara',
    # cerclic/actions/social.py:52
    'Instagram, à la forme exacte de la grille du profil': 'Instagram, profil ızgarasının tam biçiminde',
    # cerclic/actions/social.py:52
    'grille': 'ızgara',
    # cerclic/actions/social.py:53
    'Story': 'Hikaye',
    # cerclic/actions/social.py:54
    'Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts': 'Telefonda tam ekran: Hikaye, Reels, TikTok, YouTube Shorts',
    # cerclic/actions/social.py:55
    'story': 'hikaye',
    # cerclic/actions/social.py:56
    'Paysage': 'Yatay',
    # cerclic/actions/social.py:57
    "Écran d'ordinateur : YouTube, présentation, X": 'Bilgisayar ekranı: YouTube, sunum, X',
    # cerclic/actions/social.py:57
    'paysage': 'yatay',
    # cerclic/actions/social.py:58
    'Bannière': 'Banner',
    # cerclic/actions/social.py:58
    '1,91:1': '1,91:1',
    # cerclic/actions/social.py:59
    'Lien partagé ou image large sur Facebook, LinkedIn ou X': "Facebook, LinkedIn veya X'te paylaşılan bağlantı ya da geniş görüntü",
    # cerclic/actions/social.py:59
    'bannière': 'banner',
    # cerclic/actions/social.py:239
    'Format {name}': '{name} formatı',
    # cerclic/actions/social.py:176
    'Cette image est déjà en {size}.': 'Bu görüntü zaten {size} boyutunda.',
    # cerclic/actions/social.py:228
    'Taille de la vidéo illisible : fichier endommagé ?': 'Video boyutu okunamıyor: dosya hasarlı mı?',
    # cerclic/actions/social.py:230
    'Cette vidéo est déjà en {size}.': 'Bu video zaten {size} boyutunda.',
    # cerclic/actions/video.py:179
    'Le traitement a échoué : le fichier est peut-être endommagé ou dans un format inhabituel.': 'İşlem başarısız oldu: dosya hasarlı ya da alışılmadık bir biçimde olabilir.',
    # cerclic/actions/video.py:43
    'ffmpeg est introuvable : réinstalle Cerclic.': "ffmpeg bulunamadı: Cerclic'i yeniden yükleyin.",
    # cerclic/actions/video.py:170
    'Vidéo endommagée ou format non pris en charge.': 'Video hasarlı ya da biçimi desteklenmiyor.',
    # cerclic/actions/video.py:172
    'Accès refusé : le fichier est peut-être ouvert dans une autre application.': 'Erişim reddedildi: dosya başka bir uygulamada açık olabilir.',
    # cerclic/actions/video.py:598, cerclic/actions/video.py:591
    'Découpage': 'Kesiliyor',
    # cerclic/actions/video.py:237
    'Aucune image vidéo dans ce fichier.': 'Bu dosyada video görüntüsü yok.',
    # cerclic/actions/video.py:289
    'Cette vidéo est déjà bien compressée : essaie une compression plus forte.': 'Bu video zaten iyi sıkıştırılmış: daha güçlü bir sıkıştırma deneyin.',
    # cerclic/actions/video.py:500
    "Vidéo trop longue pour un GIF (plus de 2 minutes : il pèserait des centaines de Mo). Garde d'abord un passage avec « {action} ».": 'Video, GIF için çok uzun (2 dakikadan fazla: GIF yüzlerce MB tutar). Önce “{action}” ile bir bölüm seçin.',
    # cerclic/actions/video.py:509, cerclic/actions/video.py:511
    'Conversion en GIF': "GIF'e dönüştürme",
    # cerclic/actions/video.py:541, cerclic/actions/video.py:609
    "Cette vidéo n'a pas de son.": 'Bu videoda ses yok.',
    # cerclic/actions/video.py:579
    'Le passage à garder est trop court.': 'Tutulacak bölüm çok kısa.',
    # cerclic/actions/video.py:582
    'Le passage choisi est la totalité du fichier.': 'Seçilen bölüm dosyanın tamamı.',
    # cerclic/actions/video.py:594, cerclic/actions/video.py:655, cerclic/actions/video.py:720 ...
    'Aucun son dans ce fichier.': 'Bu dosyada ses yok.',
    # cerclic/actions/video.py:689
    'Aperçu impossible.': 'Önizleme yapılamıyor.',
    # cerclic/actions/video.py:727
    'Ce son est déjà léger : essaie une compression plus forte.': 'Bu ses zaten hafif: daha güçlü bir sıkıştırma deneyin.',
    # cerclic/actions/video.py:234
    "Ce fichier ne contient que du son, pas d'image : utilise « {action} » pour en faire un MP3.": 'Bu dosyada yalnızca ses var, görüntü yok: MP3 yapmak için “{action}” işlemini kullanın.',
    # cerclic/actions/video.py:687
    'Aperçu trop long à préparer.': 'Önizlemenin hazırlanması çok uzun sürüyor.',
    # cerclic/win/hotkey.py:54
    'Alt + F4 ferme les fenêtres.': 'Alt + F4, pencereleri kapatır.',
    # cerclic/win/hotkey.py:55
    'Alt + Tab change de fenêtre.': 'Alt + Tab, pencereler arasında geçiş yapar.',
    # cerclic/win/hotkey.py:56
    'Alt + Échap change de fenêtre.': 'Alt + Esc, pencereler arasında geçiş yapar.',
    # cerclic/win/hotkey.py:57
    'Alt + Espace ouvre le menu des fenêtres.': 'Alt + Boşluk, pencere menüsünü açar.',
    # cerclic/win/hotkey.py:58
    'Ctrl + Échap ouvre le menu Démarrer.': 'Ctrl + Esc, Başlat menüsünü açar.',
    # cerclic/win/hotkey.py:59
    'Ctrl + Alt + Suppr est réservé à Windows.': "Ctrl + Alt + Delete, Windows'a ayrılmıştır.",
    # cerclic/win/hotkey.py:60
    'Ctrl + Maj + Échap ouvre le Gestionnaire des tâches.': "Ctrl + Shift + Esc, Görev Yöneticisi'ni açar.",
    # contexte : touche Windows | cerclic/win/hotkey.py:93, cerclic/win/hotkey.py:92
    'touche Windows\x04Touche {code}': 'Tuş {code}',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Espace': 'Boşluk',
    # contexte : touche Windows | cerclic/win/hotkey.py:39
    'touche Windows\x04Tab': 'Tab',
    # contexte : touche Windows | cerclic/win/hotkey.py:40
    'touche Windows\x04Entrée': 'Enter',
    # contexte : touche Windows | cerclic/win/hotkey.py:41
    'touche Windows\x04Retour': 'Geri',
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
    'Ajoute une touche après Ctrl, Alt, Maj ou Win.': 'Ctrl, Alt, Shift veya Win tuşundan sonra bir tuş ekleyin.',
    # cerclic/win/hotkey.py:153
    '{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.': "{key} tuşu Windows'ta ve uygulamalarda zaten kullanılıyor (yardım, yeniden adlandır, yenile, yazım denetimi…). Örneğin Ctrl + Alt ekleyin: Ctrl + Alt + {key}.",
    # cerclic/win/hotkey.py:157
    'Alt avec le pavé numérique sert à taper des caractères (Alt + 0201 = É). Choisis une autre combinaison.': 'Alt ile sayısal tuş takımı karakter yazmaya yarar (Alt + 0201 = É). Başka bir kombinasyon seçin.',
    # cerclic/win/hotkey.py:160
    "Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche ne s'écrirait plus).": 'Kombinasyonda Ctrl, Alt veya Win olmalı (yoksa bu tuş artık yazı yazmaz).',
    # contexte : touche Windows | cerclic/win/hotkey.py:101
    'touche Windows\x04Win': 'Win',
    # contexte : touche Windows | cerclic/win/hotkey.py:103
    'touche Windows\x04Ctrl': 'Ctrl',
    # contexte : touche Windows | cerclic/win/hotkey.py:105
    'touche Windows\x04Alt': 'Alt',
    # contexte : touche Windows | cerclic/win/hotkey.py:107
    'touche Windows\x04Maj': 'Shift',
    # cerclic/win/hotkey.py:169
    "Alt + une seule touche sert déjà dans beaucoup d'applications (les menus des applications). Ajoute Maj ou Ctrl, par exemple Alt + Maj + {key}.": 'Alt + tek bir tuş birçok uygulamada zaten kullanılıyor (uygulama menüleri). Shift veya Ctrl ekleyin, örneğin Alt + Shift + {key}.',
    # cerclic/win/hotkey.py:177
    'Cette combinaison sert à taper des caractères (@, €, #, œ…) avec AltGr. Choisis-en une autre.': 'Bu kombinasyon, AltGr ile karakter yazmaya yarar (@, €, #, œ…). Başka bir kombinasyon seçin.',
    # cerclic/win/hotkey.py:166
    "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + {key}.": 'Ctrl + tek bir tuş birçok uygulamada zaten kullanılıyor (kalın, kopyala, yapıştır, kaydet…). Shift veya Alt ekleyin, örneğin Ctrl + Shift + {key}.',
}
