$ErrorActionPreference = 'Stop'

Write-Host 'Portable Vibe Engineering Toolkit — curated skill installer'
Write-Host 'This calls the official Skills CLI through npx. Review source and install prompts before accepting.'
Write-Host ''

Write-Host 'Step 1: Preview the primary lifecycle pack.'
npx skills add addyosmani/agent-skills --list
if ($LASTEXITCODE -ne 0) { throw 'Unable to list Addy Osmani skills. Check Node.js/npm and the repository.' }

$installCore = Read-Host 'Install the Addy Osmani Agent Skills pack for the available/selected agents? (y/N)'
if ($installCore -match '^(y|yes)$') {
    npx skills add addyosmani/agent-skills
    if ($LASTEXITCODE -ne 0) { throw 'Core skills installation failed.' }
} else {
    Write-Host 'Skipped core pack installation.'
}

Write-Host ''
Write-Host 'Step 2: Preview Vercel specialist skills.'
npx skills add vercel-labs/agent-skills --list
if ($LASTEXITCODE -ne 0) { throw 'Unable to list Vercel skills.' }

$installSpecialists = Read-Host 'Install React/Next.js UI review and React Native guidelines? (y/N)'
if ($installSpecialists -match '^(y|yes)$') {
    npx skills add vercel-labs/agent-skills --skill react-best-practices --skill web-design-guidelines --skill react-native-guidelines
    if ($LASTEXITCODE -ne 0) { throw 'Vercel specialist skill installation failed. Verify the skill IDs with --list.' }
} else {
    Write-Host 'Skipped Vercel specialist installation.'
}

Write-Host ''
Write-Host 'Review the results with: npx skills list'
Write-Host 'Read docs/MARKETPLACE-RESEARCH.md for source/permission caveats.'
Write-Host 'This script installs skills only. It does not configure MCP servers, run tests, or deploy anything.'
