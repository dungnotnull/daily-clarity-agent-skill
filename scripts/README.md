# Scripts Reference — Daily Clarity Agent

## Script Index

| Script | Purpose |
|---|---|
| `utils.py` | Shared utilities |
| `mode_detector.py` | Detect session mode (VENT/PATTERN/HABIT/WEEKLY_REVIEW/OPEN) + safety flags |
| `pattern_matcher.py` | Match user text against the pattern library (22 patterns) |
| `habit_suggester.py` | Suggest micro-habits based on stated goal area (8 goal areas) |

## Usage

### Detect session mode and safety flags (run FIRST, always)

```bash
python scripts/mode_detector.py --text "I keep procrastinating and I don't know why"
```

This is the most important script — it determines:
- Whether crisis protocol is needed (overrides everything else)
- Which session mode to use (VENT, PATTERN, HABIT, WEEKLY_REVIEW, OPEN)
- Emotional register to calibrate tone
- Pattern dimensions to explore (if PATTERN mode)

**Always run this first.** If `has_safety_concern` is true, follow
`references/emotional-safety.md` immediately — do not proceed to pattern
matching or habit suggestions until safety is addressed.

### Match patterns (use in PATTERN mode)

```bash
python scripts/pattern_matcher.py --text "I always feel anxious on Sunday nights before work"
```

Returns potential pattern matches with references to `pattern-library.md`.
Only use the TOP match, and only after the user has been heard — frame as
"I wonder if..." never as fact.

### Suggest micro-habits (use in HABIT mode, AFTER asking permission)

```bash
python scripts/habit_suggester.py --text "I want to sleep better but nothing works"
```

Returns 1-3 micro-habit suggestions for the detected goal area.
Always ask "want to hear an idea?" before sharing.

## Full Workflow Example

```bash
# Step 1: Always start here
python scripts/mode_detector.py --text "$USER_MESSAGE" --json

# If safety concern → stop, use emotional-safety.md protocol

# If mode == PATTERN:
python scripts/pattern_matcher.py --text "$USER_MESSAGE" --json

# If mode == HABIT (and user wants suggestions):
python scripts/habit_suggester.py --text "$USER_MESSAGE" --json
```

## Important Notes

- These scripts are **signal detectors**, not decision-makers. They surface
  possibilities for the agent to consider — the agent (Claude) makes the
  final judgment about tone, timing, and what to actually say.
- Scripts never generate the actual response text — that's the agent's job,
  guided by `references/conversation-techniques.md`.
- No data is stored between sessions by these scripts — this skill does not
  maintain a persistent journal or database (by design — see PROJECT-detail.md).
