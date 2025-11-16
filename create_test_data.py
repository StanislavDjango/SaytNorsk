"""
Convenience wrapper to seed the database with sample Norwegian test data.

This simply forwards to backend/create_test_data.py so you can run:
    python create_test_data.py
from the repository root.
"""

from pathlib import Path
import runpy


if __name__ == '__main__':
    backend_script = Path(__file__).resolve().parent / 'backend' / 'create_test_data.py'
    if not backend_script.exists():
        raise SystemExit("backend/create_test_data.py is missing.")

    runpy.run_path(str(backend_script))
