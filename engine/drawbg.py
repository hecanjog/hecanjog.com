from PIL import Image
import random

W, H = 800, 800

def drawline(img, start, end):
    x, y = start
    maxstep_x = random.randint(3, 10)
    maxstep_y = random.randint(3, 10)
    direction = random.choice([-1,1])
    a = random.randint(100, 255)
    while True:
        if x < W and x > 0 and y < H and y > 0:
            img.putpixel((x, y), (255, 255, 255, a))
        x += random.randint(2, maxstep_x) * direction
        y += random.randint(2, maxstep_y) 

        if x > W:
            direction = -1
        elif x < 0:
            direction = 1

        if y > end[1]:
            break

    return img

def drawbg(filename):
    img = Image.new('RGBA', (W, H), (255, 0, 0, 0))
    for _ in range(50):
        start = random.randint(0, W), 0
        end = random.randint(0, W), H

        img = drawline(img, start, end)
    img.save(filename)
    

if __name__ == '__main__':
    drawbg('static/img/pat-bg.png')
