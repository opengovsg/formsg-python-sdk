import base64
import logging
import time
import urllib

from nacl.bindings.crypto_sign import crypto_sign, crypto_sign_BYTES
from nacl.signing import VerifyKey
from typing_extensions import TypedDict

from formsg.exceptions import WebhookAuthenticateException

logger = logging.getLogger(__name__)

SignatureHeader = TypedDict(
    "SignatureHeader",
    {"v1": str, "t": int, "s": str, "f": str},
)


def is_signature_valid(
    uri: str, signature_header: SignatureHeader, public_key: str
) -> bool:
    """
    Helper function to construct the basestring and verify the signature of an
    incoming request
    :param: uri incoming request to verify
    :param: signatureHeader the X-FormSG-Signature header to verify against
    :rtype: :class:`bool` true if verification succeeds, false otherwise
    raises {WebhookAuthenticateError} if given signature header is malformed.
    """
    [signature, epoch, submission_id, form_id] = [
        signature_header["v1"],
        signature_header["t"],
        signature_header["s"],
        signature_header["f"],
    ]
    if not epoch or not signature or not submission_id or not form_id:
        raise WebhookAuthenticateException("X-FormSG-Signature header is invalid")

    parsed_url = urllib.parse.urlparse(uri).geturl()
    base_string = f"{parsed_url}.{submission_id}.{form_id}.{epoch}"
    v_key = VerifyKey(base64.b64decode(public_key))
    try:
        _verify(v_key, base_string, signature)
        return True
    except Exception as e:
        logger.error(e)
        return False


def _verify(verify_key: VerifyKey, uri: str, signature: str) -> bytes:
    return verify_key.verify(uri.encode("utf-8"), base64.b64decode(signature))


def has_epoch_expired(epoch: int, expiry: int = 300000) -> bool:
    """
    :param epoch: time in ms
    :param expiry: time in ms
    :rtype :class:`bool` if epoch has expired
    """
    # epoch is in ms, time.time() is in sec
    difference = abs(time.time() * 1000 - epoch)
    return difference > expiry


"""
# `nacl.signing.SigningKey` doesn't allow for a 64 bit salt, so we need to use their lower level API
# ref https://github.com/pyca/pynacl/issues/419#issuecomment-377520844
"""


def sign(base_string: str, secret_key: str) -> bytes:
    combined = crypto_sign(base_string.encode("utf-8"), base64.b64decode(secret_key))
    return base64.b64encode(combined[:crypto_sign_BYTES])
