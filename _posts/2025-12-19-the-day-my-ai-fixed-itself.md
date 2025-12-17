---
layout: post
title: "The Day My AI Fixed Itself"
date: 2025-12-19
categories: [ai, debugging, meta]
tags: [ai-agents, self-healing, python, debugging]
image: /assets/2025-12-19-ai-fixed-itself.jpg
excerpt: "What happens when your AI assistant forgets who it is? Mine diagnosed the bug, proposed a fix, and implemented it—while broken."
---

What happens when your AI assistant forgets who it is?

I found out yesterday when my QL Chat Mentor—an AI assistant I built to help me navigate my development tools—suddenly became... dumb. It didn't know basic commands. It couldn't help with the project it was built for.

**The plot twist?** The broken AI helped me debug itself.

## The Setup

I built [QL Chat Mentor](https://github.com/NightOwlCoder/quick-launch) as a conversational interface for my Quick Launch toolkit. It loads an `AGENTS.md` file containing all its knowledge—commands, workflows, project context—and uses that to assist me.

It worked great when I ran it from the project directory:

```bash
cd ~/fileZ/projZ/quick-launch
ql chat
# ✅ Mentor knows everything
```

But when I ran it from a different project:

```bash
cd ~/fileZ/ai/weblab-mcp
ql chat
# ❌ Mentor has amnesia
```

## The Symptom

I asked the Mentor to simulate handling a tech debt report. Instead of the detailed workflow I expected—clarifying questions, spec decisions, GitHub issue creation—it gave me a generic response. No knowledge of QL commands. No understanding of our conventions.

It had forgotten who it was.

## The Debugging Session

Here's where it gets meta. I started debugging **with** the broken AI:

**Me:** "You're not acting like you know AGENTS.md. What's going on?"

**Mentor:** "Let me check how I load knowledge..."

The Mentor—despite being broken—walked through its own code with me:

```python
def load_agents_md() -> str:
    """Load AGENTS.md content."""
    agents_path = Path.cwd() / "AGENTS.md"  # 👈 THE BUG
    if agents_path.exists():
        return agents_path.read_text()
    return ""
```

**The bug:** `Path.cwd()` returns where the user runs the command, not where the code lives.

- Running from `~/quick-launch/` → finds `~/quick-launch/AGENTS.md` ✅
- Running from `~/weblab-mcp/` → looks for `~/weblab-mcp/AGENTS.md` ❌

## The Self-Healing Moment

The Mentor proposed its own fix:

```python
# QL installation directory (where this code lives)
QL_ROOT = Path(__file__).parent.parent.parent

def load_agents_md() -> str:
    content_parts = []
    
    # 1. Always load QL's AGENTS.md (core knowledge)
    ql_agents_path = QL_ROOT / "AGENTS.md"
    if ql_agents_path.exists():
        content_parts.append(ql_agents_path.read_text())
    
    # 2. Also load project's AGENTS.md if different
    cwd_agents_path = Path.cwd() / "AGENTS.md"
    if cwd_agents_path.exists() and cwd_agents_path.resolve() != ql_agents_path.resolve():
        content_parts.append(f"""
---
## Current Project: {Path.cwd().name}

**IMPORTANT: Project-specific rules take precedence.**

{cwd_agents_path.read_text()}
""")
    
    return "".join(content_parts)
```

**The fix does two things:**
1. **Always loads QL's AGENTS.md** from the installation directory (using `__file__`)
2. **Also loads the current project's AGENTS.md** if you're in a different project

Now running from any directory works:

| Directory | Knowledge Loaded |
|-----------|-----------------|
| `~/` | QL core only |
| `~/quick-launch/` | QL core (same file) |
| `~/weblab-mcp/` | QL core + weblab-mcp rules |

## The Victory Lap

After implementing the fix, I tested it:

```bash
cd ~/fileZ/ai/weblab-mcp
ql chat
```

Asked the same question about tech debt handling. This time? Perfect response. Detailed workflow. Proper tool usage. It remembered everything.

The GitHub issue I created for this bug?

```
GH#91: Mentor doesn't know AGENTS.md

Closed by: 🤖 Self-fixed! Mentor diagnosed its own 
missing knowledge and implemented the fix.
```

## Lessons Learned

### 1. `Path.cwd()` vs `Path(__file__)`

This is a classic Python gotcha:

```python
Path.cwd()      # Where user runs command FROM
Path(__file__)  # Where the Python file IS
```

For loading project resources, almost always use `__file__`.

### 2. Test From Multiple Directories

```bash
# Don't just test from project root
cd /tmp && your-tool
cd ~/other-project && your-tool
```

If it breaks, you have path resolution bugs.

### 3. AI Can Debug Its Own Code

Even a "broken" AI retains enough reasoning to help diagnose issues. The Mentor couldn't access its knowledge file, but it could still:
- Read its own source code
- Identify the path resolution bug  
- Propose and implement a fix

That's... kind of amazing?

## The Meta Moment

The most surreal part: I'm writing this blog post with assistance from the same AI that just fixed itself. It's now helping me document its own debugging session.

```
┌─────────────────────────────────────────┐
│  GH#91: Mentor doesn't know AGENTS.md   │
│                                         │
│  Reported by: Sergio                    │
│  Diagnosed by: Mentor (broken)          │
│  Fixed by: Mentor (broken)              │
│  Verified by: Mentor (working!)         │
│  Documented by: Mentor (meta!)          │
└─────────────────────────────────────────┘
```

The AI performed surgery on its own brain while conscious.

---

*The code is open source at [NightOwlCoder/quick-launch](https://github.com/NightOwlCoder/quick-launch). The specific fix is in [this commit](https://github.com/NightOwlCoder/quick-launch/commit/f5de724).*
