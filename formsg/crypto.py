import base64
import json
import logging
from typing import Mapping, Optional, Union

import requests
from nacl.exceptions import CryptoError
from nacl.public import Box, PrivateKey, PublicKey
from typing_extensions import TypedDict

from formsg.exceptions import AttachmentDecryptionException, MissingPublicKeyException
from formsg.schemas.crypto import DecryptParamsSchema
from formsg.util.crypto import (
    are_attachment_field_ids_valid,
    convert_encrypted_attachment_to_file_content,
    decrypt_content,
    verify_signed_message,
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


logger = logging.getLogger(__name__)


class Crypto(object):
    def __init__(self, signing_public_key: str):
        self.signing_public_key = signing_public_key

    def decrypt(self, form_secret_key: str, decrypt_params: DecryptParams):
        """
        Decrypts an encrypted submission and returns it.
        :param: form_secret_key The base-64 secret key of the form to decrypt with.
        :param: decrypt_params :class:`dict` The params containing encrypted content and information
        :param: decrypt_params.encryptedContent The encrypted content encoded with base-64.
        :param: decrypt_params.version The version of the payload. Used to determine the decryption process to decrypt the content with.
        :param: decrypt_params.verifiedContent Optional. The encrypted and signed verified content. If given, the signingPublicKey will be used to attempt to open the signed message.
        :returns: The decrypted content if successful. Else, null will be returned.
        :throws: {MissingPublicKeyError} if a public key is not provided when instantiating this class and is needed for verifying signed content.
        """
        decrypted_bytes = None

        schema = DecryptParamsSchema()
        try:
            schema.load(
                decrypt_params, unknown="INCLUDE"
            )  # do not raise exception on unknown/unspecified fields
        except Exception as e:
            logger.error(e)
            return None

        decrypted_bytes = decrypt_content(
            form_secret_key, decrypt_params["encryptedContent"]
        )
        if not decrypted_bytes:
            raise Exception("Failed to decrypt content")

        decrypted_object = json.loads(decrypted_bytes.decode("utf-8"))
        returned_object = {}
        returned_object["responses"] = decrypted_object

        if "verifiedContent" in decrypt_params:
            if not self.signing_public_key:
                raise MissingPublicKeyException(
                    "Public signing key must be provided when instantiating the Crypto class in order to verify verified content"
                )
            decrypted_verified_content = decrypt_content(
                form_secret_key, decrypt_params["verifiedContent"]  # type: ignore
            )
            if not decrypted_verified_content:
                raise Exception("Failed to decrypt verified content")

            decrypted_verified_object = verify_signed_message(
                decrypted_verified_content, self.signing_public_key
            )
            returned_object["verified"] = decrypted_verified_object

        return returned_object

    def decrypt_file(
        self, form_secret_key: str, encrypted_file_content
    ) -> Union[bytes, None]:
        """
        Decrypt the given encrypted file content.
        :param form_secret_key Secret key as a base-64 string
        :param encrypted_file_content Object returned from encryptFile function
        :param encrypted_file_content.submissionPublicKey The submission public key as a base-64 string
        :param encrypted_file_content.nonce The nonce as a base-64 string
        :param encrypted_file_content.blob The encrypted file as a Blob object

        """
        box = Box(
            PrivateKey(base64.b64decode(form_secret_key)),
            PublicKey(
                base64.b64decode(encrypted_file_content["submission_public_key"])
            ),
        )
        try:
            decrypted = box.decrypt(
                encrypted_file_content["binary"],
                base64.b64decode(encrypted_file_content["nonce"]),
            )
            return decrypted
        except CryptoError:
            logger.error("Error decrypting file")
            return None

    def decrypt_attachments(self, form_secret_key: str, decrypt_params: DecryptParams):
        if "attachmentDownloadUrls" not in decrypt_params:
            raise Exception("`attachmentDownloadUrls` param not passed")

        # const attachmentRecords: EncryptedAttachmentRecords =
        # decryptParams.attachmentDownloadUrls ?? {}
        attachment_records = decrypt_params.get("attachmentDownloadUrls", {})

        decrypted_content_bytes = decrypt_content(
            form_secret_key, decrypt_params["encryptedContent"]
        )
        if not decrypted_content_bytes:
            return None
        decrypted_content = json.loads(decrypted_content_bytes.decode("utf-8"))

        decrypted_records = {}
        filenames = {}
        for response in decrypted_content:
            if response["fieldType"] == "attachment" and response["answer"]:
                filenames[response["_id"]] = response["answer"]

        field_ids = attachment_records.keys()
        if not are_attachment_field_ids_valid(field_ids, filenames):
            return None

        # possible improvement: make this parallel (eg. with grequests, request_futures)
        try:
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
        except AttachmentDecryptionException:
            raise
        except Exception as e:
            logger.error(e)
            return None

        return {"content": decrypted_content, "attachments": decrypted_records}
