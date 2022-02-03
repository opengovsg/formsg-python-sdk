Getting Started
===============

Installation
------------
`pip install formsg-python-sdk`

Usage
-----
.. code-block:: python
import formsg
sdk = formsg.formSdk("PRODUCTION")
FORM_SECRET_KEY = "<your-secret-key>"

# decryption
decrypted = sdk.decrypt(FORM_SECRET_KEY, encrypted_payload)

# webhook authentication
header = "req.header.'x-formsg-signature'"
sdk.authenticate(FORM_SECRET_KEY, header=HEADER_RESP, uri='your-webhook-uri')

# decryption with attachments
decrypted = sdk.decrypt_attachments(FORM_SECRET_KEY, encrypted_payload)
