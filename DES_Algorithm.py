import random

def key_scheduler():
    #Parity Drop
    par = [57, 49, 41, 33, 25, 17,  9,
            1, 58, 50, 42, 34, 26, 18,
           10,  2, 59, 51, 43, 35, 27,
           19, 11,  3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
           14,  6, 61, 53, 45, 37, 29,
           21, 13,  5, 28, 20, 12,  4]

    # P Compression table
    p_compr = [14, 17, 11, 24, 1, 5, 3, 28,
             15, 6, 21, 10, 23, 19, 12, 4,
             26, 8, 16, 7, 27, 20, 13, 2,
             41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56,
             34, 53, 46, 42, 50, 36, 29, 32]
           
    #Left rotation table
    lrt = [1, 1, 2, 2, 2, 2, 2, 2,
           1, 2, 2, 2, 2, 2, 2, 1]

    k = random.getrandbits(64)
    k = bin(k)[2:].zfill(64)
    
    key = ""
    for i in par:
        key += k[i-1]
        
    lk = key[:28]
    rk = key[28:]

    l_keys = []
    r_keys = []
    for i in range(16):
        num = lrt[i]
        
        temp = lk[0:num]
        lk = lk[num:] + temp
        l_keys.append(lk)

        temp = rk[0:num]
        rk = rk[num:] + temp
        r_keys.append(rk)

    #generate 16 48-bit keys
    keys = []
    for i in range(16):
        cat = l_keys[i] + r_keys[i]
        temp = ""
        for j in p_compr:
            temp += cat[j-1]
        keys.append(temp)

    return keys
  
def fun(R, key):
    r = int(expansion(R), 2)

    # XOR operation
    r ^= int(key, 2)
    r = bin(r)[2:].zfill(48)
    R = Sbox(r)
    R = pbox(R)
   
    return R

def expansion(R):
    # Expansion table
    e = [32,  1,  2,  3,  4,  5,
          4,  5,  6,  7,  8,  9,
          8,  9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32,  1]
    
    out = ""
    for i in e:
        out += R[i-1]

    return out

def Sbox(r):
    s = [
         # s1
         [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
          [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
          [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
          [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
         # s2
         [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
          [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
          [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
          [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
         # s3
         [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
          [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
          [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
          [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
         # s4
         [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
          [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
          [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
          [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
         # s5
         [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
          [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
          [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
          [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
         # s6
         [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
          [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
          [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
          [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
         # s7
         [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
          [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
          [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
          [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
         # s8
         [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
          [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
          [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
          [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]
        ]
    
    # Break into 8 parts
    s6 = []
    for i in range(0, 48, 6):
        s6.append(r[i:i+6])

    out = ""
    for i in range(8):
        sb = s6[i]
        row = int(sb[0]+sb[5], 2)
        col = int(sb[1:5], 2)
        out += (bin(s[i][row][col])[2:].zfill(4))

    return out

def pbox(R):
    p = [16,  7, 20, 21,
         29, 12, 28, 17,
          1, 15, 23, 26,
          5, 18, 31, 10,
          2,  8, 24, 14,
         32, 27,  3,  9,
         19, 13, 30,  6,
         22, 11,  4, 25]

    out = ""
    for i in p:
        out += R[i-1]

    return out

def ini_per(text):
    # Initial permutation table
    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]
    
    out = ""
    for i in ip:
        out += text[i-1]
        
    return out
  
def fin_per(text):
    # Final permutation
    fp = [40,  8, 48, 16, 56, 24, 64, 32,
          39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30,
          37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28,
          35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26,
          33,  1, 41,  9, 49, 17, 57, 25]
    
    out = ""
    for i in fp:
        out += text[i-1]
        
    return out
    
def encrypt(msg, keys):
    # Split plaintext into 64-bit
    texts = []
    for i in range(0, len(msg), 8):
        texts.append(msg[i:i+8])

    pt = []
    for i in texts:
        binMsg = binaryMsg(i)
        encr = cipher(binMsg, keys)
        pt.append(encr)

    out = ""
    for i in pt:
        out += i

    return out

def cipher(text, keys):
    p = ini_per(text)

    L = p[:32]
    R = p[32:]

    # 16 rounds of encryption
    for i in range(16):
        f = fun(R, keys[i])
        temp = R
        R = bin(int(L, 2) ^ int(f, 2))[2:].zfill(32)
        L = temp
        
    LR = L + R
    
    out = fin_per(LR)
        
    return out

# Convert msg to binary
def binaryMsg(text):
    out = ""
    for i in text:
        out += bin(ord(i))[2:].zfill(8)

    for i in range(64-(len(out))):
        out += "0"
        
    ptDecr = out
    
    return out
  
# Convert binary to msg
def textMsg(text):
    out = ""
    for i in range(0, 64, 8):
        out += chr(int(text[i:i+8], 2))

    return out

def decrypt(cipherText, keys):
    # Split text into 64-bit
    c_texts = []
    for i in range(0, len(cipherText), 64):
        c_texts.append(cipherText[i:i+64])

    ct = []
    for i in c_texts:
        bintext = plaintext(i, keys)
        ct.append(bintext)

    out = ""
    for i in ct:
        out += textMsg(i)
        
    return out

def plaintext(text, keys):
    p = ini_per(text)

    L1 = p[:32]
    R1 = p[32:]

    # 16 rounds of decryption
    for i in range(15, -1, -1):
        f1 = fun(L1, keys[i])
        temp = L1
        L1 = bin(int(R1, 2) ^ int(f1, 2))[2:].zfill(32)
        R1 = temp

    LR1 = L1 + R1
#     print(LR1)
    out = fin_per(LR1)
    
    return out
        
msg = input('Enter the string: ')
key = key_scheduler()
cipherText = encrypt(msg, key)
print('Cipher Text in binary form: ',cipherText)
print('Cipher Text: ',textMsg(cipherText))
plainText = decrypt(cipherText, key)
print('Plain Text after Decryption in binary form: ',binaryMsg(plainText))
print('Plain Text after Decryption: ',plainText)        
