
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
## Problems with CSV Export

While exporting TLS packet data to CSV, I encountered several issues that make parsing difficult:

- Some rows contain missing or inconsistent field values, such as empty cells or extra delimiters.
- The formatting of timestamps and use of escaped characters (e.g. `\`) varies and can cause parsing errors.
- Handshake and application data often appear in separate packets with no consistent session ID to match them reliably.
- Some entries are malformed or duplicated, especially during high-volume exchanges.
- Data fields such as cipher suites or key material can span multiple lines or include embedded commas, disrupting the CSV structure.

These inconsistencies complicate efforts to extract and match relevant cryptographic information programmatically. Improving the capture and export process — or cleaning the CSV programmatically — is necessary before analysis.

## Next Steps

The next stage is to write a Python script that parses the exported TLS CSV files. The objective is to extract and organise relevant fields from both the handshake and application data — such as IP addresses, port numbers, timestamps, key shares, RSA modulus, and ciphertext — and then match them into a single structured table.

The parser will:

- Load and clean the handshake and application data CSV files.
- Extract key fields like client random, key share, RSA modulus, and ciphertext.
- Match handshake packets to corresponding application data using shared IP/port combinations and nearby timestamps.
- Output a merged CSV file containing the matched sessions with all the necessary information.

