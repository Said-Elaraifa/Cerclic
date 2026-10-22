# Composants tiers

Cerclic s'appuie sur des logiciels libres.

## ffmpeg

L'installateur et la version portable incluent `ffmpeg.exe`, utilisé pour les
actions vidéo (compresser, MP4, GIF, MP3). ffmpeg est distribué sous licence
GPL (build BtbN, codecs GPL comme libx264). ffmpeg est un programme séparé,
appelé par Cerclic ; il n'est pas lié au code de Cerclic.

Code source et licence de ffmpeg : https://ffmpeg.org et
https://github.com/BtbN/FFmpeg-Builds

## Bibliothèques Python

- PySide6 (Qt for Python), LGPL v3
- Pillow, licence MIT-CMU ; pillow-heif (libheif, LGPL)
- PyMuPDF, GNU AGPL v3 ou licence commerciale
- pikepdf (qpdf), MPL 2.0
- pdf2docx, Apache 2.0 ; python-docx, MIT ; opencv-python-headless, Apache 2.0

Chacune reste sous sa propre licence. Cerclic lui-même est sous licence MIT
(voir LICENSE).
