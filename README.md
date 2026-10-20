# QKD–TLS Integration

A learning-focused research prototype exploring the integration of
simulated Quantum Key Distribution (QKD) with TLS using pre-shared keys
(PSK).

This project follows the general approach described in the research paper
*A Practical Framework for Simulating the Integration of QKD in TLS
Protocol Towards Quantum Secure Communication.*

## Overview

Quantum Key Distribution can be used to establish shared secret key
material. TLS can then use pre-shared key mechanisms to establish a
protected communication session.

This project explores the integration of these components using a
simulated BB84 workflow, a local Key Management System (KMS), and OpenSSL.

## Architecture

```text
QuNetSim BB84 Simulation
          |
          v
    Generated Key
          |
          v
      Key Block
          |
          v
   Key Management System
          |
          v
      TLS-PSK Handshake
          |
          v
   Protected File Transfer
          |
          v
     SHA-256 Verification
```

## Technologies

- Python
- QuNetSim
- OpenSSL
- TLS 1.2
- PSK-AES128-GCM-SHA256
- Wireshark
- Ubuntu Linux

## Project Structure

| File | Purpose |
| --- | --- |
| `bb84.py` | Simulates BB84 and generates matching key material |
| `key_block.py` | Creates a structured key block from generated key material |
| `kms_server.py` | Implements KMS key registration and retrieval logic |
| `kms_api.py` | Provides a local HTTP API for KMS operations |
| `epr_test.py` | Tests an entanglement-related QuNetSim example |
| `test_qubit.py` | Tests basic qubit operations in QuNetSim |
| `experiment_results.txt` | Local experiment results; not included in Git |
| `qll/` | Local QKD-side files and generated key material |
| `kms/key_pool/` | Local KMS key storage |

Generated keys, test files, packet captures, and local experiment results
should remain local and must not be committed to the repository.

## Requirements

- Ubuntu Linux
- Python 3.12
- OpenSSL 3.x
- QuNetSim 0.1.3.post1

The project currently does not include a `requirements.txt` file.

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd qkd-tls-integration
```

Replace the URL with the repository's actual GitHub URL.

### 2. Create a virtual environment

```bash
python3 -m venv qunetsim-venv
source qunetsim-venv/bin/activate
```

### 3. Install QuNetSim

```bash
python -m pip install qunetsim==0.1.3.post1
```

### 4. Verify OpenSSL

```bash
openssl version
```

The prototype was tested locally with OpenSSL 3.0.13.

## Experimental Workflow

The current local prototype demonstrates the following workflow:

1. Simulate BB84 using QuNetSim.
2. Generate matching 256-bit key material.
3. Create a structured key block.
4. Register and retrieve the key through the local KMS.
5. Establish a TLS 1.2 PSK connection using OpenSSL.
6. Transfer a file over the TLS connection.
7. Verify file integrity by comparing SHA-256 hashes.
8. Inspect TLS traffic using Wireshark.
9. Collect preliminary KMS latency and TLS handshake timing measurements.

The current tests run on a single Ubuntu machine, with the TLS client and
server communicating locally.

## Current Status

Verified in the local prototype:

- BB84 simulation produced matching 256-bit key material.
- Key block creation and local KMS key retrieval.
- TLS 1.2 PSK connection establishment.
- Successful transfer and SHA-256 verification of a 100 KiB file.
- A negative test using an incorrect PSK.
- Initial TLS packet inspection in Wireshark.
- Preliminary KMS API latency and TLS handshake timing measurements.

The full paper methodology has not yet been audited requirement by
requirement. Additional verification is required before claiming a
complete reproduction of the paper.

## Limitations and Security Considerations

This project is intended for learning and research experimentation. It
is not a production-secure QKD or TLS deployment.

- BB84 is simulated; no physical quantum hardware is used.
- The current BB84 workflow is simplified and does not demonstrate a
  complete practical QKD security pipeline.
- The KMS uses simplified local key storage and an HTTP API.
- The local KMS API is not intended to be exposed to an untrusted network.
- TLS uses a pre-shared key configured through OpenSSL.
- A single-machine test does not demonstrate communication between
  independent physical hosts.
- Local timing results include process startup and connection overhead.

Do not use production secrets with this prototype. Never commit generated
key material, credentials, or private configuration files.

## Research Reference

*A Practical Framework for Simulating the Integration of QKD in TLS
Protocol Towards Quantum Secure Communication.*

Add the verified publication details and official paper link here.

## License

No license has been selected yet.
