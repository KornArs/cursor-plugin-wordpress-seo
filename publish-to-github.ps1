# Publish WordPress SEO Publisher plugin to your GitHub
# Run: .\publish-to-github.ps1

$ErrorActionPreference = "Stop"
$repoName = "cursor-plugin-wordpress-seo"

Write-Host "1. Checking GitHub auth..." -ForegroundColor Cyan
gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Logging in to GitHub (browser will open)..." -ForegroundColor Yellow
    gh auth login -h github.com -p https -w
}

Write-Host "`n2. Creating repo on GitHub..." -ForegroundColor Cyan
gh repo create $repoName --public --source=. --remote=origin --push --description "Cursor plugin: WordPress SEO Publisher - create posts, publish, SEO & GEO analysis"

if ($LASTEXITCODE -eq 0) {
    $repoUrl = gh repo view --json url -q '.url'
    Write-Host "`n3. Done! Repo: $repoUrl" -ForegroundColor Green
    Write-Host "`n4. Install in Cursor: /add-plugin" -ForegroundColor Yellow
    Write-Host "   Then paste: $repoUrl" -ForegroundColor White
} else {
    Write-Host "`nIf repo already exists, run:" -ForegroundColor Yellow
    Write-Host "   gh repo set-default (your-username)/$repoName" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor White
}
