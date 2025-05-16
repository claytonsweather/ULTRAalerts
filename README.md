# Weather Alert Sender System

## Overview
This repo contains a weather alert sender system running on GitHub Actions and controlled via a simple GitHub Pages website.

## Features
- Checks weather alerts every 10 minutes via GitHub Actions.
- Control locations and system ON/OFF status via a GitHub Pages website.
- Sends alert emails using SMTP (Gmail example).
- Manual and test alert sending from website.
- Prevents duplicate alert emails.
- OFF button to disable alert checking.

## Setup Instructions

### 1. Upload repo to GitHub
Push this repo content to your GitHub.

### 2. Configure GitHub Secrets
Go to your repo settings > Secrets > Actions and add:
- SMTP_USERNAME : your SMTP username (e.g., Gmail email)
- SMTP_PASSWORD : your SMTP password or app password
- EMAIL_TO : recipient email address

### 3. Enable GitHub Pages
- Go to Settings > Pages.
- Set source to `website/` folder on `main` branch.
- Save.

### 4. Edit config.json (optional)
- Modify locations or system_on status as needed.

### 5. Usage
- The alert checker runs automatically every 10 minutes.
- Open the website (https://your-username.github.io/your-repo/) to control locations, system status, and send manual/test alerts.

## Notes
- Uses NWS API for weather alerts by zone code.
- Email sending is done by GitHub Actions using Python SMTP script.
- Customize `scripts/check_alerts.py` and website as needed.