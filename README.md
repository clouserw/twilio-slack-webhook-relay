Twilio sends webhooks as form encoded query parameters with empty bodies.  Slack expects webhook data to be JSON.  This accepts webhooks from Twilio converts them to JSON and forwards them on.

# Usage

1. **Get the code**
```bash
git clone https://github.com/clouserw/twilio-slack-webhook-relay
cd twilio-slack-webhook-relay
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configure**
Make a `.env` file in the same directory as `hook.py`.  Format:

```
# This should be a random string of URL friendly characters.  It's where you will post the incoming webhooks
INCOMING_HOOK_PATH="oaskdflaksjdflaksjdflaskdfalaksdjf"

# Where should the webhooks be sent to?
TARGET_URL="https://hooks.slack.com/triggers/abc/123/xyz"
```

3. Run it
```bash
python hook.py
```

# To deploy on Heroku

```
# Add --team <teamname> if appropriate
heroku create twilio-slack-webhook-relay
```

Set up your environment variables as above in the heroku dashboard.  

Then from the `twilio-slack-webhook-relay` directory:

```
git push heroku master
```

The log output should tell you what URL it's listening on.