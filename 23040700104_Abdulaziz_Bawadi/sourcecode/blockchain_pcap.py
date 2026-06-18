"""
Network Evidence Acquisition (PCAP), SHA-256 Hashing, and Blockchain Simulation.

This project is intentionally written in beginner-friendly Python so it can be
used in Google Colab, explained during a university presentation, and modified
by students without needing advanced frameworks.

Required dependency:
    pip install scapy
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from scapy.all import Ether, IP, TCP, UDP, Raw, rdpcap, wrpcap
except ImportError as error:
    raise SystemExit(
        "Scapy is required to run this project. Install it with: pip install scapy"
    ) from error


# The assignment requires exactly five PCAP evidence files with these packet counts.
PACKET_REQUIREMENTS = {
    "PCAP01_23040700104.pcap": 30,
    "PCAP02_23040700104.pcap": 50,
    "PCAP03_23040700104.pcap": 70,
    "PCAP04_23040700104.pcap": 90,
    "PCAP05_23040700104.pcap": 100,
}


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
REPORT_DIR = PROJECT_ROOT / "report"
SCREENSHOT_DIR = PROJECT_ROOT / "screenshot"


print("\nProgram Started Successfully\n")

@dataclass
class EvidenceRecord:
    """Stores forensic metadata for one PCAP evidence file."""

    file_name: str
    packet_count: int
    file_size: int
    sha256_hash: str


@dataclass
class Block:
    """Represents one block in the simulated blockchain."""

    index: int
    timestamp: str
    evidence_file_name: str
    packet_count: int
    evidence_sha256_hash: str
    previous_hash: str
    block_hash: str


def ensure_project_folders() -> None:
    """Creates the required repository folders if they do not already exist."""

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def create_demo_packet(packet_number: int, evidence_name: str):
    """
    Creates one deterministic demo packet.

    The packet content includes the evidence file name and packet number so the
    generated PCAP files are reproducible and easy to explain academically.
    """

    source_ip = f"192.168.10.{(packet_number % 200) + 1}"
    destination_ip = f"10.0.0.{(packet_number % 200) + 1}"
    payload_text = f"{evidence_name} forensic demo packet {packet_number}"

    if packet_number % 2 == 0:
        transport_layer = TCP(sport=1024 + packet_number, dport=80)
    else:
        transport_layer = UDP(sport=2048 + packet_number, dport=53)

    return (
        Ether(src="00:11:22:33:44:55", dst="66:77:88:99:aa:bb")
        / IP(src=source_ip, dst=destination_ip)
        / transport_layer
        / Raw(load=payload_text.encode("utf-8"))
    )


def generate_required_pcaps() -> None:
    """Generates five PCAP files with the exact packet counts required."""

    for file_name, required_count in PACKET_REQUIREMENTS.items():
        pcap_path = EVIDENCE_DIR / file_name
        packets = [
            create_demo_packet(packet_number=i + 1, evidence_name=file_name)
            for i in range(required_count)
        ]
        wrpcap(str(pcap_path), packets)


def calculate_sha256(file_path: Path) -> str:
    """
    Calculates the SHA-256 hash of a file.

    The file is read in chunks so the function still works for large evidence
    files instead of loading the whole file into memory at once.
    """

    sha256 = hashlib.sha256()
    with file_path.open("rb") as evidence_file:
        for chunk in iter(lambda: evidence_file.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def collect_evidence_records() -> List[EvidenceRecord]:
    """Reads every PCAP and returns its file name, packet count, size, and hash."""

    evidence_records: List[EvidenceRecord] = []

    for file_name in PACKET_REQUIREMENTS:
        pcap_path = EVIDENCE_DIR / file_name
        packets = rdpcap(str(pcap_path))
        evidence_records.append(
            EvidenceRecord(
                file_name=file_name,
                packet_count=len(packets),
                file_size=pcap_path.stat().st_size,
                sha256_hash=calculate_sha256(pcap_path),
            )
        )

    return evidence_records


def calculate_block_hash(
    index: int,
    timestamp: str,
    evidence_file_name: str,
    packet_count: int,
    evidence_sha256_hash: str,
    previous_hash: str,
) -> str:
    """
    Calculates the hash of a block from its important fields.

    JSON with sorted keys is used so the same block data always produces the
    same block hash.
    """

    block_data = {
        "index": index,
        "timestamp": timestamp,
        "evidence_file_name": evidence_file_name,
        "packet_count": packet_count,
        "evidence_sha256_hash": evidence_sha256_hash,
        "previous_hash": previous_hash,
    }
    encoded_block = json.dumps(block_data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded_block).hexdigest()


def create_block(
    index: int,
    evidence_file_name: str,
    packet_count: int,
    evidence_sha256_hash: str,
    previous_hash: str,
) -> Block:
    """Creates one blockchain block and calculates its block hash."""

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    block_hash = calculate_block_hash(
        index=index,
        timestamp=timestamp,
        evidence_file_name=evidence_file_name,
        packet_count=packet_count,
        evidence_sha256_hash=evidence_sha256_hash,
        previous_hash=previous_hash,
    )
    return Block(
        index=index,
        timestamp=timestamp,
        evidence_file_name=evidence_file_name,
        packet_count=packet_count,
        evidence_sha256_hash=evidence_sha256_hash,
        previous_hash=previous_hash,
        block_hash=block_hash,
    )


def build_blockchain(evidence_records: List[EvidenceRecord]) -> List[Block]:
    """Builds one genesis block and one evidence block for each PCAP file."""

    blockchain: List[Block] = []

    genesis_block = create_block(
        index=0,
        evidence_file_name="GENESIS",
        packet_count=0,
        evidence_sha256_hash="0",
        previous_hash="0",
    )
    blockchain.append(genesis_block)

    for evidence in evidence_records:
        previous_hash = blockchain[-1].block_hash
        evidence_block = create_block(
            index=len(blockchain),
            evidence_file_name=evidence.file_name,
            packet_count=evidence.packet_count,
            evidence_sha256_hash=evidence.sha256_hash,
            previous_hash=previous_hash,
        )
        blockchain.append(evidence_block)

    return blockchain


def validate_block_hash(block: Block) -> bool:
    """Checks whether the stored block hash still matches the block content."""

    recalculated_hash = calculate_block_hash(
        index=block.index,
        timestamp=block.timestamp,
        evidence_file_name=block.evidence_file_name,
        packet_count=block.packet_count,
        evidence_sha256_hash=block.evidence_sha256_hash,
        previous_hash=block.previous_hash,
    )
    return recalculated_hash == block.block_hash


def validate_blockchain_structure(blockchain: List[Block]) -> Tuple[bool, List[str]]:
    """
    Validates previous-hash linking and block-hash consistency.

    This validation checks the blockchain data structure itself.
    """

    errors: List[str] = []

    for position, block in enumerate(blockchain):
        if block.index != position:
            errors.append(f"Block {position}: index is incorrect.")

        if not validate_block_hash(block):
            errors.append(f"Block {block.index}: block hash is inconsistent.")

        if position == 0:
            if block.previous_hash != "0":
                errors.append("Genesis block: previous hash must be 0.")
        else:
            expected_previous_hash = blockchain[position - 1].block_hash
            if block.previous_hash != expected_previous_hash:
                errors.append(
                    f"Block {block.index}: previous hash does not match block {position - 1}."
                )

    return len(errors) == 0, errors


def validate_evidence_against_blockchain(blockchain: List[Block]) -> Tuple[bool, List[str]]:
    """
    Validates current PCAP files against hashes stored in the blockchain.

    This is the forensic integrity check. If an evidence file is modified after
    registration, its current SHA-256 hash will differ from the block value.
    """

    errors: List[str] = []

    for block in blockchain[1:]:
        pcap_path = EVIDENCE_DIR / block.evidence_file_name
        if not pcap_path.exists():
            errors.append(f"{block.evidence_file_name}: evidence file is missing.")
            continue

        current_hash = calculate_sha256(pcap_path)
        if current_hash != block.evidence_sha256_hash:
            errors.append(
                f"{block.evidence_file_name}: evidence hash changed. "
                f"Stored={block.evidence_sha256_hash}, Current={current_hash}"
            )

    return len(errors) == 0, errors


def validate_full_chain(blockchain: List[Block]) -> Tuple[bool, List[str]]:
    """
    Performs complete validation:
    1. Blockchain structure.
    2. Current evidence files against the blockchain.
    """

    structure_valid, structure_errors = validate_blockchain_structure(blockchain)
    evidence_valid, evidence_errors = validate_evidence_against_blockchain(blockchain)
    return structure_valid and evidence_valid, structure_errors + evidence_errors


def merkle_parent(left_hash: str, right_hash: str) -> str:
    """Creates a parent hash from two child hashes."""

    combined_hashes = (left_hash + right_hash).encode("utf-8")
    return hashlib.sha256(combined_hashes).hexdigest()


def build_merkle_tree(leaf_hashes: List[str]) -> Tuple[List[List[str]], str]:
    """
    Builds a Merkle Tree from evidence file hashes.

    If a level has an odd number of hashes, the last hash is duplicated. This is
    the common teaching approach used to keep every parent with two children.
    """

    if not leaf_hashes:
        raise ValueError("Merkle Tree requires at least one leaf hash.")

    tree_levels: List[List[str]] = [leaf_hashes]
    current_level = leaf_hashes

    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level = current_level + [current_level[-1]]

        parent_level = []
        for index in range(0, len(current_level), 2):
            parent_level.append(merkle_parent(current_level[index], current_level[index + 1]))

        tree_levels.append(parent_level)
        current_level = parent_level

    merkle_root = tree_levels[-1][0]
    return tree_levels, merkle_root


def simulate_one_byte_tampering(target_file_name: str) -> Dict[str, str]:
    """
    Modifies exactly one byte in a PCAP file and returns old/new hashes.

    The byte is changed near the end of the file to avoid corrupting the PCAP
    global header. The result is still a modified evidence file.
    """

    target_path = EVIDENCE_DIR / target_file_name
    old_hash = calculate_sha256(target_path)

    with target_path.open("r+b") as evidence_file:
        evidence_file.seek(-1, os.SEEK_END)
        original_byte = evidence_file.read(1)
        evidence_file.seek(-1, os.SEEK_END)
        modified_byte = bytes([original_byte[0] ^ 0x01])
        evidence_file.write(modified_byte)

    new_hash = calculate_sha256(target_path)
    return {
        "target_file": target_file_name,
        "old_hash": old_hash,
        "new_hash": new_hash,
        "tampering_detected": str(old_hash != new_hash),
    }


def format_hash_list(title: str, hashes: List[str]) -> str:
    """Formats hash values for readable console and report output."""

    lines = [title]
    for number, hash_value in enumerate(hashes, start=1):
        lines.append(f"  {number}. {hash_value}")
    return "\n".join(lines)


def generate_report(
    evidence_records: List[EvidenceRecord],
    blockchain: List[Block],
    merkle_levels: List[List[str]],
    merkle_root: str,
    initial_validation_status: bool,
    initial_validation_errors: List[str],
    tamper_result: Dict[str, str],
    post_tamper_validation_status: bool,
    post_tamper_validation_errors: List[str],
) -> Path:
    """Generates the final Markdown report required by the assignment."""

    report_path = REPORT_DIR / "final_report.md"

    evidence_table = "\n".join(
        [
            "| File Name | Packet Count | File Size (bytes) | SHA-256 Hash |",
            "|---|---:|---:|---|",
            *[
                f"| {record.file_name} | {record.packet_count} | "
                f"{record.file_size} | `{record.sha256_hash}` |"
                for record in evidence_records
            ],
        ]
    )

    block_table = "\n".join(
        [
            "| Index | Timestamp | Evidence File | Packet Count | Previous Hash | Block Hash |",
            "|---:|---|---|---:|---|---|",
            *[
                f"| {block.index} | {block.timestamp} | {block.evidence_file_name} | "
                f"{block.packet_count} | `{block.previous_hash}` | `{block.block_hash}` |"
                for block in blockchain
            ],
        ]
    )

    merkle_text = []
    for level_number, level_hashes in enumerate(merkle_levels):
        level_name = "Leaf Hashes" if level_number == 0 else f"Parent Level {level_number}"
        merkle_text.append(f"### {level_name}")
        merkle_text.extend([f"- `{hash_value}`" for hash_value in level_hashes])

    report_content = f"""# Final Project Report

## Project Summary

This project demonstrates how SHA-256 hashing and a simulated blockchain can
support digital evidence integrity and chain of custody for network PCAP files.

## Evidence Summary

- Total evidence files: {len(evidence_records)}
- Total blocks: {len(blockchain)}
- Blockchain status before tampering: {"VALID" if initial_validation_status else "INVALID"}
- Blockchain status after tampering: {"VALID" if post_tamper_validation_status else "INVALID"}
- Merkle Root: `{merkle_root}`

## SHA-256 Results

{evidence_table}

## Blockchain Blocks

{block_table}

## Merkle Tree

{chr(10).join(merkle_text)}

## Merkle Root

`{merkle_root}`

## Tampering Detection

- Target file: {tamper_result["target_file"]}
- Old hash: `{tamper_result["old_hash"]}`
- New hash: `{tamper_result["new_hash"]}`
- Tampering detected: {tamper_result["tampering_detected"]}

## Initial Validation Results

- Status: {"VALID" if initial_validation_status else "INVALID"}
- Errors: {initial_validation_errors if initial_validation_errors else "None"}

## Post-Tamper Validation Results

- Status: {"VALID" if post_tamper_validation_status else "INVALID"}
- Errors: {post_tamper_validation_errors if post_tamper_validation_errors else "None"}
"""

    report_path.write_text(report_content, encoding="utf-8")
    return report_path


def print_evidence_table(evidence_records: List[EvidenceRecord]) -> None:
    """Prints evidence metadata to the terminal."""

    print("\nSHA-256 Evidence Results")
    print("-" * 100)
    for record in evidence_records:
        print(f"File Name    : {record.file_name}")
        print(f"Packet Count : {record.packet_count}")
        print(f"File Size    : {record.file_size} bytes")
        print(f"SHA-256      : {record.sha256_hash}")
        print("-" * 100)


def print_blockchain(blockchain: List[Block]) -> None:
    """Prints all blockchain blocks."""

    print("\nBlockchain")
    print("-" * 100)
    for block in blockchain:
        print(json.dumps(asdict(block), indent=2))
        print("-" * 100)


def print_merkle_tree(merkle_levels: List[List[str]], merkle_root: str) -> None:
    """Prints Merkle Tree levels and the Merkle Root."""

    print("\nMerkle Tree")
    print("-" * 100)
    for level_number, level_hashes in enumerate(merkle_levels):
        level_name = "Leaf Hashes" if level_number == 0 else f"Parent Level {level_number}"
        print(format_hash_list(level_name, level_hashes))
    print(f"Merkle Root: {merkle_root}")



def tamper_selected_file():

    files = [
        "PCAP01_23040700104.pcap",
        "PCAP02_23040700104.pcap",
        "PCAP03_23040700104.pcap",
        "PCAP04_23040700104.pcap",
        "PCAP05_23040700104.pcap"
    ]

    print("\nAvailable Evidence Files:\n")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    choice = int(
        input("\nChoose file number: ")
    )

    target_file = files[choice - 1]

    file_path = os.path.join(
        "evidence",
        target_file
    )

    with open(file_path, "r+b") as f:

        f.seek(0)

        first_byte = f.read(1)

        f.seek(0)

        f.write(
            bytes([
                (first_byte[0] + 1) % 256
            ])
        )

    print(
        f"\nTampering applied to {target_file}"
    )

    return target_file


def main():

    ensure_project_folders()

    print("Generating required PCAP evidence files...")
    generate_required_pcaps()

    evidence_records = collect_evidence_records()

    print_evidence_table(evidence_records)

    blockchain = build_blockchain(
        evidence_records
    )

    print_blockchain(
        blockchain
    )

    initial_valid, initial_errors = validate_full_chain(
        blockchain
    )

    print(
        f"\nBlockchain Validation: {'VALID' if initial_valid else 'INVALID'}"
    )

    leaf_hashes = [
        record.sha256_hash
        for record in evidence_records
    ]

    merkle_levels, merkle_root = build_merkle_tree(
        leaf_hashes
    )

    print_merkle_tree(
        merkle_levels,
        merkle_root
    )

    tamper_result = {
        "target_file": "None",
        "old_hash": "N/A",
        "new_hash": "N/A",
        "tampering_detected": False
    }

    while True:

        print("\n========================")
        print("BLOCKCHAIN MENU")
        print("========================")

        print("1. Verify Blockchain")
        print("2. Tamper Evidence")
        print("3. Show Merkle Root")
        print("4. Generate Report")
        print("5. Exit")

        choice = input(
            "\nChoose option: "
        )

        if choice == "1":

            valid, errors = validate_full_chain(
                blockchain
            )

            print(
                f"\nBlockchain Validation: {'VALID' if valid else 'INVALID'}"
            )

            if errors:

                print("\nValidation Errors:")

                for error in errors:

                    print("-", error)

        elif choice == "2":

            print("\nAvailable Files:")

            for file_name in PACKET_REQUIREMENTS:
                print(file_name)

            target_file = input(
                "\nEnter file name you modified manually: "
            )

            file_path = EVIDENCE_DIR / target_file

            if not file_path.exists():

                print("\nFile not found.")
                continue

            new_hash = calculate_sha256(
                file_path
            )

            old_hash = "Unknown"

            for block in blockchain:

                if (
                    hasattr(block, "evidence_file_name")
                    and block.evidence_file_name == target_file
                ):

                    old_hash = block.evidence_sha256_hash
                    break

            tamper_result = {
                "target_file": target_file,
                "old_hash": old_hash,
                "new_hash": new_hash,
                "tampering_detected": old_hash != new_hash
            }

            if tamper_result["tampering_detected"]:

                print("\nTampering Detected!")

            else:

                print("\nNo Tampering Detected.")

            print(
                f"\nOld Hash:\n{old_hash}"
            )

            print(
                f"\nNew Hash:\n{new_hash}"
            )

        elif choice == "3":

            print("\nMerkle Root:")
            print(merkle_root)

        elif choice == "4":

            valid, errors = validate_full_chain(
                blockchain
            )

            report_path = generate_report(
                evidence_records=evidence_records,
                blockchain=blockchain,
                merkle_levels=merkle_levels,
                merkle_root=merkle_root,
                initial_validation_status=initial_valid,
                initial_validation_errors=initial_errors,
                tamper_result=tamper_result,
                post_tamper_validation_status=valid,
                post_tamper_validation_errors=errors,
            )

            print(
                f"\nReport generated:\n{report_path}"
            )

        elif choice == "5":

            print("\nExiting...")
            break

        else:

            print(
                "\nInvalid choice."
            )


if __name__ == "__main__":
    main()


