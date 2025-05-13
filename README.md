# 3DES (Triple DES) Encryption in Python

A clean and simple implementation of **Triple DES (3DES)** encryption algorithm in **ECB (Electronic Codebook)** mode using Python.

## 🚀 Features

- Full 3DES encryption and decryption logic implemented from scratch
- Supports both encryption and decryption
- ECB mode (Electronic Codebook) support
- Toggle between padded or non-padded plaintext
- Accepts ASCII or Hex formatted keys
- Good for educational use, cryptographic learning, or integration in small projects

## 📂 Components

- DES Core Logic: Built from fundamental primitives—Initial/Final Permutations, S-boxes, Expansion, and Feistel structure
- Key Management: Handles 3 keys (K1, K2, K3) for Triple DES, each with their own round key generation
- Flexible Input: Choose between plaintext in ASCII or hexadecimal format
- Padding Options: Optional PKCS-style padding for block alignment

## 📦 How It Works

- Encrypt → Decrypt → Encrypt using three keys: K1, K2, and K3
- Uses 64-bit blocks and a total of 48 DES rounds (16 per stage)
- The final encrypted/decrypted output is produced after reversing the process and applying the Final Permutation.

## 📌 Requirements

- Python 3.x
- No external libraries required (pure Python implementation)

## 🛠 Example Use Cases
- Educational demonstrations of DES and Triple DES
- Practice cryptographic algorithms from scratch
- Security simulations in academic projects

## ⚠️ Disclaimer
- This implementation is for educational purposes only. Do not use this for securing sensitive or production-level data.

## 📦 Usage

To use or test the algorithm:
```python
# Example usage
key1 = "133457799BBCDFF1"
key2 = "1122334455667788"
key3 = "AABB09182736CCDD"
plaintext = "HELLO123"
Encrypted text (hex): 63af7a505ad5fd56ede051fae138a116

ciphertext = triple_des_encrypt(plaintext, key1, key2, key3)
decrypted = triple_des_decrypt(ciphertext, key1, key2, key3)
```





