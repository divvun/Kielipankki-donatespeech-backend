"""Compatibility shim for package-based storage helpers.

This module aliases `storage` to `app.storage` for import compatibility.
"""

import sys

from app import storage as _storage

sys.modules[__name__] = _storage
