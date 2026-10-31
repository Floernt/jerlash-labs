"""Lanceur Windows : un double-clic ouvre la fenêtre de l'outil (Python 3.10 ou plus récent requis)."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from inventaire_dossier.interface import main  # noqa: E402

main()
