#!/usr/bin/env python3
"""
Simple script to run the Telegram DIAL Bot in debug mode
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot import main

if __name__ == "__main__":
    # Override sys.argv to include debug flag
    sys.argv = [sys.argv[0], '--debug', '--log-level', 'DEBUG']
    main()
