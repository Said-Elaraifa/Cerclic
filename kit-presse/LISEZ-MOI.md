# Kit presse de Cerclic

Tout ce qu'il faut pour parler de Cerclic ou en faire une vidéo : le logo, la
vraie interface (en français et en anglais), des captures complètes et des
chiffres réels. Rien ici n'est inventé : n'ajoute aucune fonction, aucun
écran, aucun chiffre qui n'y figure pas.

## Cerclic en bref

Une roue d'actions rapides sur tes fichiers. Clic droit sur un fichier (ou un
raccourci clavier), une roue s'ouvre autour de la souris : un clic et c'est
fait, sans ouvrir de logiciel.

- **Images** (JPG, PNG, WEBP, HEIC d'iPhone, AVIF, GIF…) : rogner, format
  réseaux sociaux, pivoter, redimensionner, compresser en voyant la taille
  obtenue avant de valider, convertir, assembler, en faire un PDF, anonymiser
  (retirer la position GPS).
- **PDF** : signer, rogner, compresser, fusionner, organiser les pages,
  convertir en Word, en images ou en texte, diviser, filigrane, numéros de
  page, protéger par mot de passe, déverrouiller.
- **Vidéo** : raccourcir, format réseaux sociaux, compresser, convertir en MP4
  ou en GIF, extraire le son, couper le son, pivoter.
- **Son** : raccourcir, convertir en MP3, compresser.
- **Formats réseaux sociaux** : carré 1:1, portrait 4:5, grille 3:4, story
  9:16 (Reels, TikTok, Shorts), paysage 16:9, bannière 1,91:1 ; cadrage au
  choix, ou fond flou, blanc ou noir.
- Tout se passe sur l'ordinateur, rien n'est envoyé en ligne. L'original n'est
  jamais modifié : chaque action crée un nouveau fichier à côté.
- Gratuit. Windows 10 et 11, Mac à puce Apple (macOS 12 ou plus).
- 10 langues : français, anglais, espagnol, allemand, italien, portugais,
  arabe, turc, chinois simplifié, japonais.

## Liens

- Télécharger pour Mac : https://github.com/Said-Elaraifa/Cerclic/releases/latest/download/Cerclic-Mac.dmg
- Télécharger pour Windows : https://github.com/Said-Elaraifa/Cerclic/releases/latest/download/Cerclic-Windows.exe
- Code source : https://github.com/Said-Elaraifa/Cerclic
- Contact : contact@cerclic.com

## Chiffre réel (compression d'une image)

`compression-reelle.json` : la photo de démo « Lac au coucher du soleil.jpg »
(3000 x 2000 px), compressée par Cerclic (qualité 60) :
**274 292 octets → 61 285 octets, 78 % de moins.**
Cerclic l'affiche « De 268 Ko à 60 Ko · 78 % de moins » sous Windows et
« De 274 Ko à 61 Ko » sur Mac (le Finder compte en 1000).

## Charte

- Logo : `logo/cerclic-logo.svg` (vectoriel, à utiliser tel quel, jamais
  redessiné), `cerclic-logo-2048.png` et `-512.png` (fond transparent),
  `cerclic-icone-app.png` (icône de l'app). Un anneau de 6 segments, le
  segment du haut légèrement sorti (l'action qu'on choisit), un point au centre.
- Couleurs : encre #1B2232, accent #2E7CF6, fond #EEF2F8 et blanc, bordures
  #DCE2EC. Segments du logo : #2E7CF6 #5AC8FA #34C7A6 #7C6CF2 #AF6BEA #5B8DEF.
- Typo pour la communication : Inter (l'app utilise la police du système).
- Style : clair, net, premium, beaucoup de vide.

## Fichiers

- `interface/fr` et `interface/en` : les vraies fenêtres de Cerclic,
  isolées, en PNG transparent (rendues par Cerclic lui-même) :
  - `roue-image.png` : la roue sur une image, aperçu au centre ;
  - `roue-image-survol-compresser.png` : la roue, « Compresser » survolé ;
  - `roue-pdf.png` : la roue sur un PDF ;
  - `popup-compresser.png` : la réglette de qualité, la taille obtenue et l'aperçu ;
  - `popup-reseaux-story.png` : le format Story 9:16 avec fond flou ;
  - `popup-rogner.png` : le rognage ;
  - `carte-resultat-compression.png` : la carte de résultat avec les tailles réelles ;
  - `fenetre-reglages.png` : la fenêtre de Cerclic (Général).
- `captures/fr` et `captures/en` : 5 captures complètes 1920 x 1080 (celles du
  Microsoft Store) : roue, compression, réseaux, PDF, réglages.

Les images de démo (paysage, contrat PDF) sont dessinées par le script des
captures : aucune photo extérieure.
