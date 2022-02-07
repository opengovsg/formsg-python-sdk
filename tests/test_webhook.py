import datetime

import pytest
from formsg.webhook import Webhook

PUBLIC_KEY = "KUY1XT30ar+XreVjsS1w/c3EpDs2oASbF6G3evvaUJM="
SECRET_KEY = "/u+LP57Ib9y5Ytpud56FzuitSC9O6lJ4EOLOFHpsHlYpRjVdPfRqv5et5WOxLXD9zcSkOzagBJsXobd6+9pQkw=="

uri = "https://some-endpoint.com/post"
submission_id = "someSubmissionId"
form_id = "someFormId"


class TestWebhooks:
    def webhooks(self):
        return Webhook(public_key=PUBLIC_KEY, secret_key=SECRET_KEY)

    def generate_test_signature(self, epoch: int):
        return self.webhooks().generate_signature(
            {
                "uri": uri,
                "submissionId": submission_id,
                "formId": form_id,
                "epoch": epoch,
            }
        )

    def test_sign_and_generate_correctly(self):
        epoch = 1583136171649
        signature = self.generate_test_signature(epoch)
        assert (
            signature
            == "KMirkrGJLPqu+Na+gdZLUxl9ZDgf2PnNGPnSoG1FuTMRUTiQ6o0jB/GTj1XFjn2s9JtsL5GiCmYROpjJhDyxCw=="
        )

    def test_accept_signature_within_5_min(self):
        sometime_ago = datetime.datetime.now() - datetime.timedelta(
            minutes=4, seconds=59
        )
        # .timestamp() returns seconds
        epoch = int(sometime_ago.timestamp() * 1000)
        signature = self.generate_test_signature(epoch)
        header = self.webhooks().construct_header(
            {
                "epoch": epoch,
                "submissionId": submission_id,
                "formId": form_id,
                "signature": signature,
            }
        )
        assert self.webhooks().authenticate(header, uri)
