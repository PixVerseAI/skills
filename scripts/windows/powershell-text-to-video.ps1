$PromptImagem = "Ultra-realistic cinematic scene of a brutal historical battlefield, medieval warriors clashing with steel swords and heavy shields, mud, flying blood, dark storm clouds, fire burning in the background, epic scale, dense atmosphere, 9:16"
$PromptAnimacao = "Cinematic trailer style, fast-paced action, dynamic camera movement, chaotic battlefield, hyper-realistic physics, aggressive motion"
$PromptAudio = "Intense war sounds, heavy metal clashing, swords crossing, soldiers screaming in fury, heavy cinematic war drums, explosions and burning fire"

Write-Host "Iniciando Pipeline Cinematografico (Sora 2 - 12 Segundos)..." -ForegroundColor Cyan

Write-Host "1. Gerando a imagem base (9:16)..." -ForegroundColor Yellow
$ImgOutput = pixverse create image --prompt $PromptImagem --aspect-ratio 9:16 --json | Out-String | ConvertFrom-Json
$ImageUrl = $ImgOutput.image_url

Write-Host "2. Animando a cena (Sora 2 com 12 segundos)..." -ForegroundColor Yellow
$VidOutput = pixverse create video --image $ImageUrl --prompt $PromptAnimacao --model sora-2 --duration 12 --json | Out-String | ConvertFrom-Json
$VideoId = $VidOutput.video_id
pixverse task wait $VideoId

Write-Host "3. Aplicando design de som de guerra..." -ForegroundColor Yellow
$SoundOutput = pixverse create sound --video $VideoId --prompt $PromptAudio --json | Out-String | ConvertFrom-Json
$SoundId = $SoundOutput.video_id
pixverse task wait $SoundId

Write-Host "4. Aplicando Upscale para alta fidelidade..." -ForegroundColor Yellow
$UpscaleOutput = pixverse create upscale --video $SoundId --quality 1080p --json | Out-String | ConvertFrom-Json
$FinalId = $UpscaleOutput.video_id
pixverse task wait $FinalId

Write-Host "5. Baixando o Trailer Masterizado..." -ForegroundColor Yellow
pixverse asset download $FinalId --type video

Write-Host "Processo concluido! O corte epico de 12 segundos esta salvo na sua pasta." -ForegroundColor Green
