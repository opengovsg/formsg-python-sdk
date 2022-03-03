import json
from flask import Flask, request, Response
import formsg
from formsg.exceptions import WebhookAuthenticateException

app = Flask(__name__)

FORM_SECRET_KEY = "YOUR-SECRET-KEY"
YOUR_WEBHOOK_URI = "your-webhook-uri"

# accepts STAGING or PRODUCTION, determines whether to use staging or production public signing keys
sdk = formsg.FormSdk("PRODUCTION")


@app.route("/webhook", methods=["POST"])
def webhook_route():
    posted_data = json.loads(request.data)

    try:
        sdk.webhooks.authenticate(
            request.headers["X-FormSG-Signature"], YOUR_WEBHOOK_URI
        )
    except WebhookAuthenticateException as e:
        print(e)
        return Response("Unauthorized", 401)

    # decryption without attachments
    # if `verifiedContent` exists as a key in `posted_data['data']`, the return object will include a verified key
    responses = sdk.crypto.decrypt(FORM_SECRET_KEY, posted_data["data"])

    # decryption with attachments
    responses_with_attachments = sdk.crypto.decrypt_with_attachments(
        FORM_SECRET_KEY, posted_data["data"]
    )
    return Response(json.dumps({"message": "ok"}), 202)
