from typing import Dict, Union
from typing_extensions import TypedDict
import time
import base64
from nacl.signing import VerifyKey


from formsg.exceptions import WebhookAuthenticateException

SignatureHeader = TypedDict(
    "SignatureHeader",
    {"v1": str, "t": int, "s": str, "f": str},
)


def _extract_key_values(s: str) -> dict:
    tokens = s.split(",")
    d: Dict[str, Union[str, int]] = dict()
    for token in tokens:
        k, v = token.split("=", maxsplit=1)
        d[k] = v
    return d


def _parse_signature_header(header: str):
    parsed_signature = _extract_key_values(header)
    parsed_signature["t"] = int(parsed_signature["t"])
    return parsed_signature


def is_signature_valid(
    uri: str, signature_header: SignatureHeader, public_key: str
) -> bool:
    """
    /**
     * Helper function to construct the basestring and verify the signature of an
     * incoming request
     * @param uri incoming request to verify
     * @param signatureHeader the X-FormSG-Signature header to verify against
     * @returns true if verification succeeds, false otherwise
     * @throws {WebhookAuthenticateError} if given signature header is malformed.
     */
    """
    [signature, epoch, submission_id, form_id] = [
        signature_header["v1"],
        signature_header["t"],
        signature_header["s"],
        signature_header["f"],
    ]
    if not epoch or not signature or not submission_id or not form_id:
        raise WebhookAuthenticateException("X-FormSG-Signature header is invalid")

    base_string = f"{uri}.{submission_id}.{form_id}.{epoch}"
    v_key = VerifyKey(base64.b64decode(public_key))
    return _verify(v_key, base_string, signature)


def _verify(verify_key: VerifyKey, uri: str, signature: str) -> bytes:
    return verify_key.verify(uri.encode("utf-8"), base64.b64decode(signature))


def has_epoch_expired(epoch: int, expiry: int = 300000) -> bool:
    # epoch is in ms, time.time() is in sec
    difference = abs(time.time() * 1000 - epoch)
    return difference > expiry