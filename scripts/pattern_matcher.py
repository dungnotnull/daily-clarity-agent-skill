#!/usr/bin/env python3
"""
pattern_matcher.py — Match user descriptions against the pattern library.

Suggests which patterns from references/pattern-library.md might be relevant,
to help the agent choose the right gentle reflection.

Usage:
    python scripts/pattern_matcher.py --text "I always feel anxious on Sunday nights"
    python scripts/pattern_matcher.py --text "I keep saying yes to things I don't want to do"
"""
import argparse, re, sys, json
from pathlib import Path


# ─── Pattern Signal Library ───────────────────────────────────────────────────
# Maps to entries in references/pattern-library.md

PATTERNS = {
    "sunday_anxiety": {
        "name": "Sunday Anxiety / Sunday Scares",
        "category": "time",
        "signals": ["sunday", "sunday night", "sunday evening", "dread the week",
                    "weekend is over", "sunday scaries", "before monday"],
        "ref": "pattern-library.md#sunday-anxiety--sunday-scaries",
    },
    "monday_friday_cycle": {
        "name": "Monday Energy vs Friday Crash",
        "category": "time",
        "signals": ["monday i'm motivated", "by friday i'm exhausted",
                    "start strong", "burned out by end of week", "crash by friday"],
        "ref": "pattern-library.md#monday-energy-vs-friday-crash",
    },
    "night_owl_guilt": {
        "name": "Night Owl Guilt",
        "category": "time",
        "signals": ["best work at night", "night person", "can't wake up early",
                    "everyone says i should go to bed earlier", "more productive late"],
        "ref": "pattern-library.md#night-owl-guilt",
    },
    "afternoon_wall": {
        "name": "The 3pm Wall",
        "category": "energy",
        "signals": ["3pm", "afternoon slump", "after lunch", "afternoon crash",
                    "need coffee in the afternoon", "useless after lunch"],
        "ref": "pattern-library.md#the-3pm-wall",
    },
    "empty_well": {
        "name": "The Empty Well (Chronic Exhaustion)",
        "category": "energy",
        "signals": ["always tired", "exhausted all the time", "running on empty",
                    "sleep but it doesn't help", "no energy for anything",
                    "tired no matter what"],
        "ref": "pattern-library.md#the-empty-well",
    },
    "social_battery": {
        "name": "Social Battery Drain",
        "category": "energy",
        "signals": ["exhausted after socializing", "need to recover after seeing people",
                    "social battery", "drained after being around people",
                    "love people but exhausted afterward"],
        "ref": "pattern-library.md#the-social-battery-drain",
    },
    "boom_bust_energy": {
        "name": "Boom-Bust Energy Cycle",
        "category": "energy",
        "signals": ["go hard then crash", "either obsessed or not at all",
                    "high energy then nothing", "all or nothing energy"],
        "ref": "pattern-library.md#the-boom-bust-energy-cycle",
    },
    "comfort_behaviors": {
        "name": "Comfort/Coping Behaviors",
        "category": "energy",
        "signals": ["stress eat", "emotional eating", "scroll when stressed",
                    "shop when i'm upset", "drink when stressed",
                    "comfort food when anxious"],
        "ref": "pattern-library.md#emotional-eating--comfort-behavior-patterns",
    },
    "people_pleaser": {
        "name": "People Pleaser Spiral",
        "category": "relational",
        "signals": ["say yes when i mean no", "feel guilty saying no",
                    "always the one who adjusts", "don't want to disappoint",
                    "can't say no", "afraid to upset"],
        "ref": "pattern-library.md#the-people-pleaser-spiral",
    },
    "over_explainer": {
        "name": "The Over-Explainer",
        "category": "relational",
        "signals": ["always justify myself", "explain myself too much",
                    "give long reasons", "feel like i need a reason"],
        "ref": "pattern-library.md#the-over-explainer",
    },
    "resentment_build": {
        "name": "Invisible Resentment Build",
        "category": "relational",
        "signals": ["feel resentful but don't know why", "everything is fine but i'm angry",
                    "irritable lately", "snapping at people", "feel bitter"],
        "ref": "pattern-library.md#the-invisible-resentment-build",
    },
    "specific_person_drain": {
        "name": "Specific Person Energy Drain",
        "category": "relational",
        "signals": ["exhausted after talking to", "drained after seeing",
                    "dread talking to", "anxious around", "walk on eggshells with"],
        "ref": "pattern-library.md#specific-person-energy-drain",
    },
    "comparison_spiral": {
        "name": "The Comparison Spiral",
        "category": "relational",
        "signals": ["everyone else has it together", "feel behind compared to",
                    "comparing myself to", "feel inadequate when i see",
                    "social media makes me feel"],
        "ref": "pattern-library.md#the-comparison-spiral",
    },
    "overthinking_loop": {
        "name": "The Overthinking Loop",
        "category": "cognitive",
        "signals": ["can't turn my brain off", "keep replaying", "going over it again",
                    "can't stop thinking about", "overthinking", "ruminating",
                    "mind won't quiet down"],
        "ref": "pattern-library.md#the-overthinking-loop",
    },
    "all_or_nothing": {
        "name": "All-or-Nothing Thinking",
        "category": "cognitive",
        "signals": ["i always", "i never", "all or nothing", "if i can't do it perfectly",
                    "might as well give up", "ruined it so why bother"],
        "ref": "pattern-library.md#all-or-nothing-thinking",
    },
    "catastrophizing": {
        "name": "Future Catastrophizing",
        "category": "cognitive",
        "signals": ["worst case scenario", "what if everything goes wrong",
                    "worried that if", "spiral about the future",
                    "imagining the worst"],
        "ref": "pattern-library.md#future-catastrophizing",
    },
    "impostor_cycle": {
        "name": "The Impostor Cycle",
        "category": "cognitive",
        "signals": ["don't know why they picked me", "feel like a fraud",
                    "got lucky", "waiting for someone to realize i'm not good enough",
                    "impostor", "don't deserve this"],
        "ref": "pattern-library.md#the-impostor-cycle",
    },
    "procrastination_avoidance": {
        "name": "Procrastination — Avoidance Type",
        "category": "behavioral",
        "signals": ["avoiding", "putting off", "dread doing", "know what to do but avoid it"],
        "ref": "pattern-library.md#procrastination-types-very-different",
    },
    "procrastination_perfectionism": {
        "name": "Procrastination — Perfectionism Type",
        "category": "behavioral",
        "signals": ["won't start until i know it's right", "research instead of doing",
                    "planning instead of starting", "has to be perfect"],
        "ref": "pattern-library.md#procrastination-types-very-different",
    },
    "procrastination_overwhelm": {
        "name": "Procrastination — Overwhelm Type",
        "category": "behavioral",
        "signals": ["too much to do so i do nothing", "paralyzed by my to-do list",
                    "don't know where to start so i don't"],
        "ref": "pattern-library.md#procrastination-types-very-different",
    },
    "procrastination_interest": {
        "name": "Procrastination — Interest-Based Type",
        "category": "behavioral",
        "signals": ["only do things last minute", "can't focus unless it's urgent",
                    "do well under pressure but never before",
                    "not living up to my potential"],
        "ref": "pattern-library.md#procrastination-types-very-different",
    },
    "self_sabotage": {
        "name": "The Self-Sabotage Pattern",
        "category": "behavioral",
        "signals": ["mess it up when things go well", "got close then ruined it",
                    "self sabotage", "don't know why i do this to myself",
                    "blow it right before something good"],
        "ref": "pattern-library.md#the-self-sabotage-pattern",
    },
    "all_in_all_out": {
        "name": "All-In / All-Out Pattern",
        "category": "behavioral",
        "signals": ["go all in then stop completely", "obsessed then drop it",
                    "can't do things in moderation", "extreme then nothing"],
        "ref": "pattern-library.md#the-all-in--all-out-pattern",
    },
}


def match_patterns(text, threshold=1):
    """Return patterns that have at least `threshold` signal matches."""
    text_lower = text.lower()
    matches = []

    for key, pattern in PATTERNS.items():
        matched_signals = [s for s in pattern["signals"] if s in text_lower]
        if len(matched_signals) >= threshold:
            matches.append({
                "key": key,
                "name": pattern["name"],
                "category": pattern["category"],
                "matched_signals": matched_signals,
                "score": len(matched_signals),
                "reference": pattern["ref"],
            })

    matches.sort(key=lambda x: -x["score"])
    return matches


def print_results(matches, text):
    if not matches:
        print(f"\nNo specific patterns matched. This might be a fresh topic —")
        print(f"good opportunity for open exploration rather than pattern-fitting.\n")
        return

    print(f"\n🔍 Potential Patterns Detected\n")
    for m in matches[:3]:
        print(f"  • {m['name']} ({m['category']})")
        print(f"    Matched: {', '.join(m['matched_signals'])}")
        print(f"    Reference: {m['reference']}")
        print()

    print("⚠️  Remember: Present as 'I wonder if...' — never as a diagnosis.")
    print("   Only the TOP match (if confidence is high) should typically be offered,")
    print("   and only after the user has been heard.\n")


def main():
    parser = argparse.ArgumentParser(description="Match text against pattern library")
    parser.add_argument("--text", help="User message text")
    parser.add_argument("--file", help="File containing user message")
    parser.add_argument("--threshold", type=int, default=1, help="Min signal matches")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    matches = match_patterns(text, args.threshold)

    if args.json:
        print(json.dumps(matches, indent=2))
    else:
        print_results(matches, text)


if __name__ == "__main__":
    main()
