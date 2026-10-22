# Architecture de Cerclic

## Vue d'ensemble

```
run_cerclic.py            point d'entrée de l'exécutable
cerclic/
  app.py                  tray + orchestration (geste -> sélection -> roue -> action -> toast)
  engine.py               lance une action, renvoie un résultat, ne lève jamais
  settings.py             config JSON dans %APPDATA%\Cerclic
  paths.py                noms de sortie non destructifs (jamais d'écrasement)
  actions/                fonctions pures de traitement (testées partout)
    images.py  pdf.py  video.py  registry.py
  win/                    code Windows uniquement (ctypes / pywin32)
    mouse_hook.py         détection du double clic droit, sans flash
    selection.py         fichiers sélectionnés (Explorateur via COM, Bureau)
    autostart.py          démarrage avec Windows (clé de registre Run)
  ui/                     PySide6
    radial.py             la roue, navigation catégories -> actions
    crop.py               fenêtre de rognage interactive
    toast.py  dialogs.py  settings_window.py  icons.py  trayicon.py
```

## Principes

- **Rien n'écrase l'original.** Toute sortie est un nouveau fichier voisin,
  nommé par `paths.output_for`. L'« Annuler » du toast supprime seulement ce que
  Cerclic vient de créer.
- **Le moteur ne dépend pas de l'interface.** `actions/` et `engine.py` se
  testent sur n'importe quel système (Linux inclus) ; 18 tests couvrent chaque
  action sur de vrais fichiers.
- **Une action = métadonnées + fonction.** `registry.ACTIONS` décrit chaque
  action (libellé, catégorie, familles de fichiers, besoins). La roue et le
  moteur lisent le même registre, donc ajouter une action tient en une entrée.

## Ce qui ne peut se tester que sous Windows

Ces parties compilent et sont écrites avec soin, mais ne tournent pas en cloud
Linux. À vérifier en premier au test :

1. Le geste : double clic droit ouvre la roue ; un clic droit simple garde le
   menu Windows (avec le petit délai réglable).
2. La lecture de la sélection dans une fenêtre de l'Explorateur, puis sur le
   Bureau.
3. L'icône dans la barre des tâches et le démarrage avec Windows.

Tout le traitement d'images, PDF et vidéo derrière ces gestes est déjà validé
par les tests.

## Ajouter une action

1. Écrire la fonction pure dans `actions/images.py`, `pdf.py` ou `video.py`.
2. Ajouter une `Action(...)` dans `actions/registry.py` (libellé, catégorie,
   `applies`, `handler`, et `needs`/`combine`/`primary` au besoin).
3. Ajouter un cas de test dans `tests/test_actions.py`.

La roue, le routage de la sélection et le moteur la prennent en compte sans
autre changement.
