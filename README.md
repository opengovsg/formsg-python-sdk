# formsg-python-sdk
## Requirements
Python 3.6+
## Quickstart
`pip install formsg-python-sdk`

you may also additionally need to run `pip install typing_extensions`

```
FORM_SECRET_KEY = "YOUR-SECRET-KEY"


import formsg
sdk = formsg.FormSdk("PRODUCTION")  # accepts STAGING or PRODUCTION

# decryption
# if `verifiedContent` exists as a key in `encrypted_payload`, the return object will include a verified key
decrypted = sdk.crypto.decrypt(FORM_SECRET_KEY, encrypted_payload)

# webhook authentication
HEADER_RESP = "req.header.'x-formsg-signature'"
sdk.webhooks.authenticate(header=HEADER_RESP, uri='your-webhook-uri')

# decryption with attachments
decrypted = sdk.crypto.decrypt_attachments(FORM_SECRET_KEY, encrypted_payload)
```

