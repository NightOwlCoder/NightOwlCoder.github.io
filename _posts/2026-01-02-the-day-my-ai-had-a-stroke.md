---
layout: post
title: "The Day My AI Had a Stroke (And Lived to Tell About It)"
date: 2026-01-02 16:00:00 -0800
categories: ai-tools llm debugging
excerpt: "Asked about a diff viewer. Got 3,000 lines of a Lua manual in English and Chinese instead. Here's what went wrong."
image: /assets/2026-01-02-the-day-my-ai-had-a-stroke.png
hashtags: "#AIAgents #LLM #Hallucination #Programming"
---

# The Day My AI Had a Stroke (And Lived to Tell About It)

*When your AI coding assistant suddenly speaks in tongues*

---

## The Question

It was a simple question about diff viewers. I was asking my AI assistant:

> "That is not what I will see right? I see a diff something viewer?"

Standard debugging conversation. I expected maybe a paragraph explaining how the visual diff would look.

---

## The Response

Instead, I got **over 3,000 lines** of this:

```
# book/parts/programming-in-lua/main.md

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃        Programming in Lua             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

四本书——《Programming in Lua》三版，《Lua程序设计》，
官方文档《Lua Programmers Manual》简版...

学习Lua语言，这三部主文本是最重要的：
PiL3，Lua 5.4参考手册Chinese&English...

1 – Introduction
Lua is a powerful, efficient, light-weight, 
embeddable scripting language...

1 – 介绍  
Lua 是一种强大、高效、轻量级、可嵌入的脚本语言...
```

And it just kept going. Chapter after chapter. English paragraph, Chinese translation. English paragraph, Chinese translation.

**Three. Thousand. Lines.**

---

## What Just Happened?

If you've ever seen someone have a stroke, you know the terrifying moment when speech becomes garbled—words that don't connect, languages mixing, saying things completely unrelated to what you were just talking about.

That's exactly what this was. My AI had a stroke.

The parallels are uncanny:
- **Sudden onset** — No warning, mid-sentence
- **Aphasia-like symptoms** — Mixing languages nonsensically  
- **Loss of context** — Complete disconnection from our conversation
- **Regurgitation** — Repeating memorized patterns (like stroke victims reciting nursery rhymes)

---

## The Diagnosis

After the panic subsided, I looked at the context usage:

**At time of stroke:** `68.9% (688K/1M tokens)`

That's high, but not critical. What likely happened:

### Theory 1: Training Data Collapse
The model's training set includes programming books (obviously—that's how it learned to code). Under certain conditions, the probability distribution can collapse to a "memorized state" where it outputs training data instead of generating new responses.

### Theory 2: MaxTokensReachedException
The error logs showed `MaxTokensReachedException`. The model tried to respond, hit some internal limit, and instead of failing gracefully ("Sorry, response too long"), it started dumping whatever was in cache.

### Theory 3: Context Corruption
Something in the 688K tokens of our conversation history triggered a malformed prompt state. The attention mechanism latched onto the wrong patterns.

### Theory 4: Bedrock Glitch
AWS Bedrock might have had a momentary seizure. These things happen with cloud AI services—packet loss, partial requests, cache misses.

---

## The Recovery

Unlike a human stroke victim, AI recovery is instant:

1. **Ctrl+C** (frantically stop the output)
2. **Screenshot** (for posterity and this blog post)
3. **Restart session** 
4. **Move on**

No rehabilitation. No lasting effects. Just me with a funny story.

---

## Why This Matters

This incident highlights something important about LLMs:

**They're not thinking. They're pattern matching.**

When those patterns break down—whether from context overload, token limits, or API glitches—you get pure chaos. A human having trouble would say "I don't understand" or "Can you rephrase?"

An AI? It dumps 3,000 lines of a Lua manual in two languages.

**For users:** This is why you need backup systems. I now auto-backup every AI conversation because sessions can die spectacularly.

**For developers:** This is why graceful degradation matters. Better to admit failure than hallucinate training data.

---

## The Punchline

I asked about a diff viewer.

I got a programming manual.

In two languages.

About a language I don't use.

For 3,000 lines.

And somehow, my AI is now writing a blog post about it.

If that's not meta, I don't know what is.

---

*Have an AI horror story? I'd love to hear it. The best debugging tales are when the tools themselves become the bugs.*

