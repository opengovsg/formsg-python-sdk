# from typing_extensions import Literal
# import pytest
from formsg.crypto import Crypto
import json
import os
import pathlib

PUBLIC_KEY = "KUY1XT30ar+XreVjsS1w/c3EpDs2oASbF6G3evvaUJM="
SECRET_KEY = "/u+LP57Ib9y5Ytpud56FzuitSC9O6lJ4EOLOFHpsHlYpRjVdPfRqv5et5WOxLXD9zcSkOzagBJsXobd6+9pQkw=="


def load_resource(path: str):
    f = open(path).read()
    return json.loads(f)


cwd = pathlib.Path(__file__).parent.resolve()
plain_text = load_resource(os.path.join(cwd, "resources/plaintext.json"))


def test_failed_decryption():
    crypto = Crypto(PUBLIC_KEY)
    assert crypto.decrypt(SECRET_KEY, "") == None


cipertext = "RqOjwNXwiVJqvdTrQeD/NiktpI8vzo6CXlBBNihmmwI=;+0cGJwOA42F7DmQO7Kr6tNn9YH/7poDe:2jpehB9uW+63G1EimxOs1tsfR54xxSVZQbFMQaCa8ovVoF/6isBCEl5WLmrE1CRa2c5L2G5rAgCUnhsxQ7jVa//XEKr/m9kGNMbPnVqH62RslAxh30Mzz2he/ssbMazLDBzgQwd8I+pHnrBHQW5BsLqclj7QAMX3fa10Zon0ih4irWQ1o9eYitFllitD+vIcwbBzJyigGvD/t14+2/5imZmJdmJTJXd1ySxDo1X6KjBmph4rzvWtZSUgF7rRfMtAmbyOj87i6CkkNNIN4Dtl3zEuSeLuU2IDF7IHDdAwpmgWM9ejFpwrMFfr8PRovCubuRxCDQ1hV6GOyh60SlKA3oHQMhRQ2yia2vr9yxzHgO+wVUfgoiXQn8tvXFwZmzZd/eWENC1QI+XvP1jt50RIhQ0kMbyhBiaAG9nYlhGO3UHtmGGBoOdW4l4DZaWKRItnw1qgb2oxCvxOIkWNoafq1qJbYJsldOy6a/I2lbwAPL7MzVfgHJDj11dLOBgHGZHia6ZaROXYEiFpkVP8APOO/tgV902nOOlt+w63QNIieCIoGphn9LvOTo6Y6HD8qH6sekEyXCds6jP4RVw5XIN9LGeOWlEKx/VR2rf8b9qzFcYRPzfH5M8I9rpuZkk72ANiTeLRM8C8zWFnitzDlh1B2M+jnjrg+jEYm0ugro7tvHYSmU4tKcGR3mPlDrROjtFf3eBO8+pZKzuQfdA/7kN5YekAzyNjLcixioycrDmjR+BbBKxVrwNlm0hmHLLdU1g42GYpmfUUythDnqwALAOtaZcuj1ObX50h6kmhIl4fAEcXdLKKpoASzafbHnIH0iNX1CefnflLxymDPjjTFqcGSpY1vZf2pxDxUNZPXsd3vbV4KbrYq9v/R5NJ+mW3lxm839aN0pNsMbMetyZTyX8tXofWERxKEZDDXRCoYS0Ijml5h0X58juM13hNtc48iuPyx8oBIy4WophJ+M4CJfsq1wfBK0q+a8P2Tj8odJRQbbFdCoQRRRKbFhk0nT/R3V23cRjMB/Z1DCFmo8ywhUfSlMhrs8f6f3myhmJpzP5MXPJgzRIAytYtUF34j+9fspaYtyQHg4j4f8OBIYrNOCgt6++1bmy0+aI3Y0DoBJ1eLfe9iHUt64cvPbPqmAxX8Jkb1kY+OVwjx7DTxFc5dCzkL/3VA1FAZe7IqfP0v/3fTT6oK7nuy951GUSU9sBynV8Z6zJecYUWbgFZ1u/K8ag6btR2IeRFz7dG+Ffkb8nsGTcNm0l54Q/XbudtfIPN2GTGp1PlgFZ5JERszVrQ8MIrMnHtPvnbtIlqdVzZ0KwR1YQnqtjCoNnI/TzniRZnydE/qJCc5ZwAQDJhl0XRmVes5sp4obxhreSdgGjoyybeFN70rb6uMvsuBlTS5Z6xg7q4eW0e8Xx0PlKYJi8eUsFtzQlN3iJzgFTeLGOlguK2GWnI/Myy5/nan2Np5+eZ2GZhdn6s/NYmiJGLlcbmcXRLOj53O1Z9Oornc+Hq5rz+eZKg4uYNbyFCbvJ9d/wNbRaQva9kETeEfGVosZXotnA2dxYRF4A24Qwjo+yNeRlbyQBf0V0BWY+rfJ+F2JMP4LZ5FNVhd5JI16z7PEgqvlGqm7zkfPmwlTjCzDFXYz749fz9hrzqOCALguEhmMYEsun8mK7IptW77qbKyx2jTu/2OC6pqdWhHB3PliKZXD5EgedpqzHcWQg/s9TloSXy9pE9PEs0j+el+j4yXyQcfrAjODWHSrUXNWSJc1rOM1ochIYJWYHn4pf2Jxuop90+c4DFYp5eih3k8BGy4Etp6L0N7PJ+ugSqZV8L0QYT2sLBwG2cS8FNUGJPoUkUn6R2Bg7bTQ=="


def test_decryption():
    crypto = Crypto("KUY1XT30ar+XreVjsS1w/c3EpDs2oASbF6G3evvaUJM=")
    result = crypto.decrypt(
        form_secret_key="H7B0nKJ+E7+naSkQApxGayz1y/lZe4thta4iPp1B+Ns=",
        decrypt_params={"encryptedContent": cipertext, "version": 1},
    )
    # assert str(result['responses']).replace(" ","") == plain_text
    assert json.dumps(result["responses"], sort_keys=True) == json.dumps(
        plain_text, sort_keys=True
    )
