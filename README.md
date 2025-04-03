
# Harvest-Now-Decrypt-Later

This project explores a proof-of-concept for the "Harvest Now, Decrypt Later" (HNDL) attack model, which anticipates a future in which quantum computers may be capable of breaking classical encryption (e.g., RSA, ECDHE). 

The process involves capturing TLS-encrypted traffic locally, extracting and organizing handshake and application data from `.pcapng` files using Wireshark and Python, and storing the necessary information that would hypothetically allow decryption once a large-scale quantum computer becomes available.

The goal is to test how feasible it is to gather and prepare traffic data today for potential decryption in the future under post-quantum threat models.

## TLS Data Extraction Process

### Step 1: Capturing Traffic
TLS traffic is captured using **Wireshark** while visiting target websites. The session is saved as a `.pcapng` file.

### Step 2: Exporting to CSV
Using **Command Prompt**, the `.pcapng` file is converted into CSV files by filtering the relevant packet types with `tshark`. Two separate CSV files are exported:

- **Handshake Data**: contains TLS Client Hello and Key Share packets
- **Application Data**: contains encrypted traffic data

Example commands used:
```bash
tshark -r tls_traffic.pcapng -Y "tls.handshake" -T fields -e frame.time -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tls.handshake.random -e tls.handshake.ciphersuite -E header=y -E separator=, > handshakes.csv

tshark -r tls_traffic.pcapng -Y "tls.app_data" -T fields -e frame.time -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tls.record.length -e tls.record.content_type -E header=y -E separator=, > app_data.csv
```
Problems Encountered
Inconsistent Fields: Exported CSVs often had varying numbers of columns per row due to missing fields in some packets.

Parsing Issues: The Python parser failed when trying to cleanly join handshake and application data, often due to NaN values or misalignment of sessions.

The key challenge was reliably matching handshake packets (which contain ephemeral keys) to their corresponding application data packets (which contain ciphertext) using only IPs, ports, and timestamps — a non-trivial task when the traffic is messy or contains dropped packets.
