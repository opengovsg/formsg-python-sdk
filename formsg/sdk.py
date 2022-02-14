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
        self.webhooks = Webhook(self.public_key, webhook_secret_key)
