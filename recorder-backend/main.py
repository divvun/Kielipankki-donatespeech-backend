"""Compatibility shim for the package-based FastAPI app.

This module aliases `main` to `app.main` so legacy imports and patch targets
continue to affect the runtime module during migration.
"""

import sys

from app import main as _main

sys.modules[__name__] = _main
