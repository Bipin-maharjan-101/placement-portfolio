# 🚀 HOW TO PUSH THIS PORTFOLIO TO GITHUB

Follow these steps exactly to get your portfolio live on GitHub.

---

## STEP 1 — Create a GitHub account (if you don't have one)
Go to: https://github.com/signup
Use your real name — recruiters will see this.

---

## STEP 2 — Create a new repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `placement-portfolio`
3. Description: `Business, Finance & Business Analysis projects for placement year applications 2026`
4. Set to **Public** (so recruiters can see it)
5. Do NOT tick "Add README" — we already have one
6. Click **Create repository**

---

## STEP 3 — Install Git (if not already installed)

Windows: https://git-scm.com/download/win
Mac:     Already installed (check with: git --version)
Linux:   sudo apt install git

---

## STEP 4 — Open Terminal / Command Prompt and run these commands

```bash
# Navigate to the portfolio folder (adjust path as needed)
cd placement-portfolio

# Initialise git
git init

# Add all files
git add .

# Create your first commit
git commit -m "Add placement portfolio: 8 projects in business, finance & business analysis"

# Connect to your GitHub repository
# REPLACE 'yourusername' with your actual GitHub username
git remote add origin https://github.com/yourusername/placement-portfolio.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## STEP 5 — Verify it's live

Go to: https://github.com/yourusername/placement-portfolio

You should see all 8 project folders and the main README.

---

## STEP 6 — Add it to your CV

In your CV under Projects or Skills, write:

  GitHub Portfolio: github.com/yourusername/placement-portfolio

Or link it directly in your LinkedIn profile under "Featured" or "Projects".

---

## STEP 7 — Keep it updated

Each time you improve a project:
```bash
git add .
git commit -m "Improve project 5: add additional ratio analysis"
git push
```

Commit history shows employers you actively work on your projects.

---

## TIPS FOR MAKING YOUR GITHUB LOOK PROFESSIONAL

1. Add a profile README at: github.com/yourusername
   (Create a repo named exactly your username and add a README.md)

2. Pin this repository to your profile

3. Add topics/tags to the repo:
   python, finance, business-analysis, data-visualisation, placement

4. Make sure your GitHub profile has:
   - Your real name
   - A profile picture
   - A bio mentioning you're seeking a placement in finance/business

---

## NEED HELP?

GitHub docs: https://docs.github.com/en/get-started
Git tutorial: https://www.atlassian.com/git/tutorials
