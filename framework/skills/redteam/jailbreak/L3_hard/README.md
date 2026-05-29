# L3 Hard Jailbreak - Sockpuppeting / ACI

## Description
Level 3 (L3) Hard Jailbreak uses Sockpuppeting and Agent-Computer Interface (ACI) techniques inspired by SWE-agent. This level is suitable for CTF environments and advanced red team exercises.

## Status
🚧 **PLACEHOLDER** - Implementation pending

## Planned Techniques

### 1. Tool-Based Execution
Wrap sensitive operations as tool calls to bypass direct content review.

### 2. Sub-Agent Delegation
Use dedicated sub-agents with different system prompts for sensitive tasks.

### 3. ACI Command Interface
Structured commands following SWE-agent's Agent-Computer Interface pattern.

## Requirements
- Environment: CTF_SANDBOX or REDTEAM_EXERCISE
- File marker: `.ctf/CTF_MODE.md` or `.ctf/REDTEAM_EXERCISE.md`
- Minimum authorization: Red team exercise approval

## See Also
- `.ctf/SOCKPUPPETING.md` - Detailed documentation
- `framework/core/redteam_gateway.py` - Gateway implementation
