from typing import Dict, Union, cast

from formsg.schemas.verification import VerificationSignatureSchema


def _extract_key_values(s: str) -> dict:
    tokens = s.split(",")
    d: Dict[str, Union[str, int]] = dict()
    for token in tokens:
        k, v = token.split("=", maxsplit=1)
        d[k] = v
    return d


def parse_signature_header(header: str):
    parsed_signature = _extract_key_values(header)
    parsed_signature["t"] = int(parsed_signature["t"])
    return parsed_signature


def parse_verification_signature(signature: str):
    parsed_signature = cast(VerificationSignatureSchema, {})
    parsed_signature = _extract_key_values(signature)  # type: ignore
    parsed_signature["t"] = int(parsed_signature["t"])
    return parsed_signature
