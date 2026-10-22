# Cerclic

Un menu circulaire d'actions rapides sur tes fichiers, sous Windows.

Maintiens le clic gauche sur une image, un PDF ou une vidéo : une roue
d'actions s'ouvre autour du curseur. Tu choisis, c'est fait, le résultat est
enregistré à côté de l'original. Aucune application à ouvrir.

![Aperçu du menu](docs/preview_image.png)

## Le principe

- **Maintiens le clic gauche** (environ 0,4 s, sans bouger) sur un fichier.
  Un clic normal, un double clic ou un glisser restent inchangés.
- La roue montre les actions qui conviennent au type de fichier.
- Un clic lance l'action. Une petite notification propose « Ouvrir »,
  « Dossier » et « Annuler ».
- Rien n'écrase jamais ton fichier d'origine : chaque résultat est un nouveau
  fichier, nommé clairement (`photo (compressed).jpg`).

## Ce que Cerclic sait faire (v1)

**Images** : rogner (avec formats 1:1, 4:5, 9:16...), convertir en JPG, PNG ou
WEBP, convertir les photos iPhone HEIC en JPG, compresser, redimensionner,
pivoter, assembler plusieurs images en un PDF.

**PDF** : en JPG ou PNG, en Word, compresser, fusionner, diviser, pivoter,
signer (ta signature se règle une fois dans les paramètres), filigrane,
numéros de page, protéger par mot de passe, déverrouiller.

**Vidéo** : compresser, convertir en MP4, en GIF, extraire le son en MP3.

Les actions les plus utiles sont dans le premier cercle ; les autres sont
regroupées par catégorie. D'autres actions et des sous-menus arriveront.

## Installer

Télécharge `CerclicSetup` dans la section
[Releases](../../releases), lance-le, c'est tout. Cerclic se place dans la
barre des tâches (près de l'horloge) et démarre avec Windows.

Une version portable (dossier `.zip`, sans installation) est aussi fournie.

## Réglages

Clic droit sur l'icône dans la barre des tâches, puis « Paramètres » :

- **Signature** : choisis une image PNG à fond transparent ; « Signer » la
  posera sur le PDF.
- **Geste** : clic gauche maintenu (par défaut), clic droit maintenu, ou
  double clic droit.
- **Délai** : durée d'appui avant que la roue s'ouvre.
- Qualités par défaut (compression, JPG, redimension).

## Tester sans installer

1. Décompresse le zip et ouvre le dossier `Cerclic`.
2. Double-clique **« Lancer Cerclic.bat »**. Le premier lancement installe ce
   qu'il faut (Python doit être installé), les suivants démarrent tout de suite.
3. Un message « Cerclic est prêt » s'affiche : maintiens le clic gauche sur un
   fichier, la roue s'ouvre.

## Construire depuis le code

Le build Windows se fait tout seul sur GitHub (voir
`.github/workflows/build.yml`) : il teste, compile l'exécutable et fabrique
l'installateur à chaque envoi sur `main`, et publie une release sur un tag
`vX.Y.Z`.

En local (Windows) :

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
python -m cerclic          # lancer en mode développeur
pyinstaller cerclic.spec   # fabriquer l'exécutable
```

## Tester entre amis

1. Un tag `v0.1.0` déclenche la compilation et publie `CerclicSetup` dans
   Releases.
2. Partage le lien de la release. Chacun télécharge, installe, teste.
3. Les retours et les bugs se notent dans les Issues du dépôt.

## Pile technique

Python, PySide6 pour la roue et les fenêtres, Pillow et pillow-heif pour les
images, PyMuPDF et pikepdf pour les PDF, pdf2docx pour le Word, ffmpeg pour la
vidéo. Le geste global et la lecture de la sélection de l'Explorateur passent
par l'API Windows.

ffmpeg est inclus dans l'installateur ; voir `docs/THIRD_PARTY.md`.
