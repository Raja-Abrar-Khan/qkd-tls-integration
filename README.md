# QKD–TLS Integration Prototype

A learning-focused implementation exploring how simulated Quantum Key
Distribution (QKD) can be integrated with TLS using pre-shared keys (PSK).

The project follows the general workflow described in the research paper:

*A Practical Framework for Simulating the Integration of QKD in TLS
Protocol Towards Quantum Secure Communication.*

## Overview

The prototype connects five main components:

1. **BB84 simulation:** QuNetSim simulates the BB84 quantum key distribution
   protocol and produces matching key material.
2. **Key block creation:** The generated key is represented as a structured
   key block containing metadata and an integrity digest.
3. **Key Management System (KMS):** A local KMS manages key registration
   and retrieval through a simple HTTP API.
4. **TLS-PSK:** OpenSSL establishes a TLS 1.2 connection using a pre-shared
   key obtained from the KMS.
5. **Data transfer:** A file is transferred through the TLS connection and
   its integrity is checked using SHA-256.

## Architecture

```text
QuNetSim BB84 simulation
          |
          v
   Generated key material
          |
          v
      Key block
          |
          v
    Local KMS / API
          |
          v
     TLS-PSK handshake
          |
          v
   Protected data transfer
          |
          v
     SHA-256 verification
```

## Technologies

- Python 3.12
- QuNetSim
- OpenSSL 3.x
- TLS 1.2 with `PSK-AES128-GCM-SHA256`
- Wireshark for packet inspection
- Ubuntu Linux

## Project components

| File or directory | Purpose |
| --- | --- |
| `bb84.py` | BB84 simulation and key generation |
| `key_block.py` | Creates a structured key block from generated key material |
| `kms_server.py` | KMS key registration and retrieval logic |
| `kms_api.py` | Local HTTP API for KMS operations |
| `qll/` | Local QKD-side files and generated key material |
| `kms/key_pool/` | Local KMS key pool |
| `experiment_results.txt` | Recorded preliminary measurements |
| `test_files/` | Generated test files for transfer experiments |

Generated key files and local runtime data should not be committed to the
repository.

## Environment setup

Tested in a local Ubuntu environment with Python 3.12 and OpenSSL 3.0.13.

Create and activate a virtual environment:

```bash
python3 -m venv qunetsim-venv
source qunetsim-venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Check OpenSSL:

```bash
openssl version
```

## Experimental workflow

The current workflow is:

1. Run the BB84 simulation.
2. Create a key block from the generated key material.
3. Register and retrieve the key through the local KMS.
4. Start a TLS-PSK server and connect a client using OpenSSL.
5. Transfer data over the TLS connection.
6. Compare the SHA-256 hashes of the original and received files.
7. Inspect TLS traffic with Wireshark.
8. Record preliminary KMS latency and TLS connection timing measurements.

The implementation is currently tested on a single Ubuntu machine. Alice
and Bob communicate through local processes; separate virtual machines or
physical computers are not part of the current setup.

## Current status

Verified in the local prototype:

- BB84 simulation produced matching 256-bit key material.
- Key block creation and local KMS retrieval.
- TLS 1.2 PSK connection establishment.
- Successful transfer and SHA-256 verification of a 100 KiB file.
- A negative test using an incorrect PSK.
- Initial Wireshark inspection.
- Preliminary KMS latency and TLS handshake timing measurements.

Additional testing and comparison with the paper's exact methodology remain
necessary before claiming a complete reproduction.

## Limitations and security notes

This project is intended for learning and experimentation, not production
security.

- BB84 is simulated; no physical quantum hardware is used.
- The current BB84 workflow is simplified and does not establish a complete
  practical QKD security pipeline.
- The local KMS uses a simplified implementation and local key storage.
- The local HTTP KMS API and key storage are not designed for deployment on
  an untrusted network.
- The TLS connection uses a pre-shared key configured through OpenSSL.
- Single-machine tests do not demonstrate communication between independent
  network hosts.
- Measurements include local process and connection overhead and should not
  be interpreted as pure cryptographic processing time.

Never use real production secrets with this prototype or expose the local
KMS API to an untrusted network.

## Research reference

*A Practical Framework for Simulating the Integration of QKD in TLS Protocol
Towards Quantum Secure Communication.*

Add the paper's official publication link and complete citation here after
verifying the bibliographic details.

## License

No license has been selected yet. Add a license before inviting reuse or
contributions.
