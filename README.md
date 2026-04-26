# Local Lua Agent System

Local multi-agent Lua code generation pipeline using **CrewAI + LiteLLM + Ollama**.

## What it does

- Accepts natural-language tasks in Russian or English.
- Generates initial Lua code.
- Performs deterministic local validation:
  - Lua syntax check (`luac -p`)
  - local rule checks
- Runs at least one automatic refinement loop when validation fails.
- Produces a final Lua script and validation report.

## Tech constraints alignment

- Local execution only.
- No external LLM vendors or cloud APIs at runtime.
- Open-source model via Ollama.
- Reproducible benchmark parameters fixed in code:
  - `num_ctx=4096`
  - `num_predict=256` (mapped as `max_tokens=256`)
  - `batch=1` (passed via Ollama extra body)
  - `parallel=1` (passed via Ollama extra body)

## Model

Exact demo pull command:

```bash
ollama pull qwen2.5-coder:3b
```

Set this model in `.env` (or keep default from code):

```env
OLLAMA_MODEL=qwen2.5-coder:3b
OLLAMA_BASE_URL=http://localhost:11434
MAX_REFINEMENT_LOOPS=1
```

## Setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

Optional but recommended for syntax validation:

- Install Lua toolchain and ensure `luac` is in `PATH`.

## Run

```bash
python -m app.main --task "Write a Lua script: function factorial(n) and print factorial(5)." --lang en --output output/result.json
```

Output includes:

- `final_lua`
- `validation_report`
- full context snapshot

## Benchmark script

PowerShell:

```powershell
./scripts/run_benchmark.ps1
```

Custom benchmark prompt:

```powershell
./scripts/run_benchmark.ps1 -Task "Your benchmark query" -Output "output/benchmark_result.json"
```

## VRAM peak check (<= 8.0 GiB)

PowerShell:

```powershell
./scripts/check_vram.ps1
```

This script:

- runs a generation command,
- polls `nvidia-smi`,
- reports peak VRAM in MiB/GiB,
- returns non-zero exit code if peak exceeds 8.0 GiB.

## Project structure

- `app/main.py` - CLI entrypoint and pipeline execution.
- `app/agents.py` - agent network (intake, clarifier, generator, validator, refiner).
- `app/tasks.py` - prompt builders and pipeline context model.
- `app/llm.py` - LiteLLM + Ollama call wrapper with fixed benchmark params.
- `app/validators/lua_syntax.py` - syntax validation via `luac -p`.
- `app/validators/rule_checks.py` - deterministic local template/rule checks.
- `tests/test_pipeline.py` - smoke test for generation pipeline.
- `scripts/run_benchmark.ps1` - benchmark run helper.
- `scripts/check_vram.ps1` - VRAM peak verification helper.
- `data/patterns/` - local reproducible Lua patterns.

## Notes for jury/demo

- Keep all data and model execution local.
- Do not configure any external API keys for generation.
- If using another quantized tag, update this README with the exact `ollama pull <tag>` and keep benchmark params unchanged.
