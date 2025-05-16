import argparse
import os
import json
import requests
import smtplib
from email.mime.text import MIMEText

GIST_ID = os.getenv('GIST_ID')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_TO = os.getenv('EMAIL_TO')

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = EMAIL_TO

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def get_sent_alerts():
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    gist = response.json()
    content = gist['files']['sent_alerts.json']['content']
    return json.loads(content)

def update_sent_alerts(sent_ids):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "files": {
            "sent_alerts.json": {
                "content": json.dumps(sent_ids, indent=2)
            }
        }
    }
    requests.patch(url, headers=headers, json=data)

def get_new_alerts_from_nws():
    # Dummy example alert
    return [{'id': 'abc123', 'title': 'Severe Thunderstorm Warning', 'body': 'Take cover now!'}]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-alert', action='store_true', help='Send a test alert email')
    args = parser.parse_args()

    if args.test_alert:
        send_email("Test Alert from Clayton's Weather", "This is a test alert email sent manually.")
        print("Test alert sent!")
        return

    sent_alerts = get_sent_alerts()
    new_alerts = get_new_alerts_from_nws()

    for alert in new_alerts:
        if alert['id'] not in sent_alerts:
            send_email(alert['title'], alert['body'])
            sent_alerts.append(alert['id'])

    update_sent_alerts(sent_alerts)

if __name__ == "__main__":
    main()
