"""The style tokens for these figures live one level up, in
docs/reviews/diagram_style.py, because the zeroth and first review diagrams
share them. This shim re-exports that module and points it at this folder.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import diagram_style                                        # noqa: E402
diagram_style.set_output_dir(os.path.dirname(os.path.abspath(__file__)))
from diagram_style import *                                 # noqa: E402,F401,F403
