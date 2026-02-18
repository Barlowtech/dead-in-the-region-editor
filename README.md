# Dead in the Region — Episode Editor

A Streamlit web app for collaboratively editing the Season 1 episode guide for *Dead in the Region*, a fictional true-crime podcast set in NWI and Chicagoland.

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/dead-in-the-region-editor.git
cd dead-in-the-region-editor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud (Free — Shareable URL)

This is how you get a URL you can share with a collaborator.

### Step 1: Push to GitHub

Create a new GitHub repo and push this folder:

```bash
cd dead-in-the-region-editor
git init
git add .
git commit -m "Initial commit — episode editor app"
git remote add origin https://github.com/YOUR_USERNAME/dead-in-the-region-editor.git
git push -u origin main
```

### Step 2: Create a GitHub Personal Access Token

The app needs write access to push CSV changes back to the repo.

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Name it something like `episode-editor`
4. Set **Repository access** to "Only select repositories" → select your repo
5. Under **Permissions → Repository permissions**, set **Contents** to "Read and write"
6. Click **Generate token** and copy it

### Step 3: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repo, branch (`main`), and main file (`app.py`)
5. Click **"Advanced settings"** and add your secrets:

```toml
[github]
token = "ghp_your_token_here"
repo = "YOUR_USERNAME/dead-in-the-region-editor"
file_path = "data/episodes.csv"
branch = "main"
```

6. Click **Deploy**

Your app will be live at a URL like `https://dead-in-the-region-editor.streamlit.app`.

### Step 4: Share

Send the URL to your collaborator. They can edit episodes and save changes. Every save commits the updated CSV back to GitHub, so you have a full history of every change.

## How It Works

- **Sidebar**: Select any of the 12 episodes
- **Main area**: All fields for that episode, organized into sections (Structure, Story, Host Dynamic, Season Arc, Tone & Production)
- **Save**: Writes changes to the CSV and commits to GitHub
- **Download CSV**: Export the current state as a file at any time

## File Structure

```
├── app.py                          # Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   └── episodes.csv                # Episode guide data (the source of truth)
├── .streamlit/
│   ├── config.toml                 # Theme (dark mode, firebrick red accent)
│   └── secrets.toml.example        # Template for GitHub credentials
└── README.md
```

## Without GitHub Integration

If you don't set up the GitHub token, the app still works — it saves changes to the local CSV file. This is fine for solo use or local development. The GitHub integration is only needed for the shared/deployed version where multiple people edit the same data.
