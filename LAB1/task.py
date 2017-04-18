from LAB3 import sha1
IP = []; E = []; S = []; P = [];C0 = []; D0 = []; SHIFT = []; KI = []; PI1 = []
C = []; D = []; keys = []
k = ""


def generate_keys():
    for i in xrange(16):
        keys.append(key(SHIFT[i]))

def key(change):
    global C, D
    C = C[change:] + C[:change]
    D = D[change:] + D[:change]
    return zip (*[iter([(C+D)[i-1] for i in KI])] * 6)

def inicialconst(input_key):
    global IP, P, C0, D0, SHIFT, KI, PI1, k, C, D
    temp = "".join( "0" * (8-len( bin(ord(i))[2:])) + bin(ord(i))[2:] for i in input_key)
    for i in xrange(8):
        k = k + temp[i  * 7: (i + 1) * 7] + str(sum([ int(j) for j in temp[i * 7: (i + 1) * 7] ]) % 2)
    with open("const.txt", "r") as f:
        IP = map(int, f.readline().split())
        for i in xrange(8):
            E.append(map(int, f.readline().split()))
        for i in xrange(8):
            S.append([])
            for j in xrange(4):
                S[i].append(map(int, f.readline().split()))
        P = map(int, f.readline().split())
        C0 = map(int, f.readline().split())
        D0 = map(int, f.readline().split())
        SHIFT = map(int, f.readline().split())
        KI = map(int, f.readline().split())
        PI1 = map(int, f.readline().split())
        C = [ int(k[i-1]) for i in C0]
        D = [ int(k[i-1]) for i in D0]
    generate_keys();

def f(left, k):
    e_left = [[ left[j-1] for j in i] for i in E]
    b = ""
    for i in xrange(8):
        bi = "".join(["1" if int(e_left[i][j]) != int(k[i][j]) else "0" for j in xrange(6)])
        t =  bin(S[i][int(bi[0] + bi[-1], 2) ][ int(bi[1: -1], 2)])[2:]
        b = b + ("0" * (4 - len(t)) + t)
    #print b
    #b = [i+1 for i in xrange(32)]
    return [b[i-1] for i in P]

def PI_reshuffle(block_64):
    #print len(block_64)
    block_IP = [None]*64
    for i in xrange(64):
        block_IP[i] = block_64[IP[i]-1]
    return block_IP[:32], block_IP[32:]

def PI1_reshuffle(block_64):

    block_IP1 = [None]*64
    for i in xrange(64):
        block_IP1[i] = block_64[PI1[i]-1]
    return block_IP1


def DES(block_64):
    left, right = PI_reshuffle(block_64)
    for i in xrange(0, 16, 1):
        temp1 = f(right, keys[i])
        temp = left
        left = right
        right = ["0" if temp[j] == temp1[j] else "1" for j in xrange(32)]
    block_IP = PI1_reshuffle(left + right)
    return block_IP

def DES_back(block_64):
    left, right = PI_reshuffle(block_64)
    for i in xrange(15, -1, -1):
        temp1 = f(left, keys[i])
        temp = right
        right = left
        left = ["0" if temp[j] == temp1[j] else "1" for j in xrange(32)]
    block_IP = PI1_reshuffle(left + right)
    return block_IP

def read_file(filename):
    byte_text = []
    byte = ""
    with open(filename, 'r') as f:
        for i in f.read():
            byte += "0" * (8-len( bin(ord(i))[2:])) + bin(ord(i))[2:]
    while len(byte)>63:
        byte_text.append(byte[:64])
        byte = byte[64:]
    if byte != "":
        byte_text.append(byte+ "0"*(64-len(byte)))
    return byte_text

def write_cipher_file(file_name, input_data):
    print sha1.hash("".join(input_data))
    with open(file_name, "w") as f:
        for i in input_data:
            answer = DES(i)
            while len(answer):
                f.write( chr(int("".join(answer[:8]), 2)))
                answer = answer[8:]
    print "OK"

def write_decrypted_file(file_name, input_data):
    all_text = ""
    with open(file_name, "w") as f:
        for i in input_data:
            answer = DES_back(i)
            all_text += "".join(answer)
            while len(answer):
                f.write( chr(int("".join(answer[:8]), 2)))
                answer = answer[8:]
    print sha1.hash(all_text)
    print "OK"

def main():
    inicialconst("abcdefg")
    a = raw_input("1- Encrypt, 2- decrypt, 0 - close\n")
    while a != "0":
        if a == "1":
            write_cipher_file(raw_input("write output filename:"),read_file(raw_input("write input file:")))
        elif a == "2":
            write_decrypted_file(raw_input("write output filename:"), read_file(raw_input("write input file:")))
        else: print "Error"
        a = raw_input("1- Encrypt, 2- decrypt, 0 - close\n")

if __name__ == "__main__":
    main()
