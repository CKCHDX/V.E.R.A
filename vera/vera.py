#!/usr/bin/env python3
"""
V.E.R.A - Versatile Evolving Reasoning Agent
Main Application Module

This is the core application that implements the LDS (Large Data Service) architecture.
VERA is a knowledge-base driven AI system using static JSON files for personality,
commands, safety rules, and behavior patterns.

Developer: CKCHDX at Oscyra Solutions
Project: V.E.R.A Isolated Learning Environment
"""

import json
import os
import sys
import logging
import platform
import datetime
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading


class VeraCore:
    """Core VERA system with LDS architecture"""
    
    def __init__(self, data_dir: str = "vera_data"):
        """Initialize VERA with data directory"""
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / data_dir
        self.log_dir = self.base_dir / "logs"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Load data files
        self.personality = self.load_json("vera_personality.json")
        self.commands = self.load_json("vera_commands.json")
        self.firewall = self.load_json("vera_firewall.json")
        self.system_state = self.load_json("vera_system_state.json")
        
        self.logger.info("V.E.R.A initialized successfully")
        
    def setup_logging(self):
        """Configure logging system"""
        log_file = self.log_dir / "vera_access.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('VERA')
        
    def load_json(self, filename: str) -> Dict:
        """Load JSON data file"""
        filepath = self.data_dir / filename
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded {filename}")
                    return data
            else:
                self.logger.warning(f"{filename} not found, returning empty dict")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading {filename}: {e}")
            return {}
    
    def save_json(self, filename: str, data: Dict):
        """Save JSON data file"""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Saved {filename}")
        except Exception as e:
            self.logger.error(f"Error saving {filename}: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get current system information"""
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def check_command_safety(self, command: str) -> Tuple[bool, str]:
        """Check if command is safe to execute according to firewall rules"""
        if not self.firewall:
            return True, "No firewall rules loaded"
        
        # Check for shell metacharacters that could be used for injection
        shell_metacharacters = [';', '|', '&', '$', '`', '(', ')', '<', '>', '\n', '\r']
        for char in shell_metacharacters:
            if char in command:
                return False, f"Command contains shell metacharacter: {char}"
        
        # Extract the base command (first word)
        cmd_name = command.strip().split()[0] if command.strip() else ""
        
        blacklist = self.firewall.get("blacklist", [])
        for blocked in blacklist:
            # Check if the base command matches the blocked command
            if cmd_name.lower() == blocked.lower():
                return False, f"Command '{cmd_name}' is blacklisted"
        
        return True, "Command approved"
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a command with safety checks"""
        self.logger.info(f"Command requested: {command}")
        
        # Check safety
        is_safe, message = self.check_command_safety(command)
        if not is_safe:
            self.logger.warning(f"Command blocked: {message}")
            return {
                "success": False,
                "output": "",
                "error": message
            }
        
        # Check if command is in allowed list
        if self.commands:
            allowed_commands = self.commands.get("allowed", [])
            cmd_name = command.split()[0] if command else ""
            
            if allowed_commands and cmd_name not in allowed_commands:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Command '{cmd_name}' not in allowed list"
                }
        
        # Execute command with shell=False for better security
        # Note: This limits functionality but improves security
        try:
            # Split command into args for shell=False execution
            cmd_args = command.split()
            
            result = subprocess.run(
                cmd_args,
                shell=False,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.base_dir  # Restrict to project directory
            )
            
            self.logger.info(f"Command executed: {command}")
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Command timed out after 30 seconds"
            }
        except Exception as e:
            self.logger.error(f"Command execution error: {e}")
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    def get_personality_response(self, context: str = "greeting") -> str:
        """Get a personality-driven response"""
        if not self.personality:
            return "Hello, I am V.E.R.A."
        
        responses = self.personality.get("responses", {})
        return responses.get(context, "I am V.E.R.A - Versatile Evolving Reasoning Agent")
    
    def get_status(self) -> Dict[str, Any]:
        """Get VERA's current status"""
        return {
            "name": "V.E.R.A",
            "full_name": "Versatile Evolving Reasoning Agent",
            "version": "1.0.0-ILE",
            "status": "operational",
            "personality_loaded": bool(self.personality),
            "commands_loaded": bool(self.commands),
            "firewall_active": bool(self.firewall),
            "system_state": self.system_state.get("status", "unknown"),
            "admin_mode": self.system_state.get("admin_mode", False),
            "system_info": self.get_system_info()
        }


class VeraWebInterface:
    """Web interface server for VERA"""
    
    def __init__(self, vera_core: VeraCore, port: int = 8080):
        self.vera = vera_core
        self.port = port
        self.server = None
        
    def start(self):
        """Start the web interface server"""
        handler = SimpleHTTPRequestHandler
        self.server = HTTPServer(('localhost', self.port), handler)
        
        print(f"\n{'='*60}")
        print(f"V.E.R.A Web Interface")
        print(f"{'='*60}")
        print(f"Server starting on http://localhost:{self.port}")
        print(f"Open your browser and navigate to the URL above")
        print(f"Press Ctrl+C to stop the server")
        print(f"{'='*60}\n")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down V.E.R.A...")
            self.server.shutdown()


def main():
    """Main entry point for VERA"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║              V.E.R.A - Version 1.0.0-ILE                 ║
    ║       Versatile Evolving Reasoning Agent                 ║
    ║                                                          ║
    ║         Isolated Learning Environment Edition            ║
    ║                                                          ║
    ║              Developer: CKCHDX                           ║
    ║           Oscyra Solutions - 2026                        ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize VERA core
    vera = VeraCore()
    
    # Display status
    status = vera.get_status()
    print(f"\nStatus: {status['status'].upper()}")
    print(f"Personality Loaded: {status['personality_loaded']}")
    print(f"Commands Loaded: {status['commands_loaded']}")
    print(f"Firewall Active: {status['firewall_active']}")
    print(f"Admin Mode: {status['admin_mode']}")
    print(f"\nSystem: {status['system_info']['platform']} {status['system_info']['platform_release']}")
    print(f"Python: {status['system_info']['python_version']}")
    
    # Greeting
    greeting = vera.get_personality_response("greeting")
    print(f"\n{greeting}\n")
    
    # Start web interface if available
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        interface = VeraWebInterface(vera)
        interface.start()
    else:
        print("Run with --web flag to start the web interface")
        print("Example: python vera.py --web\n")


if __name__ == "__main__":
    main()
