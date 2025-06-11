from flask import Flask, request, jsonify
from cipher.rsa import RSACipher

app = Flask(__name__)

# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    """
    Handles key generation for RSA.
    """
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/rsa/encrypt', methods=["POST"])
def rsa_encrypt():
    """
    Handles RSA encryption of a message.
    Expects a JSON payload with 'message' and 'key_type' ('public' or 'private').
    """
    data = request.json
    message = data['message']
    key_type = data['key_type']

    # Load keys (assuming rsa_cipher.load_keys() returns (private_key, public_key))
    private_key, public_key = rsa_cipher.load_keys()

    key = None
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})

    # Encrypt the message using the determined key
    encrypted_message = rsa_cipher.encrypt(message, key)
    # Convert the encrypted message to hexadecimal for display/transfer
    encrypted_hex = encrypted_message.hex()
    return jsonify({'encrypted_message': encrypted_hex})

@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    """
    Handles RSA decryption of a ciphertext.
    Expects a JSON payload with 'ciphertext' (hexadecimal) and 'key_type' ('public' or 'private').
    """
    data = request.json
    ciphertext_hex = data['ciphertext']
    key_type = data['key_type']

    # Convert hexadecimal ciphertext back to bytes
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        return jsonify({'error': 'Invalid hexadecimal ciphertext'}), 400

    # Load keys (assuming rsa_cipher.load_keys() returns (private_key, public_key))
    private_key, public_key = rsa_cipher.load_keys()

    key = None
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})

    try:
        # Decrypt the ciphertext using the determined key
        decrypted_message = rsa_cipher.decrypt(ciphertext, key)
        # Return the decrypted message
        return jsonify({'decrypted_message': decrypted_message.decode('utf-8')}) # Assuming UTF-8 encoding
    except Exception as e:
        # Handle decryption errors
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    """
    Handles RSA signing of a message.
    Expects a JSON payload with 'message'.
    """
    data = request.json
    message = data['message']

    # Load private key for signing (assuming rsa_cipher.load_keys() returns (private_key, public_key))
    private_key, _ = rsa_cipher.load_keys() # We only need the private key for signing

    # Sign the message
    signature = rsa_cipher.sign(message, private_key)
    # Convert the signature to hexadecimal for display/transfer
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    """
    Handles RSA signature verification.
    Expects a JSON payload with 'message' and 'signature' (hexadecimal).
    """
    data = request.json
    message = data['message']
    signature_hex = data['signature']

    # Load public key for verification (assuming rsa_cipher.load_keys() returns (private_key, public_key))
    public_key, _ = rsa_cipher.load_keys() # We only need the public key for verification

    # Convert hexadecimal signature back to bytes
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return jsonify({'error': 'Invalid hexadecimal signature'}), 400

    # Verify the signature
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# Main function to run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

