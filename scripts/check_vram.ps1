param(
  [string]$Command = "python -m app.main --task `"Write Lua function sum(a,b) and print sum(2,3).`" --output output/vram_check.json",
  [int]$PollIntervalMs = 500
)

$ErrorActionPreference = "Stop"
$peak = 0

Write-Host "Starting monitored command..."
$proc = Start-Process powershell -ArgumentList "-NoProfile", "-Command", $Command -PassThru

while (-not $proc.HasExited) {
  $usage = & nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>$null
  if ($usage) {
    foreach ($line in $usage) {
      $value = [int]$line.Trim()
      if ($value -gt $peak) { $peak = $value }
    }
  }
  Start-Sleep -Milliseconds $PollIntervalMs
  $proc.Refresh()
}

Write-Host "Command exit code: $($proc.ExitCode)"
Write-Host "Peak VRAM (MiB): $peak"
Write-Host ("Peak VRAM (GiB): {0:N2}" -f ($peak / 1024.0))

if (($peak / 1024.0) -gt 8.0) {
  Write-Warning "Peak VRAM exceeded 8.0 GiB limit."
  exit 1
}
