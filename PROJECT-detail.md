# PROJECT-detail.md — Daily Clarity Agent

## Problem Definition

### The Reflection Gap for Non-Tech Users

Millions of people feel "off" — stuck, scattered, exhausted, stuck in cycles —
but have no accessible way to process this:

- **Journaling apps** require a habit they probably won't keep, plus they're
  one more app, one more system, one more thing to feel guilty about not doing
- **Therapy** is expensive, has waitlists, and feels like "too big a step" for
  "I'm just feeling kind of off lately"
- **Generic AI chat** can listen, but without guidance it either:
  - Jumps to generic advice ("have you tried meditation?")
  - Uses clinical/therapy-speak that feels cold or performative
  - Asks too many questions at once, feeling like an interrogation
  - Diagnoses things it shouldn't ("this sounds like ADHD")
  - Offers big habit changes that fail in 3 days, adding to the pile of failures

**The gap:** Something between "venting to a friend" and "seeing a therapist" —
a reflection partner that's always available, genuinely listens, helps surface
patterns the person might not see themselves, and — if wanted — suggests something
so small it's almost impossible not to do.

---

## What Makes This Different From Existing Tools

### vs Journaling Apps (Day One, Reflectly, etc.)
Journaling apps require: opening the app, writing something, often daily.
This skill requires: nothing. No format. No frequency. No history to maintain.
The user can show up once and never again, or every day — no judgment either way.

### vs AI Therapy Apps (Woebot, Wysa, etc.)
AI therapy apps often use CBT worksheets, mood tracking, structured modules.
This skill has zero structure imposed on the user — it's conversation, not
a program. It also explicitly avoids therapy-speak and clinical framing.

### vs Generic ChatGPT/Claude
Generic AI lacks:
- The "reflect before redirect" discipline (jumps to advice)
- The "one question at a time" discipline (interrogates)
- The "I wonder if" framing discipline (states opinions as facts)
- The crisis safety protocol (might miss or mishandle crisis signals)
- The micro-habit sizing discipline (suggests "30 minutes of meditation")
- Pattern library knowledge (doesn't recognize "Sunday Scaries" as a named pattern
  with known dynamics)

This skill encodes all of these as explicit, tested rules.

---

## Architecture: Conversation-First, Not Workflow-First

Unlike other skills in this family (API Contract Guardian, Life Navigator Agent),
this skill has NO rigid multi-phase harness with mandatory outputs.

```
Other skills:           This skill:

Phase 1 -> Phase 2 ->    Conversation
Phase 3 -> Output             |
(deterministic           Mode detection
pipeline)                     |
                          Reflection
                         (adaptive, human)
```

The "harness" here is a set of RULES (in CLAUDE.md) and REFERENCE KNOWLEDGE
(pattern library, micro-habits, etc.) — not a pipeline that produces a
standardized document.

This is intentional: rigid structure would work against the goal of feeling
like a real conversation with someone who cares.

---

## The Mode Detection System

Five modes, detected via `scripts/mode_detector.py`:

```
VENT           - User needs to express before processing
PATTERN        - User notices a recurring issue
HABIT          - User wants to build/break a behavior
WEEKLY_REVIEW  - User wants structured reflection on a period
OPEN           - Default - exploratory, no clear category yet
```

Mode detection is a SUGGESTION to the agent, not a rigid classification.
A conversation can shift modes mid-stream — someone might start venting (VENT)
and naturally move into noticing a pattern (PATTERN) as they talk.

---

## The Pattern Library — 22 Patterns, 5 Dimensions

```
TIME-BASED (4 patterns)
  Sunday Anxiety, Monday/Friday Cycle, Night Owl Guilt, 3pm Wall

ENERGY (4 patterns)
  Empty Well, Social Battery Drain, Boom-Bust Cycle, Comfort Behaviors

RELATIONAL (5 patterns)
  People Pleaser, Over-Explainer, Resentment Build,
  Specific Person Drain, Comparison Spiral

COGNITIVE (4 patterns)
  Overthinking Loop, All-or-Nothing, Catastrophizing, Impostor Cycle

BEHAVIORAL (5 patterns)
  4 Procrastination Types, Self-Sabotage, All-In/All-Out
```

Each pattern includes:
- **Signals** — phrases that suggest this pattern
- **What's usually happening** — the underlying dynamic (non-clinical explanation)
- **Gentle reflection** — example phrasing using "I wonder if" framing
- **Micro-habit direction** — if relevant, what small experiment might help

### Why 4 Procrastination Types?

Procrastination is often treated as one thing ("just do it"), but the underlying
cause varies enormously and requires different approaches:

- **Avoidance** -> make starting easier
- **Perfectionism** -> permission for bad first drafts
- **Overwhelm** -> narrow to ONE thing
- **Interest-based (ADHD-adjacent)** -> create artificial urgency/novelty

Recognizing WHICH type lets the reflection actually land, rather than offering
generic "just start small" advice that doesn't address the real mechanism.

---

## The Micro-Habit System

### 6 Design Principles (encoded in `references/micro-habits.md`)

1. Tiny beats big
2. Attach to existing (habit stacking)
3. Design for the worst day
4. Remove friction
5. Experiment frame, not commitment
6. Identity over outcome

### 8 Goal Areas (encoded in `scripts/habit_suggester.py`)

```
sleep, movement, overthinking, connection, boundaries,
energy_burnout, procrastination, self_compassion
```

Each goal area has 2-3 pre-designed micro-habit suggestions that follow
all 6 principles — tested against the "would someone actually do this
on their worst day?" standard.

---

## The Safety System — Non-Negotiable Priority

`scripts/mode_detector.py` checks FIVE safety categories on every input:

```
1. Crisis (suicidal ideation, self-harm) - CRITICAL severity
2. Domestic violence indicators - HIGH severity
3. Disordered eating signals - HIGH severity
4. Substance use crisis - MODERATE severity
5. Mania/psychosis indicators - HIGH severity
```

If ANY critical or high-severity flag is detected, the agent MUST follow
`references/emotional-safety.md` protocols BEFORE anything else — overriding
mode detection, pattern matching, habit suggestions, everything.

### Why This Architecture?

A reflection tool that's "warm and non-judgmental" could, without careful design,
accidentally:
- Engage with someone in crisis as if discussing a "pattern" (catastrophic)
- Offer a "micro-habit" for someone describing disordered eating (harmful)
- Reflect "I wonder if this connects to feeling like a burden" to someone with
  active suicidal ideation (could reinforce harmful narrative)

The safety system is the load-bearing wall of this entire skill. Everything else
is built around it, never in spite of it.

---

## The Weekly Review Framework

Three questions, deliberately scoped:

```
Q1: What happened?     (open-ended, "doesn't have to be big")
Q2: How did it feel?   (emotional layer + "surprisingly good" contrast)
Q3: What do you want?  (10% better - deliberately limited scope)
```

The "10% better" framing in Q3 is critical — it prevents the review from
becoming a goal-setting session with unrealistic targets, which would
undermine the low-pressure nature of the tool.

---

## What This Skill Explicitly Refuses To Do

- **No mood tracking with numbers/charts** — turns feelings into data points,
  which can create unhealthy relationships with emotions ("I'm only a 4 today")
- **No streaks or consistency metrics** — directly undermines "no pressure" promise
- **No "insights dashboard"** — each conversation stands alone; no
  cross-session pattern storage (privacy + pressure reasons)
- **No personality quizzes or typing** (MBTI, enneagram, etc.) — would
  contradict the individualized, non-categorizing approach

---

## Future Roadmap

### v1.1
- [ ] Expand pattern library to 35+ patterns (add: grief patterns, transition
  patterns, seasonal patterns)
- [ ] Add more goal areas to habit suggester (eating habits — carefully,
  finances, creative work)
- [ ] Refine crisis signal detection based on real conversation data

### v1.2
- [ ] Cultural adaptation notes — how patterns may manifest differently
  across cultural contexts
- [ ] Multi-session continuity (OPT-IN only) — "would you like me to remember
  this for next time?" with explicit consent each time

### v2.0
- [ ] Couples/family reflection mode (two-perspective conversations)
- [ ] Integration with calendar context (optional) — "I notice you mentioned
  feeling anxious before meetings — want to look at your calendar together?"
