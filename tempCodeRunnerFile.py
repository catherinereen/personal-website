
from nltk.corpus import brown
from collections import Counter

import nltk
nltk.download('brown')

# Get all words, lowercase them
words = [w.lower() for w in brown.words() if w.isalpha()]

freq = Counter(words)

# Most common words
common_words = [w for w, _ in freq.most_common(50)]

print(common_words)

def encode(text):
    '''
    Returns an array of integers
    Normal characters come in between 0 and 26
    Note: this overrides some ASCII control characters
    '''
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            out.append(ord(ch) - ord('A'))
        elif 'a' <= ch <= 'z':
            out.append(ord(ch) - ord('a'))
        else:
            out.append(ord(ch))
    return out

def decode(nums):
    '''
    Returns a string from an array of numbers (encoded characters)
    '''
    out = []
    for num in nums:
        if num < 26:
            out.append(ord(num) + ord('A'))
        else:
            out.append(num)
    return str(bytes(out), 'utf8')


c1 = "2e4f9531b05d20bebabd36b37662ded71d82b98c10f513c29f2cac81457df099fbdb4afaa79a5f74289cb7eaa99519232573ed459fb2ea965bdac787bb39ca0553df9d1e0f8ad27fbd9358442b6d927fcbd6a0cce4782e03ca2da6c2ef9488328050acf11d8d2b87f4353d3c31a69acd5a4e18d5d19bfa2d29d074f993b5c7f0bd73584e7349432a3431bd1798143372652568bc2ff384bbcd76fc74fddb668463b202baaf0f379c76a2d974f02dfaec7b0f54ba996c55ea1e8aa04ee4875f9d75725d33ddd622a1116cda21d053a35c1dd419ba2e4b22871a6df4569e1218b7f95bb3dc0934a17d3dd99535c922dab4958740d2ad0721ba1b9c1a49409367d0"
c2 = "2d40932aa15125b5a4bd12bd246892d24ec9b68d47de5dc99232acc90a78bf8de3c659f7ee9d5e2d7b8dffeeb594192f2527e25edae5e2815bf98b80aa3f821a5ec9c45226c3dc6ef29c1a632b3488759890e4f7bf3b0c1ed76ab9caec80937b9347e0fd49962cc6f3783e353ee783c75a5d15c4d182fc3767d57cfdd2b58ee7ac71491c74064835341fb71dd1053f37262d7eb677ff92f08c49fd7fba9967943dfb03bbaf18308c2482d93bbf25f2a5491306b7933575ea1584e26ff294438077726839cac966e529638f75b979ee0e0c9c0bf22a4c768e1b65b55082471fbaf415ac940567c67b26cc8828d72ed6acd0ea0fefad4b2cbb089079525c9a61c9"
c3 = "234d852ae25720b7b5e962957667c0de5c84a3c32ebb44cb902fffd5453b9d99e3d64efca2904878698fbee6b5de19032273f04fdaa8ee8b5bcf88c5b339ca3f1bc39c1d04ce9078e4d24e402b6d8f6284deecd2ab2c0257d568b0cfe89d9c32954de9a5018764c3f5312a3571a68fcc1e091bce83d2ef7e7ede7ce1d6f9e7a4aa7048027506493c607ebe1fcc05293b652475a17ae988f0cd55f568fdce62926ff00caefd093cc970be9c35b565b6d1761906bed76243f847cbe25be682468173391f37d6c122a45e619534995ee25b089b00f23b5767cf0861e15dc31225fff354b4900523a17d3e89973f9a2fcabd91c440ffa74b39bd0990564448956196"

bc1 = bytes.fromhex(c1)
bc2 = bytes.fromhex(c2)
bc3 = bytes.fromhex(c3)

xored_bytes1_2 = bytes(c1 ^ c2 for c1, c2 in zip(bc1, bc2))
xored_bytes2_3 = bytes(c2 ^ c3 for c2, c3 in zip(bc2, bc3))
xored_bytes1_3 = bytes(c1 ^ c3 for c1, c3 in zip(bc1, bc3))
#print(xored_bytes.hex())

bytes_list = [xored_bytes1_2, xored_bytes1_3, xored_bytes2_3]
data_bytes = [i for i in bytes_list]

xo1_2 = []
for i in range(len(data_bytes[0])):
    xo1_2.append(data_bytes[0][i])
#print(((xo1_2)))

xo1_3 = []
for i in range(len(data_bytes[1])):
    xo1_3.append(data_bytes[1][i])

#print(((xo1_3)))

xo2_3 = []
for i in range(len(data_bytes[2])):
    xo2_3.append(data_bytes[2][i])


result = []
for i in range(len(xo2_3)):
    num = xo1_2[i]
    if 32 <= num <= 126:
        result.append(chr(num))
    else:
         result.append(num)


# 1. Define your "crib" (the guess)
for j in common_words:
    crib = j

    # 2. Extract the first 5 bytes of the secret key based on this guess
    # Formula: Key = Ciphertext XOR Plaintext
    potential_key = [bc1[i] ^ ord(crib[i]) for i in range(len(crib))]

    print(f"Potential Key Bytes: {[hex(k) for k in potential_key]}")
    # 3. Test this potential key on the other two ciphertexts
    p2_reveal = "".join(chr(bc2[i] ^ potential_key[i]) for i in range(len(crib)))
    p3_reveal = "".join(chr(bc3[i] ^ potential_key[i]) for i in range(len(crib)))

    print(f"If P1 starts with '{crib}':")
    print(f"P2 starts with: '{p2_reveal}'")
    print(f"P3 starts with: '{p3_reveal}'")

