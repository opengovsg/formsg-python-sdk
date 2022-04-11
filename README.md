# formsg-python-sdk
This is the Python version of the [Form Javascript SDK](https://github.com/opengovsg/formsg-javascript-sdk/), which provides utility functions for verifying FormSG webhooks, as well as decrypting form submissions.

Note that this library is still in beta. 

## Requirements
Python 3.6+
## Quickstart
`pip install formsg-python-sdk`
```python
import formsg
# accepts STAGING or PRODUCTION, determines whether to use staging or production public signing keys
sdk = formsg.FormSdk("PRODUCTION")

# Your form's secret key downloaded from FormSG upon form creation
FORM_SECRET_KEY = "YOUR-SECRET-KEY"

# This is where your domain is hosted, and should match
# the URI supplied to FormSG in the form dashboard
YOUR_WEBHOOK_URI = "your-webhoook-uri"

# decryption without attachments
# if `verifiedContent` exists as a key in `encrypted_payload`, the return object will include a verified key
decrypted = sdk.crypto.decrypt(FORM_SECRET_KEY, encrypted_payload)

# webhook authentication
HEADER_RESP = "req.header.'x-formsg-signature'"
sdk.webhooks.authenticate(header=HEADER_RESP, uri=YOUR_WEBHOOK_URI)

# decryption with attachments
decrypted_with_attachments = sdk.crypto.decrypt_attachments(FORM_SECRET_KEY, encrypted_payload)
```

Refer to the [example app](https://github.com/opengovsg/formsg-python-sdk/blob/develop/example_app/flask.py) if you're running a flask server.

## End-to-end Encryption
### Format of Submission Response

| Key                    | Type                   | Description                                                                                              |
| ---------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------- |
| formId                 | str                 | Unique form identifier.                                                                                  |
| submissionId           | str                 | Unique response identifier, displayed as 'Response ID' to form respondents                               |
| encryptedContent       | str                 | The encrypted submission in base64.                                                                      |
| created                | str                 | Creation timestamp.                                                                                      |
| attachmentDownloadUrls | Mapping[str, str] | (Optional) Records containing field IDs and URLs where encrypted uploaded attachments can be downloaded. |

### Format of Decrypted Submissions

`crypto.decrypt(form_secret_key: str, decrypt_params: DecryptParams)`
takes in `decrypt_params` as the second argument, and returns an an object with
the shape

<pre>
{
  responses: FormField[]
  verified?: NotRequired[Mapping[str, Any]]
}
</pre>

The `decryptParams.encryptedContent` field decrypts into a list of `FormField` objects, which will be assigned to the `responses` key of the returned object.

Furthermore, if `decryptParams.verifiedContent` exists, the function will
decrypt and open the signed decrypted content with the package's own
`signingPublicKey` in
[`constants.py`](https://github.com/opengovsg/formsg-python-sdk/blob/develop/formsg/constants.py).
The resulting decrypted verifiedContent will be assigned to the `verified` key
of the returned object.

> **NOTE** <br>
> If any errors occur, either from the failure to decrypt either `encryptedContent` or `verifiedContent`, or the failure to authenticate the decrypted signed message in `verifiedContent`, `None` will be returned.

Note that due to end-to-end encryption, FormSG servers are unable to verify the data format.

However, the `decrypt` function exposed by this library [validates](https://github.com/opengovsg/formsg-python-sdk/blob/develop/formsg/util/validate.py) the decrypted content and will **return `None` if the
decrypted content does not fit the schema displayed below.**

| Key         | Type     | Description                                                                                              |
| ----------- | -------- | -------------------------------------------------------------------------------------------------------- |
| question    | str   | The question listed on the form                                                                          |
| answer      | str   | The submitter's answer to the question on form. Either this key or `answerArray` must exist.             |
| answerArray | List[str] | The submitter's answer to the question on form. Either this key or `answer` must exist.                  |
| fieldType   | str   | The type of field for the question.                                                                      |
| \_id        | str   | A unique identifier of the form field. WARNING: Changes when new fields are created/removed in the form. |

The full schema can be viewed in
[`validate.ts`](https://github.com/opengovsg/formsg-javascript-sdk/tree/master/src/util/validate.ts).

If the decrypted content is the correct shape, then:

1. the decrypted content (from `decryptParams.encryptedContent`) will be set as the value of the `responses` key.
2. if `decryptParams.verifiedContent` exists, then an attempt to
   decrypted the verified content will be called, and the result set as the
   value of `verified` key. There is no shape validation for the decrypted
   verified content. **If the verification fails, `None` is returned, even if
   `decryptParams.encryptedContent` was successfully decrypted.**