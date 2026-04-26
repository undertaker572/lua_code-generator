param(
  [string]$Task = "Напиши Lua-скрипт: функция factorial(n) и вывод factorial(5).",
  [string]$Output = "output/benchmark_result.json"
)

$ErrorActionPreference = "Stop"

Write-Host "Running benchmark query with fixed generation parameters..."
python -m app.main --task "$Task" --lang "auto" --output "$Output"

if ($LASTEXITCODE -ne 0) {
  throw "Benchmark run failed with exit code $LASTEXITCODE"
}

Write-Host "Benchmark output saved to $Output"
