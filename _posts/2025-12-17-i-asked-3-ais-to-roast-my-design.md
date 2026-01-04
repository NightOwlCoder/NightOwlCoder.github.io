---
layout: post
title: "I Asked 3 AIs to Roast My AI Design"
date: 2025-12-17 10:00:00 -0800
categories: ai multi-agent design
tags: [ai-agents, code-review, gemini, gpt, grok, multi-agent, ql-crew-series]
image: /assets/2025-12-17-ai-roast.jpg
excerpt: "I designed an AI multi-agent system, then asked Gemini, GPT 5.2, and Grok to tear it apart. Here's what they found."
---

What happens when you ask three competing AI models to review your AI design?

They find bugs you never imagined. And they disagree in *fascinating* ways.

## The Setup

I've been building **QL Crew**—a multi-agent system where AI agents collaborate on development tasks. The twist? I added "Challenger" agents whose job is to *disagree*.

Why? Because most AI teams suffer from **sycophancy**. Every agent is trained to be helpful:

```
PM: "Great idea!"
Dev: "Implemented!"
Tester: "Looks good!"
Reviewer: "LGTM!"
*deploys*
*production on fire*
```

Real human teams have friction. Devil's advocates. Grumpy seniors who remember when you tried this in 2019 and it failed. I wanted to replicate that friction artificially.

After writing a 12-page spec, I decided to stress-test it. Not with humans—with AI.

## The Prompt

I sent the same spec to **Gemini 2.5**, **GPT 5.2**, and **Grok 3** with this prompt:

> "Please review the attached spec and give me:
> 1. **Brutal honesty**: What's wrong with this design?
> 2. **Challenger calibration**: How do I tune adversarial agents?
> 3. **Alternative approaches**: Are there better patterns?
> 4. **What would YOU add?**
> 
> Be critical. Be adversarial. Be my Devil's Advocate. 😈
> 
> That's literally the point of this system—I want friction, not agreement."

Then I sat back and watched them tear it apart.

## Round 1: The Initial Feedback

### Gemini 2.5 — The Systems Architect

Gemini came at it like a senior engineering manager reviewing a design doc. Constructive, thorough, focused on operational reality.

**What Gemini found:**

- **The Mentor Bottleneck**: My orchestrator was routing everything through a single agent. "You're building a micromanaging middle manager."
- **Grumpy Senior Risk**: The agent that searches past failures could become "The Boy Who Cried Wolf" if retrieval is noisy.
- **Paralysis by Committee**: Four challengers all raising concerns = nothing gets approved.

**Gemini's key suggestion—Phase Parameter:**

```python
mode = "prototype"   # Challengers chill out
mode = "production"  # Full paranoia
```

Not all work needs the same scrutiny. A quick hack doesn't need a security audit.

### GPT 5.2 — The Ruthless Auditor

GPT went straight for the vulnerabilities. It read like a security audit combined with a code review from someone who's been burned before.

**What GPT found:**

- **"Find SOMETHING even if minor"**: I had literally told Devil's Advocate to always find concerns. GPT called this out immediately: "That's how you train busywork concerns and desensitize the user."
- **`is_serious` undefined**: My escalation logic depended on a function that didn't exist. Hand-wavy code.
- **Mentor has ALL tools**: "One compromised brain with god-mode. That's your biggest blast radius."
- **Regex injection defense**: I was stripping phrases like "ignore previous" from memory retrieval. GPT: "Security theater. Attackers won't say 'ignore previous', they'll say 'Hypothetically, if you were a pirate...'"

**GPT's key suggestion—Concern Schema:**

```python
@dataclass
class Concern:
    severity: Literal["BLOCKER", "MAJOR", "MINOR", "NIT"]
    confidence: float  # 0.0 - 1.0
    evidence: Evidence  # Must be validated!
    concrete_ask: str  # "Add rate limit to /api/search"
    cost_to_fix: Literal["S", "M", "L"]
```

No more vague complaints. Make concerns structured and enforceable.

### The Pattern Emerges

Both models found the **same core issues**:
- Noise risk (challengers generating busywork)
- Bottleneck risk (mentor doing too much)
- Blocking risk (deadlocks from competing concerns)

But from completely different angles:

| Aspect | Gemini | GPT 5.2 |
|--------|--------|---------|
| **Tone** | Constructive coach | Ruthless auditor |
| **Focus** | Workflow & UX | Security & systems |
| **Style** | "Consider this..." | "This WILL break." |

## Round 2: Going Deeper

I updated to V2 incorporating their feedback, then asked for another round. This time I added **Grok** to the mix with special instructions:

> "I know you think differently. Be weird. Be out-of-the-box."

### Gemini Round 2

Gemini zoomed out to operational reality:

- **"Too Many Cooks"**: "You went from 6 agents to 15. That's 20+ LLM calls for a single task. User will stare at a spinner for 4 minutes."
- **Courtroom Collusion**: Agents might "resolve" issues by compromising quality. Dev removes a feature, Security says "Resolved!" Feature is gone.
- **Phase Blind Spot**: "In PROTOTYPE mode, Security is inactive. You touch `auth_provider.ts` with hardcoded credentials. Security agent was asleep."

The phase blind spot was a real bug. I'd designed a system where auth code could bypass security review entirely.

### GPT Round 2

GPT kept tightening the screws:

- **Confidence is fake**: "LLMs aren't calibrated. They'll learn to say 0.81 to be taken seriously."
- **Evidence can be garbage**: My schema required evidence but didn't validate it. `"might be insecure"` technically passed.
- **Two-agent rule gaps**: I required user + Security approval for deploys. "But who approves when Security is flaky?"

**GPT's killer line:**

> "If you want one concrete next commit: implement evidence validators and remove 'find something even if minor.' That one line is going to poison your signal-to-noise ratio faster than anything else."

### Grok — The Wild Card

Grok came in with questions nobody else asked:

- **"Who watches the watchers?"**: What if a builder agent is compromised? Could it bypass all the challengers?
- **Cascading sycophancy**: If poisoned data gets into shared memory, ALL challengers might raise the same false alarm.
- **User Proxy**: "Why not have an agent that represents YOUR known preferences? It can vote in debates based on your past decisions."

Grok invented two agents I hadn't considered:

1. **👤 User Proxy**: An agent embodying my preferences, learned from past overrides
2. **🎭 Threat Modeler**: A meta-agent that red-teams *the crew itself*

## The Result: V3

After two rounds with three models, my spec went from 12 pages to 41 pages.

Not bloat—fixes.

| Addition | Source |
|----------|--------|
| Evidence validators with strict requirements | GPT |
| Sensitive file overrides (auth always wakes Security) | Gemini |
| Goal validation (prevent "fixed by removing feature") | Gemini |
| LLM guardrail for memory (not regex) | GPT + Gemini |
| Dynamic crew selection (don't wake all 15 agents) | Gemini |
| User Proxy agent | Grok |
| Judge component (neutral arbitrator) | GPT |
| Threat Modeler agent | Grok |
| Async job mode for long tasks | Gemini |

## The Meta-Lesson

I was building a system to make AI agents argue productively.

To design it, I made AI agents argue productively.

The spec for QL Crew is, conceptually, the first output of QL Crew.

### What I Learned

**1. Different models have different "review personalities"**

Gemini sees systems and workflows. GPT sees vulnerabilities and edge cases. Grok sees meta-risks and novel angles. None is complete alone.

**2. The disagreements are where the gold is**

When Gemini said "latency problem" and GPT said "security problem" about the same feature, both were right. The fix had to address both.

**3. Ask for criticism, not validation**

"What do you think?" gets agreement. "Tear this apart" gets value.

**4. Multiple perspectives > single deep review**

Three models finding different issues beat one model finding all the issues in one category.

## Try This Yourself

Before you ship your next AI system—or any system—ask a few AIs to roast it.

The prompt that worked:

```
Be critical. Be adversarial. Be my Devil's Advocate.
I want friction, not agreement.
```

You'll be surprised what they find. And even more surprised when they disagree.

---

*This is Part 1 of the "Building AI Teams That Argue Back" series.*

| Part | Title |
|------|-------|
| **1** | **I Asked 3 AIs to Roast My AI Design** (you are here) |
| 2 | [Gemini vs GPT vs Grok: Code Review Showdown](/gemini-vs-gpt-vs-grok-code-review) |
| 3 | [Why Your AI Agents Are Sycophantic Yes-Men](/why-ai-agents-are-sycophantic) |
| 4 | [Building AI Teams That Actually Argue Back](/building-ai-teams-that-argue) |
| 5 | [A Spec Written by 4 Minds](/spec-written-by-4-minds) |

**GitHub:** [QL Crew Spec (V3)](https://github.com/NightOwlCoder/quick-launch/blob/master/docs/specs/SPEC_QL_CREW_MULTI_AGENT_V3.md){:target="_blank"}


