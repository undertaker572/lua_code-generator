from dataclasses import dataclass


@dataclass
class PipelineContext:
    user_task: str
    language: str = "auto"
    clarifications: str = ""
    initial_lua: str = ""
    refined_lua: str = ""
    validation_report: str = ""


def intake_prompt(user_task: str, language: str) -> str:
    return (
        "Analyze the user request and decide if there is enough context to generate Lua code. "
        "If context is missing, return: NEEDS_CLARIFICATION. Otherwise return: READY.\n"
        f"Language hint: {language}\n"
        f"Task:\n{user_task}"
    )


def clarifier_prompt(user_task: str, language: str) -> str:
    return (
        "Ask up to 3 concise clarifying questions to improve Lua code generation quality. "
        "Questions may be in Russian or English based on the task language.\n"
        f"Language hint: {language}\n"
        f"Task:\n{user_task}"
    )


def generator_prompt(user_task: str, clarifications: str) -> str:
    return (
        "Generate workable Lua code for the task. "
        "Output only code in a fenced ```lua block and then a short explanation.\n"
        f"Task:\n{user_task}\n"
        f"Additional context:\n{clarifications}"
    )


def refiner_prompt(user_task: str, lua_code: str, validation_report: str) -> str:
    return (
        "Refine the Lua code according to validation errors. "
        "Return improved Lua code in a fenced ```lua block.\n"
        f"Task:\n{user_task}\n"
        f"Current code:\n{lua_code}\n"
        f"Validation report:\n{validation_report}"
    )
