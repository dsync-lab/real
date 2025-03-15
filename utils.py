import base64

def encode_id(raw_id):
    return base64.urlsafe_b64encode(str(raw_id).encode()).decode()

def decode_id(encoded_id):
    return int(base64.urlsafe_b64decode(encoded_id.encode()).decode())
