# Quick Start Cheat Sheet

## First Time Setup (Do Once)

```bash
# 1. Install Git (if not already installed)
git --version  # Check if installed
brew install git  # Mac
# Or download from https://git-scm.com

# 2. Configure Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Go to github.com and create an account

# 4. Create a new repository on GitHub
#    - Name: sec-filing-renamer
#    - Don't initialize with README
#    - Copy the repository URL

# 5. Navigate to your project folder
cd /path/to/sec-filing-renamer

# 6. Initialize and push
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOURUSERNAME/sec-filing-renamer.git
git branch -M main
git push -u origin main
```

## Daily Workflow

```bash
# After making changes to your code:

git status              # See what changed
git add .               # Stage all changes
git commit -m "Fix percentage extraction bug"
git push                # Send to GitHub
```

## That's It!

Those are the only commands you'll use 90% of the time.

## View Your Project

Go to: `https://github.com/YOURUSERNAME/sec-filing-renamer`

## Common Issues

**Git asks for password**: Use a Personal Access Token instead
- GitHub → Settings → Developer settings → Personal access tokens
- Generate new token → Copy it
- Use token as password when Git asks

**"Permission denied"**: Authentication issue, check your token/credentials

**Want to undo changes before commit**: 
```bash
git checkout -- filename.py
```

**Made a bad commit**:
```bash
git reset --soft HEAD~1  # Undo commit, keep changes
```
