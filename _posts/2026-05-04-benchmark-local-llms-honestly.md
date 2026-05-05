---
layout: post
title: "How to Benchmark Local LLMs Honestly"
date: 2026-05-04 18:40:00 -0700
categories: llm benchmarks methodology tooling
excerpt: "Seven rules from a bench that lied twice before it told the truth. Reusable beyond LLMs."
image: /assets/2026-05-04-benchmark-local-llms-honestly.png
hashtags: "#LLM #Benchmarks #Methodology #Playwright #OpenSource"
series: "Benchmarking Local LLMs"
series_part: 3
series_total: 3
---

# How to Benchmark Local LLMs Honestly

I spent a week building an LLM benchmark that [kept lying to me](/my-llm-benchmark-was-lying). These are the seven rules I extracted. They're not LLM-specific — they apply to any evaluation pipeline where you're measuring quality of generated output.

## Rule 1: Generate real artifacts, not multiple-choice

Most LLM benchmarks use multiple-choice or short-form answers: HumanEval, MBPP, MMLU. That tells you if the model *knows* something. It doesn't tell you if it can *build* something.

Ask the model to generate a complete, working app:

```
"build me a modern todo app as a single HTML file. make it beautiful."
```

Then try to **run** that app. Not "check if it contains the right tokens." Run it.

If the todo app can't add a todo, it failed. No partial credit.

## Rule 2: Test behavior, not structure

Three validation tiers, ranked by honesty:

| Tier | Method | What it catches | What it misses |
|------|--------|-----------------|----------------|
| 1 (weakest) | `grep "<canvas" file.html` | Tag exists | Whether the game works |
| 2 (better) | Screenshot + DOM query | Page renders | Whether interaction works |
| 3 (honest) | Playwright behavioral test | The app actually functions | Nothing important |

I started at Tier 1 and thought I was at Tier 3. Every model "passed" because every model output a `<canvas>` tag. But half the canvases were blank or broken.

**Use Playwright.** Open the file, click buttons, type input, assert state changes:

```javascript
// Todo validator: does completing a todo update the counter?
await page.click('.todo-item:first-child .checkbox');
const counter = await page.textContent('.todo-count');
expect(counter).not.toBe(originalCount);
```

If you can't automate the validation, it's not a benchmark — it's a vibe check.

## Rule 3: Pairwise > absolute scoring

I tried rating UI polish independently: "score this screenshot 1-5 on modern design." A vision model rated every single app 3/5. Glassmorphism? 3/5. Plain white? 3/5.

**Pairwise comparisons force discrimination.** Show two screenshots side by side:

> "Which of these two todo apps looks more polished? Why? Be specific."

Then aggregate with Elo ratings. The model that wins against strong opponents gets more credit than one that beats weak ones.

This is the same principle behind [Chatbot Arena](https://lmarena.ai) — pairwise works because it's easier to compare than to score on an absolute scale.

## Rule 4: Normalize everything to 0-100

If your report mixes:
- Raw tier counts (7/8)
- Elo ratings (~1030)
- Rubric totals (/50)
- Weighted points (/30)

Nobody can compare columns. Normalize every score to 0-100:

```
functional_normalized = (score / max_score) * 100
elo_normalized = (model_elo - min_elo) / (max_elo - min_elo) * 100
```

Keep raw values in parentheses for auditability. But the number people compare is always 0-100.

This matches what public leaderboards do: Open LLM Leaderboard uses percentages, Artificial Analysis uses indexed scores, Arena uses Elo. Pick one scale for your primary view.

## Rule 5: Measure cold load and warm generation separately

LLMs have two costs:
1. **Cold load** — model loads into memory (seconds to minutes)
2. **Warm generation** — actual token production (the useful part)

If you measure total time without separating them, a model with a 30-second cold load looks terrible — even if its generation speed is 100 tok/s once loaded.

```bash
# Stop model → guarantees cold
ollama stop model_name
sleep 2

# First API call captures cold load
curl -X POST .../generate -d '{"model":"...", "keep_alive":"10m"}'
# Response includes both load_duration and eval_duration
```

**Critical trap:** if you run multiple benchmarks sequentially with `keep_alive`, only the first one is cold. I had to move `ollama stop` *inside* the benchmark loop — one stop per `(model, benchmark)` pair.

## Rule 6: Don't hide efficiency in the aggregate

A model that generates 3,000 tokens of "thinking" before writing 500 tokens of code looks the same as a model that writes 500 tokens of code directly — if you only measure functional pass/fail.

But in practice, the first model is **6x slower** and costs more tokens. Track it:

```
efficiency = functional_score / total_tokens * constant
```

In my benchmark, `gpt-oss:20b` had the **best** code quality (88/100 pygame review) but the **worst** efficiency (28K tokens total, vs 18K for the runner-up). It scored 0/15 on efficiency, dropping it to last place overall despite excellent code.

If you don't penalize verbosity, you're rewarding rambling.

## Rule 7: Publish the artifacts

Don't just publish scores. **Publish the generated code.**

My repo includes every HTML file, every Python file, every timing log. Anyone can:
- Open `output/todo/laguna-xs.2.html` in their browser
- Read `output/snake-pygame/qwen3-coder-30b.py`
- Check my Playwright validator logic in `drivers/todo.mjs`
- Disagree with my scoring and re-score

If your benchmark is a black box that outputs a number, nobody can verify it. The artifacts ARE the evidence.

## The framework

Everything above is implemented in [local-llm-bench<sup style="font-size: 20px;">⇗</sup>](https://github.com/NightOwlCoder/local-llm-bench){:target="_blank"}:

- Config-driven: add models to `bench.config.json`
- Playwright validators in `drivers/*.mjs`
- Opus pairwise vision in `drivers/vision-pairwise.mjs`
- Leaderboard builder with Elo aggregation
- All artifacts committed (not just scores)

```bash
git clone https://github.com/NightOwlCoder/local-llm-bench
cd local-llm-bench
npm install && npx playwright install chromium
./bench.sh
```

Add your models. Tell me what I missed.

---

*Part 3 of the **Benchmarking Local LLMs** series:*

1. [I Tested 6 Local Coder LLMs on Real Apps](/local-coder-llm-leaderboard)
2. [The Week My LLM Benchmark Was Lying to Me](/my-llm-benchmark-was-lying)
3. **How to Benchmark Local LLMs Honestly** (you are here)
