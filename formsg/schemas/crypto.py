from marshmallow import Schema, fields
from typing_extensions import TypedDict

from formsg.util.crypto import FieldType, FormField

EncryptedFile = TypedDict("EncryptedFile", {})
EncryptedContent = TypedDict("EncryptedContent", {})


class DecryptParamsSchema(Schema):
    encryptedContent = fields.Str(required=True)
    version = fields.Number(required=True)
    verifiedContent = fields.Str()
    attachmentDownloadUrls = fields.Dict()
