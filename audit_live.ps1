# Full live crawl via curl (works when Python SSL flaky on Windows)
$base = "https://iqos-store.ru"
$errors = @()
$ok = @()

function Test-Url($url) {
    try {
        $r = curl.exe -sS -o NUL -w "%{http_code}" --connect-timeout 20 --max-time 30 $url 2>$null
        return [int]$r
    } catch { return 0 }
}

$codes = @(
    (Test-Url "http://iqos-store.ru/robots.txt"),
    (Test-Url "$base/robots.txt"),
    (Test-Url "$base/sitemap.xml"),
    (Test-Url "$base/"),
    (Test-Url "$base/catalog"),
    (Test-Url "$base/search?q=iluma"),
    (Test-Url "$base/search?q=iluma"),
    (Test-Url "$base/health")
)
$names = @("robots HTTP","robots HTTPS","sitemap","home","catalog","search iluma","search","health")
for ($i=0; $i -lt $names.Count; $i++) {
    if ($codes[$i] -eq 200) { $ok += "$($names[$i]) -> 200" } else { $errors += "$($names[$i]) -> $($codes[$i])" }
}

$xml = curl.exe -sS --connect-timeout 25 "$base/sitemap.xml" 2>$null
$urls = [regex]::Matches($xml, '<loc>([^<]+)</loc>') | ForEach-Object { $_.Groups[1].Value }
$ok += "sitemap URLs: $($urls.Count)"

$broken = @()
foreach ($u in $urls) {
    $c = Test-Url $u
    if ($c -ne 200) { $broken += "$u -> $c" }
}
if ($broken.Count -eq 0) { $ok += "All $($urls.Count) sitemap pages -> 200" }
else { $errors += $broken }

$home = curl.exe -sS --connect-timeout 25 "$base/" 2>$null
foreach ($needle in @("f5f465a5a59bd8da","HQ9vRHnnwg","WebSite","index, follow")) {
    if ($home -match [regex]::Escape($needle)) { $ok += "SEO tag: $needle" }
    else { $errors += "SEO missing: $needle" }
}

Write-Host "=== LIVE AUDIT (curl) ==="
$ok | ForEach-Object { Write-Host " OK  $_" }
$errors | Select-Object -First 25 | ForEach-Object { Write-Host " ERR $_" }
Write-Host "Total errors: $($errors.Count)"
