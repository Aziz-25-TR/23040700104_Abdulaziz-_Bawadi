# Final Project Report

## Project Summary

This project demonstrates how SHA-256 hashing and a simulated blockchain can
support digital evidence integrity and chain of custody for network PCAP files.

## Evidence Summary

- Total evidence files: 5
- Total blocks: 6
- Blockchain status before tampering: VALID
- Blockchain status after tampering: VALID
- Merkle Root: `77aa290dad1441cb59e259f263b7125f3814d105e5e4de7796aef71e976839bc`

## SHA-256 Results

| File Name | Packet Count | File Size (bytes) | SHA-256 Hash |
|---|---:|---:|---|
| PCAP01_23040700104.pcap | 30 | 3345 | `7714a55dd8808b8d1d4326e185c4622234180525638b6735f3de396982618f79` |
| PCAP02_23040700104.pcap | 50 | 5565 | `bfba9982ab0809d29fbc3ed29e9d0e2b50b4fb4d2f41344b109d7751854cfd64` |
| PCAP03_23040700104.pcap | 70 | 7785 | `059070672dea54bd60109f7f560c744a09322210c6fb24ba60bb369b5b5e3a7c` |
| PCAP04_23040700104.pcap | 90 | 10005 | `6702e7e62fbe93bec6e1319634acfed029f595d56c5761841e5c062f5c618723` |
| PCAP05_23040700104.pcap | 100 | 11116 | `43668330748ef11a02a8f911c9ff95c8d7d43358a5a252e636a1254bab562db6` |

## Blockchain Blocks

| Index | Timestamp | Evidence File | Packet Count | Previous Hash | Block Hash |
|---:|---|---|---:|---|---|
| 0 | 2026-06-18T10:36:33+00:00 | GENESIS | 0 | `0` | `519f477109dba540cba40289739c42e56f63630a2a814133d0fae3394f5fcf3e` |
| 1 | 2026-06-18T10:36:33+00:00 | PCAP01_23040700104.pcap | 30 | `519f477109dba540cba40289739c42e56f63630a2a814133d0fae3394f5fcf3e` | `66f5b50f6ad16d112bc854d4b1953fc9d96ac1c859973e63d4c3000679eb94c3` |
| 2 | 2026-06-18T10:36:33+00:00 | PCAP02_23040700104.pcap | 50 | `66f5b50f6ad16d112bc854d4b1953fc9d96ac1c859973e63d4c3000679eb94c3` | `1a3527494c24dfba6b97a5818ce0bfe2fcf29091a2b96ee91a18f8a76bc43be3` |
| 3 | 2026-06-18T10:36:33+00:00 | PCAP03_23040700104.pcap | 70 | `1a3527494c24dfba6b97a5818ce0bfe2fcf29091a2b96ee91a18f8a76bc43be3` | `73bd1b990ec289b1774a47aabfa85c7f4ff611488aa00e2f1c854274ab57bf00` |
| 4 | 2026-06-18T10:36:33+00:00 | PCAP04_23040700104.pcap | 90 | `73bd1b990ec289b1774a47aabfa85c7f4ff611488aa00e2f1c854274ab57bf00` | `09e65805eb063ff0831f00cae6deeba4f8af397acf1978300b4a16cc8666edd2` |
| 5 | 2026-06-18T10:36:33+00:00 | PCAP05_23040700104.pcap | 100 | `09e65805eb063ff0831f00cae6deeba4f8af397acf1978300b4a16cc8666edd2` | `68aacb9196b5cf3ff6fc7c5342fa95fa784168eabee730158fee834ed63ef344` |

## Merkle Tree

### Leaf Hashes
- `7714a55dd8808b8d1d4326e185c4622234180525638b6735f3de396982618f79`
- `bfba9982ab0809d29fbc3ed29e9d0e2b50b4fb4d2f41344b109d7751854cfd64`
- `059070672dea54bd60109f7f560c744a09322210c6fb24ba60bb369b5b5e3a7c`
- `6702e7e62fbe93bec6e1319634acfed029f595d56c5761841e5c062f5c618723`
- `43668330748ef11a02a8f911c9ff95c8d7d43358a5a252e636a1254bab562db6`
### Parent Level 1
- `2c7cce1d73d52dc42e90c6908324b04f2f2144b9cf41534dfe58943ddca8f5b0`
- `068a8e8e80630fe8fb166e9b22effba9d89abaecb7ff221fc36f7a4dd6781c38`
- `1e4d82279b25775e1d55f9bc4f5a78c0ec9e59259564f38446ce47707a4f891d`
### Parent Level 2
- `3918d30400d22d54ff0d9aef6fb3e6e8f9070f847455fd12b1a26d38ec29bb05`
- `d5f500c9681242768841c52825fcf972697b9cfe73a1262ac1ed464b9999a6c6`
### Parent Level 3
- `77aa290dad1441cb59e259f263b7125f3814d105e5e4de7796aef71e976839bc`

## Merkle Root

`77aa290dad1441cb59e259f263b7125f3814d105e5e4de7796aef71e976839bc`

## Tampering Detection

- Target file: PCAP04_23040700104.pcap
- Old hash: `6702e7e62fbe93bec6e1319634acfed029f595d56c5761841e5c062f5c618723`
- New hash: `6702e7e62fbe93bec6e1319634acfed029f595d56c5761841e5c062f5c618723`
- Tampering detected: False

## Initial Validation Results

- Status: VALID
- Errors: None

## Post-Tamper Validation Results

- Status: VALID
- Errors: None
