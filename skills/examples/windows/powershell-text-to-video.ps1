# Text -> video -> download on Windows PowerShell. Requires Node.js >= 22.12 and an authenticated CLI.
# Uses the region's default video model. Shared behavior: ../../references/execution-contract.md
param(
    [string]$Prompt = "A medieval fortress at dawn; the camera slowly approaches as banners move in the wind",
    [string]$OutputDirectory = (Join-Path ([IO.Path]::GetTempPath()) ("pixverse-" + [guid]::NewGuid()))
)
$ErrorActionPreference = 'Stop'

function Invoke-PixverseJson {
    param([string[]]$CliArgs)
    $Raw = & pixverse @CliArgs --json | Out-String
    $Code = $LASTEXITCODE
    if ($Code -ne 0) {
        throw "PixVerse exited with code $Code. Retain any submitted IDs for recovery; do not blindly resubmit. Output: $Raw"
    }
    return ($Raw | ConvertFrom-Json)
}

New-Item -ItemType Directory -Path $OutputDirectory -ErrorAction Stop | Out-Null
# Default create waits for completion; the key makes an unconfirmed retry of this same request safe.
$Video = Invoke-PixverseJson -CliArgs @('create', 'video', '--prompt', $Prompt, '--idempotency-key', [guid]::NewGuid().ToString())
if ($Video.status -ne 'completed' -or -not $Video.video_id) { throw "Expected a completed video with video_id; got status '$($Video.status)'" }
$Download = Invoke-PixverseJson -CliArgs @('asset', 'download', [string]$Video.video_id, '--type', 'video', '--dest', $OutputDirectory)
if (-not $Download.file) { throw 'Download result has no file path' }
Write-Host "Video saved to: $($Download.file)"
