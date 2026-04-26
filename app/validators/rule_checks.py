import re
from dataclasses import dataclass


@dataclass
class RuleCheckResult:
    ok: bool
    details: str


def run_rule_checks(lua_code: str, user_task: str) -> RuleCheckResult:
    """Run local deterministic checks for practical safety and task shape."""
    issues = []

    dangerous_patterns = [
        r"\bos\.execute\b",
        r"\bio\.popen\b",
        r"\bloadstring\b",
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, lua_code):
            issues.append(f"Disallowed pattern detected: `{pattern}`")

    if "function" not in lua_code:
        issues.append("No function declaration found; output may be incomplete.")

    if "print" in user_task.lower() and "print(" not in lua_code:
        issues.append("Task implies output, but no print(...) call was found.")

    if issues:
        return RuleCheckResult(ok=False, details="\n".join(issues))
    return RuleCheckResult(ok=True, details="Rule checks passed.")
