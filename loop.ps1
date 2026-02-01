param (
    [string]$Arg1,
    [string]$Arg2
)

$TotalStopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$IterationTimings = @()
$LogFile = "bezi_performance.csv"

# --- SELF-HEALING VENV LOGIC ---
$VenvPath = "$PSScriptRoot\.venv"
if (-not (Test-Path $VenvPath)) {
    py -m venv .venv
    & "$VenvPath\Scripts\Activate.ps1"
    python -m pip install --upgrade pip
    if (Test-Path "requirements.txt") { python -m pip install -r requirements.txt }
} else {
    & "$VenvPath\Scripts\Activate.ps1"
}

# Parse arguments
if ($Arg1 -eq "plan") {
    $Mode = "plan"; $PromptFile = "PROMPT_plan.md"
    $MaxIterations = if ($Arg2 -match '^\d+$') { [int]$Arg2 } else { 0 }
}
elseif ($Arg1 -match '^\d+$') {
    $Mode = "build"; $PromptFile = "PROMPT_build.md"
    $MaxIterations = [int]$Arg1
}
else {
    $Mode = "build"; $PromptFile = "PROMPT_build.md"; $MaxIterations = 0
}

$CurrentBranch = git branch --show-current

# Simplified Visual Box (Standard ASCII)
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "| MODE:   $($Mode.PadRight(36)) |" -ForegroundColor Cyan
Write-Host "| PROMPT: $($PromptFile.PadRight(36)) |" -ForegroundColor Cyan
Write-Host "| BRANCH: $($CurrentBranch.PadRight(36)) |" -ForegroundColor Cyan
Write-Host "| ITER:   $($MaxIterations.ToString().PadRight(36)) |" -ForegroundColor Cyan 
Write-Host "------------------------------------------------" -ForegroundColor Cyan

if (-not (Test-Path $PromptFile)) { Write-Error "Error: $PromptFile not found"; exit 1 }

# Init the Bezi Bridge
Start-Process -FilePath "py" -ArgumentList "bezi_bridge.py", "--init" -NoNewWindow -Wait

$Iteration = 0
$TempPromptPath = Join-Path $env:TEMP "bezi_prompt_tmp.md"

try {
    while ($true) {
        if ($MaxIterations -gt 0 -and $Iteration -ge $MaxIterations) { break }

        $LoopTimer = [System.Diagnostics.Stopwatch]::StartNew()
        $ThreadName = "$Mode $Iteration"
        
        # Pass the prompt via file to avoid shell escaping issues
        Get-Content -Path $PromptFile -Raw | Out-File -FilePath $TempPromptPath -Encoding utf8
        
        # Run bridge
        Start-Process -FilePath "py" -ArgumentList "bezi_bridge.py -t `"$ThreadName`" `"$TempPromptPath`"" -NoNewWindow -Wait
        
        $LoopTimer.Stop()
        $Iteration++
        
        $Seconds = [Math]::Round($LoopTimer.Elapsed.TotalSeconds, 2)
        $IterationTimings += [PSCustomObject]@{
            Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            Mode      = $Mode
            Iteration = $Iteration
            Duration  = $Seconds
        }

        Write-Host "`n--- LOOP $Iteration COMPLETED IN $($Seconds)s ---`n" -ForegroundColor Green
    }
}
finally {
    $TotalStopwatch.Stop()
    $TotalMin = [Math]::Round($TotalStopwatch.Elapsed.TotalMinutes, 2)
    
    # Final Timing Report (Standard ASCII)
    Write-Host "`n----------------- EXECUTION REPORT ----------------" -ForegroundColor Yellow
    foreach ($entry in $IterationTimings) {
        $Label = "Loop $($entry.Iteration)"
        Write-Host "| $($Label.PadRight(10)) : $($entry.Duration.ToString().PadRight(32))s |" -ForegroundColor Yellow
    }
    Write-Host "|-----------------------------------------------|" -ForegroundColor Yellow
    Write-Host "| TOTAL TIME : $($TotalMin.ToString().PadRight(31)) min |" -ForegroundColor Yellow
    Write-Host "-------------------------------------------------" -ForegroundColor Yellow

    # Log to CSV
    if ($IterationTimings.Count -gt 0) {
        $IterationTimings | Export-Csv -Path $LogFile -NoTypeInformation -Append
        Write-Host "Performance data logged to $LogFile" -ForegroundColor Gray
    }

    if (Test-Path $TempPromptPath) { Remove-Item $TempPromptPath }
    if (Get-Command deactivate -ErrorAction SilentlyContinue) { deactivate }
}