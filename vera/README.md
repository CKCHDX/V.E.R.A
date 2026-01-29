# V.E.R.A Python Implementation

This directory contains the Python implementation of V.E.R.A (Versatile Evolving Reasoning Agent) following the LDS (Large Data Service) architecture.

## Quick Start

### Basic Usage (Command Line)
```bash
python vera/vera.py
```

### With Web Interface
```bash
python vera/vera.py --web
```
Then open http://localhost:8080/vera_interface_v2.html in your browser

## What's Included

### Core Components
- **vera.py** - Main application with VeraCore class implementing the LDS architecture
- **vera_interface_v2.html** - Modern web interface for interacting with V.E.R.A
- **vera_data/** - Configuration directory with JSON files

### Configuration Files (vera_data/)
- **vera_personality.json** - Defines V.E.R.A's character, responses, and behavior patterns
- **vera_commands.json** - Command library with allowed commands and documentation
- **vera_firewall.json** - Safety rules and blacklisted operations
- **vera_system_state.json** - Runtime state and phase tracking

### Logging
- **logs/vera_access.log** - Activity log tracking all operations

## Architecture

V.E.R.A uses the LDS (Large Data Service) architecture which means:
- ✅ **Safety**: No self-modifying code, immutable core files
- ✅ **Speed**: JSON loaded at startup, zero overhead
- ✅ **Completeness**: Full command library embedded
- ✅ **Control**: Easy to update personality without touching code
- ✅ **Reliability**: Predictable behavior, no learning artifacts

## Features

### Implemented (Phase 1)
- JSON-based personality system
- Command safety firewall
- Safe command execution with timeout protection
- Activity logging
- System information gathering
- Web interface
- Status reporting

### Planned (Phase 2-5)
- Persistent memory across sessions
- Knowledge base with fact storage
- Reasoning engine with verification
- Self-awareness tracking
- Continuous learning system

## Testing

Run a basic test:
```bash
python vera/vera.py
```

You should see:
```
╔══════════════════════════════════════════════════════════╗
║              V.E.R.A - Version 1.0.0-ILE                 ║
║       Versatile Evolving Reasoning Agent                 ║
╚══════════════════════════════════════════════════════════╝

Status: OPERATIONAL
Personality Loaded: True
Commands Loaded: True
Firewall Active: True
```

## Documentation

- **README.md** (parent directory) - Complete project vision and philosophy
- **LDS.md** (parent directory) - Architecture documentation
- **SETUP.md** (parent directory) - Detailed setup guide

## Safety & Security

V.E.R.A is designed with safety as a core principle:
1. **Complete Containment** - Cannot access unauthorized files
2. **Command Firewall** - Destructive operations are blocked
3. **Transparent Logging** - All activities logged for audit
4. **Timeout Protection** - 30-second timeout on commands
5. **No Privilege Escalation** - Cannot gain elevated permissions

## Development Status

**Current Phase:** Phase 1 - Foundation  
**Status:** ✅ Operational  
**Version:** 1.0.0-ILE

---

**Developer:** CKCHDX @ Oscyra Solutions  
**Created:** 2026-01-29  
**Project:** V.E.R.A Isolated Learning Environment
