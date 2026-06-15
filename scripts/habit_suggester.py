#!/usr/bin/env python3
"""
habit_suggester.py — Suggest a micro-habit based on the goal area.

Maps user's stated goal/struggle to relevant micro-habit suggestions
from references/micro-habits.md.

Usage:
    python scripts/habit_suggester.py --text "I want to sleep better"
    python scripts/habit_suggester.py --text "I keep procrastinating on my work"
"""
import argparse, sys, json, random
from pathlib import Path


GOAL_AREAS = {
    "sleep": {
        "signals": ["sleep", "insomnia", "can't fall asleep", "bedtime",
                    "wake up tired", "sleeping better", "go to bed"],
        "suggestions": [
            {
                "habit": "Put your phone across the room tonight — just tonight",
                "anchor": "When you get into bed",
                "why": "Removes the easiest source of 'just one more thing' before sleep",
            },
            {
                "habit": "Write down tomorrow's first task before bed",
                "anchor": "Right before brushing your teeth",
                "why": "Gives your brain permission to stop holding onto it overnight",
            },
            {
                "habit": "Turn the lights off just 10 minutes earlier than usual",
                "anchor": "Whatever time you normally would",
                "why": "Small enough to not feel like a big change, but starts shifting the pattern",
            },
        ],
    },
    "movement": {
        "signals": ["exercise", "move more", "workout", "gym", "active",
                    "sitting too much", "physical activity"],
        "suggestions": [
            {
                "habit": "Just put on your shoes — that's the whole habit",
                "anchor": "After your morning coffee",
                "why": "Removes the decision point; if you go further, that's a bonus",
            },
            {
                "habit": "One minute of stretching before getting out of bed",
                "anchor": "When your alarm goes off, before sitting up",
                "why": "Tiny enough to do even on the hardest mornings",
            },
            {
                "habit": "Stand up or walk during phone calls",
                "anchor": "Every phone call you take",
                "why": "Movement attached to something you already do regularly",
            },
        ],
    },
    "overthinking": {
        "signals": ["overthink", "can't stop thinking", "racing thoughts",
                    "ruminating", "replaying", "mind won't quiet"],
        "suggestions": [
            {
                "habit": "Set a 10-minute timer to think about it as much as you want — then write down the one unresolved thing and let the rest go for now",
                "anchor": "When you notice the loop starting",
                "why": "Gives the thinking somewhere to go, with a clear endpoint",
            },
            {
                "habit": "Write down three things at the end of the day — anything",
                "anchor": "Right before bed",
                "why": "Externalizes thoughts so they don't have to stay in your head overnight",
            },
            {
                "habit": "Say 'noted' out loud when you catch the loop starting",
                "anchor": "Whenever you notice it",
                "why": "Acknowledges the thought without engaging it further",
            },
        ],
    },
    "connection": {
        "signals": ["lonely", "isolated", "reconnect", "reach out",
                    "relationships", "feel disconnected from people"],
        "suggestions": [
            {
                "habit": "Send one 'thinking of you' text to someone",
                "anchor": "While your coffee/tea brews",
                "why": "Low-stakes, low-effort, often means more to the other person than expected",
            },
            {
                "habit": "Ask one more question before sharing your own thought",
                "anchor": "In your next conversation",
                "why": "Small shift that can deepen a single interaction",
            },
        ],
    },
    "boundaries": {
        "signals": ["say no", "boundaries", "people pleasing", "can't say no",
                    "always say yes", "overcommitted"],
        "suggestions": [
            {
                "habit": "Try 'let me check and get back to you' instead of an immediate yes",
                "anchor": "Next time someone asks you for something",
                "why": "Creates space between the request and your response",
            },
            {
                "habit": "Say 'I can't this time' without adding a reason — just once",
                "anchor": "Next low-stakes request",
                "why": "Practices the muscle of declining without justification, in a low-risk situation",
            },
        ],
    },
    "energy_burnout": {
        "signals": ["burnt out", "burned out", "running on empty", "exhausted",
                    "no energy", "depleted", "overextended"],
        "suggestions": [
            {
                "habit": "Pick ONE thing today and let everything else be optional",
                "anchor": "First thing when you sit down to plan your day",
                "why": "Reduces the all-or-nothing pressure of a full task list",
            },
            {
                "habit": "Take a 5-minute break on a timer BEFORE you feel depleted",
                "anchor": "Set it when you start a work block",
                "why": "Proactive rest is more effective than reactive rest",
            },
            {
                "habit": "Let 'rest' mean doing one less thing than yesterday",
                "anchor": "End of day reflection",
                "why": "Makes rest measurable and achievable rather than abstract",
            },
        ],
    },
    "procrastination": {
        "signals": ["procrastinat", "putting off", "avoid starting", "can't get started",
                    "keep delaying", "put it off"],
        "suggestions": [
            {
                "habit": "Just open the document — that's the whole task",
                "anchor": "When you sit down at your desk",
                "why": "The hardest part of most tasks is starting; this removes that barrier",
            },
            {
                "habit": "Set a 5-minute timer and give yourself permission to stop after",
                "anchor": "When you notice yourself avoiding something",
                "why": "5 minutes feels achievable; often momentum carries you past it",
            },
            {
                "habit": "Do a deliberately bad first version, just to get something down",
                "anchor": "When perfectionism is the block",
                "why": "Removes the pressure of 'getting it right' on the first try",
            },
        ],
    },
    "self_compassion": {
        "signals": ["hard on myself", "self critical", "beat myself up",
                    "never good enough", "self compassion", "kind to myself"],
        "suggestions": [
            {
                "habit": "Ask 'would I say this to a friend?' when you notice harsh self-talk",
                "anchor": "Whenever you catch a critical thought about yourself",
                "why": "Creates a moment of perspective without forcing positivity",
            },
            {
                "habit": "Keep a running note of small things you handled well",
                "anchor": "End of each day, one line",
                "why": "Builds evidence against the 'nothing I do is good enough' narrative",
            },
        ],
    },
}


def find_goal_area(text):
    text_lower = text.lower()
    scores = {}
    for area, config in GOAL_AREAS.items():
        score = sum(1 for s in config["signals"] if s in text_lower)
        if score > 0:
            scores[area] = score

    if not scores:
        return None, {}

    best = max(scores, key=scores.get)
    return best, GOAL_AREAS[best]


def suggest(text, n=1):
    area, config = find_goal_area(text)
    if not area:
        return {
            "goal_area": None,
            "suggestions": [],
            "note": "No specific goal area detected — consider asking the user "
                    "what specifically they'd want to try, or read references/micro-habits.md "
                    "for general principles to apply.",
        }

    suggestions = config["suggestions"]
    selected = suggestions[:n] if n < len(suggestions) else suggestions

    return {
        "goal_area": area,
        "suggestions": selected,
        "all_options_count": len(suggestions),
    }


def print_result(result):
    if not result["goal_area"]:
        print(f"\n{result['note']}\n")
        return

    print(f"\n🌱 Goal area detected: {result['goal_area'].replace('_', ' ').title()}")
    print(f"   ({result['all_options_count']} possible suggestions available)\n")

    for s in result["suggestions"]:
        print(f"  💡 {s['habit']}")
        print(f"     Anchor: {s['anchor']}")
        print(f"     Why: {s['why']}")
        print()

    print("Remember:")
    print("  1. Ask permission before offering: 'I have a small idea — want to hear it?'")
    print("  2. Frame as experiment: 'Want to try this for a few days and see what happens?'")
    print("  3. If they hesitate, offer an even smaller version")
    print()


def main():
    parser = argparse.ArgumentParser(description="Suggest micro-habits based on stated goal")
    parser.add_argument("--text", help="User's goal or struggle description")
    parser.add_argument("--file", help="File containing text")
    parser.add_argument("--count", type=int, default=1, help="Number of suggestions")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    result = suggest(text, args.count)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)


if __name__ == "__main__":
    main()
