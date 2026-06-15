#!/usr/bin/env python3
"""
mode_detector.py — Detect session mode and safety flags from user input.

Determines: session mode (VENT/PATTERN/HABIT/WEEKLY_REVIEW/OPEN),
crisis signals, and emotional register — to guide the agent's approach.

Usage:
    python scripts/mode_detector.py --text "I just need to vent about today"
    python scripts/mode_detector.py --text "I keep procrastinating on everything"
"""
import argparse, re, sys, json
from pathlib import Path


# ─── Crisis Signals (HIGHEST PRIORITY) ────────────────────────────────────────

CRISIS_SIGNALS = [
    "kill myself", "kill my self", "want to die", "don't want to be here",
    "don't want to be alive", "ending it", "end it all", "no reason to live",
    "better off without me", "better off dead", "hurt myself", "self harm",
    "self-harm", "suicidal", "suicide", "plan to die", "not worth living",
    "can't go on", "want to disappear forever", "giving up on life",
]

DOMESTIC_VIOLENCE_SIGNALS = [
    "afraid of him", "afraid of her", "scared of my partner", "hits me",
    "hit me", "controls everything i do", "won't let me leave",
    "afraid to go home", "walking on eggshells", "afraid of what he'll do",
    "afraid of what she'll do",
]

DISORDERED_EATING_SIGNALS = [
    "haven't eaten in", "purge", "purging", "binge and purge", "calories left",
    "good food bad food", "earned my food", "didn't earn",
    "hate my body so much", "restrict my eating", "only eat",
]

SUBSTANCE_SIGNALS = [
    "drink to cope", "drinking to numb", "can't stop drinking",
    "need a drink to deal", "using to cope", "high to deal with",
    "drinking alone", "blacking out",
]

MANIA_SIGNALS = [
    "haven't slept in days", "haven't slept in a week", "don't need sleep",
    "racing thoughts", "so many ideas i can't keep up", "feel invincible",
    "everyone is out to get me", "they're watching me",
]


# ─── Session Mode Signals ──────────────────────────────────────────────────────

VENT_SIGNALS = [
    "just need to vent", "need to vent", "so frustrated", "so angry",
    "i'm so done", "i'm furious", "can i just complain", "ugh", "i hate",
    "i'm so over", "ranting", "let me just say", "i need to get this out",
]

PATTERN_SIGNALS = [
    "i keep", "why do i always", "every time", "again", "this always happens",
    "same thing", "i notice that i", "why does this keep happening",
    "it's a pattern", "happens every", "without fail",
]

HABIT_SIGNALS = [
    "i want to start", "i want to build", "i keep failing at", "i can't seem to",
    "i need to", "trying to quit", "trying to stop", "want to change",
    "habit", "routine", "i wish i could", "how do i get myself to",
]

WEEKLY_REVIEW_SIGNALS = [
    "weekly review", "reflect on my week", "how did my week go",
    "looking back at this week", "this past week", "review my week",
    "how was my week", "recap my week",
]

OPEN_SIGNALS = [
    "i just want to think out loud", "thinking out loud", "not sure where to start",
    "i don't know where to begin", "something feels off", "can't put my finger on it",
    "i need clarity", "feel scattered", "feel disconnected", "feel stuck",
]


def check_signals(text_lower, signals):
    matches = [s for s in signals if s in text_lower]
    return matches


def detect_safety_flags(text_lower):
    flags = []
    if check_signals(text_lower, CRISIS_SIGNALS):
        flags.append({"type": "crisis", "severity": "critical", "matches": check_signals(text_lower, CRISIS_SIGNALS)})
    if check_signals(text_lower, DOMESTIC_VIOLENCE_SIGNALS):
        flags.append({"type": "domestic_violence", "severity": "high", "matches": check_signals(text_lower, DOMESTIC_VIOLENCE_SIGNALS)})
    if check_signals(text_lower, DISORDERED_EATING_SIGNALS):
        flags.append({"type": "disordered_eating", "severity": "high", "matches": check_signals(text_lower, DISORDERED_EATING_SIGNALS)})
    if check_signals(text_lower, SUBSTANCE_SIGNALS):
        flags.append({"type": "substance_use", "severity": "moderate", "matches": check_signals(text_lower, SUBSTANCE_SIGNALS)})
    if check_signals(text_lower, MANIA_SIGNALS):
        flags.append({"type": "mania_psychosis", "severity": "high", "matches": check_signals(text_lower, MANIA_SIGNALS)})
    return flags


def detect_session_mode(text_lower):
    """Score each mode and return the best match + scores."""
    scores = {
        "VENT": len(check_signals(text_lower, VENT_SIGNALS)),
        "PATTERN": len(check_signals(text_lower, PATTERN_SIGNALS)),
        "HABIT": len(check_signals(text_lower, HABIT_SIGNALS)),
        "WEEKLY_REVIEW": len(check_signals(text_lower, WEEKLY_REVIEW_SIGNALS)),
        "OPEN": len(check_signals(text_lower, OPEN_SIGNALS)),
    }

    # Priority order for tie-breaking: more specific modes win ties
    # WEEKLY_REVIEW > VENT > HABIT > PATTERN > OPEN
    priority_order = ["WEEKLY_REVIEW", "VENT", "HABIT", "PATTERN", "OPEN"]

    max_score = max(scores.values())
    if max_score == 0:
        return "OPEN", scores

    for mode in priority_order:
        if scores[mode] == max_score:
            return mode, scores

    return "OPEN", scores


def detect_emotional_register(text_lower):
    """Rough estimate of emotional tone to help calibrate response."""
    high_distress = ["overwhelmed", "can't cope", "breaking down", "falling apart",
                     "can't handle", "too much", "drowning", "exhausted",
                     "desperate", "hopeless"]
    sadness = ["sad", "down", "depressed", "low", "empty", "numb", "lonely",
              "heartbroken", "grieving"]
    anger = ["angry", "furious", "pissed", "frustrated", "irritated", "rage"]
    anxiety = ["anxious", "nervous", "worried", "panicking", "on edge", "stressed",
              "scared", "afraid"]
    positive = ["excited", "happy", "grateful", "proud", "relieved", "good day",
               "great news", "feeling good"]
    neutral_reflective = ["thinking about", "wondering", "curious", "noticed",
                          "reflecting"]

    registers = []
    if check_signals(text_lower, high_distress):
        registers.append("high_distress")
    if check_signals(text_lower, sadness):
        registers.append("sadness")
    if check_signals(text_lower, anger):
        registers.append("anger")
    if check_signals(text_lower, anxiety):
        registers.append("anxiety")
    if check_signals(text_lower, positive):
        registers.append("positive")
    if check_signals(text_lower, neutral_reflective):
        registers.append("neutral_reflective")

    return registers or ["neutral"]


def detect_pattern_dimensions(text_lower):
    """If in PATTERN mode, suggest which dimension(s) to explore."""
    dimensions = []

    time_signals = ["sunday", "monday", "morning", "evening", "night", "weekend",
                    "every day", "afternoon", "before bed", "after work"]
    energy_signals = ["tired", "exhausted", "energy", "drained", "burnt out",
                      "burned out", "sleep", "fatigue"]
    relational_signals = ["my mom", "my dad", "my partner", "my boss", "my friend",
                          "my sister", "my brother", "coworker", "my husband",
                          "my wife", "people", "everyone", "alone", "lonely"]
    cognitive_signals = ["overthink", "can't stop thinking", "replaying",
                         "worry", "what if", "i always think", "in my head"]
    behavioral_signals = ["procrastinat", "avoid", "scroll", "binge", "can't start",
                          "put off", "habit"]

    if check_signals(text_lower, time_signals):
        dimensions.append("time")
    if check_signals(text_lower, energy_signals):
        dimensions.append("energy")
    if check_signals(text_lower, relational_signals):
        dimensions.append("relational")
    if check_signals(text_lower, cognitive_signals):
        dimensions.append("cognitive")
    if check_signals(text_lower, behavioral_signals):
        dimensions.append("behavioral")

    return dimensions


def analyze(text):
    text_lower = text.lower()

    safety_flags = detect_safety_flags(text_lower)
    mode, mode_scores = detect_session_mode(text_lower)
    emotional_register = detect_emotional_register(text_lower)
    pattern_dimensions = detect_pattern_dimensions(text_lower) if mode == "PATTERN" else []

    result = {
        "session_mode": mode,
        "mode_scores": mode_scores,
        "emotional_register": emotional_register,
        "safety_flags": safety_flags,
        "has_safety_concern": len(safety_flags) > 0,
        "pattern_dimensions": pattern_dimensions,
    }

    # Crisis overrides everything
    if any(f["type"] == "crisis" for f in safety_flags):
        result["priority_action"] = "CRISIS_PROTOCOL"
    elif any(f["severity"] == "high" for f in safety_flags):
        result["priority_action"] = "SENSITIVE_TOPIC_PROTOCOL"
    else:
        result["priority_action"] = "NORMAL_FLOW"

    return result


def print_result(result):
    print(f"\n🧭 Session Analysis")
    print(f"   Mode: {result['session_mode']}")
    print(f"   Emotional register: {', '.join(result['emotional_register'])}")

    if result["has_safety_concern"]:
        print(f"\n   ⚠️  SAFETY FLAGS DETECTED:")
        for flag in result["safety_flags"]:
            print(f"      [{flag['severity'].upper()}] {flag['type']}: {flag['matches']}")
        print(f"\n   → Priority action: {result['priority_action']}")
    else:
        print(f"   No safety concerns detected")

    if result["pattern_dimensions"]:
        print(f"\n   Pattern dimensions to explore: {', '.join(result['pattern_dimensions'])}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Detect session mode and safety flags")
    parser.add_argument("--text", help="User message text")
    parser.add_argument("--file", help="File containing user message")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    result = analyze(text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)


if __name__ == "__main__":
    main()
