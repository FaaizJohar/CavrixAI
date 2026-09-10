# Cavrix AI — Migration Strategy

This document outlines the step-by-step strategy for splitting the monolithic Python codebase into the Web/Desktop architecture.

## Phase 1: Audit and Documentation
- Document the architecture, security model, and protocol (This folder).
- Inventory all existing features to ensure nothing is lost during the rewrite.

## Phase 2: Shared Protocol
- Define the JSON/WebSocket message schemas.
- Implement Pydantic models in Python and TypeScript interfaces in a shared package.
- This ensures both the Web and Desktop speak the exact same language.

## Phase 3: Desktop Agent Extraction
- Branch the existing codebase.
- Decouple `ui.py` (PyQt6 UI) from `main.py`.
- Introduce the `PermissionEngine` and wrap the `actions/` folder.
- Implement the WebSocket client that connects to the Realtime Gateway.
- Implement the DevAgent Sandbox and File System boundaries.

## Phase 4: Realtime Gateway & Backend
- Setup the WebSocket relay service.
- Build the device pairing flow (Web generates a code, Desktop inputs the code to pair).
- Setup PostgreSQL database for managing user accounts, device public keys, and connection routing.

## Phase 5: Cavrix Web (Next.js)
- Build the web interface, preserving the original Reactor HUD and theming.
- Connect Web UI to the Gateway.
- Re-implement Gemini Live Voice via WebRTC/Browser Audio APIs.
- Build the UI panels for Memory, Undo, and Device Management.

## Phase 6: Testing & Rollout
- Write regression tests for every module in `actions/`.
- Test path traversal and file boundary security.
- End-to-end testing of the complete message flow: Web -> Gateway -> Desktop -> Gateway -> Web.
