from PIL import Image
import numpy as np

im=Image.open(r"sample24(440x320).png")
#im.show()
width, height=im.size
w = (int)(width/2)
h = (int)(height/2)
#im1=Image.new(mode="RGB", size=(width*2,height*2), color=(200,200,200))
#mask=Image.new(mode="RGB", size=(width*2,height*2), color=(255,255,255))
downsample=Image.new(mode='RGB', size=(w,h), color=(200,200,200))
px3=downsample.load()

def downsize():
    for i in range (0, w, 1):
        for j in range (0, h, 1):
            px3[i,j]=im.getpixel((2*i,2*j))

downsize()
print(downsample.size)
downsample.show()
downsample.save("sample24downsized.png")