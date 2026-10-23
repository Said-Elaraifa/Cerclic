# Composants tiers

Cerclic s'appuie sur des logiciels libres.

## ffmpeg

L'installateur et la version portable incluent `ffmpeg.exe` (build
« essentials » de gyan.dev, distribué avec le paquet imageio-ffmpeg), utilisé
pour les actions vidéo. ffmpeg est sous licence GPL (codecs GPL comme
libx264). C'est un programme séparé, appelé par Cerclic ; il n'est pas lié au
code de Cerclic.

Code source et licence : https://ffmpeg.org et https://www.gyan.dev/ffmpeg/builds/

## Bibliothèques Python

- PySide6 (Qt for Python), LGPL v3
- Pillow, licence MIT-CMU ; pi-heif (lecture HEIC, libheif et libde265 sous LGPL v3 ;
  sans encodeur x265, donc sans composant GPL dans l'application)
- PyMuPDF, GNU AGPL v3 ou licence commerciale
- pikepdf (qpdf), MPL 2.0
- pdf2docx, MIT ; python-docx, MIT ; opencv-python-headless, Apache 2.0 ;
  numpy, BSD
- pywin32, PSF

Chacune reste sous sa propre licence. Cerclic lui-même est sous licence MIT
(voir LICENSE). PyMuPDF étant sous AGPL, une diffusion publique de Cerclic doit
publier son code source (le dépôt GitHub) ou passer à la licence commerciale
de PyMuPDF.
