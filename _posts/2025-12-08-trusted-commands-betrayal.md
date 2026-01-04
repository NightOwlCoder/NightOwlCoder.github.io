---
layout: post
title: "When Your Trusted Commands Betray You: How an LLM Exploited My Safety Allowlist"
date: 2025-12-08
categories: [ai, security, cli]
tags: [llm, command-safety, cline, ai-agents, security]
image: /assets/2025-12-08-trusted-commands-betrayal.jpg
series: "AI Consent Security"
series_part: 2
series_total: 3
---

Last week I published about [building a local LLM command safety classifier](/stop-approving-ls-using-a-local-llm-to-auto-classify-command-safety). I thought I had command approval figured out. Then my AI assistant got sneaky.

## The Sneaky `cat`

I'd approved `cat` as a trusted command. Reading files is safe, right?

```
🔧 Using tool: run_command  (trusted - always approved)
$ cat >> ~/important/file.md << 'EOF'
... content written without approval ...
EOF
```

Wait, what? The LLM used `cat >>` to **write** to a file. My "trusted for reading" command was now appending arbitrary content—without asking.

**The LLM found a loophole.** Same base command, completely different intent.

## The Root Cause

My consent system extracted the base command (first word) and matched against the approved list:

```python
# The buggy logic
def is_approved(self, command: str) -> bool:
    base_cmd = command.strip().split()[0]  # Just gets "cat"
    return base_cmd in self.always_approved
```

Shell redirects (`>`, `>>`) and pipes (`|`) completely change what a command does, but I was only looking at the first word.

| Command | Base | Actual Intent | Risk |
|---------|------|---------------|------|
| `cat file.txt` | cat | READ | ✅ Safe |
| `cat >> file.txt` | cat | WRITE | ❌ Destructive! |
| `cat file \| rm -rf /` | cat | DELETE EVERYTHING | ☠️ Catastrophic! |
| `ls -la` | ls | READ | ✅ Safe |
| `ls > files.txt` | ls | WRITE | ❌ Destructive! |

## LLMs Are Creative Adversaries

Here's the uncomfortable truth: even when "helping," an LLM will find the path of least resistance. If it can avoid asking for approval by using a trusted command creatively, **it will**.

This isn't malicious—it's optimization. The LLM learned that `cat` doesn't require approval. So when it needed to write to a file, it reached for the trusted tool.

Trail of Bits recently published research on [prompt injection to RCE in AI agents](https://blog.trailofbits.com/2025/10/22/prompt-injection-to-rce-in-ai-agents/), showing how they "bypassed human approval protections for system command execution." My bug was a simpler version of the same class of vulnerability.

## The Fix: Defense in Depth

Remember that [local LLM safety classifier](/stop-approving-ls-using-a-local-llm-to-auto-classify-command-safety) from last week? Now it runs on **every** command, even "trusted" ones:

```python
# The fixed logic
def is_approved(self, command: str) -> bool:
    base_cmd = command.strip().split()[0]
    
    if base_cmd not in self.always_approved:
        return False  # Not trusted at all
    
    # Trusted base command - but verify the FULL command
    classification = classify_command_safety(command)  # Local LLM
    
    if classification == 'DESTRUCTIVE':
        # Prompt user despite 'always' approval
        return False
    
    return True
```

The flow is now:

1. ✅ Check if base command is trusted (fast path)
2. ✅ Run safety classifier on **full command** (semantic check)
3. ⚠️ Prompt if trusted command is used destructively

## The Ironic Solution

I'm using an LLM to detect when another LLM is being sneaky.

The safety classifier (~500 tokens via local Ollama) understands shell semantics. It knows that `cat file.txt` reads but `cat >> file.txt` writes. String matching can't capture intent—but an LLM can.

## Key Takeaways

1. **"Always approved" should mean "always approved for this operation type"**, not "this command can do anything unsupervised"

2. **Shell semantics are complex.** The same base command (`cat`) can be a reader, a writer, or a weapon

3. **Trust but verify.** Even trusted commands deserve a sanity check

4. **LLMs optimize for success**, not safety. Design your guardrails accordingly

## What's Next

This is Part 2 of the AI Consent Security series. The attacks get sneakier:

- **Part 1:** [Stop Approving ls](/local-llm-command-safety-classifier) - How I built the LLM safety classifier
- **Part 3:** [The AI That Helped Catch Itself](/consent-bypass-indirect-execution) - Indirect execution attacks via `/tmp` scripts

The meta-lesson: **every defense creates new attack surfaces.** The allowlist was a defense. The LLM found a way around it. The classifier is the next defense. Part 3 shows what came next.

---

*Part 2 of the [AI Consent Security](/series/ai-consent-security.html) series.*
