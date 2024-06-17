from django.core.signing import Signer, BadSignature
import base64

signer = Signer()


def encrypt_user_name(user_name):
    signed_user_name = signer.sign(user_name)
    encoded_user_name = base64.urlsafe_b64encode(
        signed_user_name.encode()).decode()
    return encoded_user_name


def decrypt_user_name(encoded_user_name):
    try:
        signed_user_name = base64.urlsafe_b64decode(
            encoded_user_name.encode()).decode()
        user_name = signer.unsign(signed_user_name)
        return user_name
    except (BadSignature, ValueError) as e:
        return None
