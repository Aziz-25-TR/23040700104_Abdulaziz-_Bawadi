


## 1. Assignment Analysis

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



## 2. System Design

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

### Stage 2: Evidence Hashing

For each PCAP file, the program calculates:

- File name
- Packet count
- File size
- SHA-256 hash

The SHA-256 hash acts as the digital fingerprint of the evidence.

### Stage 3: Blockchain Creation

The blockchain contains:

- 1 genesis block
- 5 evidence blocks

Each evidence block stores the SHA-256 hash of one PCAP file.

### Stage 4: Blockchain Validation

The program validates:

- Whether each previous hash is correct
- Whether each block hash is correct
- Whether current PCAP files still match the hashes stored in the blockchain

### Stage 5: Tampering Detection

The program modifies one byte in a PCAP file and recalculates the hash.

If the new hash is different from the old hash, tampering is detected.

### Stage 6: Final Reporting

The system generates a final report containing:

- Evidence file summary
- SHA-256 results
- Blockchain data
- Merkle Root
- Tampering result
- Validation result



---

## 3. Blockchain Architecture

A blockchain is a chain of blocks where each block is connected to the previous block using a cryptographic hash.

In this project, the blockchain is not connected to a real cryptocurrency network. It is a simulation designed for academic understanding.

### Genesis Block

The genesis block is the first block in the blockchain.

It does not represent evidence. Its purpose is to start the chain.

The genesis block has:

- Index: 0
- Evidence file name: GENESIS
- Packet count: 0
- Evidence hash: 0
- Previous hash: 0

### Evidence Blocks

Each evidence block represents one PCAP evidence file.

Each evidence block contains:

- Index
- Timestamp
- Evidence file name
- Packet count
- Evidence SHA-256 hash
- Previous hash
- Block hash

### Why Previous Hash Is Important

The previous hash connects one block to the block before it.

For example:

```text
Block 1 stores the hash of Block 0
Block 2 stores the hash of Block 1
Block 3 stores the hash of Block 2
```

If Block 1 is changed, its block hash changes. Then Block 2 will no longer point correctly to Block 1. This breaks the blockchain.

This is how blockchain detects unauthorized changes.

### How Blockchain Preserves Evidence Integrity

The blockchain stores the original SHA-256 hash of each evidence file.

Later, if someone checks the evidence again, the program recalculates the hash of the current file.

If the current hash matches the blockchain hash, the evidence is unchanged.

If the current hash does not match, the evidence has been modified.

---

## 4. Python Implementation

The project uses Python because it is beginner-friendly, readable, and suitable for Google Colab.

The main Python file is:

```text
sourcecode/main.py
```

### Main Classes

#### EvidenceRecord

`EvidenceRecord` stores information about one PCAP file.

It contains:

- `file_name`
- `packet_count`
- `file_size`
- `sha256_hash`

This class is used so evidence metadata is organized clearly.

#### Block

`Block` represents one blockchain block.

It contains:

- `index`
- `timestamp`
- `evidence_file_name`
- `packet_count`
- `evidence_sha256_hash`
- `previous_hash`
- `block_hash`

This class makes the blockchain easier to understand because each block has a clear structure.

### Main Functions

#### generate_required_pcaps()

This function creates five PCAP files with the required packet counts.

It ensures the project follows the assignment requirements exactly.

#### calculate_sha256()

This function calculates the SHA-256 hash of a file.

It reads the file in small chunks so it can also work with large evidence files.

#### collect_evidence_records()

This function reads each PCAP file and collects:

- Packet count
- File size
- SHA-256 hash

The result is a list of evidence records.

#### calculate_block_hash()

This function calculates the hash of one block.

It uses important block data such as:

- Index
- Timestamp
- Evidence file name
- Packet count
- Evidence hash
- Previous hash

#### build_blockchain()

This function creates:

- The genesis block
- Five evidence blocks

Each evidence block is linked to the previous block.

#### validate_blockchain_structure()

This function checks whether the blockchain structure is correct.

It verifies:

- Block index order
- Previous hash consistency
- Block hash consistency

#### validate_evidence_against_blockchain()

This function checks whether the current PCAP files still match the hashes stored in the blockchain.

This is the main digital forensic validation step.

#### validate_full_chain()

This function combines blockchain validation and evidence validation.

It returns:

```text
Blockchain Validation: VALID
```

or

```text
Blockchain Validation: INVALID
```

#### build_merkle_tree()

This function builds a Merkle Tree from the SHA-256 hashes of the PCAP files.

It returns:

- Leaf hashes
- Parent hashes
- Merkle Root

#### simulate_one_byte_tampering()

This function modifies one byte in a PCAP file.

It then recalculates the SHA-256 hash to prove that even a tiny change creates a completely different hash.

#### generate_report()

This function creates the final project report in Markdown format.

The report is saved in:

```text
report/final_report.md
```

---

## 5. Testing Procedure

To test the project, run:

```bash
pip install scapy
python sourcecode/main.py
```

### Expected Output

The program should show the SHA-256 results for all five PCAP files.

Then it should show the blockchain blocks.

Before tampering, the validation result should be:

```text
Blockchain Validation: VALID
```

After the one-byte tampering simulation, the validation result should become:

```text
Blockchain Validation: INVALID
```

This proves that the system can detect evidence modification.

### Files Generated

After running the program, the following files should exist:

```text
evidence/PCAP01.pcap
evidence/PCAP02.pcap
evidence/PCAP03.pcap
evidence/PCAP04.pcap
evidence/PCAP05.pcap
report/final_report.md
```

---

## 6. Tampering Demonstration

Tampering means modifying evidence without authorization.

In this project, tampering is simulated by changing only one byte in `PCAP03.pcap`.

Before modification, the file has an original SHA-256 hash.

After modification, the program recalculates the SHA-256 hash.

The output shows:

```text
Old hash: original hash value
New hash: modified hash value
Tampering detected: True
```

### Why One Byte Changes the Entire Hash

SHA-256 has a property called the avalanche effect.

This means a very small change in the input creates a very large and unpredictable change in the output hash.

For example, changing one byte in a PCAP file causes the SHA-256 hash to become completely different.

This is why hashing is very useful in digital forensics.

---

## 7. Merkle Tree Demonstration

A Merkle Tree is a tree structure made from hashes.

In this project, the leaf hashes are the SHA-256 hashes of the PCAP files.

### Merkle Tree Structure

The bottom level contains the evidence hashes:

```text
Hash 1   Hash 2   Hash 3   Hash 4   Hash 5
```

Then pairs of hashes are combined and hashed again to create parent hashes.

This process continues until one final hash remains.

That final hash is called the Merkle Root.

### Merkle Root

The Merkle Root is one hash that represents all evidence files.

If one evidence file changes, its leaf hash changes.

Then its parent hash changes.

Finally, the Merkle Root changes.

### Why Merkle Trees Are Used in Blockchain

Merkle Trees are used in Bitcoin and other blockchain systems because they make verification efficient.

Instead of checking every transaction or evidence item one by one, a system can use the Merkle Root and a small number of hashes to prove that a specific item belongs to the full data set.

---

## 8. Final Report Generation

The program automatically creates the final report.

The report is saved as:

```text
report/final_report.md
```

The report includes:

- Total evidence files
- Total blocks
- SHA-256 results
- Blockchain block information
- Merkle Tree levels
- Merkle Root
- Tampering detection results
- Validation results

This report can be submitted as part of the assignment documentation.

---

## 9. GitHub Repository Setup

The required repository structure is:

```text
NIM_Name/
├── evidence/
├── sourcecode/
├── screenshot/
├── report/
└── README.md
```

### Folder Explanation

#### evidence/

This folder stores the PCAP evidence files.

The files are:

```text
PCAP01.pcap
PCAP02.pcap
PCAP03.pcap
PCAP04.pcap
PCAP05.pcap
```

#### sourcecode/

This folder stores the Python source code.

The main file is:

```text
main.py
```

#### screenshot/

This folder stores screenshots for the assignment report or presentation.


#### report/

This folder stores the final written report.

The generated report is:

```text
final_report.md
```

#### README.md

This file explains the project, how to run it, and what features are included.

Before submission, rename `NIM_Name` using the student’s real NIM and name.

---

## 10. Presentation and Viva Preparation

During the lecturer presentation, explain the project in this order:

### Step 1: Introduce the Problem

Explain that digital forensic evidence must remain unchanged.

If evidence is modified, investigators must be able to detect it.

### Step 2: Explain PCAP Evidence

Explain that PCAP files store captured network packets.

In this project, each PCAP file is treated as one evidence item.

### Step 3: Explain SHA-256

Explain that SHA-256 creates a unique digital fingerprint of each file.

If the file changes, the hash changes.

### Step 4: Explain Blockchain

Explain that the blockchain stores evidence hashes inside linked blocks.

Each block stores the hash of the previous block.

This creates a chain.

### Step 5: Show Valid Blockchain

Run the program and show:

```text
Blockchain Validation: VALID
```

Explain that this means the evidence files still match the hashes stored in the blockchain.

### Step 6: Show Merkle Tree

Explain that the Merkle Root summarizes all evidence hashes.

If any evidence hash changes, the Merkle Root will also change.

### Step 7: Show Tampering Attack

Show that the program modifies one byte in a PCAP file.

Then show:

```text
Tampering detected: True
Blockchain Validation: INVALID
```

Explain that the blockchain detected the evidence modification.

### Step 8: Conclude

Conclude that the project demonstrates how hashing and blockchain can help preserve digital evidence integrity and chain of custody.

---

## Possible Viva Questions and Answers

### What is SHA-256?

SHA-256 is a cryptographic hash function that produces a 256-bit hash value. It is used to create a digital fingerprint of data.

### Why is hashing important in digital forensics?

Hashing is important because it helps prove whether evidence has changed. If the hash before and after analysis is the same, the evidence is still intact.

### What is a genesis block?

The genesis block is the first block in a blockchain. It starts the chain and does not have a normal previous block.

### Why does each block store the previous hash?

Each block stores the previous hash to link the blocks together. If one block changes, the link breaks and tampering can be detected.

### What is chain of custody?

Chain of custody is the documented history of evidence handling, from collection to analysis and presentation in court or academic investigation.

### Why does changing one byte change the full SHA-256 hash?

Because SHA-256 has the avalanche effect. A tiny input change creates a completely different output hash.

### What is a Merkle Root?

A Merkle Root is the final hash at the top of a Merkle Tree. It summarizes all the hashes below it.

### Which parts are mandatory?

The mandatory parts are PCAP files, SHA-256 hashing, blockchain simulation, validation, report generation, and repository structure.

### Which parts are bonus?

The bonus parts are tampering simulation and Merkle Tree implementation.
```