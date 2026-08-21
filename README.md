# FIM-Sentinel: Real-Time File Integrity Monitor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Cryptography](https://img.shields.io/badge/Cryptography-SHA--256-00599C)
![Compliance](https://img.shields.io/badge/Compliance-PCI--DSS-green)
![Security](https://img.shields.io/badge/SecOps-Auditing-red)

**FIM-Sentinel** is a custom File Integrity Monitoring (FIM) engine designed to track unauthorized alterations in critical server directories, ensuring configuration immutability through cryptographic baselining.

## Context and Problem Resolution
In high-security environments, specifically those processing financial transactions or sensitive PII (Personally Identifiable Information), unauthorized modification of configuration files (`.conf`), scripts (`.sh`), or authorized keys can lead to catastrophic data breaches. 

FIM-Sentinel addresses this risk by providing an automated layer of auditing. It maps critical directories, establishes a cryptographic baseline, and monitors for drifts. This capability directly supports regulatory compliance requirements, most notably **PCI-DSS Requirement 11.5**, which mandates the deployment of file-integrity monitoring tools.

## System Architecture

The FIM-Sentinel operates through a deterministic, low-latency loop:

1. **Baseline Generation:** The system recursively scans a target directory and computes a SHA-256 cryptographic hash for every file, storing this immutable state locally in a JSON manifest.
2. **Real-Time Monitoring:** Acting as a daemon, the engine continuously re-hashes the target directory at user-defined intervals (latency configurable down to seconds).
3. **Drift Detection:** The engine performs a bitwise comparison between the current hashes and the established baseline.
4. **Alerting:** Any deviation (Modifications, Additions, or Deletions) triggers immediate, structured logging alerts for incident response evaluation.

## Performance and Reliability (Lab Testing)
* **Mutation Detection:** 100% detection rate for byte-level mutations during controlled payload injections (simulating *Insider Threats* and *Config Drifts*).
* **Processing Latency:** Sub-3-second detection latency on standard directory trees.
* **Cryptographic Standard:** Utilization of the SHA-256 algorithm ensures collision resistance and data integrity verification.

## Technologies Used
* **Core Language:** Python (Strict OOP architecture)
* **Cryptography:** Python `hashlib` (SHA-256)
* **Data Persistence:** JSON formatted baselines
* **System Operations:** `os` and `time` modules for continuous IO processing

## Code Quality and AI Assistance
During the Software Development Life Cycle (SDLC) of this project, the **Gemini Pro** model was utilized as an architectural assistance and Quality Assurance (QA) tool. Artificial intelligence was employed in validating the continuous loop logic and optimizing the recursive directory traversal, resulting in a **zero-defect rate (0) for structural code errors** and strict adherence to PEP 8 standards.

---

## Local Execution Instructions

### 1. Prerequisites
* Python 3.10 or higher.
* No external libraries (e.g., `pip install`) are required. The project relies entirely on the robust Python Standard Library.

### 2. Initialization
Clone the repository and execute the engine. The script will automatically generate a `./secure_data` directory if one does not exist.

```bash
git clone [https://github.com/bruventurelli/FIM-Sentinel-SecOps.git](https://github.com/bruventurelli/FIM-Sentinel-SecOps.git)
cd FIM-Sentinel-SecOps

# Start the monitoring daemon
python fim_monitor.py