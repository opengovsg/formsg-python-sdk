# formsg-python-sdk

## Quickstart
`pip install formsg-python-sdk`

you may also additionally need to run `pip install typing_extensions`

```
FORM_SECRET_KEY = "YOUR-SECRET-KEY"


import formsg
sdk = formsg.FormSdk("PRODUCTION")  # accepts STAGING or PRODUCTION

# decryption
decrypted = sdk.decrypt(FORM_SECRET_KEY, encrypted_payload)

# webhook authentication
header = "req.header.'x-formsg-signature'"
sdk.authenticate(header=HEADER_RESP, uri='your-webhook-uri')

# decryption with attachments
decrypted = sdk.decrypt_attachments(FORM_SECRET_KEY, encrypted_payload)
```