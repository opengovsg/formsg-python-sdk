from typing import Optional

from formsg.constants import PUBLIC_KEY_PRODUCTION, PUBLIC_KEY_STAGING
from formsg.crypto import Crypto, DecryptParams
from formsg.webhook import Webhook


class FormSdk(object):
    # TODO: type(mode) == Literal
    def __init__(self, mode: str, webhook_secret_key: Optional[str] = None):
        self.mode = mode
        self.public_key: str
        if self.mode == "STAGING":
            self.public_key = PUBLIC_KEY_STAGING
        elif self.mode == "PRODUCTION":
            self.public_key = PUBLIC_KEY_PRODUCTION
        else:  # default to prod
            self.public_key = PUBLIC_KEY_PRODUCTION

        self.crypto = Crypto(self.public_key)
        self.webhook = Webhook(self.public_key, webhook_secret_key)

    def authenticate(self, header: str, uri: str) -> bool:
        return self.webhook.authenticate(header, uri)

    def decrypt(self, form_secret_key: str, decrypt_params: DecryptParams):
        return self.crypto.decrypt(form_secret_key, decrypt_params)

    def decrypt_attachments(self, form_secret_key: str, decrypt_params: DecryptParams):
        return self.crypto.decrypt_attachments(form_secret_key, decrypt_params)
