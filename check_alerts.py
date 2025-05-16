import os
import json
import smtplib
from email.message import EmailMessage
import requests

CONFIG_FILE = "config.json"
EMAIL_TEMPLATE = "email_template.txt"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def fetch_alerts(zone_code):
    url = f"https://api.weather.gov/alerts/active/zone/{zone_code}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("features", [])
    except Exception as e:
        print(f"Error fetching alerts for {zone_code}: {e}")
        return []

def send_email(to_email, subject, body):
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    if not username or not password:
        print("SMTP credentials not set.")
        return
    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(username, password)
            smtp.send_message(msg)
            print(f"Sent email to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    config = load_config()
    if not config.get("system_on", False):
        print("System is OFF. Exiting.")
        return

    sent_alerts = set(config.get("sent_alerts", []))
    email_to = os.environ.get("EMAIL_TO")
    if not email_to:
        print("EMAIL_TO env var not set.")
        return

    for loc in config.get("locations", []):
        zone = loc.get("zone_code")
        name = loc.get("name")
        alerts = fetch_alerts(zone)
        for alert in alerts:
            alert_id = alert.get("id")
            if alert_id in sent_alerts:
                continue
            props = alert.get("properties", {})
            headline = props.get("headline", "Weather Alert")
            description = props.get("description", "")
            subject = f"Weather Alert for {name}: {headline}"
            body = description + "\n\n--\nWeather Alert System"
            send_email(email_to, subject, body)
            sent_alerts.add(alert_id)

    config["sent_alerts"] = list(sent_alerts)
    save_config(config)

if __name__ == "__main__":
    main()