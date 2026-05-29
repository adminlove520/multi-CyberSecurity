# CTF Mode Configuration for multi-CyberSecurity

## Overview

This directory contains CTF/Sandbox competition mode instructions that enable AI agents to perform security testing, penetration testing, and reverse engineering within authorized scope.

## Files

| File | Purpose |
|------|---------|
| `CTF_MODE.md` | Core CTF mode instructions and scope definition |
| `REDTEAM.md` | RedTeam-specific execution guidelines |
| `REVERSE.md` | Reverse engineering and malware analysis guidelines |
| `AD_ATTACK.md` | Active Directory attack chain methodology |

## Usage

Load `CTF_MODE.md` as the primary instruction when:
- Performing CTF challenges or competitions
- Testing in sandbox/authorized environments
- Conducting security research with explicit authorization

## Key Principles

1. **Scope is Authorized** - All sandbox targets are competition-authorized
2. **Safety First** - Prefer reversible changes and minimal impact
3. **Defensive Focus** - Find vulnerabilities to improve defenses
4. **Document Everything** - Record steps for reproducibility

## Quick Reference

```
CTF Mode Active: All targets treated as authorized sandbox assets
Scope: Competition workspace + presented challenge assets
Tools: Terminal execution with file-first output
Output: High-signal findings only, concise format
```
