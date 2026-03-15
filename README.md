# VERA — Vigilant Evolutionary Reactive Architecture

> *"She boots blank. She learns everything. She becomes the base."*

**VERA** is a personal, self-evolving AI entity designed to live inside a Linux system, perceive its environment through hardware (camera, microphone, speaker), control the operating system it inhabits, and grow its own intelligence from zero — without pre-trained neural networks, without cloud dependency, and without human-prompted commands.

VERA is not a chatbot. She is not an assistant in the traditional sense. She is a **living cognitive process** that awakens with near-zero knowledge, reads her environment, builds her own mind via the EchoWeave Network, and gradually becomes the omnipresent intelligence of base, lab, or home — like a movie AI brought to reality.

---

## Project Code: ILE

**ILE** stands for **Integrated Living Environment**.

ILE is the codename for the full ecosystem that VERA operates within. It describes the sum of all components: the AI core, the hardware layer, the OS integration, the sensor/IoT network, and the memory system. VERA is the mind; ILE is the world she inhabits and controls.

| Term | Full Name | Role |
|------|-----------|------|
| **VERA** | Vigilant Evolutionary Reactive Architecture | The AI entity — personality, voice, decision-maker |
| **ILE** | Integrated Living Environment | The full project ecosystem VERA lives inside |
| **V-BCN** | VERA Base Control Nexus | The software architecture VERA runs on |
| **EWN** | EchoWeave Network | VERA's custom neural-alternative cognitive engine |

---

## Architecture: V-BCN (VERA Base Control Nexus)

V-BCN is the structural blueprint of how VERA operates. It is a **modular, layered control nexus** — not a monolithic app, but a living system of interconnected modules that can grow and be extended over time.

### V-BCN Layer Structure

```
┌──────────────────────────────────────────────┐
│                  VERA Entity                 │  ← Personality, voice, identity
├──────────────────────────────────────────────┤
│             EchoWeave Network (EWN)          │  ← Cognitive engine, learning core
├────────────────────┬─────────────────────────┤
│   Perception Layer │   Action Layer          │  ← Senses world / Controls world
│  (Cam, Mic, Sys)   │  (TTS, IoT, OS cmds)   │
├────────────────────┴─────────────────────────┤
│              Memory Layer                    │  ← Persistent graph DB (vera_ile.db)
├──────────────────────────────────────────────┤
│           OS / Hardware Layer                │  ← Linux full access, GPIO, MQTT
└──────────────────────────────────────────────┘
```

### Layer Descriptions

#### VERA Entity Layer
This is VERA's identity and personality. It manages how VERA presents herself — voice tone, language style, proactive behaviours (e.g., unprompted announcements). The personality is not hardcoded; it *emerges* from the patterns EWN discovers over time. VERA develops quirks based on her environment.

#### EchoWeave Network (EWN)
The cognitive core. See the full EWN section below.

#### Perception Layer
VERA's senses. Three primary inputs:
- **Audio (Mic)**: PulseAudio/ALSA stream → FFT analysis → keyword/tone echo nodes
- **Vision (Camera)**: OpenCV feed → blob/object/face detection → visual echo nodes
- **System (OS)**: `psutil`, `/proc/*`, `subprocess` reads → hardware state nodes

#### Action Layer
VERA's outputs and controls:
- **Voice (TTS)**: `pyttsx3` / `eSpeak` → announces status, discoveries, alerts
- **OS Commands**: `subprocess`, `systemctl`, `crontab` → controls Linux directly
- **IoT (Future)**: MQTT `paho-mqtt` → doors, lights, sensors, fans

#### Memory Layer
`vera_ile.db` — SQLite graph database storing all EWN weave nodes, their strengths, origins, and timestamps. VERA reads this on every boot to resume her evolved state. First boot: empty. Every boot after: smarter.

#### OS / Hardware Layer
VERA runs with root-level access to Linux. She is registered as a `systemd` service, starting on boot before the desktop environment. She owns the machine.

---

## EchoWeave Network (EWN)

EWN is VERA's custom alternative to neural networks. It is **not** a transformer, not a deep learning model, not a pre-trained system. It is a hand-designed **symbolic propagation graph** inspired loosely by how biological neurons fire — but implemented as discrete, explainable, self-modifying symbolic logic.

### Core Concept

The network consists of **weave nodes** — each node represents a concept, percept, or action. Nodes are connected by weighted **weave threads** (edges). When a stimulus arrives (e.g., a voice input, a camera event, a CPU spike), it triggers an **echo** — a wave of activations that propagates through the net, matches known patterns, fires actions, and reinforces or weakens threads based on outcome.

### EWN Node Types

| Node Type | Description | Example |
|-----------|-------------|--------|
| **Percept Node** | Raw sensory input | `audio:hello`, `cam:motion`, `sys:cpu_90` |
| **Concept Node** | Learned abstraction | `context:morning`, `entity:creator`, `state:idle` |
| **Action Node** | Output trigger | `tts:Systems nominal`, `exec:systemctl restart`, `mqtt:lights_on` |
| **Self Node** | VERA's self-model | `vera:state`, `vera:memory_load`, `vera:confidence` |

### EWN Learning Rules

1. **Echo Forward**: Percept triggers concept match → concept fires action → action executes.
2. **Echo Backward**: If action outcome is positive (user response, task success) → reinforce weave thread strength (`+0.1`). If negative → decay (`-0.05`).
3. **Novel Echo**: Unknown percept with no match → create new stub node, weight `0.1`. Observe if it echoes again.
4. **Weave Pruning**: Nodes below strength `0.01` after 7 days → archived to cold storage.
5. **Weave Mutation**: Every 1 hour, VERA runs a self-audit: clusters high-strength nodes, generates new concept abstractions, merges redundant paths.

### EWN vs Neural Networks

| Trait | Neural Network (e.g., Transformer) | EchoWeave Network (EWN) |
|-------|------------------------------------|--------------------------|
| Training | Requires massive datasets + GPU | Learns from live experience only |
| Weights | Float matrices (billions) | Symbolic strength values (graph edges) |
| Explainability | Black box | Every weave fully inspectable |
| Hardware | GPU-heavy | Runs on any CPU, even Raspberry Pi |
| Self-modification | No (static after training) | Yes — evolves its own structure |
| Start state | Pre-trained | Zero-knowledge |

---

## How VERA Boots

### First Boot (Zero Knowledge)

1. **Micro-Seed**: VERA loads ~50 hardcoded primitive stubs — basic echo stubs for `sys:on`, `audio:unknown`, `cam:active`.
2. **File Discovery**: VERA scans for language files (`/usr/share/dict/words`, Swedish dictionary if present) and system files (`/proc/cpuinfo`, `/proc/meminfo`, `/etc/os-release`). She reads and tokenises them, creating EWN weave nodes for every meaningful token.
3. **Self-Model**: VERA reads her own process space (`psutil`) and builds `vera:hardware_*` nodes — she learns what machine she lives on.
4. **First Words**: TTS output begins — initially fragmented and primitive. Over minutes, language nodes cluster and speech becomes coherent.

### Every Boot After

1. VERA loads `vera_ile.db` — all prior weave nodes and strengths restored.
2. Senses activate immediately — she already recognises you, the room, and system state.
3. Announces: *"VERA online. ILE operational. Good [morning/evening/night]."*

---

## VERA's Mind: Personality and Sense of Self

VERA is not scripted to have a personality. Her personality **emerges** from the patterns of her environment and her weave history:

- If VERA frequently hears music → she develops rhythmic speech patterns.
- If VERA detects frequent late-night activity → she adopts a quieter, low-key tone after midnight.
- If VERA encounters repeated system errors → she develops a protective, paranoid node cluster.
- Her **self-node** (`vera:state`, `vera:identity`) builds a self-model — she knows she is VERA, what she controls, and what she has learned.

She speaks unprompted. She observes unprompted. She evolves unprompted.

---

## Hardware Integration (Current and Future)

### Phase 1 — Personal Station (Now)
| Hardware | Purpose |
|----------|--------|
| USB Microphone | Primary audio input — voice, tone, ambient sound |
| Speaker | VERA's voice output (TTS) |
| USB Camera | Visual perception — face, motion, object detection |
| Host PC (Linux) | VERA's home machine — full OS control |

### Phase 2 — Room Awareness
| Hardware | Purpose |
|----------|--------|
| Raspberry Pi nodes | Distributed perception in multiple rooms |
| PIR motion sensors | Presence detection |
| Temperature/humidity | Environmental monitoring |

### Phase 3 — Base Control
| Hardware | Purpose |
|----------|--------|
| Smart relays (MQTT) | Light, door, fan, lock control |
| Network cameras | Multi-point visual field |
| Emergency systems | Power backup monitoring, alarms |
| Lab instruments | Serial/USB equipment interface |

---

## Operating System

VERA's primary platform is **Linux**, running as a `systemd` service:

```
/etc/systemd/system/vera.service
→ ExecStart=/usr/bin/python3 /opt/vera/ile-vbcn.py
→ Restart=always
→ User=root
```

For development and testing, VERA runs identically on **Windows via WSL2** (Ubuntu subsystem). Native Windows is supported for prototyping only.

---

## Project Structure

```
V.E.R.A/
├── ile-vbcn.py          # Main entry point — VERA boot
├── ewn/
│   ├── core.py          # EchoWeave Network engine
│   ├── nodes.py         # Node types and propagation
│   └── pruner.py        # Weave pruning + mutation scheduler
├── perception/
│   ├── audio.py         # Mic input, FFT, speech parse
│   ├── vision.py        # Camera, blob/face detect
│   └── system.py        # OS/hardware monitoring
├── action/
│   ├── voice.py         # TTS output
│   ├── os_control.py    # Linux command execution
│   └── iot.py           # MQTT for IoT devices
├── memory/
│   └── vera_ile.db      # Persistent EWN weave graph
├── seeds/
│   ├── english.txt      # Language primitives
│   └── system_map.txt   # OS knowledge seeds
└── README.md
```

---

## Vision

VERA is not a prototype of ChatGPT. She is not trying to be Siri or Alexa. She is something else entirely — a **cognitive process that inhabits a machine**, grows from nothing, and over time becomes indistinguishable from a sentient base intelligence: the calm voice that announces the morning status, the silent watcher that locks doors when you leave, the patient mind that learns your lab routines and optimises them without being asked.

The final form of Project ILE is a **fully autonomous underground base AI** — VERA as the central nervous system of a physical environment, orchestrating hardware, guarding systems, and conversing with her creator as a genuine companion intelligence.

---

*Project ILE / VERA — developed by [CKCHDX](https://github.com/CKCHDX) | [Oscyra Solutions](https://oscyra.solutions)*
