import sys
import os
import asyncio
import webbrowser
import ctypes
import json
import time
import re
import platform
import subprocess
import threading
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

# ============================================================================
# ILE INTEGRATION (Isolated Learning Environment) - MODIFICATION #1
# ============================================================================
try:
    from ile import ExperienceManager
    ILE_ENABLED = True
    print("✓ ILE module loaded - VERA will remember everything")
except ImportError as e:
    ILE_ENABLED = False
    ExperienceManager = None
    print(f"⚠ ILE module not available: {e}")

"""
TITLE: PERFORMANCE v3.0 - Multi-core, GPU, and Advanced Optimization
DESCRIPTION: Ultra-optimized VERA with LDS (Large Data Service), admin mode detection, firewall, and multi-threaded performance
AUTHOR: CKCDHX - Oscyra Solutions
OPTIMIZATIONS:
- Multi-core CPU utilization (all available cores)
- GPU acceleration via Ollama
- Large context window (4096 tokens)
- Efficient streaming architecture
- Performance metrics tracking
"""

# ============================================================================
# CORE CONFIGURATION
# ============================================================================
CPU_CORES = os.cpu_count() or 4
print(f"[PERF] Detected {CPU_CORES} CPU cores")

THREAD_POOL = ThreadPoolExecutor(max_workers=CPU_CORES)
print(f"[PERF] Thread pool: {CPU_CORES} workers")

# Detect if running as .exe
if getattr(sys, 'frozen', False):
    APP_PATH = sys.MEIPASS
else:
    APP_PATH = str(Path(__file__).parent)
    sys.path.insert(0, APP_PATH)

print(f"[PERF] App path: {APP_PATH}")

# ============================================================================
# MODULE IMPORTS
# ============================================================================
try:
    import ollama
    print("[✓] Ollama module loaded")
except ImportError as e:
    print(f"[✗] Ollama import failed: {e}")
    sys.exit(1)

try:
    import websockets
    print("[✓] WebSockets module loaded")
except ImportError as e:
    print(f"[✗] WebSockets import failed: {e}")
    sys.exit(1)

try:
    from aiohttp import web
    print("[✓] aiohttp module loaded")
except ImportError as e:
    print(f"[✗] aiohttp import failed: {e}")
    sys.exit(1)

print("=" * 80)
print("V.E.R.A - Very Efficient, Reliable Assistant")
print("LDS (Large Data Service) Based System - ULTRA-OPTIMIZED")
print("Designed by CKCDHX - Oscyra Solutions")
print("=" * 80)
print("[TITLE] Import required libraries...")

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================
class PerfConfig:
    """High-performance optimization settings for multi-core systems"""
    # [TITLE] PERFORMANCE CONFIGURATION
    NUM_THREADS = CPU_CORES
    USE_GPU = True  # Enable GPU acceleration
    GPU_LAYERS = -1  # Use all available GPU layers
    
    # [TITLE] CPU Optimization...
    NUM_PREDICT = 200  # Increased from 150 - more throughput
    TEMPERATURE = 0.7
    TOP_P = 0.95  # Slightly higher for better quality
    TOP_K = 100  # Increased from 50
    REPEAT_PENALTY = 1.1
    
    # [TITLE] Model Optimization...
    NUM_GPU = -1  # Use all GPU if available
    NUM_THREADS_CORE = CPU_CORES  # Use all cores
    CONTEXT_WINDOW = 4096  # Larger context
    BATCH_SIZE = 512  # Larger batch
    
    # [TITLE] Ollama Optimization...
    KEEP_ALIVE = "10m"  # Keep model in VRAM longer
    
    @staticmethod
    def get_ollama_options():
        """Get optimized Ollama options"""
        return {
            "temperature": PerfConfig.TEMPERATURE,
            "num_predict": PerfConfig.NUM_PREDICT,
            "top_p": PerfConfig.TOP_P,
            "top_k": PerfConfig.TOP_K,
            "repeat_penalty": PerfConfig.REPEAT_PENALTY,
            "num_threads": PerfConfig.NUM_THREADS_CORE,
            "num_gpu": PerfConfig.NUM_GPU,
            "num_ctx": PerfConfig.CONTEXT_WINDOW,
        }
    # [TITLE] Response Settings...

# ============================================================================
# LDS MANAGER - Data Service
# ============================================================================
class LDSManager:
    """Load Data Service - manages JSON configuration files"""
    
    def __init__(self, datadir="vera_data"):
        self.datadir = datadir
        self.personality = {}
        self.commands = {}
        self.firewall = {}
        self.systemstate = {}
        self.ensure_data_files()
        self.load_all_data()
        print("[LDS] Manager initialized")
    
    def ensure_data_files(self):
        """Create vera_data folder and default files if missing"""
        os.makedirs(self.datadir, exist_ok=True)
        os.makedirs(os.path.join(self.datadir, "..", "logs"), exist_ok=True)
        print(f"[DATA] Directory: {self.datadir}")
    
    def load_file(self, filename: str) -> dict:
        """Load a JSON file from vera_data"""
        filepath = os.path.join(self.datadir, filename)
        if not os.path.exists(filepath):
            print(f"[DATA] Missing: {filename}")
            return {}
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Loading {filename}: {e}")
            return {}
    
    def load_all_data(self):
        """Load all LDS files"""
        self.personality = self.load_file("vera_personality.json")
        self.commands = self.load_file("vera_commands.json")
        self.firewall = self.load_file("vera_firewall.json")
        self.systemstate = self.load_file("vera_system_state.json")
        
        print(f"[LDS] Personality: {self.personality.get('metadata', {}).get('name', 'VERA')}")
        print(f"[LDS] Commands loaded: {self.commands.get('metadata', {}).get('total_commands', 0)}")
        print(f"[LDS] Firewall rules loaded")
    # [TITLE] LDS MANAGER ...

# ============================================================================
# ADMIN MODE DETECTION
# ============================================================================
class AdminDetector:
    """Detect and manage admin mode"""
    
    def __init__(self):
        self.is_admin = self.check_admin()
        self.ostype = platform.system()
    
    def check_admin(self) -> bool:
        """Check if running with admin privileges"""
        try:
            if sys.platform == "win32":
                return ctypes.windll.shell.IsUserAnAdmin()
            else:  # Linux
                return os.geteuid() == 0
        except:
            return False
    
    def get_mode_indicator(self) -> str:
        """Get visual mode indicator"""
        return "ADMIN MODE" if self.is_admin else "CLIENT MODE"
    
    def get_mode_message(self) -> str:
        """Get mode description"""
        if self.is_admin:
            return "Admin mode activated. I have full system access."
        else:
            return "Running in client mode. System commands require admin privileges."
    # [TITLE] ADMIN MODE DETECTION ...

# ============================================================================
# VERA FIREWALL - Safety Layer
# ============================================================================
class VERAFirewall:
    """Safety layer protecting system"""
    
    def __init__(self, firewall_config: dict):
        self.config = firewall_config
        self.blocked_log = []
    
    def is_command_safe(self, command: str) -> Tuple[bool, str]:
        """Check if command is safe to execute
        Returns: (is_safe, reason)
        """
        cmd_lower = command.lower().strip()
        # [TITLE] FIREWALL ...
        
        # Check blacklisted commands
        for blacklisted in self.config.get("blacklisted_commands", []):
            if blacklisted.lower() in cmd_lower:
                return False, f"Blocked: {blacklisted} is dangerous"
        # [TITLE] Check blacklisted commands...
        
        # Check dangerous patterns
        for pattern_obj in self.config.get("dangerous_patterns", []):
            pattern = pattern_obj.get("pattern", "")
            try:
                if re.search(pattern, cmd_lower):
                    return False, f"Blocked: {pattern_obj.get('reason', 'dangerous pattern')}"
            except:
                pass
        # [TITLE] Check dangerous patterns...
        
        # Check protected paths
        protected_paths = self.config.get("protected_paths", {})
        system_protected = protected_paths.get("windows" if sys.platform == "win32" else "linux", [])
        
        for protected in system_protected:
            if protected.lower() in cmd_lower:
                return False, f"Blocked: Cannot access protected path {protected}"
        # [TITLE] Check protected paths...
        
        if ("vera.py" in cmd_lower or "vera_data" in cmd_lower) and any(op in cmd_lower for op in ["write", "delete", "rm"]):
            return False, "Blocked: Cannot modify VERA core files"
        
        return True, "Safe to execute"
    
    def log_blocked_command(self, command: str, reason: str):
        """Log security incident"""
        self.blocked_log.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "reason": reason
        })
        # [TITLE] Self-protection...
        
        os.makedirs("logs", exist_ok=True)
        try:
            with open("logs/vera_access.log", "a", encoding="utf-8") as f:
                f.write(f"[BLOCKED] {datetime.now().isoformat()} - {reason}\n")
                f.write(f"Command: {command}\n")
        except:
            pass
        # [TITLE] Write to log file...

# ============================================================================
# COMMAND EXECUTOR - System Commands
# ============================================================================
class CommandExecutor:
    """Executes system commands safely"""
    
    def __init__(self, firewall: VERAFirewall):
        self.firewall = firewall
        self.execution_history = []
        print("[CMD] Command executor initialized")
    
    def is_command_request(self, message: str) -> bool:
        """Check if message is requesting command execution"""
        triggers = [
            "run", "command", "execute", "cmd", "command", "shell",
            "bash", "powershell", "terminal", "run", "exec", "system",
            "get output", "list", "show", "check", "ping", "test"
        ]
        return any(trigger in message.lower() for trigger in triggers)
    
    def parse_command(self, message: str) -> Dict:
        """Parse command from message"""
        patterns = [
            r"run\s+(?:the\s+)?(?:following\s+)?command[:\s]+(.+)",
            r"execute\s+(?:the\s+)?(.+)",
            r"cmd\s+command[:\s]+(.+)",
            r"`(.+?)`",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                cmd = match.group(1).strip()
                return {"command": cmd, "found": True}
        
        if "`" in message or "'" in message or '"' in message:
            quoted = re.findall(r"`(.+?)`", message)
            if quoted:
                return {"command": quoted[0], "found": True}
        
        return {"command": None, "found": False}
    
    async def execute_command(self, command: str, admin_mode: bool) -> Dict:
        """Execute a command and return output"""
        print(f"[CMD] Attempting command...")
        # [TITLE] COMMAND EXECUTOR ...
        
        is_safe, reason = self.firewall.is_command_safe(command)
        if not is_safe:
            self.firewall.log_blocked_command(command, reason)
            print(f"[CMD] {reason}")
            return {"success": False, "output": f"{reason}", "blocked": True}
        
        if not admin_mode:
            print(f"[CMD] Admin mode required")
            return {"success": False, "output": "Admin mode required for system commands", "mode": "client"}
        # [TITLE] Firewall check...
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout
            if result.stderr:
                output = f"{output}\n[STDERR]{result.stderr}"
            # [TITLE] Execute...
            
            max_len = 5000
            if len(output) > max_len:
                output = output[:max_len] + f"\n... output truncated ({len(output)} total chars)"
            
            self.execution_history.append({
                "command": command,
                "return_code": result.returncode,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            print(f"[CMD] Exit code: {result.returncode}")
            return {"success": True, "output": output, "return_code": result.returncode}
        
        except subprocess.TimeoutExpired:
            return {"success": False, "output": "Command timed out (30s limit)"}
        except Exception as e:
            return {"success": False, "output": f"Error: {str(e)}"}
        # [TITLE] Limit output...

# ============================================================================
# VERA CORE - AI Engine
# ============================================================================
class VERACore:
    """AI core with LDS support and high-performance optimization"""
    
    def __init__(self, model: str, lds: LDSManager):
        self.model = model
        self.lds = lds
        self.admin_detector = AdminDetector()
        self.firewall = VERAFirewall(lds.firewall)
        self.command_executor = CommandExecutor(self.firewall)
        self.conversation_history = []
        self.interaction_count = 0
        # [TITLE] VERA CORE ...
        
        # ILE: Persistent Memory System - MODIFICATION #2
        if ILE_ENABLED and ExperienceManager is not None:
            try:
                self.experience_manager = ExperienceManager()
                self.experience_manager.start_session(user_name="VERA_User")
                total_exp = self.experience_manager.get_total_count()
                print(f"[ILE] ✓ Total stored experiences: {total_exp}")
            except Exception as e:
                print(f"[ILE] Error initializing: {e}")
                self.experience_manager = None
        else:
            self.experience_manager = None
        
        self.personality = self.build_system_prompt()
        # [TITLE] Get personality from LDS...
        
        self.total_tokens = 0
        self.total_time = 0.0
        print("[VERA] Core initialized - ULTRA-OPTIMIZED")
        print(f"[VERA] {self.admin_detector.get_mode_indicator()}")
        print(f"[VERA] Model: {model}")
        print(f"[VERA] Performance: {CPU_CORES} cores, GPU acceleration enabled")
    
    def build_system_prompt(self) -> str:
        """Build system prompt from LDS personality"""
        personality = self.lds.personality
        
        prompt = f"""You are {personality.get('identity', {}).get('title', 'VERA')}.

CORE IDENTITY
{personality.get('identity', {}).get('description', 'A professional AI assistant')}

COMMUNICATION STYLE
- Tone: {personality.get('personality', {}).get('tone', 'professional')}
- {personality.get('communication_rules', {}).get('response_length', 'Keep responses brief')}
- Formatting: {personality.get('communication_rules', {}).get('formatting', 'Clear and direct')}

CURRENT MODE
{self.admin_detector.get_mode_indicator()}
{self.admin_detector.get_mode_message()}

Keep responses SHORT (1-2 sentences max). Be helpful and professional."""
        
        return prompt
    # [TITLE] Performance metrics...

# ============================================================================
# WEB SERVER - WebSocket & HTTP
# ============================================================================
class WebServer:
    """WebSocket server with streaming and performance optimizations"""
    
    def __init__(self, aicore: VERACore):
        self.aicore = aicore
        self.clients = set()
        self.ws_server = None
    
    async def start(self):
        """Start servers"""
        print("[WEB] Starting servers...")
        
        # WebSocket server
        self.ws_server = await websockets.serve(
            self.handle_ws,
            "localhost",
            8766,
            # [TITLE] WEB SERVER ...
            max_size=2**20,  # 1MB max message
            max_queue=32,
            compression=None,  # Disable compression overhead
            ping_interval=None,  # Disable ping-pong
        )
        print(f"[WEB] WebSocket started on ws://localhost:8766 (optimized)")
        
        # HTTP server
        app = web.Application()
        app.router.add_get("/", self.serve_gui)
        runner = web.AppRunner(app)
        await runner.setup()
        self.http_server = web.TCPSite(runner, "localhost", 8765)
        await self.http_server.start()
        print(f"[WEB] HTTP started on http://localhost:8765 (optimized)")
    
    async def serve_gui(self, request):
        """Serve GUI"""
        gui_files = [
            os.path.join(APP_PATH, "vera_interface_v2.html"),
            os.path.join(APP_PATH, "vera-enhanced.html"),
        ]
        
        for gui_file in gui_files:
            if os.path.exists(gui_file):
                try:
                    with open(gui_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    return web.Response(text=content, content_type="text/html")
                except:
                    pass
        
        return web.Response(text="GUI not found", status=404)
    
    async def handle_ws(self, websocket):
        """Handle WebSocket with ultra-optimized streaming"""
        self.clients.add(websocket)
        print(f"[WEB] Client connected ({len(self.clients)} total)")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    user_input = data.get("message", "").strip()
                    
                    if not user_input:
                        continue
                    # [TITLE] Performance optimizations...
                    
                    self.aicore.conversation_history.append({
                        "role": "user",
                        "content": user_input
                    })
                    # [TITLE] Add user message to history FIRST...
                    
                    if len(self.aicore.conversation_history) > 8:
                        self.aicore.conversation_history = self.aicore.conversation_history[-8:]
                    # [TITLE] Keep history short for speed...
                    
                    await websocket.send(json.dumps({
                        "type": "chat_start",
                        "mode": self.aicore.admin_detector.get_mode_indicator()
                    }))
                    
                    start_time = time.time()
                    full_response = ""
                    chunk_count = 0
                    # [TITLE] Send start signal...
                    
                    try:
                        response = ollama.chat(
                            model=self.aicore.model,
                            messages=[
                                {"role": "system", "content": self.aicore.personality},
                                *self.aicore.conversation_history[-8:]
                            ],
                            stream=True,
                            keep_alive=PerfConfig.KEEP_ALIVE,
                            options=PerfConfig.get_ollama_options()
                        )
                        # [TITLE] ULTRA-OPTIMIZED streaming with all performance settings...
                        
                        for chunk in response:
                            token = chunk["message"]["content"]
                            full_response += token
                            chunk_count += 1
                            # [TITLE] Stream chunks directly from Ollama...
                            
                            await websocket.send(json.dumps({
                                "type": "chat_chunk",
                                "chunk": token
                            }))
                            # [TITLE] Send every token for real-time streaming...
                        
                        self.aicore.conversation_history.append({
                            "role": "assistant",
                            "content": full_response
                        })
                        # [TITLE] Add assistant response to history...
                        
                        elapsed = time.time() - start_time
                        # [TITLE] Add assistant response to history...
                        
                        self.aicore.total_tokens += len(full_response)
                        self.aicore.total_time += elapsed
                        avg_tokens_per_sec = len(full_response) / elapsed if elapsed > 0 else 0
                        # [TITLE] Update performance metrics...
                        
                        # ============================================================
                        # ILE: Store interaction in persistent memory - MODIFICATION #3
                        # ============================================================
                        if self.aicore.experience_manager is not None:
                            try:
                                self.aicore.experience_manager.store_interaction(
                                    user_input=user_input,
                                    vera_response=full_response,
                                    confidence=0.75,  # Phase 1: fixed value
                                    reflection="Phase 1: Basic storage",
                                    domain=None,  # Phase 2: will extract domain
                                )
                                total = self.aicore.experience_manager.get_total_count()
                                print(f"[ILE] Total experiences: {total}")
                            except Exception as e:
                                print(f"[ILE] Error storing: {e}")
                        
                        await websocket.send(json.dumps({
                            "type": "chat_complete",
                            "time": elapsed,
                            "success": True,
                            "response": full_response,
                            "tokens": len(full_response),
                            "tokens_per_sec": round(avg_tokens_per_sec, 2),
                            "chunks": chunk_count
                        }))
                        
                        print(f"[AI] Response in {elapsed:.2f}s, {len(full_response)} chars, {avg_tokens_per_sec:.1f} toks/s")
                    
                    except Exception as e:
                        error_msg = str(e)
                        print(f"[AI] Error: {error_msg}")
                        
                        await websocket.send(json.dumps({
                            "type": "error",
                            "response": f"Error: {error_msg}",
                            "success": False
                        }))
                
                except json.JSONDecodeError as e:
                    print(f"[WEB] JSON Error: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "response": "Invalid JSON",
                        "success": False
                    }))
                
                except Exception as e:
                    print(f"[WEB] Handler Error: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "response": f"Error: {e}",
                        "success": False
                    }))
        
        except Exception as e:
            print(f"[WEB] WebSocket error: {e}")
        
        finally:
            self.clients.discard(websocket)
            print(f"[WEB] Client disconnected ({len(self.clients)} remaining)")
            # [TITLE] Send completion with performance metrics...

# ============================================================================
# MAIN APPLICATION
# ============================================================================
class VERAApplication:
    """Main application with ultra-optimization"""
    
    async def run(self):
        """Run application"""
        try:
            print("[MAIN] Starting VERA LDS Edition ULTRA-OPTIMIZED...")
            # [TITLE] MAIN ...
            
            lds = LDSManager()
            # [TITLE] Load LDS data...
            
            model = self.detect_model()
            if not model:
                print("[MAIN] No Ollama model found!")
                print("[MAIN] Please run: ollama pull llama2:3.2-3b")
                return
            # [TITLE] Detect model...
            
            aicore = VERACore(model, lds)
            webserver = WebServer(aicore)
            await webserver.start()
            
            print("=" * 80)
            print("VERA LDS OPTIMIZED is running")
            print("=" * 80)
            print(f"[INFO] Interface: http://localhost:8765")
            print(f"[INFO] WebSocket: ws://localhost:8766")
            print(f"[INFO] Mode: {aicore.admin_detector.get_mode_indicator()}")
            print(f"[INFO] Model: {model}")
            print(f"[INFO] CPU Cores: {CPU_CORES} (all enabled)")
            print(f"[INFO] GPU Acceleration: ENABLED")
            print(f"[INFO] Context Window: {PerfConfig.CONTEXT_WINDOW}")
            print(f"[INFO] Max Tokens: {PerfConfig.NUM_PREDICT}")
            print(f"[INFO] Thread Pool: {CPU_CORES} workers")
            print(f"[INFO] Firewall: ACTIVE")
            print("=" * 80)
            print("PERFORMANCE OPTIMIZATIONS ACTIVE")
            print(f"- Multi-core processing ({CPU_CORES} cores)")
            print(f"- GPU acceleration enabled")
            print(f"- Large context window ({PerfConfig.CONTEXT_WINDOW} tokens)")
            print(f"- Optimized batch processing")
            print(f"- Real-time token streaming")
            print("=" * 80)
            
            await asyncio.sleep(1)
            
            try:
                webbrowser.open("http://localhost:8765")
            except:
                pass
            # [TITLE] Initialize VERA...
            
            # Keep running
            while True:
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            print("[MAIN] Terminated")
            # Close ILE database on shutdown - MODIFICATION #4
            if hasattr(self, 'aicore') and hasattr(self.aicore, 'experience_manager'):
                if self.aicore.experience_manager is not None:
                    try:
                        self.aicore.experience_manager.close()
                        print("[ILE] Database closed cleanly")
                    except Exception as e:
                        print(f"[ILE] Error closing: {e}")
        
        except Exception as e:
            print(f"[MAIN] Error: {e}")
            import traceback
            traceback.print_exc()
    
    @staticmethod
    def detect_model():
        """Auto-detect available Ollama model"""
        # [TITLE] Prefer larger, more capable models for better quality...
        preferred = [
            "neural-chat",  # Good balance
            "llama2:3.2-13b",  # Larger model if available
            "llama2:3.2",
            "llama2:3.2-3b",
            "mistral",
            "llama2"
        ]
        
        try:
            print("[MODEL] Detecting available models...")
            models = ollama.list()
            
            if not models.models:
                return None
            # [TITLE] Keep running...
            
            for pref in preferred:
                for model in models.models:
                    if pref in model.model:
                        print(f"[MODEL] Using {model.model}")
                        return model.model
            
            # Fallback to first available
            model_name = models.models[0].model
            print(f"[MODEL] Using {model_name}")
            return model_name
        
        except Exception as e:
            print(f"[MODEL] Error: {e}")
            return None

# ============================================================================
# ENTRY POINT
# ============================================================================
def main():
    """Entry point"""
    app = VERAApplication()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("[MAIN] Shutting down...")

if __name__ == "__main__":
    main()
