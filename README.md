# CST-MCP: AI Agent Interface for CST Studio Suite

## Overview

**CST-MCP** is an implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) designed to bridge Large Language Models (LLMs) with **CST Studio Suite**. It empowers AI agents to autonomously perform electromagnetic simulation tasks, including geometric modeling, solver configuration, and results analysis.

This project aims to transform CST Studio Suite into a controllable environment for AI, moving beyond simple scripting to full "agentic" capabilities where the AI can close the loop between design, simulation, and verification.

## Project Goal

To build a robust set of tools and an MCP server that allows an AI Agent to:
1.  **Model**: Create and manipulate 3D structures using boolean operations and parametric modeling.
2.  **Simulate**: Configure boundaries, ports, and solvers, and execute simulations.
3.  **Analyze**: Export and interpret results (S-parameters, field monitors) to make design decisions.
4.  **Iterate**: Automatically correct errors (e.g., geometry intersection, mesh failures) and optimize designs.

## Features (Planned & Implemented)

- **MCP Server**: A standardized interface for agents to discover and call CST tools.
- **Geometric Primitives**: Create bricks, cylinders, spheres, etc.
- **Boolean Operations**: Union, subtract, intersect for complex modeling.
- **Simulation Control**: Open projects, set parameters, run solvers (T-Solver, F-Solver).
- **Results Export**: Extract Touchstone files (S-parameters) and key metrics (bandwidth, resonance).

## Structure

- `server/`: Implementation of the MCP server.
- `tools/`: Core logic for CST interactions (wrappers around CST Python libraries).
- `utils/`: Helper functions for geometry and data handling.
- `demos/`: Example scripts demonstrating automated workflows.

## Roadmap

### Phase 1: The Automation Loop
- [x] Establish minimal Python automation (Open -> Model -> Solve -> Export).
- [ ] Stabilize core tools using official CST Python Libraries or COM interface.

### Phase 2: Minimal MCP Server
- [ ] Implement `open_project`, `set_parameters`, `run_solver`, `export_results` tools.
- [ ] specific geometry tools (`make_brick`, `boolean_subtract`, etc.) for detailed modeling.

### Phase 3: Intelligent Feedback
- [ ] **Experiment Tracking**: Log every tool call with complete context for reproducibility.
- [ ] **Auto-Diagnosis**: Detect and classify common failures (mesh errors, port overlaps).
- [ ] **Semantic Results**: Return structured engineering metrics (e.g., "10dB Bandwidth") instead of raw files.

## Getting Started

*(Instructions on how to set up the environment and run the server will be added here)*

## License

[MIT License](LICENSE)
