# Simulating Logistis Systems with SimPy 🏥⚕️

Learn to design, build, and validate **Discrete-Event Simulation (DES)** models for real scenarios (such as healthcare) using **SimPy**—an elegant, focused, and industry-recognized Python library backed by a large community.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![SimPy](https://img.shields.io/badge/SimPy-ready-success)

---

## Why SimPy?
- **Focused & powerful:** Purpose-built for DES—no noisy extra toolkit.
- **Intuitive modeling:** Express processes naturally; skip needless abstractions.
- **Scales with you:** From small clinics to large, multi-department hospital systems.
- **Thriving community:** Plenty of examples, discussions, and AI-assisted solutions.

---

## What You’ll Build
- **Patient arrival & triage flows** (emergency department)
- **Appointment scheduling & resource contention** (doctors, nurses, equipment)
- **Bed occupancy management** in wards and ICUs
- **Operating room scheduling** with prep/recovery delays
- **Diagnostics & lab workflows** (tests, queues, prioritization)
- Experiments: warm-up, multiple replications, confidence intervals

---

## Course Flow
1. **Foundations:** Events, processes, resources, queues
2. **Patient Pathways:** Arrivals, service, transfers, priorities
3. **Data & Calibration:** Input models, randomness, validation
4. **Experiments:** KPIs, replications, sensitivity, what-if
5. **Capstone:** End-to-end hospital simulation

---

## Quick Start

### Prereqs
- Python **3.10+**  
- Recommended: `venv` for isolation

### Setup
```bash
# create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# install dependencies
pip install simpy numpy pandas matplotlib
