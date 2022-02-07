from typing import Any, List, Mapping, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

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

FormField = TypedDict(
    "FormField",
    {
        "_id": str,
        "question": str,
        "fieldType": FieldType,
        "isHeader": bool,
        "signature": Optional[str],
        "answer": Optional[str],
        "answerArray": Optional[Union[List[str], List[List[str]]]],
    },
)
DecryptedContent = TypedDict(
    "DecryptedContent",
    {"responses": List[FormField], "verified": NotRequired[Mapping[str, Any]]},
)

DecryptedFile = TypedDict("DecryptedFile", {"filename": str, "content": bytes})
DecryptedAttachments = Mapping[str, DecryptedFile]
DecryptedContentAndAttachments = TypedDict(
    "DecryptedContentAndAttachments",
    {"content": DecryptedContent, "attachments": DecryptedAttachments},
)


EncryptedAttachmentRecords = Mapping[str, str]

EncryptedFileContent = TypedDict(
    "EncryptedFileContent",
    {"submission_public_key": str, "nonce": str, "binary": bytes},
)


DecryptParams = TypedDict(
    "DecryptParams",
    {
        "encryptedContent": str,
        "version": str,
        "verifiedContent": Optional[str],
        "attachmentDownloadUrls": Optional[EncryptedAttachmentRecords],
    },
)
