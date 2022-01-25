import base64
from formsg.util.crypto import (
    are_attachment_field_ids_valid,
    convert_encrypted_attachment_to_file_content,
    decrypt_content,
    verify_signed_message,
)
from formsg.exceptions import AttachmentDecryptionException, MissingPublicKeyException
from typing import Mapping, Optional
from typing_extensions import TypedDict

from nacl.public import Box, PrivateKey, PublicKey
import json

import requests

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


class Crypto(object):
    def __init__(self, signing_public_key: str):
        self.signing_public_key = signing_public_key

    """
    /**
    * Decrypts an encrypted submission and returns it.
    * @param formSecretKey The base-64 secret key of the form to decrypt with.
    * @param decryptParams The params containing encrypted content and information.
    * @param decryptParams.encryptedContent The encrypted content encoded with base-64.
    * @param decryptParams.version The version of the payload. Used to determine the decryption process to decrypt the content with.
    * @param decryptParams.verifiedContent Optional. The encrypted and signed verified content. If given, the signingPublicKey will be used to attempt to open the signed message.
    * @returns The decrypted content if successful. Else, null will be returned.
    * @throws {MissingPublicKeyError} if a public key is not provided when instantiating this class and is needed for verifying signed content.
    */
    """

    def decrypt(self, form_secret_key: str, decrypt_params: DecryptParams):
        decrypted_bytes = decrypt_content(
            form_secret_key, decrypt_params["encryptedContent"]
        )
        # nacl.exceptions.CryptoError?

        decrypted_object = json.loads(decrypted_bytes.decode("utf-8"))
        returned_object = {}
        returned_object["responses"] = decrypted_object

        # do I need to verify?
        if "verifiedContent" in decrypt_params:
            if not self.signing_public_key:
                raise MissingPublicKeyException(
                    "Public signing key must be provided when instantiating the Crypto class in order to verify verified content"
                )
            decrypted_verified_content = decrypt_content(
                form_secret_key, decrypt_content["verifiedContent"]
            )
            if not decrypted_verified_content:
                raise Exception("Failed to decrypt verified content")

            decrypted_verified_object = verify_signed_message(
                decrypted_verified_content, self.signing_public_key
            )
        return returned_object

    def decrypt_file(self, form_secret_key: str, encrypted_file_content):
        """ """
        # nacl.box.open(box, nonce, theirPublicKey, mySecretKey)
        box = Box(
            PrivateKey(base64.b64decode(form_secret_key)),
            PublicKey(
                base64.b64decode(encrypted_file_content["submission_public_key"])
            ),
        )
        return box.decrypt(
            encrypted_file_content["binary"],
            base64.b64decode(encrypted_file_content["nonce"]),
        )

    def decrypt_attachments(self, form_secret_key: str, decrypt_params: DecryptParams):
        if "attachmentDownloadUrls" not in decrypt_params:
            raise Exception("`attachmentDownloadUrls` param not passed")

        # const attachmentRecords: EncryptedAttachmentRecords =
        # decryptParams.attachmentDownloadUrls ?? {}
        attachment_records = decrypt_params.get("attachmentDownloadUrls", {})

        decrypted_content_bytes = decrypt_content(
            form_secret_key, decrypt_params["encryptedContent"]
        )
        decrypted_content = json.loads(decrypted_content_bytes.decode("utf-8"))
        # TODO: raise exception

        decrypted_records = {}
        filenames = {}
        for response in decrypted_content:
            if response["fieldType"] == "attachment" and response["answer"]:
                filenames[response["_id"]] = response["answer"]

        field_ids = attachment_records.keys()

        if not are_attachment_field_ids_valid(field_ids, filenames):
            return None

        # TODO: does this need to be parallel?
        for field_id in field_ids:
            resp = requests.get(attachment_records[field_id])
            data = resp.json()
            encrypted_file = convert_encrypted_attachment_to_file_content(data)
            decrypted_file = self.decrypt_file(form_secret_key, encrypted_file)
            if not decrypted_file:
                raise AttachmentDecryptionException()
            decrypted_records[field_id] = {
                "filename": filenames[field_id],
                "content": decrypted_file,
            }

        return {"content": decrypt_content, "attachments": decrypted_records}
