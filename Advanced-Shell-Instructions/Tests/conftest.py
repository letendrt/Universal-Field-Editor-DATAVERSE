"""
Pytest configuration for Universal Field Editor tests

This file is automatically loaded by pytest and configures the test environment.
"""

import sys
import os

# Add parent directory to path to import the universal_field_editor_V2 module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
