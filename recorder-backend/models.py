"""Compatibility shim for package-based models.

This module aliases `models` to `app.models` for import compatibility.
"""

import sys

from app import models as _models

sys.modules[__name__] = _models
