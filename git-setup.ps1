# PowerShell helper to initialize git and push to remote
# Usage:
#   ./git-setup.ps1            -> initializes local repo and commits
#   ./git-setup.ps1 <remote>   -> initializes and adds remote origin then pushes

param(
    [string]$remote
)

# Initialize git and create main branch
if (-not (Test-Path .git)) {
    git init -b main
} else {
    Write-Host ".git already exists"
}

# Add .gitignore and files
git add .gitignore
git add -A

git commit -m "chore: initial commit"

if ($remote) {
    git remote add origin $remote
    git branch -M main
    git push -u origin main
}
