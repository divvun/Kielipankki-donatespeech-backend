"""Compatibility entrypoint for package-based app loading.

This module delegates to the existing root-level `main.py` so runtime behavior
stays unchanged while migration to package layout proceeds incrementally.
"""

from main import *  # noqa: F401,F403
from main import app

__all__ = ["app"]
