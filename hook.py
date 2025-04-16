from flask import Flask, request, Response
import json
import os
import requests
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import get_lexer_by_name
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables with defaults
INCOMING_HOOK_PATH = os.environ.get('INCOMING_HOOK_PATH', 'hook')
TARGET_URL = os.environ.get('TARGET_URL', '')

app = Flask(__name__)


@app.route("/")
def healthcheck():
    return "OK"


@app.route(f"/{INCOMING_HOOK_PATH}", methods=["POST"])
def relay_webhook():
    # Prepare headers dictionary
    #headers_dict = dict(request.headers)

    # Handle different content types
    content_type = request.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        body_data = request.json
    elif 'application/x-www-form-urlencoded' in content_type:
        body_data = request.form.to_dict()
    else:
        body_data = {"raw_data": request.data.decode('utf-8', errors='replace')}

    # Log the payload for debugging
    #print(f"Relaying webhook to: {TARGET_URL}")
    #print(_highlight(json.dumps(payload, indent=4)))

    # Send to target URL if configured
    if TARGET_URL:
        try:
            response = requests.post(
                TARGET_URL,
                json=body_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Relayed to target.  Target response status: {response.status_code}")
            return f"{response.status_code}", response.status_code
        except requests.RequestException as e:
            print(f"Error relaying to target: {e}")
            return f"500", 500
    else:
        print("No TARGET_URL configured. Webhook received but not relayed.")
        return "OK", 200


def _highlight(json_data):
    return highlight(
        code=json_data,
        lexer=get_lexer_by_name("json"),
        formatter=Terminal256Formatter(style="solarized-dark"),
    )


if __name__ == '__main__':
    print(f"Listening for webhooks at /{INCOMING_HOOK_PATH}")
    print(f"Target URL: {TARGET_URL or 'Not configured'}")
    app.run(debug=False)
