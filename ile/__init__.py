"""
V.E.R.A ILE - Isolated Learning Environment
Adds persistent memory, learning, and self-awareness to VERA.
"""

__version__ = "0.1.0"

from .database import VERADatabase
from .experience_manager import ExperienceManager

__all__ = ["VERADatabase", "ExperienceManager"]
