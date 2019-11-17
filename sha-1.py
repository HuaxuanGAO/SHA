
def text2ASCII(text):
    return [code for code in text.encode('ascii')]

def ASCII2binary(ascii):
    return ["{0:08b}".format(b) for b in ascii]

def mod512448(bstr):
    while(len(bstr)%512!=448):
        bstr += '0'
    return bstr

def length2binary(bstr):
    # ignore the appended 1
    bstr = "{0:64b}".format(len(bstr)-1)
    bstr = bstr.replace(" ", "0")
    return bstr

def int2bstr(k):
    #  integer k to n bit string
    return "{0:32b}".format(k).replace(" ", "0")

def splitChunk(bstr):
    return [bstr[i:i+32] for i in range(0, len(bstr), 32)]

def leftRotate(bstr, n):
    return bstr[n:]+bstr[0:n]

def negate(bstr):
    return int2bstr(int(bstr,2) ^ (2**32-1))

def extendChunks(chunks):
    i = len(chunks)
    while i < 80:
        a = chunks[i-3]
        b = chunks[i-8]
        c = chunks[i-14]
        d = chunks[i-16]
        xor = int(a,2) ^ int(b,2) ^ int(c,2) ^ int(d,2)
        xor = int2bstr(xor)
        # left rotate
        chunks.append(leftRotate(xor,1))
        i += 1
    return chunks 

def bitOp1(B, C, D):
    # (B AND C) OR (!B AND D)
    F = (int(B,2) & int(C,2)) | (not int(B,2) & int(D,2))
    K = "01011010100000100111100110011001"
    return int2bstr(F), K

def bitOp2(B, C, D):
    # B XOR C XOR D
    F = int(B,2) ^ int(C,2) ^ int(B,2) ^ int(D,2)
    K = "01101110110110011110101110100001"
    return int2bstr(F), K

def bitOp3(B, C, D):
    # (B AND C) OR (B AND D) OR (C AND D)
    F = (int(B,2) & int(C,2)) | (int(B,2) & int(D,2)) | (int(C,2) & int(D,2))
    K = "10001111000110111011110011011100"
    return int2bstr(F), K

def bitOp4(B, C, D):
    # B XOR C XOR D
    F = int(B,2) ^ int(C,2) ^ int(B,2) ^ int(D,2)
    K = "11001010011000101100000111010110"
    return int2bstr(F), K

def SHA1(text):
    ascii = text2ASCII(text)
    print("to ascii \n %s"%(ascii))

    binary = ASCII2binary(ascii)
    print("to binary \n %s"%(binary))

    bstr = "".join(binary)+"1"
    mod = mod512448(bstr)
    print("pad until mod 512 == 448\n %s"%(mod))

    len_binary = length2binary(bstr)
    print("length to binary\n %s"%(len_binary))

    bstr = mod + len_binary
    print("join and pad 1 and length \n %s"%(bstr))

    print(len(bstr))
    chunks = splitChunk(bstr)
    print("split chunks \n %s"%(chunks))

    chunks = extendChunks(chunks)
    print("extend chunks \n %s"%(chunks))

    h0 = "01100111010001010010001100000001"
    h1 = "11101111110011011010101110001001"
    h2 = "10011000101110101101110011111110"
    h3 = "00010000001100100101010001110110"
    h4 = "11000011110100101110000111110000"
    A = h0
    B = h1
    C = h2
    D = h3
    E = h4
    for i, chunk in enumerate(chunks):
        if i < 20:
            F, K = bitOp1(B, C, D)
        if i < 40:
            F, K = bitOp2(B, C, D)
        if i < 60:
            F, K = bitOp3(B, C, D)
        if i < 80:
            F, K = bitOp4(B, C, D)
        # (A left rotate 5) + F + E + K + (the current word)
        alrt = leftRotate(A, 5)
        temp = int2bstr(int(alrt,2)+ int(F,2) +int(E,2)+int(K,2)+int(chunk,2))
        # keep right most 32
        temp = temp[-32:]
        print("iter %d, temp %s"%(i, temp))
        E = D
        D = C
        C = leftRotate(B, 30)
        B = A
        A = temp

    h0 = h0 + A
    h1 = h1 + B
    h2 = h2 + C
    h3 = h3 + D
    h4 = h4 + E

    return '{:08x}'.format(int(h0[-32:], 2)) + '{:08x}'.format(int(h1[-32:], 2)) + '{:08x}'.format(int(h2[:-32], 2))\
         + '{:08x}'.format(int(h3[:-32], 2)) + '{:08x}'.format(int(h4[-32:], 2))

text = "this is great!"
sha = SHA1(text)
print(text)
print(sha)

# 98bb2b7d040eae5b98badcfe103254768f2a2e86