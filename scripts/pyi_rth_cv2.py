# PyInstaller runtime hook for Cerclic.app (cerclic_mac.spec).
# OpenCV's loader finds its binary only if its own folder comes first on
# sys.path. In a .app, cv2's .py files sit in Contents/Resources and its binary
# in Contents/Frameworks (linked back into Resources), so the loader does not
# recognise the layout and imports itself again: "recursion is detected during
# loading of cv2" (pdf2docx, the "En Word" action). This flag, read by OpenCV's
# loader, puts its folder first.
import sys

sys.OpenCV_REPLACE_SYS_PATH_0 = True
