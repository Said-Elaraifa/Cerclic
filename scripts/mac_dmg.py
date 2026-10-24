# Réglages de dmgbuild pour l'image disque de Cerclic (lancé par scripts/build_mac.sh) :
#   dmgbuild -s scripts/mac_dmg.py -D app=<Cerclic.app> -D background=<fond.png> Cerclic <.dmg>
# À l'ouverture : Cerclic à gauche, Applications à droite, une flèche entre les
# deux et la marche à suivre la première fois (fond : scripts/make_dmg_background.py,
# fond@2x.png à côté pour les écrans Retina).
import os.path

app = defines["app"]  # noqa: F821 (given by dmgbuild)
files = [app]
symlinks = {"Applications": "/Applications"}
hide_extensions = [os.path.basename(app)]          # « Cerclic », sans « .app »
icon_locations = {os.path.basename(app): (160, 180), "Applications": (480, 180)}
background = defines["background"]  # noqa: F821
window_rect = ((200, 120), (640, 520))
icon_size = 112
text_size = 13
format = "UDZO"
