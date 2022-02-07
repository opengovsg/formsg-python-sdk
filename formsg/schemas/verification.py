from typing_extensions import TypedDict

VerificationAuthenticateOptions = TypedDict(
    "VerificationAuthenticateOptions",
    {
        "signatureString": str,
        "submissionCreatedAt": int,
        "fieldId": str,
        "answer": str,
        "publicKey": str,
    },
)

VerificationSignatureSchema = TypedDict(
    "VerificationSignatureSchema", {"v": str, "t": int, "s": str, "f": str}
)

HeaderSignatureSchema = TypedDict(
    "HeaderSignatureSchema", {"v1": str, "t": int, "s": str, "f": str}
)
