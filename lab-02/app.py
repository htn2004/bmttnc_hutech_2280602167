# app.py

from flask import Flask, render_template, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher # Import the new TranspositionCipher class

app = Flask(__name__)

# Route for home page
@app.route("/")
def home():
    return render_template('index.html')

# --- Caesar Cipher Routes ---
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/caesar_encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt_text(text, key)
    return f"Văn bản gốc: {text}<br/>Khóa: {key}<br/>Văn bản đã mã hóa: {encrypted_text}"

@app.route("/caesar_decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt_text(text, key)
    return f"Văn bản đã mã hóa: {text}<br/>Khóa: {key}<br/>Văn bản đã giải mã: {decrypted_text}"

# --- Vigenere Cipher Routes ---
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere = VigenereCipher()
    encrypted_text = vigenere.vigenere_encrypt(text, key)
    return f"Văn bản gốc: {text}<br/>Khóa: {key}<br/>Văn bản đã mã hóa: {encrypted_text}"

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere = VigenereCipher()
    decrypted_text = vigenere.vigenere_decrypt(text, key)
    return f"Văn bản đã mã hóa: {text}<br/>Khóa: {key}<br/>Văn bản đã giải mã: {decrypted_text}"

# --- Rail Fence Cipher Routes ---
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    num_rails = int(request.form['inputKeyPlain'])
    railfence = RailFenceCipher()
    encrypted_text = railfence.rail_fence_encrypt(text, num_rails)
    return f"Văn bản gốc: {text}<br/>Số đường ray: {num_rails}<br/>Văn bản đã mã hóa: {encrypted_text}"

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    num_rails = int(request.form['inputKeyCipher'])
    railfence = RailFenceCipher()
    decrypted_text = railfence.rail_fence_decrypt(text, num_rails)
    return f"Văn bản đã mã hóa: {text}<br/>Số đường ray: {num_rails}<br/>Văn bản đã giải mã: {decrypted_text}"

# --- Playfair Cipher Routes ---
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    plain_text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    
    playfair = PlayFairCipher()
    playfair_matrix = playfair.create_playfair_matrix(key)
    encrypted_text = playfair.playfair_encrypt(plain_text, playfair_matrix)
    
    return f"Văn bản gốc: {plain_text}<br/>Khóa: {key}<br/>Văn bản đã mã hóa: {encrypted_text}"

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    cipher_text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    
    playfair = PlayFairCipher()
    playfair_matrix = playfair.create_playfair_matrix(key)
    decrypted_text = playfair.playfair_decrypt(cipher_text, playfair_matrix)
    
    return f"Văn bản đã mã hóa: {cipher_text}<br/>Khóa: {key}<br/>Văn bản đã giải mã: {decrypted_text}"

@app.route("/playfair_create_matrix", methods=['POST'])
def playfair_create_matrix():
    key = request.form['key']
    playfair = PlayFairCipher()
    matrix = playfair.create_playfair_matrix(key)
    return jsonify(matrix) # Return matrix as JSON

# --- Transposition Cipher Routes ---
@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/transposition_encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    transposition = TranspositionCipher()
    encrypted_text = transposition.encrypt(text, key)
    return f"Văn bản gốc: {text}<br/>Khóa: {key}<br/>Văn bản đã mã hóa: {encrypted_text}"

@app.route("/transposition_decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    transposition = TranspositionCipher()
    decrypted_text = transposition.decrypt(text, key)
    return f"Văn bản đã mã hóa: {text}<br/>Khóa: {key}<br/>Văn bản đã giải mã: {decrypted_text}"


# Main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
