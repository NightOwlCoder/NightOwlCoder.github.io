# Blog Ideas — Pending

Ideas tagged during dev sessions. Pick one, write it, ship it.

## Pending

### ilha's UnifiedCommand vs Claude Code's Split Architecture

- **Tagged:** 2026-04-01 (Claude Code leak dissection)
- **Rating:** ⭐⭐⭐⭐⭐
- **Categories:** ai-tools rust architecture design-patterns
- **Angle:** Claude Code has SEPARATE systems for tools (LLM-facing) and commands (slash). ilha's `UnifiedCommand` trait gives CLI + slash + LLM tool from ONE implementation. Compare the DX, show real code from both, argue why unified is better.
- **Key points:**
  - Claude Code: 100+ commands + 40+ tools = separate registrations, separate code paths
  - ilha: `register_command!` macro → all three access methods automatically
  - ilha: `--json` on everything (Claude Code slash commands don't have this)
  - ilha: compile-time schema validation via serde vs runtime Zod
  - Side-by-side code comparison: their `buildTool()` + command registration vs our single trait
  - Bonus: their tool count (40+) vs ours (47) — similar scope, half the boilerplate
- **Source session:** ilha session 1775077228288
- **Source material:** `ilha/docs/CLAUDE_CODE_DISSECTION.md` step 1

## Published

(none yet)
