#!/usr/bin/env python3
"""
Prompt Forge CLI — compile prompts from the command line.

Usage:
    python pf.py forge "your intent here" --model claude --mode build
    python pf.py forge "fix the login bug" --model gemini --mode debug
    python pf.py forge "audit the auth flow" --model openai
"""

from __future__ import annotations

import argparse
import sys
import os

# Allow importing from sibling api/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from main import ADAPTERS, MODE_EMPHASIS, infer_mode  # noqa: E402


def run_forge(intent: str, model: str, mode: str | None) -> None:
    """Compile a prompt and print it."""
    # Resolve mode
    resolved_mode = mode if mode else infer_mode(intent)

    # Validate
    if model not in ADAPTERS:
        print(f"Error: unknown model '{model}'. Choose from: claude, gemini, openai", file=sys.stderr)
        sys.exit(1)

    if resolved_mode not in MODE_EMPHASIS:
        print(f"Error: unknown mode '{resolved_mode}'. Choose from: build, audit, debug, research, optimize", file=sys.stderr)
        sys.exit(1)

    # Compile
    emphasis = MODE_EMPHASIS[resolved_mode]
    adapter_fn = ADAPTERS[model]
    compiled = adapter_fn(intent, resolved_mode, emphasis["sections"])

    # Output clean prompt only
    print(compiled)


def main():
    parser = argparse.ArgumentParser(
        prog="pf",
        description="Prompt Forge — LLM-agnostic prompt compiler",
    )
    subparsers = parser.add_subparsers(dest="command")

    # forge subcommand
    forge_parser = subparsers.add_parser("forge", help="Compile a prompt from raw intent")
    forge_parser.add_argument("intent", help="Raw developer intent (e.g., 'add stripe payments')")
    forge_parser.add_argument(
        "--model", "-m",
        choices=["claude", "gemini", "openai"],
        default="claude",
        help="Target LLM (default: claude)",
    )
    forge_parser.add_argument(
        "--mode",
        choices=["build", "audit", "debug", "research", "optimize"],
        default=None,
        help="Compilation mode (auto-detected from intent if omitted)",
    )

    args = parser.parse_args()

    if args.command == "forge":
        run_forge(args.intent, args.model, args.mode)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
