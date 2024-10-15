def generate_matrix(key):
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))  # Remove duplicates, keep order
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    used = set()

    for char in key:
        if char not in used and char != 'J':  # 'J' is usually omitted in Playfair
            matrix.append(char)
            used.add(char)

    for char in alphabet:
        if char not in used:
            matrix.append(char)
            used.add(char)

    return [matrix[i:i + 5] for i in range(0, len(matrix), 5)]

def prepare_text(text):
    text = text.upper().replace("J", "I")  # Replace 'J' with 'I' in Playfair
    text = ''.join([char for char in text if char.isalpha()])  # Remove non-letters

    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'X'
        
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2

    return pairs

def playfair_encrypt(pairs, matrix):
    def get_position(char):
        for row in range(5):
            if char in matrix[row]:
                return row, matrix[row].index(char)
        return None

    encrypted = []
    for pair in pairs:
        row1, col1 = get_position(pair[0])
        row2, col2 = get_position(pair[1])

        if row1 == row2:
            encrypted.append(matrix[row1][(col1 + 1) % 5])
            encrypted.append(matrix[row2][(col2 + 1) % 5])
        elif col1 == col2:
            encrypted.append(matrix[(row1 + 1) % 5][col1])
            encrypted.append(matrix[(row2 + 1) % 5][col2])
        else:
            encrypted.append(matrix[row1][col2])
            encrypted.append(matrix[row2][col1])

    return ''.join(encrypted)

def playfair_decrypt(pairs, matrix):
    def get_position(char):
        for row in range(5):
            if char in matrix[row]:
                return row, matrix[row].index(char)
        return None

    decrypted = []
    for pair in pairs:
        row1, col1 = get_position(pair[0])
        row2, col2 = get_position(pair[1])

        if row1 == row2:
            decrypted.append(matrix[row1][(col1 - 1) % 5])
            decrypted.append(matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:
            decrypted.append(matrix[(row1 - 1) % 5][col1])
            decrypted.append(matrix[(row2 - 1) % 5][col2])
        else:
            decrypted.append(matrix[row1][col2])
            decrypted.append(matrix[row2][col1])

    return ''.join(decrypted)

# Key for the Playfair Cipher
key = "TEKNIKINFORMATIKA".replace("J", "I").upper()
matrix = generate_matrix(key)

# The 3 texts
texts = [
    "GOOD BROOM SWEEP CLEAN", 
    "REDWOOD NATIONAL STATE PARK", 
    "JUNK FOOD AND HEALTH PROBLEMS"
]

# Store results
final_results = []

for text in texts:
    pairs = prepare_text(text)
    encrypted = playfair_encrypt(pairs, matrix)
    decrypted = playfair_decrypt(prepare_text(encrypted), matrix)
    final_results.append((text, encrypted, decrypted))

# Print results
for original, encrypted, decrypted in final_results:
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print("-" * 50)
