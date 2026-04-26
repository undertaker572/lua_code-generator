import subprocess
import tempfile
from dataclasses import dataclass


@dataclass
class SyntaxValidationResult:
    ok: bool
    details: str


def validate_lua_syntax(lua_code: str) -> SyntaxValidationResult:
    """Validate Lua syntax via luac -p if available."""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False, encoding="utf-8") as tmp:
            tmp.write(lua_code)
            tmp_path = tmp.name

        proc = subprocess.run(
            ["luac", "-p", tmp_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return SyntaxValidationResult(ok=True, details="Lua syntax check passed (luac -p).")

        details = (proc.stderr or proc.stdout or "Unknown luac error").strip()
        return SyntaxValidationResult(ok=False, details=f"Lua syntax check failed: {details}")
    except FileNotFoundError:
        return SyntaxValidationResult(
            ok=False,
            details="luac not found in PATH. Install Lua compiler/interpreter for syntax checks.",
        )
