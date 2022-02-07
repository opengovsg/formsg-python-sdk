from typing import Any, List, Mapping, Optional, Union

from typing_extensions import Literal, TypedDict

FieldType = Union[
    Literal["section"],
    Literal["radiobutton"],
    Literal["dropdown"],
    Literal["checkbox"],
    Literal["nric"],
    Literal["email"],
    Literal["table"],
    Literal["number"],
    Literal["rating"],
    Literal["yes_no"],
    Literal["decimal"],
    Literal["textfield"],  # short text
    Literal["textarea"],  # long text
    Literal["attachment"],
    Literal["date"],
    Literal["mobile"],
    Literal["homeno"],
]
FormFieldSignature = TypedDict(
    "FormFieldSignature",
    {
        "answer": Optional[str],
        "answer_array": Optional[Union[List[str], List[List[str]]]],
    },
)
FormField = TypedDict(
    "FormField",
    {
        "_id": str,
        "question": str,
        "field_type": FieldType,
        "is_header": bool,
        "signature": Optional[FormFieldSignature],
    },
)
DecryptedContent = TypedDict(
    "DecryptedContent",
    {"responses": List[FormField], "verified": Optional[Mapping[str, Any]]},
)

DecryptedFile = TypedDict("DecryptedFile", {"filename": str, "content": bytes})
DecryptedAttachments = Mapping[str, DecryptedFile]
DecryptedContentAndAttachments = TypedDict(
    "DecryptedContentAndAttachments",
    {"content": DecryptedContent, "attachments": DecryptedAttachments},
)


EncryptedAttachmentRecords = Mapping[str, str]

DecryptParams = TypedDict(
    "DecryptParams",
    {
        "encryptedContent": str,
        "version": str,
        "verifiedContent": Optional[str],
        "attachmentDownloadUrls": Optional[EncryptedAttachmentRecords],
    },
)
