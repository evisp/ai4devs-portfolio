"""
conftest.py — pytest configuration for backend tests.

Adds the backend/ directory to sys.path so that app.py, ml_service.py,
and preprocessing.py are importable from the tests/ subdirectory.
"""

import sys
import os

# backend/ directory (one level up from tests/)
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
