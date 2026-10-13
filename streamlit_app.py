"""
AgriSense - Root Streamlit Entrypoint
Allows running: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Run the agrisense application
from agrisense.app import *
