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

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sls
   ```

2. **Create virtual environment**
   ```bash
   py -m venv venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate.ps1
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Complete Analysis

Execute the full simulation across all scenarios:

```bash
> cd .\01\ 
> py <python-file.py>
```
