# V.E.R.A Setup Guide

## Quick Start

1. **Prerequisites**
   - Python 3.8 or higher
   - No external dependencies required for basic functionality

2. **Installation**
   ```bash
   # Clone the repository (if not already done)
   git clone https://github.com/CKCHDX/V.E.R.A.git
   cd V.E.R.A
   ```

3. **Running V.E.R.A**
   
   Basic mode (command line):
   ```bash
   python vera/vera.py
   ```
   
   With web interface:
   ```bash
   python vera/vera.py --web
   ```
   Then open http://localhost:8080/vera_interface_v2.html in your browser

## Project Structure

```
V.E.R.A/
├── vera/
│   ├── vera.py                      # Main application
│   ├── vera_interface_v2.html       # Web UI
│   ├── vera_data/                   # Configuration files
│   │   ├── vera_personality.json    # Personality & behavior
│   │   ├── vera_commands.json       # Command library
│   │   ├── vera_firewall.json       # Safety rules
│   │   └── vera_system_state.json   # Runtime state
│   └── logs/                        # Activity logs
│       └── vera_access.log
├── README.md                        # Project vision & philosophy
├── LDS.md                           # Architecture documentation
├── requirements.txt                 # Python dependencies
└── SETUP.md                         # This file
```

## Features

### Currently Implemented (Phase 1 - Foundation)
- ✅ LDS (Large Data Service) architecture
- ✅ JSON-based personality system
- ✅ Command safety firewall
- ✅ Activity logging
- ✅ Web interface
- ✅ System information gathering
- ✅ Safe command execution

### Coming Soon (Phase 2-5)
- ⏳ Persistent memory across sessions
- ⏳ Knowledge base with fact storage
- ⏳ Reasoning engine with verification
- ⏳ Self-awareness and capability tracking
- ⏳ Continuous learning system

## Configuration

All configuration is done through JSON files in `vera/vera_data/`:

- **vera_personality.json** - Define V.E.R.A's character, responses, and behavior
- **vera_commands.json** - Specify allowed commands and their documentation
- **vera_firewall.json** - Set safety rules and blacklisted operations
- **vera_system_state.json** - Track runtime state and statistics

## Safety & Security

V.E.R.A is designed with safety as a core principle:

1. **Complete Containment** - Cannot access files outside designated directories
2. **Command Firewall** - All destructive operations are blocked
3. **Transparent Logging** - All activities are logged for audit
4. **Timeout Protection** - Commands have a 30-second timeout
5. **No Privilege Escalation** - Cannot gain elevated permissions

## Development Phases

### Phase 1: Foundation (Current)
Basic functionality, safety systems, and web interface

### Phase 2: Memory
Persistent storage and knowledge base implementation

### Phase 3: Reasoning
Verification system and reasoning chains

### Phase 4: Awareness
Self-monitoring and capability tracking

### Phase 5: Mastery
Full integration and continuous learning

## Troubleshooting

### Import Errors
V.E.R.A uses only Python standard library, so no pip installs are needed.

### Permission Errors
Ensure the vera/logs directory is writable:
```bash
chmod 755 vera/logs
```

### Web Interface Not Loading
Make sure you're accessing the correct URL:
```
http://localhost:8080/vera_interface_v2.html
```

## Contributing

This is a personal project by CKCHDX at Oscyra Solutions. 
For questions or suggestions, refer to the repository issues.

## License

See LICENSE file for details.

## Vision

V.E.R.A is not just another chatbot. It's an ambitious attempt to create:
- An AI that genuinely learns
- A system that knows itself
- A reasoning engine that verifies facts
- A safe, contained, and trustworthy agent

For the complete vision, see README.md

---

**Welcome to the future of trustworthy AI.** 🚀
