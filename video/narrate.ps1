$ErrorActionPreference = 'Stop'
$afVideoRoot = $PSScriptRoot
$afStoryboard = Get-Content -Raw -LiteralPath (Join-Path $afVideoRoot 'storyboard.json') -Encoding UTF8 | ConvertFrom-Json
$afAudioRoot = Join-Path $afVideoRoot 'generated'
New-Item -ItemType Directory -Force -Path $afAudioRoot | Out-Null
Add-Type -AssemblyName System.Speech
$afNarrator = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
  $afNarrator.SelectVoice($afStoryboard.voice)
  $afNarrator.Rate = 1
  $afNarrator.Volume = 90
  foreach ($afScene in $afStoryboard.scenes) {
    $afNarrator.SetOutputToWaveFile((Join-Path $afAudioRoot ($afScene.id + '.wav')))
    $afNarrator.Speak($afScene.narration)
    $afNarrator.SetOutputToNull()
    Write-Output ('Narrated: ' + $afScene.id)
  }
} finally { $afNarrator.Dispose() }
