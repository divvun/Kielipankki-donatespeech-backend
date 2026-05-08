"""Compatibility shim for package-based YLE utilities.

This module aliases `yle_utils` to `app.yle_utils` for import compatibility.
"""

import sys

from app import yle_utils as _yle_utils

sys.modules[__name__] = _yle_utils
