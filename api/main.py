"""
Prompt Forge API — FastAPI server for LLM-agnostic prompt compilation.

POST /forge
  Input:  { intent, target_model, mode }
  Output: { compiled_prompt, metadata }
"""

from __future__ import annotations

import os
import textwrap
from enum import Enum
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODES = {"build", "audit", "debug", "research", "optimize"}
MODELS = {"claude", "gemini", "openai"}

MODE_EMPHASIS = {
    "build": {
        "lead": "Implementation structure and pattern references",
        "constraint_weight": "medium",
        "sections": ["context", "pattern_reference", "implementation_plan", "scope", "done_criteria"],
    },
    "audit": {
        "lead": "Constraints, compliance, verification gates",
        "constraint_weight": "high",
        "sections": ["scope", "audit_checklist", "constraints", "findings_format", "verification"],
    },
    "debug": {
        "lead": "Investigation-first, root cause before fix",
        "constraint_weight": "medium",
        "sections": ["symptoms", "affected_code", "investigation_steps", "constraints", "verification"],
    },
    "research": {
        "lead": "Exploration, alternatives, trade-off analysis",
        "constraint_weight": "low",
        "sections": ["question", "starting_points", "exploration_approach", "output_format"],
    },
    "optimize": {
        "lead": "Measurement-first, bottleneck identification",
        "constraint_weight": "medium",
        "sections": ["problem", "affected_code", "profiling_steps", "optimization_constraints", "verification"],
    },
}

# ---------------------------------------------------------------------------
# Adapter formatting
# ---------------------------------------------------------------------------


def _format_claude(intent: str, mode: str, sections: list[str]) -> str:
    """Format prompt for Claude models using XML structure."""
    emphasis = MODE_EMPHASIS[mode]
    parts = [
        "Before starting, read @CLAUDE.md for project conventions.\n",
        f"<context>\nMode: {mode} — {emphasis['lead']}\n</context>\n",
        f"<task>\n{intent}\n</task>\n",
    ]
    if emphasis["constraint_weight"] in ("medium", "high"):
        parts.append(
            "<constraints>\n"
            "- Follow existing project patterns\n"
            "- Do NOT introduce unnecessary changes outside scope\n"
            "- Verify work after each step\n"
            "</constraints>\n"
        )
    parts.append(
        "<verification>\n"
        "Run the project's test suite after changes. Fix any failures before completing.\n"
        "</verification>"
    )
    return "\n".join(parts)


def _format_gemini(intent: str, mode: str, sections: list[str]) -> str:
    """Format prompt for Gemini models using MUST/MUST NOT structure."""
    emphasis = MODE_EMPHASIS[mode]
    parts = [
        f"Role: Senior software engineer performing a {mode} task.\n",
        f"## Context\nMode: {mode} — {emphasis['lead']}\n",
        f"## Task\n{intent}\n",
    ]
    if emphasis["constraint_weight"] in ("medium", "high"):
        parts.append(
            "## Rules\n"
            "- MUST follow existing project patterns\n"
            "- MUST NOT introduce changes outside scope\n"
            "- MUST verify work after each step\n"
        )
    parts.append(
        "## Verification\n"
        "Run the project's test suite after changes. Report results.\n"
    )
    return "\n".join(parts)


def _format_openai(intent: str, mode: str, sections: list[str]) -> str:
    """Format prompt for OpenAI models using system/user split."""
    emphasis = MODE_EMPHASIS[mode]
    parts = [
        f"[System]\nYou are a senior software engineer performing a {mode} task. "
        f"Focus: {emphasis['lead']}. "
        "Follow existing project patterns exactly. Verify your work.\n",
        f"[User]\n{intent}\n",
    ]
    if emphasis["constraint_weight"] in ("medium", "high"):
        parts.append(
            "Requirements:\n"
            "- **Do NOT** introduce changes outside the defined scope\n"
            "- **Do NOT** skip verification steps\n"
            "- Follow existing patterns in the codebase\n"
        )
    parts.append(
        "After implementing, run the test suite and report results.\n"
    )
    return "\n".join(parts)


ADAPTERS = {
    "claude": _format_claude,
    "gemini": _format_gemini,
    "openai": _format_openai,
}

# ---------------------------------------------------------------------------
# Intent analysis (lightweight — mirrors core logic from intent_parser.md)
# ---------------------------------------------------------------------------

MODE_SIGNALS = {
    "build": ["add", "build", "create", "implement", "new", "feature"],
    "audit": ["audit", "review", "check", "verify", "secure", "compliance"],
    "debug": ["fix", "bug", "broken", "error", "debug", "not working"],
    "research": ["how", "why", "explore", "compare", "understand", "explain"],
    "optimize": ["slow", "optimize", "performance", "speed", "cache", "fast"],
}


def infer_mode(intent: str) -> str:
    """Infer compilation mode from intent keywords."""
    intent_lower = intent.lower()
    scores = {mode: 0 for mode in MODES}
    for mode, signals in MODE_SIGNALS.items():
        for signal in signals:
            if signal in intent_lower:
                scores[mode] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "build"


# ---------------------------------------------------------------------------
# API models
# ---------------------------------------------------------------------------


class TargetModel(str, Enum):
    claude = "claude"
    gemini = "gemini"
    openai = "openai"


class ForgeMode(str, Enum):
    build = "build"
    audit = "audit"
    debug = "debug"
    research = "research"
    optimize = "optimize"


class ForgeRequest(BaseModel):
    intent: str = Field(..., min_length=1, description="Raw developer intent")
    target_model: TargetModel = Field(..., description="Target LLM")
    mode: Optional[ForgeMode] = Field(None, description="Compilation mode (auto-detected if omitted)")


class ForgeResponse(BaseModel):
    compiled_prompt: str
    metadata: dict


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Prompt Forge",
    description="LLM-agnostic prompt compiler for agentic systems",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "Prompt Forge",
        "version": "1.0.0",
        "endpoint": "POST /forge",
    }


@app.post("/forge", response_model=ForgeResponse)
def forge(req: ForgeRequest):
    # Resolve mode
    mode = req.mode.value if req.mode else infer_mode(req.intent)
    model = req.target_model.value

    # Get adapter
    adapter_fn = ADAPTERS.get(model)
    if not adapter_fn:
        raise HTTPException(status_code=400, detail=f"Unknown target model: {model}")

    emphasis = MODE_EMPHASIS.get(mode)
    if not emphasis:
        raise HTTPException(status_code=400, detail=f"Unknown mode: {mode}")

    # Compile prompt
    compiled = adapter_fn(req.intent, mode, emphasis["sections"])

    return ForgeResponse(
        compiled_prompt=compiled,
        metadata={
            "target_model": model,
            "mode": mode,
            "mode_emphasis": emphasis["lead"],
            "constraint_weight": emphasis["constraint_weight"],
            "sections": emphasis["sections"],
        },
    )
