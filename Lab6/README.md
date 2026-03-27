# ITSA-5504 – Module 6: Security & Compliance in Integration

This lab secures a Flask REST API with **JWT** authentication and runs over **HTTPS** using a self-signed certificate. It also simulates **IAM role checks** (admin vs user).

## Run locally
```bash
python -m venv .venv
source .venv/Scripts/activate        # Git Bash on Windows
pip install -r requirements.txt
python app.py