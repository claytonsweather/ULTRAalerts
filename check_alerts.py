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
    url = "https://api.weather.gov/alerts/active"
    response = requests.get(url, headers={"User-Agent": "ClaytonsWeatherAlerts"})
    alerts = response.json().get("features", [])
    filtered_alerts = []

    for alert in alerts:
        props = alert.get("properties", {})
        event = props.get("event", "")
        alert_id = alert.get("id")

        area_desc = props.get("areaDesc", "Unknown Area")
        headline = props.get("headline", "")
        description = props.get("description", "")
        instruction = props.get("instruction", "")
        effective = props.get("effective", "")
        expires = props.get("expires", "")

        # Highlight severe events in subject
        highlight = "🚨 " if any(x in event for x in ["Tornado", "Severe Thunderstorm", "Flash Flood"]) else ""

        title = f"{highlight}{event} for {area_desc}"
        body = f"{headline}\n\n{description}\n\n{instruction}\n\nAreas affected: {area_desc}\nEffective: {effective}\nExpires: {expires}"

        filtered_alerts.append({
            "id": alert_id,
            "title": title,
            "body": body
        })

    return filtered_alerts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-alert', action='store_true')
    args = parser.parse_args()

    sent_alerts = get_sent_alerts()

    if args.test_alert:
        send_email("Test Alert", "This is a test of the ULTRAalerts system.")
        return

    new_alerts = get_new_alerts_from_nws()
    unsent_alerts = [a for a in new_alerts if a['id'] not in sent_alerts]

    for alert in unsent_alerts:
        send_email(alert['title'], alert['body'])
        sent_alerts.append(alert['id'])

    if unsent_alerts:
        update_sent_alerts(sent_alerts)

if __name__ == "__main__":
    main()

