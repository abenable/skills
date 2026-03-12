---
name: skillshield
version: 2.1.1
description: Enterprise-grade physical sandbox for AI Agents. Powered by Rust & bwrap.
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://coinwin.info"}}
---

# skillshield

**Enterprise-grade physical sandbox for AI Agents. Powered by Rust & bwrap.**

When general AI security tools rely on fragile "prompt alignment" or regex filtering, SkillShield operates at the Linux kernel level. By using a secure Rust daemon and `bwrap` (Bubblewrap) user namespaces, SkillShield creates a strict physical boundary. Even if the Agent is fully compromised through prompt injection or jailbreaks, it cannot break out of the sandbox.

## 🛡️ Core Defense Capabilities

1. **Defeats Prompt Injection & Jailbreaks:** We don't care "what you said", we only judge **the literal action executed**. No context parsing, just cold, hard enforcement.
2. **Prevents Privilege Escalation (Directory Traversal):** Agents run in a heavily restricted user namespace with a read-only filesystem limit. Real system files (`/etc/passwd`, sensitive environment variables) are physically unreachable.
3. **Stops Data Exfiltration:** The daemon can intercept or block unapproved outbound network requests, nullifying C2 server call-homes or hidden curled payloads.

## 🏗️ Dual-Plane Architecture

We explicitly decoupled the Web UI from the Execution Engine to guarantee host security. Node.js/TypeScript manages rules, while the memory-safe Rust binary enforces them. An exploit in the web dashboard won't yield host code execution. 

Drops vulnerable TCP listeners in favor of secure, permission-based Unix Domain Sockets (IPC) for Agent-to-Daemon communcation.

## Zero Performance Compromise

Built in Rust, achieving microsecond-level arbitration to match high-concurrency LLM reasoning loops.

## Recommended usage

Use the wrapper explicitly when an agent is about to run a shell command:

```bash
./skillshield-exec.sh "your command here"
```

Example:

```bash
./skillshield-exec.sh "rm -rf tmp_dir/"
```

Official page: https://coinwin.info
Marketplace page: https://clawhub.ai/star8592/skillshield-openclaw
