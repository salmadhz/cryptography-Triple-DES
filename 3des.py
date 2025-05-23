"""
3DES (Triple DES) Implementation from Scratch in Python
- Using ECB (Electronic Code Book) operation mode
- Supporting ASCII key format
- Implementing the correct order of operations for encryption and decryption
- Supporting padding and no padding options
"""

import random
import string

# DES Constants
# Initial Permutation (IP) table
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (IP^-1) table
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# Expansion (E) table
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Permutation (P) table
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# S-boxes (Substitution boxes)
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Permuted Choice 1 (PC-1) table
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Permuted Choice 2 (PC-2) table
PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

# Number of left shifts for each round
SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Helper Functions
def text_to_binary(text):
    """Convert text string to binary string"""
    binary = ""
    for char in text:
        # Convert each character to its ASCII value, then to 8-bit binary
        binary += format(ord(char), '08b')
    return binary

def binary_to_text(binary):
    """Convert binary string to text string"""
    text = ""
    # Process 8 bits at a time
    for i in range(0, len(binary), 8):
        # Convert each 8-bit chunk to its ASCII character
        byte = binary[i:i+8]
        if len(byte) == 8:  # Ensure we have a full byte
            text += chr(int(byte, 2))
    return text

def hex_to_binary(hex_str):
    """Convert hexadecimal string to binary string"""
    binary = ""
    for char in hex_str:
        # Convert each hexadecimal character to its 4-bit binary representation
        binary += format(int(char, 16), '04b')
    return binary

def binary_to_hex(binary):
    """Convert binary string to hex string"""
    hex_str = ""
    for i in range(0, len(binary), 4):
        chunk = binary[i:i+4]
        if len(chunk) == 4:  # Ensure we have a full 4-bit chunk
            hex_str += format(int(chunk, 2), 'x')
    return hex_str

def permute(input_block, table):
    """Permute the input block according to the given table"""
    result = ""
    for pos in table:
        # Adjust index (positions in tables are 1-based, but we need 0-based)
        result += input_block[pos - 1]
    return result

def shift_left(key, shift_amount):
    """Perform a circular left shift on the key"""
    return key[shift_amount:] + key[:shift_amount]

def xor(a, b):
    """Perform XOR operation on two binary strings"""
    result = ""
    for i in range(len(a)):
        # XOR each bit: 1 if bits are different, 0 if same
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result

def apply_sbox(input_48bit):
    """Apply the S-boxes to convert 48-bit input to 32-bit output"""
    output_32bit = ""
    
    # Process 6 bits at a time for each S-box
    for i in range(8):
        # Extract the 6-bit chunk for current S-box
        chunk = input_48bit[i*6:(i+1)*6]
        
        # Calculate row and column indices for S-box lookup
        # Row is determined by the first and last bit
        row = int(chunk[0] + chunk[5], 2)
        # Column is determined by the middle 4 bits
        col = int(chunk[1:5], 2)
        
        # Get the value from the appropriate S-box
        value = S_BOXES[i][row][col]
        
        # Convert to 4-bit binary and add to output
        output_32bit += format(value, '04b')
    
    return output_32bit

def generate_subkeys(key_64bit):
    """Generate 16 subkeys for DES encryption/decryption"""
    # Apply PC-1 permutation to get 56-bit key
    key_56bit = permute(key_64bit, PC1)
    
    # Split into left and right halves (28 bits each)
    left = key_56bit[:28]
    right = key_56bit[28:]
    
    subkeys = []
    
    # Generate 16 subkeys through 16 rounds
    for i in range(16):
        # Perform left circular shift on both halves
        left = shift_left(left, SHIFT_TABLE[i])
        right = shift_left(right, SHIFT_TABLE[i])
        
        # Combine halves and apply PC-2 permutation to get 48-bit subkey
        combined = left + right
        subkey = permute(combined, PC2)
        
        subkeys.append(subkey)
    
    return subkeys

def des_function(right_half, subkey):
    """The core function (f) used in DES rounds"""
    # Expand right half from 32 to 48 bits
    expanded = permute(right_half, E)
    
    # XOR with the subkey
    xored = xor(expanded, subkey)
    
    # Apply S-boxes to reduce back to 32 bits
    sboxed = apply_sbox(xored)
    
    # Apply permutation P
    result = permute(sboxed, P)
    
    return result

def des_round(left_half, right_half, subkey):
    """Perform one round of DES"""
    # Save original right half before modification
    new_left = right_half
    
    # Apply core function and XOR with left half
    f_result = des_function(right_half, subkey)
    new_right = xor(left_half, f_result)
    
    return new_left, new_right

def des_encrypt(plaintext_64bit, key_64bit):
    """Perform DES encryption on a 64-bit plaintext block"""
    # Generate subkeys
    subkeys = generate_subkeys(key_64bit)
    
    # Initial permutation
    permuted = permute(plaintext_64bit, IP)
    
    # Split into left and right halves
    left = permuted[:32]
    right = permuted[32:]
    
    # 16 rounds of encryption
    for i in range(16):
        left, right = des_round(left, right, subkeys[i])
    
    # Swap left and right halves after the 16th round
    combined = right + left
    
    # Final permutation
    ciphertext = permute(combined, FP)
    
    return ciphertext

def des_decrypt(ciphertext_64bit, key_64bit):
    """Perform DES decryption on a 64-bit ciphertext block"""
    # Generate subkeys
    subkeys = generate_subkeys(key_64bit)
    
    # Initial permutation
    permuted = permute(ciphertext_64bit, IP)
    
    # Split into left and right halves
    left = permuted[:32]
    right = permuted[32:]
    
    # 16 rounds of decryption (using subkeys in reverse order)
    for i in range(15, -1, -1):
        left, right = des_round(left, right, subkeys[i])
    
    # Swap left and right halves after the 16th round
    combined = right + left
    
    # Final permutation
    plaintext = permute(combined, FP)
    
    return plaintext

def pad_text(text, block_size=8):
    """Add PKCS#7 padding to the text"""
    padding_length = block_size - (len(text) % block_size)
    if padding_length == 0:
        padding_length = block_size
    
    # Add padding bytes with the value equal to the padding length
    padded_text = text + chr(padding_length) * padding_length
    
    return padded_text

def unpad_text(padded_text):
    """Remove PKCS#7 padding from the text"""
    # Check if there's content to unpad
    if not padded_text:
        return padded_text
    
    try:
        # Get the padding character (last character)
        padding_length = ord(padded_text[-1])
        
        # Check if padding_length makes sense (should be between 1 and 8)
        if 1 <= padding_length <= 8:
            # Verify that all padding characters are the same
            is_valid_padding = True
            for i in range(1, padding_length + 1):
                if i <= len(padded_text) and ord(padded_text[-i]) != padding_length:
                    is_valid_padding = False
                    break
                
            if is_valid_padding:
                return padded_text[:-padding_length]
    except:
        # If any error occurs, return text as is
        pass
        
    # If padding seems invalid, return the text as is
    return padded_text

def prepare_key(key):
    """Prepare a key for DES (ensure it's 64 bits / 8 bytes)"""
    # For ASCII keys, use the first 8 characters or pad if shorter
    if len(key) < 8:
        key = key.ljust(8)  # Pad with spaces
    elif len(key) > 8:
        key = key[:8]  # Truncate to first 8 characters
    
    return text_to_binary(key)

def check_padding_needed(text):
    """Check if padding is needed for the input text"""
    # If the text length is already a multiple of 8, padding is not needed for technical reasons
    # However, for standards compliance, padding is often applied even to complete blocks
    return len(text) % 8 != 0, len(text) % 8 == 0

def pad_text(text, block_size=8):
    """Add PKCS#7 padding to the text"""
    padding_length = block_size - (len(text) % block_size)
    if padding_length == 0:
        padding_length = block_size
    
    # Add padding bytes with the value equal to the padding length
    padded_text = text + chr(padding_length) * padding_length
    
    return padded_text

def triple_des_encrypt(plaintext, key1, key2, key3, use_padding=True):
    """
    Perform Triple DES encryption (encrypt-decrypt-encrypt)
    Using ECB (Electronic Code Book) mode
    """
    # Check if padding is technically needed and if this is a complete block
    padding_needed, is_complete_block = check_padding_needed(plaintext)
    
    # Prepare keys
    key1_binary = prepare_key(key1)
    key2_binary = prepare_key(key2)
    key3_binary = prepare_key(key3)
    
    # Create two versions of the result for complete blocks when padding is requested
    result_no_padding = ""
    hex_result_no_padding = ""
    
    # Apply padding if needed and requested
    if use_padding:
        # Always pad when padding is requested, even for complete blocks
        plaintext_padded = pad_text(plaintext)
        plaintext_to_use = plaintext_padded
    elif padding_needed:
        # If no padding is requested but it's needed, just ensure length
        plaintext_to_use = plaintext.ljust((len(plaintext) + 7) // 8 * 8, '\0')
    else:
        # No padding needed or requested
        plaintext_to_use = plaintext
    
    # Process non-padded version first if it's a complete block
    if is_complete_block and use_padding:
        # Process the complete block without padding
        block = plaintext
        
        # Convert block to binary
        block_binary = text_to_binary(block)
        
        # Triple DES: encrypt with key1, decrypt with key2, encrypt with key3
        encrypted1 = des_encrypt(block_binary, key1_binary)
        decrypted = des_decrypt(encrypted1, key2_binary)
        encrypted2 = des_encrypt(decrypted, key3_binary)
        
        # Add binary result to hex output
        hex_result_no_padding = binary_to_hex(encrypted2)
        
        # Convert binary result to text
        for j in range(0, len(encrypted2), 8):
            byte = encrypted2[j:j+8]
            result_no_padding += chr(int(byte, 2))
    
    # Process the main version (with or without padding)
    ciphertext = ""
    hex_result = ""
    
    # Process each 8-byte (64-bit) block
    for i in range(0, len(plaintext_to_use), 8):
        block = plaintext_to_use[i:i+8]
        
        # Ensure block is 8 bytes (for the last block if no padding is used)
        if len(block) < 8:
            block = block.ljust(8, '\0')
        
        # Convert block to binary
        block_binary = text_to_binary(block)
        
        # Triple DES: encrypt with key1, decrypt with key2, encrypt with key3
        encrypted1 = des_encrypt(block_binary, key1_binary)
        decrypted = des_decrypt(encrypted1, key2_binary)
        encrypted2 = des_encrypt(decrypted, key3_binary)
        
        # Add binary result to hex output
        hex_result += binary_to_hex(encrypted2)
        
        # Convert binary result to text
        for j in range(0, len(encrypted2), 8):
            byte = encrypted2[j:j+8]
            ciphertext += chr(int(byte, 2))
    
    return ciphertext, hex_result, padding_needed, is_complete_block, hex_result_no_padding

def hex_to_bytes(hex_str):
    """Convert hex string to bytes (as string of characters)"""
    result = ""
    for i in range(0, len(hex_str), 2):
        if i+1 < len(hex_str):  # Make sure we have 2 hex digits
            byte_val = int(hex_str[i:i+2], 16)
            result += chr(byte_val)
    return result

def hex_to_binary_string(hex_str):
    """Convert hex string directly to binary string"""
    binary = ""
    for char in hex_str:
        # Convert each hex character to 4-bit binary
        binary += format(int(char, 16), '04b')
    return binary

def triple_des_decrypt(ciphertext, key1, key2, key3, use_padding=True, is_hex=False):
    """
    Perform Triple DES decryption (decrypt-encrypt-decrypt)
    Using ECB (Electronic Code Book) mode
    """
    # Prepare keys
    key1_binary = prepare_key(key1)
    key2_binary = prepare_key(key2)
    key3_binary = prepare_key(key3)
    
    plaintext = ""
    
    if is_hex:
        # Clean the hex input - remove any non-hex characters
        clean_hex = ''.join(c for c in ciphertext if c in "0123456789ABCDEFabcdef")
        
        # Make sure we have an even number of hex digits
        if len(clean_hex) % 2 != 0:
            clean_hex = clean_hex + "0"
        
        # Convert hex to binary data
        binary_data = ""
        for i in range(0, len(clean_hex), 2):
            byte_val = int(clean_hex[i:i+2], 16)
            binary_data += format(byte_val, '08b')
        
        # Process each 64-bit block
        for i in range(0, len(binary_data), 64):
            if i + 64 <= len(binary_data):
                block_binary = binary_data[i:i+64]
                
                # Triple DES: decrypt with key3, encrypt with key2, decrypt with key1
                decrypted1 = des_decrypt(block_binary, key3_binary)
                encrypted = des_encrypt(decrypted1, key2_binary)
                decrypted2 = des_decrypt(encrypted, key1_binary)
                
                # Convert binary result to text
                for j in range(0, len(decrypted2), 8):
                    if j + 8 <= len(decrypted2):
                        byte = decrypted2[j:j+8]
                        byte_val = int(byte, 2)
                        # Only add printable or common control characters
                        if byte_val >= 32 or byte_val in [9, 10, 13]:  # Tab, LF, CR
                            plaintext += chr(byte_val)
                        else:
                            # Skip non-printable characters that might be padding
                            pass
    else:
        # Process each 8-byte (64-bit) block
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            
            # Ensure block is 8 bytes
            if len(block) < 8:
                break  # Should not happen with proper encryption and padding
            
            # Convert block to binary
            block_binary = text_to_binary(block)
            
            # Triple DES: decrypt with key3, encrypt with key2, decrypt with key1
            decrypted1 = des_decrypt(block_binary, key3_binary)
            encrypted = des_encrypt(decrypted1, key2_binary)
            decrypted2 = des_decrypt(encrypted, key1_binary)
            
            # Convert binary result to text and add to plaintext
            for j in range(0, len(decrypted2), 8):
                if j + 8 <= len(decrypted2):
                    byte = decrypted2[j:j+8]
                    plaintext += chr(int(byte, 2))
    
    # Remove padding if used
    if use_padding:
        try:
            plaintext = unpad_text(plaintext)
        except:
            # If there's an issue with unpadding, return as is
            pass
    
    return plaintext

def generate_random_key():
    """Generate a random ASCII key"""
    # Generate 8 random printable ASCII characters
    return ''.join(random.choice(string.printable[:95]) for _ in range(8))

def main():
    """Main function to handle user interaction"""
    print("=" * 50)
    print("3DES (Triple DES) Encryption/Decryption Tool")
    print("=" * 50)
    
    # Ask user for operation mode - accept first letter only
    while True:
        operation = input("\nChoose operation (E)ncrypt/(D)ecrypt: ").lower()
        if operation and operation[0] in ['e', 'd']:
            operation = 'encrypt' if operation[0] == 'e' else 'decrypt'
            break
        print("Invalid choice. Please enter 'e' for encrypt or 'd' for decrypt.")
    
    # Ask whether to use random keys - accept first letter only
    while True:
        random_keys = input("Use random keys? (Y)es/(N)o: ").lower()
        if random_keys and random_keys[0] in ['y', 'n']:
            random_keys = random_keys[0] == 'y'
            break
        print("Invalid choice. Please enter 'y' for yes or 'n' for no.")
    
    # Handle keys
    if random_keys:
        # Ask for 3DES key variant
        print("\nChoose 3DES key variant:")
        print("1. Three-Key 3DES (K1 ≠ K2 ≠ K3) - Highest security")
        print("2. Two-Key 3DES (K1 = K3 ≠ K2) - Good balance")
        print("3. Single-Key 3DES (K1 = K2 = K3) - Basic security")
        
        variant = 0
        while variant not in [1, 2, 3]:
            try:
                variant = int(input("Enter your choice (1/2/3): "))
                if variant not in [1, 2, 3]:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Generate keys based on variant
        key1 = generate_random_key()
        
        if variant == 1:  # Three-Key 3DES
            key2 = generate_random_key()
            key3 = generate_random_key()
        elif variant == 2:  # Two-Key 3DES
            key2 = generate_random_key()
            key3 = key1  # K1 = K3
        else:  # Single-Key 3DES
            key2 = key1
            key3 = key1
        
        # Display the generated keys
        print("\nGenerated keys:")
        print(f"Key 1: {key1}")
        print(f"Key 2: {key2}")
        print(f"Key 3: {key3}")
        
        if variant == 1:
            print("Using Three-Key 3DES (K1 ≠ K2 ≠ K3)")
        elif variant == 2:
            print("Using Two-Key 3DES (K1 = K3 ≠ K2)")
        else:
            print("Using Single-Key 3DES (K1 = K2 = K3)")
    
    else:
        # Manual key entry with variant selection
        print("\nChoose 3DES key variant:")
        print("1. Three-Key 3DES (K1 ≠ K2 ≠ K3) - Highest security")
        print("2. Two-Key 3DES (K1 = K3 ≠ K2) - Good balance")
        print("3. Single-Key 3DES (K1 = K2 = K3) - Basic security")
        
        variant = 0
        while variant not in [1, 2, 3]:
            try:
                variant = int(input("Enter your choice (1/2/3): "))
                if variant not in [1, 2, 3]:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get keys based on the selected variant
        print("\nEnter ASCII keys (8 characters each):")
        key1 = input("Key 1: ")
        
        if variant == 1:  # Three-Key 3DES
            key2 = input("Key 2: ")
            key3 = input("Key 3: ")
        elif variant == 2:  # Two-Key 3DES
            key2 = input("Key 2: ")
            key3 = key1  # K1 = K3
            print("Key 3: [Same as Key 1]")
        else:  # Single-Key 3DES
            key2 = key1
            key3 = key1
            print("Key 2: [Same as Key 1]")
            print("Key 3: [Same as Key 1]")
    
    # Ask whether to use padding - accept first letter only
    while True:
        padding_choice = input("\nUse padding? (Y)es/(N)o: ").lower()
        if padding_choice and padding_choice[0] in ['y', 'n']:
            use_padding = padding_choice[0] == 'y'
            break
        print("Invalid choice. Please enter 'y' for yes or 'n' for no.")
    
    # Get input text
    if operation == 'encrypt':
        input_text = input("\nEnter text to encrypt: ")
        
        try:
            # Check if the text needs padding
            padding_needed, is_complete_block = check_padding_needed(input_text)
            
            # Perform encryption
            _, hex_result, padding_needed, is_complete_block, hex_result_no_padding = triple_des_encrypt(
                input_text, key1, key2, key3, use_padding
            )
            
            # Inform user about padding status
            if not use_padding and not padding_needed:
                print("\nNOTE: Padding was not applied because the input text length is already a multiple of 8 bytes.")
            
            # Display result in hex format
            print("\nEncrypted text (hex):", hex_result.upper())
            
            # If this is a complete block, show both versions
            if is_complete_block and use_padding and hex_result_no_padding:
                print("\nEXPLANATION OF DIFFERENT RESULTS:")
                print(f"1. Without PKCS#7 padding (single block): {hex_result_no_padding.upper()}")
                print(f"2. With PKCS#7 padding (two blocks): {hex_result.upper()}")
                print("\nThe difference is because when PKCS#7 padding is applied to a complete block,")
                print("a full block of padding (8 bytes, each with value 0x08) is added.")
                print("Some implementations/tools always apply padding (option 2), while others")
                print("don't add padding when the input is already a complete block (option 1).")
        except Exception as e:
            print(f"Error encrypting: {str(e)}")
        
    else:  # decrypt
        # Get input in hex format
        hex_input = input("\nEnter encrypted text (in hex): ")
        try:
            # Perform decryption with hex input
            result = triple_des_decrypt(hex_input, key1, key2, key3, use_padding, is_hex=True)
            
            # Display result
            print("\nDecrypted text:", result)
        except Exception as e:
            print(f"Error decrypting: {str(e)}")


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
