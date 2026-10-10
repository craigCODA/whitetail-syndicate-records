$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifest = Get-Content (Join-Path $base 'manifest_all.json') -Raw | ConvertFrom-Json

function Slug([string]$text) {
  if ([string]::IsNullOrWhiteSpace($text)) { return 'item' }
  $text = $text -replace '[^a-zA-Z0-9]+','-'
  return $text.Trim('-').ToLower()
}

function Download-Group($groupName, $items) {
  $out = Join-Path $base "downloads/$groupName"
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  $i = 1
  foreach ($item in $items) {
    $title = Slug $item.title
    $variant = Slug ($item.variant)
    if (-not $variant) { $variant = 'default' }
    $ext = '.jpg'
    if ($item.image_url.ToLower().Contains('.png')) { $ext = '.png' }
    $name = ('{0:D2}_{1}__{2}{3}' -f $i, $title, $variant, $ext)
    $target = Join-Path $out $name
    Write-Host "Downloading $($item.title) -> $name"
    Invoke-WebRequest -Uri $item.image_url -OutFile $target
    $i++
  }
}

Download-Group 'hats-beanies' $manifest.hats_beanies
Download-Group 'gear-accessories' $manifest.gear_accessories
Write-Host 'Done.'
