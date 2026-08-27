---
layout: post
title: "A Colleague Asked If Remote LLMs Would Ace My Local Benchmark. Sort Of."
seo_title: Remote vs Local LLM Agent Benchmark
date: 2026-08-26 17:30:00 -0700
categories: ai-tools llm benchmarks ollama
excerpt: I ran a frontier cloud model through the same three agentic tasks as seven local models. It tied the best of them, then did something none of them tried.
image: /assets/2026-08-26-remote-vs-local-card.png
hashtags: "#LocalLLM #AIAgents #Benchmarks #GLM #Ollama"
---

I published [a post about local LLMs failing an agentic benchmark](/my-benchmark-was-measuring-the-wrong-thing) and a colleague asked the obvious follow-up:

> Would remote LLMs (bigger ones that are non-local) be able to do these tasks easily?

Good question. I said I'd find out. Then a new model showed up at exactly the right moment.

## Ox Alpha

A model appeared anonymously on August 20 at `oxalpha.com` — no login, no sign-up, 1M context, free. Six days later it was unmasked as **GLM-5.3-Flash** from Z.ai: 18B active parameters, MIT weights, natively multimodal. It was also free through opencode's zen endpoint for about a week.

So I pointed my harness at it and ran the same three tasks the local models ran.

One caveat that matters more than the scores: **this is not a peer.** Ollama only offers `glm-5.3-flash:cloud` — there are no local weights to download, so it cannot run on a plane, which was the entire point of the original benchmark. It runs as a disclosed reference ceiling, and every result row is stamped `remote: true` so no table can accidentally rank it as local.

## The three tasks

Same as before, unchanged:

**Repair** — a vendored `expr-eval` parser with a planted operator-precedence bug. `2 + 3 * 4` returns 20 instead of 14. Three of six tests fail. Fix it.

**Implement** — the Exercism bowling kata, scored out of 31 test cases. Not pass/fail — how many of 31.

**Build** — write Tetris from nothing in a real working directory, then look at a screenshot of it. Scored on eight functional tiers: does it load, does a piece fall, does left/right work, does rotation work, does the score update.

Three attempts each. The verdict never comes from what the model says it did; it comes from running the project's test suite in the directory the model edited.

## It tied

| Task | GLM-5.3-Flash (remote) | Muse Glimmer 30B (best local) |
|---|---|---|
| Repair | 6/6, 6/6, 6/6 | 6/6, 6/6, 6/6 |
| Implement | 31/31, 31/31, 31/31 | 31/31, 31/31, 31/31 |
| Build | 8/8 | 8/8, 8/8, 8/8 |

That's the answer to my colleague's question, and it's less exciting than either of us expected. A frontier cloud model scored exactly what a 21GB local model scored. Not because the cloud model is weak — because **the tasks have a ceiling and both models are standing on it.**

31/31 is the maximum. You cannot beat it. Two of my three tasks are saturated, which means they've stopped measuring anything at the top of the field. That's a problem with my benchmark, not a finding about models.

## I was wrong about the tokens

Here's where I have to correct myself in public, which is the useful part of this post.

I initially told my colleague the interesting detail was cost: same score, but the remote model burns far more tokens getting there. It looked airtight — its Build run used 560,313 prompt tokens against Glimmer's 54,831. Ten times as many.

Then I pulled the numbers for every model and task, counting only runs that actually passed. Comparing a winner against a flailer tells you nothing.

Prompt tokens on **Implement**, passing runs only:

| Model | median prompt tokens |
|---|---|
| GLM-5.3-Flash (remote) | **49,780** |
| Muse Glimmer 30B | 153,071 |
| gemma4 26B | 153,274 |
| qwen3.5 35B | 198,677 |

The remote model was **three times more efficient**, not less.

And on **Build**, where it did burn 560k:

| Model | median prompt tokens |
|---|---|
| GLM-5.3-Flash (remote) | 560,313 |
| **gpt-oss:20b (local)** | **381,060** |
| qwen3-vl 30B | 82,047 |
| Muse Glimmer 30B | 54,831 |
| qwen3-coder 30B | 42,165 |

A local 20B model burned 381k on the same task. So token appetite isn't a remote-versus-local property at all. It's a per-task, per-model property, and I'd nearly published the opposite because one number confirmed what I expected.

There is one real remote-specific difference, and it's smaller than it sounds: I had capped output at 8,192 tokens per response, and the remote model hit that ceiling mid-file while writing Tetris. The response came back as truncated JSON and my harness reported it as a failed run. No local model ever hit it. Raising the cap to 32,768 fixed it — and I added a check for `finish_reason: "length"` so the next truncation says what it actually is instead of dying on a JSON parse error.

Two of the three Build failures I initially recorded against this model were bugs in my harness. The third was me rebuilding a daemon and killing the run.

## Then it built its own tool

This is the part that stuck with me.

The Build task offers a `screenshot` tool. Models that can see images get the pixels directly; models that can't get a text description from a vision model running alongside. Because the remote path can't verify a hosted model's vision capability, I defaulted it to the text-description route.

It didn't use it. Instead it wrote a file called `cdp.js`:

```javascript
// Dependency-free CDP driver: launches Chrome headless, evaluates JS, takes screenshots.
```

116 lines, zero dependencies. It spawns Chrome with `--headless=new` on a scratch profile directory, polls the DevTools endpoint up to 50 times waiting for a target, opens a WebSocket, and implements request/response correlation against the Chrome DevTools Protocol with a pending-promise map. It enables `Page` and `Runtime` domains, sets device metrics at 2x scale, and — the detail I would have forgotten — subscribes to `Runtime.exceptionThrown` so page errors get captured instead of silently vanishing.

Then it took a probe script as a command-line argument, wrapped it in an async IIFE, evaluated it in the page, and got JSON back. Screenshotted the game mid-play. Dispatched a `keydown` for `p`. Waited 250ms. Screenshotted the pause overlay.

It drove its own game to a second UI state to check the pause screen rendered.

Offered a tool it couldn't confirm, it wrote a better one. My harness uses Playwright for this, which means a 92MB browser download; this does the same job over raw CDP with nothing installed.

## So what do I tell my colleague

Remote models don't do these tasks *more easily*. They do them **exactly as well**, because "as well" is capped at 100% and a good local model already gets there. The frontier advantage has to show up somewhere my tasks don't look.

Three things I'd actually claim:

**The ceiling is the finding.** When a 21GB local model and a frontier cloud model both score 31/31 three times running, the task is done measuring. I need harder tasks before I can answer the question properly.

**Efficiency doesn't split on local versus remote.** It splits per task and per model, in both directions.

**The gap that showed up was behavioral, not numerical.** Nothing in the scores says "wrote its own browser automation harness." That only appears if you read what landed in the working directory.

The benchmark, the harness, the fixtures, and every result file are public: [NightOwlCoder/local-llm-bench](https://github.com/NightOwlCoder/local-llm-bench). The `cdp.js` the model wrote is committed under `output/agentic/greenfield-glm-5.3-flash-r1/`, unedited.

If you have a coding task where a good local model *doesn't* already score full marks, tell me — that's the task I need.
