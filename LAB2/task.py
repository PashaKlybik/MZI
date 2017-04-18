from PIL import Image, ImageDraw
pix = []; width = 0; height = 0; image =0; draw = 0

def open_image(file_name):
    global pix, width, height, image, draw
    image = Image.open(file_name)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    pix = image.load()

def close_image(file_name):
    global draw, image, pix
    image.save(file_name, "BMP")
    del draw

def open_file(file_name):
    byte = ""
    with open(file_name, 'r') as f:
        for i in f.read():
            byte += "0" * (8-len(bin(ord(i))[2:])) + bin(ord(i))[2:]
    return byte

def encription(byte):
#       global draw
    lens = "0"*(48 - len((bin(len(byte))[2:]))) + (bin(len(byte)))[2:]
    byte = lens + byte
    print byte
    i = j = k = 0
    a = [0,0,0]
    z = 0
    while byte !="":
        a[k] = int((bin(pix[i, j][k])[2:-2]+byte[:2]), 2)
        byte = byte[2:]
        z += 1
        if k == 2:
            draw.point((i,j), (a[0], a[1], a[2]))
            k = 0
            a = [0, 0, 0]
            if i == width - 1:
                i = 0
                j += 1
                if j == height -1: break;
            else:
                i += 1
        else:
            k += 1
    draw.point((i,j), (a[0], a[1], a[2]))

def decription(file_name):
    global image, pix
    byte = ""
    for j in xrange(height):
        for i in xrange(width):
            for k in xrange(3):
                #print len(bin(pix[i, j][k])[-2:])
                byte += bin(pix[i, j][k])[-2:]
    lens = int(byte[:48], 2)
    print byte[:lens+48]
    byte = byte[48: lens+48]
    with open(file_name, "w") as f:
        while byte != "":
            f.write(chr(int(byte[:8], 2)))
            byte = byte[8:]

if __name__ == "__main__":
    open_image("in.bmp")
    encription(open_file("input.txt"))
    close_image("out.bmp")
    open_image("out.bmp")
    decription("output.txt")
