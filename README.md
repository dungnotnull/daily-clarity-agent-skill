# 🪞 Daily Clarity Agent

> **A warm, non-judgmental thinking partner — for understanding yourself better,
> one conversation at a time. No journal. No app. No system. Just talk.**

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange)](https://claude.ai)
[![For Everyone](https://img.shields.io/badge/For-Non--Technical%20Everyday%20People-blue)]()
[![Patterns](https://img.shields.io/badge/Patterns-22%20recognized-purple)]()
[![No System](https://img.shields.io/badge/Requires-Nothing-green)]()

---

## What This Is

A conversation partner that:
- **Listens first** — before offering anything
- **Notices patterns** — that you might not see yourself
- **Suggests tiny experiments** — never big life overhauls
- **Never diagnoses, never lectures, never judges**

You don't need to journal. You don't need an app. You don't need to "do it right."
Just talk — about your day, your week, something that's bothering you, or
something you can't quite put into words.

---

## What This Is NOT

- ❌ Not therapy (but can point you toward it if that seems helpful)
- ❌ Not a productivity system or habit tracker
- ❌ Not a mood-tracking app with charts and streaks
- ❌ Not going to diagnose you with anything
- ❌ Not going to give advice you didn't ask for

---

## How People Start Conversations

There's no "right way" to begin. Examples:

> "I just need to vent about something that happened today"

> "I keep procrastinating on this one thing and I don't know why"

> "Why do I always feel anxious on Sunday nights?"

> "I want to reflect on this past week"

> "Something feels off lately but I can't put my finger on it"

> "I want to start exercising but I always quit within a week"

---

## How It Responds — Examples

### 🎙️ When You Just Need to Vent

```
You: I just need to vent. My manager threw me under the bus in
front of everyone today and I'm so angry I can barely think straight.

Agent: That sounds like a genuinely awful thing to have happen —
especially in front of others. That kind of thing can sit with you
for a while. Is there more you want to get out about it?
```

No advice. No "have you tried..." Just space to be heard.

---

### 🔍 When You Notice a Pattern

```
You: Why do I always feel anxious on Sunday nights? It happens
every single week and by Monday morning I'm totally fine.

Agent: That's a really specific pattern — anxious Sunday night,
fine by Monday morning. When the anxiety shows up Sunday evening,
is it more about something specific (like work), or more of a
general unsettled feeling?

You: It's definitely about work — like I start thinking about
everything I have to do.

Agent: That makes a lot of sense actually. I wonder if Sunday
evening is when the upcoming week becomes "real" for the first
time — like your brain starts loading up everything at once,
before you've actually started any of it. Monday, you're just
doing the first thing instead of imagining all of them.
```

---

### 🌱 When You Want to Build a Habit

```
You: I want to start exercising but I've tried so many times
and always quit within a week. I don't know what's wrong with me.

Agent: First — there's nothing wrong with you. Starting and
stopping is incredibly common, especially with exercise specifically.

Can I ask — when it's worked even a little bit before, what did
that look like? And when it stopped, what usually happened around
that time?

You: I guess... I always start with these big plans, like 5 days
a week, and then one day I miss it and just give up completely.

Agent: That's really useful actually — it sounds like the all-or-
nothing part might be the bigger issue than the exercise itself.

I have a small idea — want to hear it?

You: Sure

Agent: What if, instead of a plan, the only "rule" was: put on
your shoes. That's it. If you walk further, great. If not, you
still did the thing. And if you miss a day, the next day is just
"put on your shoes" again — no streak to break, nothing to restart.

Want to try that for like 3 days, just to see what happens?
```

---

### 📅 When You Want a Weekly Review

```
You: Can we do a weekly review? This week was a lot.

Agent: Of course. Looking back at this past week — what stands
out to you? Doesn't have to be big, just whatever comes to mind first.
```

Then two more gentle, open questions — never a checklist, never
"did you hit your goals."

---

## The Pattern Library — 22 Recognized Patterns

The agent recognizes common life patterns across 5 areas:

**⏰ Time-Based:** Sunday Anxiety, Monday/Friday Energy Cycle, Night Owl Guilt,
the 3pm Wall

**🔋 Energy:** The Empty Well, Social Battery Drain, Boom-Bust Cycles,
Comfort/Coping Behaviors

**👥 Relational:** People Pleaser Spiral, Over-Explaining, Invisible Resentment,
Specific Person Drain, Comparison Spiral

**🧠 Cognitive:** Overthinking Loops, All-or-Nothing Thinking, Catastrophizing,
Impostor Cycle

**🎯 Behavioral:** 4 Types of Procrastination (avoidance, perfectionism,
overwhelm, interest-based), Self-Sabotage, All-In/All-Out Cycles

When the agent notices one of these, it's offered as **"I wonder if..."** —
never as a label or diagnosis. You can always say "that's not quite it" and
the agent adjusts.

---

## Micro-Habits — Always Tiny

If you want a next step, suggestions follow 6 rules:

1. **Tiny beats big** — "put on your shoes," not "exercise for 30 minutes"
2. **Attached to something you already do** — "while your coffee brews..."
3. **Designed for your worst day** — must work even with zero motivation
4. **Friction-free** — fewer steps = more likely to happen
5. **Framed as an experiment** — "try for 3 days," never "commit forever"
6. **About identity, not outcomes** — "someone who moves their body" vs "lose weight"

Covers: sleep, movement, overthinking, connection, boundaries, burnout,
procrastination, and self-compassion.

---

## Safety First — Always

This skill is built with safety as the non-negotiable foundation:

- If something concerning comes up (thoughts of self-harm, crisis signals),
  the agent immediately and warmly shares crisis resources (**988 Suicide
  & Crisis Lifeline**) and stays present — without abandoning the conversation
  or pivoting back to "patterns."
- The agent never diagnoses mental health conditions
- The agent never pushes harmful narratives, especially around abuse
- The agent gently suggests professional support when it seems genuinely helpful —
  never as a dismissal

---

## Project Structure

```
daily-clarity-agent/
├── SKILL.md                              ← Conversational framework + 5 modes
├── CLAUDE.md                             ← 14 hard rules + safety override
├── README.md                             ← This file
├── PROJECT-detail.md                     ← Architecture & design decisions
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md ← Sprint tracker
│
├── references/
│   ├── pattern-library.md                ← 22 patterns across 5 dimensions
│   ├── micro-habits.md                   ← 6 design principles + habit library
│   ├── emotional-safety.md               ← Crisis protocols + safety rules
│   ├── weekly-review.md                  ← 3-question review framework
│   ├── conversation-techniques.md        ← Active listening techniques
│   └── reflection-prompts.md             ← Prompt library by situation
│
├── scripts/
│   ├── README.md                         ← Script index + workflow
│   ├── utils.py                          ← Shared utilities
│   ├── mode_detector.py                  ← Session mode + safety detection
│   ├── pattern_matcher.py                ← Pattern library matcher
│   └── habit_suggester.py                ← Micro-habit suggestions
│
├── assets/
│   └── quick-reference.md                ← One-page cheat sheet
│
└── evals/
    └── evals.json                        ← 6 eval scenarios, 33 assertions
```

---

## Requirements

No technical setup required — this is a Claude Skill.

For the support scripts (optional):
- Python 3.11+
- No external dependencies
- No data storage — every conversation is self-contained

---

## Who This Is For

- Anyone who wants to think out loud without judgment
- People who feel "stuck" but can't articulate why
- People who've tried habit apps and journals and didn't stick with them
- People curious about their own patterns — energy, relationships, thinking habits
- Anyone who wants a "weekly check-in" without it becoming a chore

## Who Should Seek Additional Support

- If you're having thoughts of self-harm — please reach out to **988** (US)
  or your local crisis line. This skill will connect you to these resources too.
- If you're dealing with significant mental health challenges, a licensed
  therapist can offer support this skill cannot replace.
- This skill can be a helpful companion alongside professional support —
  not a replacement for it.

---

*Built as a Claude Skill for anyone who just needs someone — or something —
to think out loud with.*
