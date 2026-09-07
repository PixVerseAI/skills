# Image -> Sora 2 video -> upscale -> download. Node.js >= 22.12; authenticated CLI.
# Shared behavior: ../../references/execution-contract.md
param(
    [string]$ImagePrompt = "A medieval fortress at dawn, cinematic composition",
    [string]$AnimationPrompt = "Camera slowly approaches the fortress as banners move in the wind",
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
$Image = Invoke-PixverseJson -CliArgs @('create', 'image', '--prompt', $ImagePrompt, '--aspect-ratio', '9:16', '--idempotency-key', [guid]::NewGuid().ToString())
if (-not $Image.image_url) { throw 'Completed image result has no image_url' }
$Video = Invoke-PixverseJson -CliArgs @('create', 'video', '--image', $Image.image_url, '--prompt', $AnimationPrompt, '--model', 'sora-2', '--duration', '12', '--idempotency-key', [guid]::NewGuid().ToString())
if (-not $Video.video_id) { throw 'Completed video result has no video_id' }
$Upscale = Invoke-PixverseJson -CliArgs @('create', 'upscale', '--video', [string]$Video.video_id, '--quality', '2160p', '--idempotency-key', [guid]::NewGuid().ToString())
if (-not $Upscale.video_id) { throw 'Completed upscale result has no video_id' }
# Default create calls already waited. No additional task wait is needed.
$Download = Invoke-PixverseJson -CliArgs @('asset', 'download', [string]$Upscale.video_id, '--type', 'video', '--dest', $OutputDirectory)
if (-not $Download.file) { throw 'Download result has no file path' }
Write-Host "Final video saved to: $($Download.file)"
