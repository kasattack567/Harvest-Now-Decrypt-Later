
# Harvest-Now-Decrypt-Later

This project explores a proof-of-concept for the "Harvest Now, Decrypt Later" (HNDL) attack model, which anticipates a future in which quantum computers may be capable of breaking classical encryption (e.g., RSA, ECDHE). 

The process involves capturing TLS-encrypted traffic locally, extracting and organizing handshake and application data from `.pcapng` files using Wireshark and Python, and storing the necessary information that would hypothetically allow decryption once a large-scale quantum computer becomes available.

The goal is to test how feasible it is to gather and prepare traffic data today for potential decryption in the future under post-quantum threat models.
