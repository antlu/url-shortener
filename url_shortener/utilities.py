import hashlib
from http import HTTPStatus


def hash_string(string, length=6):
    bytestring = string.encode()
    return hashlib.sha1(bytestring).hexdigest()[:length]

def error_response(message, code=HTTPStatus.BAD_REQUEST):
    return ({'error': message}, code)
