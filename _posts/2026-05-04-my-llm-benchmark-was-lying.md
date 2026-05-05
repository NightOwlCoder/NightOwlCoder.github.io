---
layout: post
title: "The Week My LLM Benchmark Was Lying to Me"
date: 2026-05-04 18:35:00 -0700
categories: ai-tools llm debugging benchmarks
excerpt: "Two overnight runs. Two rankings. Neither was real. Here's how my benchmark lied and what fixed it."
image: /assets/2026-05-04-my-llm-benchmark-was-lying.png
hashtags: "#LocalLLM #Benchmarks #Playwright #Debugging #AITools"
series: "Benchmarking Local LLMs"
series_part: 2
series_total: 3
---

# The Week My LLM Benchmark Was Lying to Me

I built a benchmark to test local coder LLMs. It took a week to get honest results. Not because the models were hard to test — because my tooling kept lying.

This is the debugging story.

## Lie #1: Stdin piping merges your prompts

First attempt: pipe two prompts through `ollama run --verbose`.

```bash
printf 'oi\ngive me a snake pygame please\n/bye\n' | ollama run model --verbose
```

Expected: two responses with separate timings.
Got: one response that said *"User said: oi, give me a snake pygame please, /bye"* and answered everything at once.

Non-interactive mode treats stdin as a **single user turn**. There's no prompt boundary. My "cold load vs warm generation" split was a fantasy.

## Lie #2: ANSI escape codes in everything

Even after switching to sequential calls, `ollama run` emits terminal cursor codes between every token:

```
```\u001b[?25l\u001b[?25hpython\u001b[?25l\u001b[?25h
```

My code extraction regex looked for ` ```python `. The actual log had ANSI garbage interleaved into the fence. Every code block extraction silently failed.

I only noticed when the `snake/` output directory was empty after a full overnight run.

## The fix: HTTP API

Both lies disappeared when I switched to Ollama's HTTP API:

```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"laguna-xs.2", "prompt":"oi", "stream":false, "keep_alive":"10m"}'
```

One call = one prompt = one clean JSON response. No TTY, no ANSI, no merged prompts. Load duration, eval count, total duration — all right there.

## Lie #3: Cold load leaked between benchmarks

Next overnight run looked great. Until I checked:

```
laguna-xs.2:
  oi:         load=8.87s   ← cold (honest)
  snake-html: load=90ms    ← warm (lying)
  tetris:     load=74ms    ← warm (lying)
  todo:       load=89ms    ← warm (lying)
```

I stopped all models once, ran all benchmarks sequentially per model. `keep_alive: 10m` meant the model stayed loaded across all prompts. Only the first benchmark got an honest cold-load measurement.

Fix: `ollama stop` **inside** the benchmark loop. Every single `(model, benchmark)` pair starts cold.

## Lie #4: Disk full fails silently

Third overnight. Models all cached. Ran. Logs showed:

```
=== laguna-xs.2 ===
  FAILED (pull error)
=== devstral:24b ===
  FAILED (oi API call)
=== qwen3-coder-next ===
  FAILED (pull error)
```

`df -h` showed 0 bytes free. The previous night's model pulls ate 293 GB of `~/.ollama/models`.

`ollama pull` doesn't pre-check disk space. The API call to write the response JSON also fails silently — `curl` gets back an empty response, my script logs "FAILED" and moves on. No crash, no alert. Just wrong results.

## Lie #5: caxi said "no canvas" on every page

After HTTP API + cold-load-per-benchmark, I added `caxi` (Chrome DevTools Protocol) to validate generated HTML files. Open each file, check if `<canvas>` exists, screenshot it.

Result: **all 10 snake.html files reported `has_canvas: false`.**

Reality check:

```bash
grep -c "<canvas" output/snake-html/*.html
# devstral-24b: 1
# gemma4-26b: 2
# gpt-oss-20b: 1
# laguna-xs.2: 1
# qwen3-coder-30b: 0  ← only one actually missing it
# qwen3-coder-next: 1
# ...
```

9 out of 10 had canvas. Caxi reported 0 out of 10.

The problem: `caxi` maintains a single Chrome session. After navigating to the first file, subsequent `caxi open` calls didn't fully reload — they hit stale DOM from the previous model's page. Every `caxi eval "document.querySelector('canvas')"` was querying the wrong page.

## The fix: Playwright

Replaced all caxi validators with Playwright scripts. Each validation gets a **fresh browser context**, loads the file, waits for `networkidle`, then runs real behavioral checks:

```javascript
const browser = await chromium.launch();
const page = await (await browser.newContext()).newPage();
await page.goto(`file://${artifact}`, { waitUntil: 'networkidle' });

// Actually interact with the app
await page.keyboard.press('ArrowRight');
await page.waitForTimeout(200);
const moved = await page.evaluate(() => /* check snake position changed */);
```

Not "does canvas exist" — "does the game respond to input."

## Lie #6: Vision models can't score UIs

I tried scoring visual polish with `qwen3.6-plus` vision: "rate this UI 1-5 on modern design."

Every single app scored 3/5. Todo apps with glassmorphism: 3/5. Plain white background with Times New Roman: 3/5. The model couldn't distinguish.

Fix: **pairwise comparisons** with Opus 4.7. Show two screenshots side by side, ask "which is more polished and why?" Winner gets Elo points. Much harder to game, and the rankings finally matched what my eyes saw.

## The honest results

After fixing all six lies, the leaderboard changed completely:

- `gemma4:26b-mlx-bf16` went from "probably mid-tier" to **#1 overall** (visual polish carried it)
- `qwen3-coder:30b` went from "obvious winner" to **#5** (games-only specialist)
- `gpt-oss:20b` went from "fastest snake" to **#6** (efficiency killed it despite best code quality)

The full leaderboard: [I Tested 6 Local Coder LLMs on Real Apps](/local-coder-llm-leaderboard)

## Lesson

**Your tools lie. Test the tests.**

Every layer between "model generates code" and "you see a score" is a potential corruption point. Piping, ANSI, session state, disk space, Chrome context, vision models — all produced plausible-looking results that were completely wrong.

The benchmark that lies confidently is worse than no benchmark at all.

---

*Part 2 of the **Benchmarking Local LLMs** series:*

1. [I Tested 6 Local Coder LLMs on Real Apps](/local-coder-llm-leaderboard)
2. **The Week My LLM Benchmark Was Lying to Me** (you are here)
3. [How to Benchmark Local LLMs Honestly](/benchmark-local-llms-honestly)
