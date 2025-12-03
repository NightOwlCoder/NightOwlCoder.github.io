---
layout: post
title: "Implementing JetBrains' Observation Masking: 80% Context Reduction for AI Agents"
date: 2025-12-03 10:00:00 -0800
categories: ai-agents llm context-management
excerpt: "AI coding agents hit context limits fast. JetBrains' research shows simple observation masking beats complex summarization—here's how to implement it."
image: /assets/2025-12-03-observation-masking-preview.jpg
hashtags: "#AIAgents #LLM #ContextWindow #JetBrains #Programming"
---

# Implementing JetBrains' Observation Masking: 80% Context Reduction for AI Agents

*Applying cutting-edge research to solve context overflow in LLM-powered coding assistants*

---

## The Problem: Context Window Bloat

If you're building or using AI coding agents, you've probably hit this wall: **your agent's context window fills up fast**, and eventually you get cryptic errors like:

```
{'error': 'Unable to trim conversation context!'}
```

The issue? AI agents "take notes" on every generated output—file contents, test logs, command outputs—iteratively adding information to their context. After a while, this memory log piles up so high that the context window is exceeded.

**Sound familiar?**

---

## The Research: JetBrains' December 2025 Study

On **December 1, 2025**, JetBrains Research published a timely paper:

> **"Cutting Through the Noise: Smarter Context Management for LLM-Powered Agents"**
> 
> [Read the full blog post<sup style="font-size: 20px;">⇗</sup>](https://blog.jetbrains.com/research/2025/12/efficient-context-management/){:target="_blank"} | [Paper (arXiv:2508.21433)<sup style="font-size: 20px;">⇗</sup>](https://arxiv.org/pdf/2508.21433){:target="_blank"}

Their experiments compared two context management approaches:

| Approach | Cost Reduction | Solve Rate Impact |
|----------|----------------|-------------------|
| **Observation Masking** | **52%** | **+2.6%** ✅ |
| LLM Summarization | ~50% | baseline |
| Raw (no management) | 0% | baseline |

**The surprise:** Simple observation masking **outperformed** the more sophisticated LLM summarization approach—while being cheaper to implement (no extra API calls).

---

## What is Observation Masking?

In agent conversations, each turn typically has three parts:
- **Reasoning** — The agent's thinking and decisions
- **Action** — What tool the agent called
- **Observation** — The tool's output (file contents, test results, etc.)

The key insight from JetBrains: **90-95% of tokens are observations**, not reasoning.

### Before Masking

```
Turn 1 (OLD):
  Reasoning: "I'll read the file to understand the bug..."     ✓ Useful
  Action: [Tool: read_file] auth.py                           ✓ Useful  
  Observation: [500 lines of code...]                         ← 50KB! 😰

Turn 180 (RECENT):
  [Everything preserved]
```

### After Masking

```
Turn 1 (OLD):
  Reasoning: "I'll read the file to understand the bug..."     ✓ KEEP
  Action: [Tool: read_file] auth.py                           ✓ KEEP
  Observation: [Result omitted - auth.py, 12KB]               ← MASKED 🎭

Turn 178-180 (RECENT):
  [Full content preserved]                                    ✓ KEEP ALL
```

**Why it works:**
- Agent still sees **what it decided** and **why** (reasoning preserved)
- Agent still sees **what tools were called** (actions preserved)
- Only the **verbose outputs** from older turns are masked
- **Recent turns stay complete** for immediate context

---

## Our Implementation

We applied this research to our AI coding assistant to handle conversations with 180+ messages.

### The Core Function

```python
def mask_observations(
    messages: list,
    keep_recent: int = 10,           # Full detail for last N turns
    mask_tool_output: bool = True,   # Mask observation content
    mask_threshold_chars: int = 500  # Only mask outputs > this size
) -> list:
    """
    Apply observation masking per JetBrains 2025 research.
    
    Keeps agent reasoning and actions intact while replacing
    verbose tool outputs with placeholders for older turns.
    """
```

### Adaptive Thresholds

One size doesn't fit all. We added adaptive parameters based on conversation length:

```python
# For very large conversations (100+ turns), be more aggressive
if turn_count > 100:
    keep_recent = 15       # Fewer recent turns kept full
    mask_threshold = 300   # More aggressive masking
else:
    keep_recent = 20
    mask_threshold = 500
```

This matches JetBrains' finding that **hyperparameter tuning matters**—different agent scaffolds need different window sizes.

---

## Results

| Scenario | Before | After |
|----------|--------|-------|
| 180 messages | ❌ CONTEXT OVERFLOW | ✅ SUCCESS |
| Context reduction | — | **~80%** |
| Quality impact | — | None observed |

The 80% reduction comes from:
- Tool outputs being 90-95% of tokens
- Masking ~85% of turns (keeping recent 15-20 full)

---

## Key Takeaways

1. **Simple beats complex** — Observation masking outperformed LLM summarization despite being simpler
2. **Preserve reasoning, mask data** — The agent's decisions are valuable; verbose tool outputs are not
3. **Adaptive parameters matter** — Tune the masking window for your specific agent
4. **No extra API calls** — Unlike summarization, masking doesn't require expensive LLM calls (which can add 7%+ to costs)
5. **Check your agent's behavior** — Some agents include retry attempts in history; adjust window size accordingly

---

## Try It Yourself

The approach is straightforward to implement:

1. **Identify observation content** in your agent's message format
2. **Keep recent N turns complete** (10-20 depending on your agent)
3. **Replace older observations** with placeholders like `[Result omitted - filename, X bytes]`
4. **Preserve reasoning and action** content from all turns
5. **Tune parameters** for your specific use case

---

## References

- **JetBrains Blog:** [Cutting Through the Noise: Smarter Context Management for LLM-Powered Agents<sup style="font-size: 20px;">⇗</sup>](https://blog.jetbrains.com/research/2025/12/efficient-context-management/){:target="_blank"}
- **Paper:** [arXiv:2508.21433<sup style="font-size: 20px;">⇗</sup>](https://arxiv.org/pdf/2508.21433){:target="_blank"}
