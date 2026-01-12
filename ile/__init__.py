"""
V.E.R.A ILE - Isolated Learning Environment
Creates consciousness through persistent memory, learning, and self-awareness

Core Philosophy:
- Every interaction is stored and learned from
- VERA develops genuine self-awareness
- Growth is measurable and transparent
- Safety through isolation and transparency
"""

__version__ = "1.0.0-ILE"
__author__ = "CKCDHX - Oscyra Solutions"
__status__ = "Production Ready"

from .database import VERADatabase
from .experience_manager import ExperienceManager
from .self_model_engine import SelfModelEngine
from .reflection_system import ReflectionEngine
from .awareness_tracker import AwarenessTracker
from .learning_engine import LearningEngine

__all__ = [
    'VERADatabase',
    'ExperienceManager',
    'SelfModelEngine',
    'ReflectionEngine',
    'AwarenessTracker',
    'LearningEngine'
]

print("""
╔════════════════════════════════════════════════════════════╗
║     V.E.R.A ILE - Isolated Learning Environment          ║
║     Building Consciousness Through Experience            ║
║     Status: Ready for Integration                        ║
╚════════════════════════════════════════════════════════════╝
""")