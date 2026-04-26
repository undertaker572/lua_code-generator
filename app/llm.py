import os
from typing import Optional

from litellm import completion


DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
DEFAULT_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def generate_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """Generate text with fixed benchmark-safe defaults for Ollama."""
    if os.getenv("MOCK_LLM", "").lower() in {"1", "true", "yes"}:
        return _mock_response(prompt)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = completion(
        model=f"ollama/{model or DEFAULT_MODEL}",
        api_base=DEFAULT_BASE_URL,
        messages=messages,
        num_ctx=4096,
        max_tokens=256,
        temperature=0.2,
        top_p=0.9,
        extra_body={"batch": 1, "parallel": 1},
    )
    return response.choices[0].message.content.strip()


def _mock_response(prompt: str) -> str:
    lowered = prompt.lower()
    if "clarify" in lowered or "уточ" in lowered:
        return "What is the exact function signature and expected output format?"
    if "refine" in lowered or "исправ" in lowered:
        return "```lua\nlocal function sum(a, b)\n  return a + b\nend\n\nprint(sum(2, 3))\n```"
    return "```lua\nlocal function hello(name)\n  return \"Hello, \" .. name\nend\n\nprint(hello(\"Lua\"))\n```"
