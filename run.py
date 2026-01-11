#!/usr/bin/env python3
"""
Convenience script to run pi_detector without installation.
Usage: python run.py [--config path/to/config.json]
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Now import and run
from pi_detector.main import main

if __name__ == "__main__":
    main()
