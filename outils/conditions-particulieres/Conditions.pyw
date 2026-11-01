"""Lanceur Windows : un double-clic ouvre la fenêtre de l'outil (Python 3.10 ou plus récent requis)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

try:
    from conditions_particulieres.interface import main  # noqa: E402
except ImportError as e:  # tkinter absent : sous pythonw, rien ne s'afficherait
    import ctypes
    ctypes.windll.user32.MessageBoxW(None, f"La fenêtre ne peut pas s'ouvrir ({e}). "
                                     "Réinstallez Python en cochant l'option « tcl/tk and IDLE ».",
                                     "Conditions particulières et générales", 0x10)
    raise SystemExit(2)

main()
