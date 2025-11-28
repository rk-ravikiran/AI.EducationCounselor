# Convert Markdown with Mermaid to PDF using Pandoc
# Prerequisites:
# 1. Install Pandoc: choco install pandoc (or download from https://pandoc.org/installing.html)
# 2. Install Node.js: choco install nodejs
# 3. Install mermaid-filter: npm install -g mermaid-filter
# 4. Install puppeteer: npm install -g puppeteer

Write-Host "🔄 Converting ARCHITECTURE.md to PDF with Mermaid diagrams..." -ForegroundColor Cyan

# Check if pandoc is installed
if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Pandoc not found. Install with: choco install pandoc" -ForegroundColor Red
    exit 1
}

# Check if mermaid-filter is installed
if (!(Get-Command mermaid-filter -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ mermaid-filter not found. Installing..." -ForegroundColor Yellow
    npm install -g mermaid-filter
}

# Convert to PDF
pandoc ARCHITECTURE.md `
    --filter=mermaid-filter `
    --pdf-engine=wkhtmltopdf `
    -o ARCHITECTURE.pdf `
    --metadata title="Singapore Education Counselor - Architecture" `
    --toc `
    --number-sections `
    -V geometry:margin=1in

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ PDF generated: ARCHITECTURE.pdf" -ForegroundColor Green
} else {
    Write-Host "❌ Conversion failed. Try Option 3 (online service) instead." -ForegroundColor Red
}
