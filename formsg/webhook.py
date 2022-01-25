from formsg.util.webhook import (
    _parse_signature_header,
    is_signature_valid,
    has_epoch_expired,
)
from formsg.exceptions import WebhookAuthenticateException


class Webhook(object):
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key

    def authenticate(self, header: str, uri: str) -> bool:
        """
        * Injects the webhook public key for authentication
        * @param header X-FormSG-Signature header
        * @param uri The endpoint that FormSG is POSTing to
        * @returns true if the header is verified
        * @throws {WebhookAuthenticateError} If the signature or uri cannot be verified
        """
        signature_header = _parse_signature_header(header)
        [signature, epoch, submission_id, form_id] = [
            signature_header["v1"],
            signature_header["t"],
            signature_header["s"],
            signature_header["f"],
        ]

        # verify signature authenticity
        try:
            is_signature_valid(uri, signature_header, self.public_key)
        except:
            raise WebhookAuthenticateException(
                f"Signature could not be verified for uri={uri} submission_id={submission_id} form_id={form_id} epoch={epoch} signature={signature}"
            )

        # verify epoch recency
        if has_epoch_expired(epoch):
            raise WebhookAuthenticateException(
                "Signature is not recent for uri={uri} submission_id={submission_id} form_id={form_id} epoch={epoch} signature={signature}"
            )

        return True
