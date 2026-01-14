# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., "Social_Media_Apps")
5. Choose public or private
6. **DO NOT** initialize with README, .gitignore, or license
7. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, run these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME and REPOSITORY_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git

# Push your code to GitHub
git push -u origin main
```

## Alternative: Using SSH (if you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
git push -u origin main
```

## Example Commands

If your GitHub username is "johndoe" and repository name is "Social_Media_Apps":

```bash
git remote add origin https://github.com/johndoe/Social_Media_Apps.git
git push -u origin main
```

## What's Already Done

✅ Git repository initialized
✅ .gitignore file created (excludes venv, db.sqlite3, media files, etc.)
✅ README.md created with project documentation
✅ Initial commit made with all project files

## Files Included

- All source code (Python, HTML, CSS, JavaScript)
- Templates
- Static files
- Configuration files
- Requirements.txt

## Files Excluded (via .gitignore)

- Virtual environment (venv/)
- Database file (db.sqlite3)
- Media uploads (/media)
- Python cache files (__pycache__/)
- IDE files (.vscode/, .idea/)
