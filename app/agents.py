import json
import re
from dataclasses import asdict
from typing import Dict

from crewai import Agent

from app.llm import generate_text
from app.tasks import PipelineContext, clarifier_prompt, generator_prompt, intake_prompt, refiner_prompt
from app.validators.lua_syntax import validate_lua_syntax
from app.validators.rule_checks import run_rule_checks


def _extract_lua_block(text: str) -> str:
    match = re.search(r"```lua\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()


class AgentNetwork:
    """Minimal multi-agent pipeline based on CrewAI role definitions."""

    def __init__(self, max_refinement_loops: int = 1):
        self.max_refinement_loops = max_refinement_loops
        self.intake_agent = Agent(
            role="TaskIntakeAgent",
            goal="Assess whether enough context is available to start Lua generation.",
            backstory="A strict analyst who avoids writing incorrect code without context.",
            verbose=False,
            allow_delegation=False,
        )
        self.clarifier_agent = Agent(
            role="ClarifierAgent",
            goal="Ask high-impact clarifying questions.",
            backstory="An expert requirements engineer for software tasks.",
            verbose=False,
            allow_delegation=False,
        )
        self.generator_agent = Agent(
            role="LuaGeneratorAgent",
            goal="Generate practical, readable Lua scripts.",
            backstory="A Lua engineer focused on clear and robust scripts.",
            verbose=False,
            allow_delegation=False,
        )
        self.validator_agent = Agent(
            role="ValidatorAgent",
            goal="Validate generated Lua with deterministic checks.",
            backstory="A QA engineer who trusts tests and static checks over assumptions.",
            verbose=False,
            allow_delegation=False,
        )
        self.refiner_agent = Agent(
            role="RefinerAgent",
            goal="Fix and improve Lua based on validation findings.",
            backstory="A reviewer specializing in iterative repair loops.",
            verbose=False,
            allow_delegation=False,
        )

    def run(self, user_task: str, language: str = "auto", clarifications: str = "") -> Dict[str, str]:
        ctx = PipelineContext(user_task=user_task, language=language, clarifications=clarifications)

        intake = generate_text(intake_prompt(ctx.user_task, ctx.language))
        needs_clarification = "NEEDS_CLARIFICATION" in intake.upper()

        if needs_clarification and not ctx.clarifications:
            ctx.clarifications = generate_text(clarifier_prompt(ctx.user_task, ctx.language))

        initial_response = generate_text(generator_prompt(ctx.user_task, ctx.clarifications))
        ctx.initial_lua = _extract_lua_block(initial_response)
        active_code = ctx.initial_lua

        for _ in range(self.max_refinement_loops + 1):
            syntax = validate_lua_syntax(active_code)
            rules = run_rule_checks(active_code, ctx.user_task)
            ctx.validation_report = "\n".join([syntax.details, rules.details]).strip()
            if syntax.ok and rules.ok:
                break

            refined = generate_text(refiner_prompt(ctx.user_task, active_code, ctx.validation_report))
            active_code = _extract_lua_block(refined)

        ctx.refined_lua = active_code
        return {
            "needs_clarification": str(needs_clarification),
            "clarifications": ctx.clarifications,
            "initial_lua": ctx.initial_lua,
            "final_lua": ctx.refined_lua,
            "validation_report": ctx.validation_report,
            "context": json.dumps(asdict(ctx), ensure_ascii=False, indent=2),
        }
