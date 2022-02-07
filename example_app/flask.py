import json
from flask import Flask, request, Response
import formsg

app = Flask(__name__)

FORM_SECRET_KEY = "YOUR-SECRET-KEY"


@app.route("/webhook", methods=["POST"])
def webhook_route():
    posted_data = json.loads(request.data)
    print(posted_data)
    print(request.headers)
    uri = "this endpoint's uri"
    sdk = formsg.FormSdk("PRODUCTION")
    sdk.authenticate(request.headers["X-FormSG-Signature"], uri)
    responses = sdk.decrypt(FORM_SECRET_KEY, posted_data["data"])
    print(responses)
    return Response(json.dumps({"message": "ok"}), 202)
