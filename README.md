🎯 VERA LDS Architecture

📋 Description
VERA LDS (Large Data Service) is a knowledge-base driven AI system using static JSON files that define VERA's personality, command knowledge, safety rules, and behavior patterns. This approach ensures:

Safety: No self-modifying code, immutable core files

Speed: JSON loaded at startup, zero overhead

Completeness: Full Windows/Linux command library embedded

Control: Easy to update personality without touching code

Reliability: Predictable behavior, no learning artifacts

vera/
├── vera.py                         # Main application (enhanced)
├── vera_interface_v2.html          # Web UI (unchanged)
├── vera_data/
│   ├── vera_personality.json       # VERA's character & style
│   ├── vera_commands.json          # All allowed commands + help
│   ├── vera_firewall.json          # Safety rules & blacklists
│   └── vera_system_state.json      # Admin mode, system info
└── logs/
    └── vera_access.log             # Command execution log
