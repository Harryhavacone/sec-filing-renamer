# GitHub Beginner's Guide for Your SEC Filing Renamer Project

This guide will walk you through setting up Git, creating a GitHub account, and publishing your project.

## What Are Git and GitHub?

- **Git**: Version control software that tracks changes to your code over time
- **GitHub**: A website that hosts Git repositories and makes sharing/collaboration easy

Think of it like "Track Changes" for code, but much more powerful.

## Step 1: Install Git

### On Mac:
```bash
# Check if Git is already installed
git --version

# If not installed, install via Homebrew
brew install git

# Or download from: https://git-scm.com/download/mac
```

### On Windows:
Download and install from: https://git-scm.com/download/win

### On Linux:
```bash
sudo apt install git  # Ubuntu/Debian
```

## Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

This information will be attached to your commits (saved changes).

## Step 3: Create a GitHub Account

1. Go to https://github.com
2. Click "Sign up"
3. Follow the prompts to create your account
4. Verify your email address

## Step 4: Create a New Repository on GitHub

1. Log into GitHub
2. Click the "+" in the top right corner
3. Select "New repository"
4. Fill in:
   - **Repository name**: `sec-filing-renamer`
   - **Description**: "Automatically rename SEC filing PDFs based on their content"
   - **Public or Private**: Choose based on preference
     - Public: Anyone can see it (good for portfolio)
     - Private: Only you can see it
   - **Do NOT check** "Initialize this repository with a README" (we already have one)
5. Click "Create repository"

GitHub will show you a page with instructions. Keep this page open!

## Step 5: Initialize Git in Your Project

Open Terminal and navigate to your project folder:

```bash
cd /path/to/sec-filing-renamer
```

Initialize Git:

```bash
# Initialize a new Git repository
git init

# Add all files to staging
git add .

# Make your first commit
git commit -m "Initial commit: SEC filing PDF renamer"
```

## Step 6: Connect Your Local Project to GitHub

Copy the commands from the GitHub page (under "…or push an existing repository from the command line"):

```bash
# Add GitHub as the remote repository
git remote add origin https://github.com/yourusername/sec-filing-renamer.git

# Rename the default branch to 'main' (modern standard)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Note**: Replace `yourusername` with your actual GitHub username.

If prompted for credentials, you may need to set up a Personal Access Token (GitHub no longer accepts passwords). See "Authentication" section below.

## Step 7: Making Changes and Updating GitHub

After you modify your code:

```bash
# Check which files have changed
git status

# Add specific files
git add src/renamer.py

# Or add all changed files
git add .

# Commit with a descriptive message
git commit -m "Fix: Handle uppercase Row in percentage extraction"

# Push to GitHub
git push
```

## Common Git Commands

```bash
# See current status
git status

# See commit history
git log

# See what changed in a file
git diff src/renamer.py

# Undo changes to a file (before committing)
git checkout -- src/renamer.py

# Create a new branch for experiments
git checkout -b new-feature

# Switch back to main branch
git checkout main

# Pull latest changes from GitHub
git pull
```

## Authentication with GitHub

GitHub requires authentication for pushing code. You have two options:

### Option 1: Personal Access Token (Recommended)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "My laptop"
4. Select scopes: Check "repo" (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)
7. When Git asks for password, paste the token instead

### Option 2: SSH Keys (More Secure, Slightly More Setup)

Follow GitHub's guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Understanding the Workflow

```
1. Make changes to code
   ↓
2. git add (stage changes)
   ↓
3. git commit (save changes locally)
   ↓
4. git push (send to GitHub)
```

## Good Commit Message Practices

Good commit messages help you understand what changed and why:

**Good examples:**
- `Fix: Handle multi-line percentage format in PDFs`
- `Add: Support for DEF 14A filing type`
- `Update: README with new installation instructions`
- `Refactor: Extract date parsing into separate function`

**Bad examples:**
- `fix bug`
- `changes`
- `asdf`
- `working version`

## .gitignore Explained

The `.gitignore` file tells Git which files to ignore. We're ignoring:
- `*.pdf` - Don't commit actual PDF files to the repo
- `__pycache__/` - Python's compiled bytecode files
- `.vscode/`, `.idea/` - Editor configuration files
- `test_files/` - Your local test directory

## Viewing Your Project on GitHub

After pushing, go to: `https://github.com/yourusername/sec-filing-renamer`

You'll see:
- Your README displayed nicely
- File browser
- Commit history
- Issues, Pull Requests (for collaboration)

## Project Structure Best Practices

Your project now follows standard Python conventions:

```
sec-filing-renamer/
├── README.md              # First thing people see - explains the project
├── requirements.txt       # Lists dependencies (pip install -r requirements.txt)
├── .gitignore            # Files Git should ignore
├── LICENSE               # How others can use your code
├── src/
│   └── renamer.py        # Main source code
└── (future additions)
    ├── tests/            # Unit tests (optional but good practice)
    └── docs/             # Additional documentation
```

## Next Steps

Once you're comfortable with basics:

1. **Branches**: Create feature branches for experiments
   ```bash
   git checkout -b add-excel-export
   # Make changes
   git commit -m "Add: Excel export feature"
   git push -u origin add-excel-export
   ```

2. **Issues**: Track bugs and features on GitHub's Issues tab

3. **Releases**: Tag versions when you have stable milestones
   ```bash
   git tag -a v1.0.0 -m "First release"
   git push origin v1.0.0
   ```

4. **Collaborators**: Invite others to contribute

## Troubleshooting

**"Permission denied"**: Check your authentication (token or SSH)

**"Your branch is behind 'origin/main'"**: Someone else pushed changes
```bash
git pull  # Get the latest changes
```

**"Merge conflict"**: Two people edited the same lines
- Git will mark the conflicts in the file
- Edit the file to resolve
- `git add` the resolved file
- `git commit`

**Want to undo the last commit**:
```bash
git reset --soft HEAD~1  # Keeps your changes
git reset --hard HEAD~1  # Discards your changes (careful!)
```

## Resources

- GitHub's interactive tutorial: https://skills.github.com
- Git documentation: https://git-scm.com/doc
- GitHub docs: https://docs.github.com

## Quick Reference Card

```bash
# Setup (once)
git init
git remote add origin https://github.com/user/repo.git

# Daily workflow
git status                    # What changed?
git add .                     # Stage all changes
git commit -m "Description"   # Save changes
git push                      # Send to GitHub

# Get updates
git pull                      # Download latest from GitHub

# Check history
git log                       # See commit history
git log --oneline             # Compact history
```

Happy coding! Remember: commit early, commit often, and write descriptive messages!
