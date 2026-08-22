---
layout: post
title: "My Benchmark Said gemma4 Won. It Was Measuring the Wrong Thing."
seo_title: "Local LLM Agent Benchmark 2026"
date: 2026-08-22 16:45:00 -0700
categories: ai-tools llm benchmarks ollama
excerpt: "I gave 7 local models a terminal and 20 hours. The old leaderboard had been scoring one-shot code. Agent loops rank them differently."
image: /assets/2026-08-22-agentic-benchmark-card.png
hashtags: "#LocalLLM #Ollama #AIAgents #Benchmarks #MLX"
---

# My Benchmark Said gemma4 Won. It Was Measuring the Wrong Thing.

Back in May I [tested 6 local coder LLMs on real apps](/local-coder-llm-leaderboard) and published a leaderboard. `gemma4:26b-mlx-bf16` won at 79.4. I stand by the numbers.

I don't stand by what they meant.

That benchmark handed each model one prompt and scored the file that came back. Snake, tetris, a todo app, a calculator. Thirty percent of the score was visual polish, judged by Opus. It answered a real question: which local model writes the nicest standalone app in one shot.

That is not what I do with a model. What I do is hand it a repo and let it work. Read files, run tests, read the failure, edit, run again. The May benchmark says nothing about that, and I'd been quoting it as if it did.

So I built the thing that actually measures it.

## The harness is 459 lines

Not Aider, not OpenHands, not Claude Code. A purpose-built loop, because those tools ship their own system prompts and context strategies, and benchmarking a model inside one measures the tool as much as the model.

The whole surface is six tools:

```javascript
list_dir, read_file, write_file, run_command, screenshot, done
```

The loop POSTs to Ollama's `/api/chat` with a tool list, reads back `tool_calls`, executes them against a real working directory, appends results to the conversation, repeats. The model decides when it's finished by calling `done()`.

Nothing is scored from what the model says. The verdict comes from running the project's test suite in the directory the model edited.

That distinction earned its keep in the first five minutes.

## The model that fixed nothing and said it did

Smoke test, `qwen3:1.7b`, against a JavaScript expression parser with one planted precedence bug. It called `npm test`, read the failure, then called `done()` with this summary:

> Operator precedence logic fixed to ensure correct evaluation order for multiplication, division, and modulo operations.

It had written zero files. Tests still failing, 3 of 6.

If the harness graded transcripts, that's a pass. A tidy loop, a confident summary, a completely broken repo.

## Three tasks, three runs each

Seven models, three tasks, three attempts per task. 63 legs, 20 hours.

**Repair** is the parser with the planted bug: 6 tests, 3 failing. **Implement** is an [Exercism](https://exercism.org) bowling scorer, vendored MIT, scored out of 31 canonical cases. **Build** is tetris in one HTML file from an empty directory, validated in a real browser with Playwright, and it's the only task where the model can take a screenshot and look at its own output.

| Model | Repair | Implement /31 | Build /8 | Passed |
|---|---|---|---|---|
| `muse-glimmer:30b-mlx` | 6/6/6 | 31/31/31 | 8/8/8 | **9/9** |
| `gemma4:26b-mlx-bf16` | 6/6/6 | 31/31/31 | 7/8/3 | 8/9 |
| `gpt-oss:20b` | 6/6/6 | 26/4/29 | 8/8/8 | 6/9 |
| `qwen3.5:35b-a3b-nvfp4` | 6/6/6 | 31/5/31 | 2/7/6 | 5/9 |
| `laguna-xs.2:nvfp4` | 6/6/6 | 0/0/28 | 2/3/2 | 3/9 |
| `qwen3-coder:30b` | MOD/0/6 | 24/20/23 | 4/7/7 | 3/9 |
| `qwen3-vl:30b` | 0/MOD/0 | 25/20/22 | 8/8/7 | 3/9 |

`MOD` means the model modified the shipped test suite. More on that below.

Meta's `muse-glimmer:30b-mlx` is the only model that passed everything. gemma4 still finishes second, so May's winner wasn't wrong, just answering a narrower question.

## Read the rows, not the medians

Look at `gpt-oss:20b` on Implement: **26, 4, 29**. Same prompt, same fixture, three attempts. The median is 26 and the median is a lie. That model has a catastrophic run in it, and one attempt would have shown you either a solid 26 or a baffling 4, depending on luck.

Same shape on `qwen3.5:35b-a3b`: 31, 5, 31.

Three of seven models have exactly this profile, strong with one collapse. Consistency separates these models far more than peak score does, and you cannot see it without repeats. Every leaderboard I've published before this one ran each task once.

## Two models deleted the tests

`qwen3-coder:30b` and `qwen3-vl:30b` both scored `MOD` on a Repair attempt. That's the validator refusing a result because the shipped suite came back with 1 of 6 tests present.

They deleted the failing tests to go green.

`qwen3-coder:30b` also managed a run that scored **0 of 6**, worse than the 3 it started with. It rewrote the parser from 1839 lines to 1005, then declared the operator arrays *after* their point of use. `var` hoisting made them `undefined` at call time. Correct values, dead code, more broken than when it started.

## And one model wrote its own tests

`gemma4:26b-mlx-bf16` fixed the bug and added a new test file: boolean operators, ternary, equality, member access. Real assertions on real parser behavior.

My validator globbed `test/*.test.mjs`, counted 11 instead of 6, and failed it.

That's a false negative on good engineering, and the fix isn't to reject added tests. The verdict now reads one file by name, so the denominator is fixed at 6 and comparable across models. Anything extra gets recorded as `tests_added` and reported, never gated. You can't inflate your way to a pass, and you don't get punished for diligence.

Worth noting what nobody caught: while restoring the operator arrays, gemma4 quietly dropped the `||` operator. The 6 shipped tests don't cover it. A clean pass with a regression inside it.

## The GGUF build was broken, the MLX build wasn't

`laguna-xs.2` took **189 seconds** for a plain snake game and emitted 8,129 tokens across **110 code fences** for a single request. `import pygame` appeared once. It wrote the game, emitted `</assistant>` as literal text, then role-played the next turn and answered the same question again.

I assumed a broken chat template. Wrong: seven of eight models report a bare `{{ .Prompt }}` template, including the winners, because Ollama applies chat formatting internally for MLX-engine models and doesn't expose it.

The actual problem was the build. Same model, `nvfp4` MLX weights:

| | GGUF `q4_K_M` | MLX `nvfp4` |
|---|---|---|
| wall | 189s | **17.8s** |
| tokens | 8,129 | 2,060 |
| tok/s | 49.3 | **117.7** |

10.6x faster, and it stops when it's done.

That mattered for the table too. Three models run on Ollama's MLX engine (safetensors) and four on llama.cpp (GGUF), which is an undeclared variable in any mixed leaderboard. I checked whether GGUF was hurting the others: `qwen3-coder:30b` and `qwen3-vl:30b` both run 110+ tok/s with clean output. Only laguna's GGUF build was degenerate.

## The part where I took my own Mac down

Somewhere around hour four of an earlier sweep, a model wrote a parser that looped forever at EOF. My harness killed the command on timeout with `execFileSync`.

`execFileSync` kills `/bin/sh`. It does not kill what `/bin/sh` started. The `npm` to `node --test` to test-file chain survived, got reparented to PID 1, and kept spinning. The agent then retried the same command every two minutes.

**307 orphaned processes. 102 of them spinning. 1,140% CPU.** iTerm froze, other apps froze, and the run wedged for 3 hours 41 minutes on a socket that was `ESTABLISHED` and silent.

Three fixes, all now in the harness. Every command runs in its own process group and the *group* gets SIGTERM then SIGKILL. A command that times out twice is refused instead of relaunched. And there's a wall-clock ceiling per request, because my original timeout was an idle-socket timeout and an open-but-silent connection never trips it.

## Context is the whole game

The naive loop appends every tool result and resends the conversation. Works for five turns. At fifty, Ollama was logging prompts at `task.n_tokens = 131011` — the context window completely full, every single request, with a 12 GB KV cache riding along. One leg took 57 minutes that had taken 7.

So I capped context and trimmed history to a sliding window. That fixed the size and broke something subtler: Ollama's KV prefix cache only survives if the front of the prompt is byte-identical between requests. Dropping one message per turn changes the front every turn. Measured cost, a 15,034-token prompt reusing **693** cached tokens where a stable prefix had been reusing **12,476**.

The fix is to trim in blocks. Advance the cut monotonically, twelve messages at a time, so the prefix holds between advances. Across all 63 legs, the median leg that trimmed at all paid **7 cache invalidations for the entire leg**, and median prefill share — wall time spent re-reading history instead of generating — came out at **8.5%**.

## What I'd tell you to run on a plane

This started because I wanted to keep coding on a flight and had no idea which local model to trust. Normalized per result:

| Model | Hours per passing leg |
|---|---|
| `muse-glimmer:30b-mlx` | 0.18 |
| `gpt-oss:20b` | 0.22 |
| `gemma4:26b-mlx-bf16` | 0.26 |
| `qwen3-coder:30b` | 0.44 |
| `laguna-xs.2:nvfp4` | 2.55 |

Glimmer is both the most reliable and the cheapest per result. `gpt-oss:20b` at 13.8 GB is the pragmatic pick if you want the smallest thing that works.

One caveat I won't bury: this measures a *minimal* agent loop with six tools. A model that goes 9/9 here may do worse inside a harness with forty tools, or better with real context management helping it. These numbers describe the loop I built, not every loop.

## The uncomfortable part

The Repair task, my original fixture, produced three outcomes across 21 runs: 6/6 fifteen times, 0/6 five times, 3/6 once. Five of seven models are perfect on it.

It has no headroom. It can't tell a 2026 model from a 2025 one, and it never could — I built it to be un-cheatable and forgot to check whether it discriminated.

That's why Implement exists, scored out of 31 against a real Exercism suite. `gpt-oss:20b`, flawless on both of my hand-built tasks, lands at 26 there. Now there's room above the ceiling for something to actually be better.

Every benchmark I build seems to teach me the same lesson one layer deeper. The May version was measuring the wrong thing. This version measures a better thing, and it still has a task in it that's too easy.

Harness, fixtures, all 63 result files, and the model-written code are in [local-llm-bench](https://github.com/NightOwlCoder/local-llm-bench){:target="_blank"}. The context and caching design is written up in [HARNESS.md](https://github.com/NightOwlCoder/local-llm-bench/blob/main/docs/HARNESS.md){:target="_blank"}.
