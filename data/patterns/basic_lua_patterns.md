# Local Lua Patterns

These deterministic patterns are local reference hints for generation/refinement:

- Prefer pure functions for computation tasks.
- Return values from functions; only print in entry flow.
- Use straightforward loops (`for`, `while`) with clear boundaries.
- Avoid shell/process execution helpers (`os.execute`, `io.popen`) unless explicitly requested.
