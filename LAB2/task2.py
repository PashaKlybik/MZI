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

def digital_signature(key, n, g):
    S = 0.0
    for i in xrange(n):
        a = i*key + 2
        b = i*key + 1
        print pix[a / width, a % width]
        ar, ag, ab = pix[a / width, a % width]
        br, bg, bb = pix[b / width, b % width]
        S += ((ar - br) + (ag - bg) + (ab - bb)) / 3.0
        draw.point((a / width, a % width), (ar + g, ag + g, ab + g))
        draw.point((b / width, b % width), (br - g, bg - g, bb - g))
    print S / n

def check_digital_signatre(key, n):
        S = 0.0
        for i in xrange(n):
            a = i*key + 2
            b = i*key + 1
            ar, ag, ab = pix[a / width, a % width]
            br, bg, bb = pix[b / width, b % width]
            S += ((ar - br) + (ag - bg) + (ab - bb)) /3.0
        print S / n

def main():
    #open first image and change it
    open_image("in.bmp")
    digital_signature(3, 10000, 3)
    close_image("out2.bmp")
    open_image("out2.bmp")
    check_digital_signatre(3, 10000)

if __name__ == "__main__":
    main()
