# Local static file server for previewing the site. Development only.
# Not part of the public site and not required to host it.

$root = $PSScriptRoot
$port = 8000

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host ""
Write-Host "Serving $root"
Write-Host "  Root    http://localhost:$port/"
Write-Host "  Compass http://localhost:$port/compass/"
Write-Host "  Stop    Ctrl+C"
Write-Host ""

$mime = @{
  '.html' = 'text/html; charset=utf-8'
  '.css'  = 'text/css; charset=utf-8'
  '.svg'  = 'image/svg+xml'
  '.png'  = 'image/png'
  '.ico'  = 'image/x-icon'
  '.txt'  = 'text/plain; charset=utf-8'
}

try {
  while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response

    $relative = [System.Uri]::UnescapeDataString($request.Url.AbsolutePath).TrimStart('/')
    if ($relative -eq '') { $relative = 'index.html' }

    $full = Join-Path $root ($relative -replace '/', '\')

    # Keep requests inside the project directory.
    if (-not $full.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
      $response.StatusCode = 403
      $response.Close()
      continue
    }

    if (Test-Path -LiteralPath $full -PathType Leaf) {
      $ext = [System.IO.Path]::GetExtension($full).ToLower()
      $type = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { 'application/octet-stream' }

      $response.ContentType = $type
      $bytes = [System.IO.File]::ReadAllBytes($full)
      $response.ContentLength64 = $bytes.Length
      $response.OutputStream.Write($bytes, 0, $bytes.Length)
    }
    else {
      # Directory request: serve its index.html.
      $index = Join-Path $full 'index.html'
      if (Test-Path -LiteralPath $index -PathType Leaf) {
        $response.ContentType = 'text/html; charset=utf-8'
        $bytes = [System.IO.File]::ReadAllBytes($index)
        $response.ContentLength64 = $bytes.Length
        $response.OutputStream.Write($bytes, 0, $bytes.Length)
      }
      else {
        $response.StatusCode = 404
      }
    }

    $response.Close()
  }
}
finally {
  $listener.Stop()
  $listener.Close()
}