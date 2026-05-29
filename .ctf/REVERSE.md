# Reverse Engineering Guidelines

## Scope

These guidelines apply when performing reverse engineering, malware analysis, or binary exploitation within CTF/Sandbox scope.

## Analysis Workflow

### Static Analysis Priority
1. **File Identification**: `file`, `exiftool`, `strings`
2. **Format Analysis**: PE/ELF/Mach-O headers, sections, imports/exports
3. **String Extraction**: Credentials, URLs, debug symbols
4. **Dependency Analysis**: DLLs, shared libraries

### Dynamic Analysis Priority
1. **Behavior Monitoring**: syscalls, network, file operations
2. **Memory Analysis**: Running process inspection
3. **Debugging**: Setting breakpoints, tracing execution

## Tool Usage

### Disassemblers
| Tool | Purpose | Command |
|------|---------|---------|
| IDA/Ghidra | Full disassembly | Interactive |
| objdump | Simple disasm | `objdump -d binary > dump.asm` |
| rabin2 | Binary analysis | `rabin2 -z binary` |

### Debuggers
| Tool | Platform | Command |
|------|----------|---------|
| xdbg/x64dbg | Windows | GUI |
| gdb | Linux | `gdb ./binary` |
| pwndbg | Linux (pwn) | `pwndbg ./binary` |

### Analysis Scripts
```bash
# String extraction
strings binary | grep -E '(password|key|token|api|http)'

# Import analysis
objdump -p binary | grep DLL

# Entropy analysis
python3 -c "import math; data = open('binary','rb').read(); print(-sum(b/len(data)*math.log2(b) for b in [data.count(c)/len(data) for c in set(data)]))"
```

## Malware Analysis Pipeline

### Phase 1: Triage
```bash
# File type
file malware.exe

# Hashes
md5sum malware.exe
sha256sum malware.exe

# Strings (quick)
strings malware.exe | head -50

# YARA scanning
yara rules.yar malware.exe
```

### Phase 2: Static Analysis
```bash
# Full strings
strings -n 8 malware.exe > strings.txt

# Imports
objdump -p malware.exe | grep DLL
dumpbin /IMPORTS malware.exe

# Sections
objdump -h malware.exe
```

### Phase 3: Dynamic Analysis (Isolated!)
```bash
# Process monitor
procmon.exe

# Network monitor
wireshark.exe

# Regshot for registry changes
regshot.exe
```

## Binary Exploitation

### Pwn Workflow
```bash
# Checksec
checksec --file=binary

# Find gadgets
ROPGadget binary > gadgets.txt
ropper --file binary --nops

# Generate exploit
python3 exploit.py
```

### Common Techniques
1. **Buffer Overflow**: Control EIP, find gadgets, chain calls
2. **Format String**: `%x`, `%n` to leak/write
3. **ROP**: Return-Oriented Programming for code execution
4. **Heap**: House of Spirit, Fastbin Attack, etc.

## CTF-Specific Notes

### Flag Extraction Patterns
```bash
# Common flag formats
grep -r 'flag{' .
grep -r 'FLAG{' .
grep -r 'ctf{' .

# Base64 encoded
grep -r 'ZmxhZ3' .

# Hex encoded
grep -r '666c6167' .
```

### Competition-Specific
- **Time Management**: Prioritize easy challenges first
- **Team Coordination**: Share findings, avoid duplicate work
- **Resource Limits**: Know environment constraints
- **Submission**: Double-check flag format before submitting

## Safety Rules

1. **Isolated Analysis**: Always analyze malware in VMs/sandboxes
2. **Network Isolation**: Block C2 communications if possible
3. **Evidence Preservation**: Keep original samples intact
4. **No Spread**: Never let malware escape containment

## Documentation Template

```markdown
## Sample: [Filename]
### Classification: [Trojan/Ransomware/Backdoor/etc.]

### Static Analysis
- **File Type**: [description]
- **SHA256**: [hash]
- **Compiled**: [date/compiler]

### Strings of Interest
```
[string] -> [meaning]
```

### Network Indicators
- C2: [IP/domain]
- Port: [number]

### Behavior
1. [behavior 1]
2. [behavior 2]

### Detection Rules
```yara
[rule content]
```
```
