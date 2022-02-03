import base64
from typing import Any, Dict, List, Mapping, Optional, Union
from typing_extensions import Literal, TypedDict
from black import json


from nacl.public import Box, PrivateKey, PublicKey
from nacl.signing import VerifyKey


"""

// A field type available in FormSG as a string
export type FieldType =
  | 'section'
  | 'radiobutton'
  | 'dropdown'
  | 'checkbox'
  | 'nric'
  | 'email'
  | 'table'
  | 'number'
  | 'rating'
  | 'yes_no'
  | 'decimal'
  | 'textfield' // Short Text
  | 'textarea' // Long Text
  | 'attachment'
  | 'date'
  | 'mobile'
  | 'homeno'

export type DecryptedContent = {
  responses: FormField[]
  verified?: Record<string, any>
}

export type FormField = {
  _id: string
  question: string
  fieldType: FieldType
  isHeader?: boolean
  signature?: string
} & (
  | { answer: string; answerArray?: never }
  | { answer?: never; answerArray: string[] | string[][] }
)


"""

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


"""
/**
 * Helper method to verify a signed message.
 * @param msg the message to verify
 * @param publicKey the public key to authenticate the signed message with
 * @returns the signed message if successful, else an error will be thrown
 * @throws {Error} if the message cannot be verified
 */
export const verifySignedMessage = (
  msg: Uint8Array,
  publicKey: string
): Record<string, any> => {
  const openedMessage = nacl.sign.open(msg, decodeBase64(publicKey))
  if (!openedMessage)
    throw new Error('Failed to open signed message with given public key')
  return JSON.parse(encodeUTF8(openedMessage))
}
"""


def verify_signed_message(msg: str, public_key: str) -> Dict[str, Any]:
    verify_key = VerifyKey(base64.b64decode(public_key))
    opened_message = verify_key.verify(msg)
    if not opened_message:
        raise Exception("Failed to open signed message with given public key")
    return json.loads(opened_message.decode("utf-8"))


def decrypt_content(form_private_key: str, encrypted_content: str) -> bytes:
    [submission_public_key, nonce_encrypted] = encrypted_content.split(";")
    [nonce, encrypted] = list(
        map(lambda x: base64.b64decode(x), nonce_encrypted.split(":"))
    )
    private_key = PrivateKey(base64.b64decode(form_private_key))
    public_key = PublicKey(base64.b64decode(submission_public_key))
    box = Box(private_key, public_key)
    # TODO: check if nonce needs to be b64
    return box.decrypt(encrypted, nonce)


def retrieve_attachment_filenames(decrypted_content: FieldType):
    return decrypted_content["field_type"] == "attachment" and decrypted_content.answer


def are_attachment_field_ids_valid(
    field_ids: List[str], filenames: Mapping[str, str]
) -> bool:
    return all(map(lambda field_id: field_id in filenames, field_ids))


def convert_encrypted_attachment_to_file_content(encrypted_attachment):
    print(
        "convert_encrypted_attachment_to_file_content.encrypted_attachment",
        encrypted_attachment,
    )
    return {
        "submission_public_key": encrypted_attachment["encryptedFile"][
            "submissionPublicKey"
        ],
        "nonce": encrypted_attachment["encryptedFile"]["nonce"],
        "binary": base64.b64decode(encrypted_attachment["encryptedFile"]["binary"]),
    }