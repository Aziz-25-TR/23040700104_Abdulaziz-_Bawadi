
## 🪪 Student Identity:
Nama: Abdulaziz Abdullah Bawadi

NIM: 23040700104

## 📋 1. Assignment Analysis

The assignment title is:

**Network Evidence Acquisition (PCAP), SHA-256 Hashing, and Blockchain Simulation Using Python**

The goal of this project is to demonstrate how blockchain concepts can be used to protect the integrity and chain of custody of digital network evidence.

In digital forensics, evidence must not be changed without detection. If a PCAP file is modified, even by one byte, investigators must be able to prove that the file is no longer the same as the original evidence. This project solves that problem by combining:

- PCAP evidence files
- SHA-256 hashing
- Blockchain block linking
- Blockchain validation
- Tampering detection
- Merkle Tree verification

### ⚒️ Tools:


### Mandatory Requirements

The mandatory parts are:

- Use 5 PCAP files.
- Use packet counts of 30, 50, 70, 90, and 100.
- Calculate SHA-256 hash for every PCAP file.
- Store evidence metadata inside a blockchain.
- Create a genesis block.
- Create 5 evidence blocks.
- Validate the blockchain.
- Generate a final report.



## ⚙️ 2. System Design

The system is divided into several stages.

### Stage 1: Evidence Acquisition

The program creates five PCAP files:

| File Name | Packet Count |
|---|---:|
| PCAP01.pcap | 30 |
| PCAP02.pcap | 50 |
| PCAP03.pcap | 70 |
| PCAP04.pcap | 90 |
| PCAP05.pcap | 100 |

Each PCAP file represents one piece of network evidence.

### 🔎 Stage 2: Evidence Hashing

For each PCAP file, the program calculates:

- File name
- Packet count
- File size
- SHA-256 hash

The SHA-256 hash acts as the digital fingerprint of the evidence.

### ⛓️ Stage 3: Blockchain Creation

The blockchain contains:

- 1 genesis block
- 5 evidence blocks

Each evidence block stores the SHA-256 hash of one PCAP file.

### ✅ Stage 4: Blockchain Validation

The program validates:

- Whether each previous hash is correct
- Whether each block hash is correct
- Whether current PCAP files still match the hashes stored in the blockchain

### Stage 5: Tampering Detection

The program modifies one byte in a PCAP file and recalculates the hash.

If the new hash is different from the old hash, tampering is detected.

### 📄 Stage 6: Final Reporting

The system generates a final report containing:

- Evidence file summary
- SHA-256 results
- Blockchain data
- Merkle Root
- Tampering result
- Validation result

##

### Presentation Vedieo:
https://drive.google.com/file/d/1lWGD5dvYGGbTpKt2FediHWszZfyhH0bA/view?usp=sharing
