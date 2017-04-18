
def append_bit(bit):
    """create list of element lens 512 byte """
    bit_group = []
    l = bin(len(bit))[2:]
    l = "0" * (64 - len(l)) + l
    while len(bit) >= 512:
        bit_group.append(bit[:512])
        bit = bit[512:]
    if len(bit) < 448:
        bit_group.append(bit + "1" + "0"*(447 - len(bit)) + l)
    else:
        bit_group.append(bit + "1" + "0"*(511 - len(bit)))
        bit_group.append(bit + "0"*(448 - len(bit)) + l)
    return bit_group

def _left_rotate(n, b):
    """Left rotate a 32-bit integer n by b bits."""
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def hash_block(blocks):
    h0 = 0x67452301; h1 = 0xEFCDAB89; h2 = 0x98BADCFE; h3 = 0x10325476; h4 = 0xC3D2E1F0
    for block in blocks:
        w = []
        for i in xrange(16):
            w.append(int(block[i * 32: (i + 1) * 32], 2))
        for i in xrange(16, 80):
            w.append( _left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1) )
        a = h0; b = h1; c = h2; d = h3; e = h4
        for i in xrange(80):
            if 0 <= i <=19:
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = ( b ^ c ^ d )
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = ((b & c) | (b & d) |(c & d))
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = (b ^ c ^ d)
                k = 0xCA62C1D6
            a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, a, _left_rotate(b, 30), c, d)
#            temp = (((a << 5) & 0xffffffff) + f + e + k + w[i])& 0xffffffff
#            d = c
#            c = (b << 30) & 0xffffffff
#            b = a
#            a =temp
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        answer = hex(h0)[2:] + " " + hex(h1)[2:] + " " + hex(h2)[2:] + " " + hex(h3)[2:] + " " + hex(h4)[2:]
    return answer

def main(text):

    text = unicode(text, "utf-8")
    byte = ''
    for i in text:
        byte += "0" * (8-len( bin(ord(i))[2:])) + bin(ord(i))[2:]
    print byte
    print hash_block(append_bit(byte))
