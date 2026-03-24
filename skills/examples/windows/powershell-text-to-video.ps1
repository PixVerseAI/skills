# PixVerse CLI — Full Video Production Pipeline (PowerShell)
#
# This script demonstrates a complete cinematic video pipeline:
#   1. Generate a base image (T2I)
#   2. Animate the image into a 12-second video using Sora 2 (I2V)
#   3. Add war sound effects
#   4. Upscale to 1080p
#   5. Download the final video
#
# Prerequisites:
#   - Node.js >= 20
#   - npm install -g pixverse
#   - pixverse auth login --json

$ImagePrompt = "Ultra-realistic cinematic scene of a brutal historical battlefield, medieval warriors clashing with steel swords and heavy shields, mud, flying blood, dark storm clouds, fire burning in the background, epic scale, dense atmosphere, 9:16"
$AnimationPrompt = "Cinematic trailer style, fast-paced action, dynamic camera movement, chaotic battlefield, hyper-realistic physics, aggressive motion"
$AudioPrompt = "Intense war sounds, heavy metal clashing, swords crossing, soldiers screaming in fury, heavy cinematic war drums, explosions and burning fire"

Write-Host "Starting Cinematic Pipeline (Sora 2 - 12 Seconds)..." -ForegroundColor Cyan

Write-Host "1. Generating base image (9:16)..." -ForegroundColor Yellow
$ImgOutput = pixverse create image --prompt $ImagePrompt --aspect-ratio 9:16 --json | Out-String | ConvertFrom-Json
$ImageUrl = $ImgOutput.image_url

Write-Host "2. Animating the scene (Sora 2, 12 seconds)..." -ForegroundColor Yellow
$VidOutput = pixverse create video --image $ImageUrl --prompt $AnimationPrompt --model sora-2 --duration 12 --json | Out-String | ConvertFrom-Json
$VideoId = $VidOutput.video_id
pixverse task wait $VideoId

Write-Host "3. Adding war sound design..." -ForegroundColor Yellow
$SoundOutput = pixverse create sound --video $VideoId --prompt $AudioPrompt --json | Out-String | ConvertFrom-Json
$SoundId = $SoundOutput.video_id
pixverse task wait $SoundId

Write-Host "4. Upscaling to high fidelity..." -ForegroundColor Yellow
$UpscaleOutput = pixverse create upscale --video $SoundId --quality 1080p --json | Out-String | ConvertFrom-Json
$FinalId = $UpscaleOutput.video_id
pixverse task wait $FinalId

Write-Host "5. Downloading the mastered trailer..." -ForegroundColor Yellow
pixverse asset download $FinalId --type video

Write-Host "Done! The 12-second epic cut is saved to your current folder." -ForegroundColor Green
