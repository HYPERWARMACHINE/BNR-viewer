from OpenGL.GL import *
from OpenGL.GLUT import *
import struct
import sys

def main():
    
    pixels = []
    linear_pixels = []

    file_path = str(sys.argv[1])
    file = open(file_path, "rb").read()
    
    checksum = sum(file[0:4])
    if checksum != 275 and 276:
        print("Checksum failed, supported file?")

    for i in range(0x20, 0x1820, 2):
        pixels.append((file[i] << 8) + file[i+1])

    #decodes 4x4 components of bnr
    for vblock in range(8):
        vblock_i = vblock*96*4
        for line in range(4):
            line_i = line*4
            for hblock in range(24):
                hblock_i = hblock*16+line_i
                for i in range(4):
                    linear_pixels.append(pixels[vblock_i+hblock_i+i])

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    if len(sys.argv) > 2:
        if sys.argv[2] == "full":
            window_width = glutGet(GLUT_SCREEN_WIDTH)
            window_height = window_width/3
        else:
            scale = int(sys.argv[2])/100
            window_width = 96*scale
            window_height = 32*scale
    else:
        window_width = 480
        window_height = 160

    glutInitWindowSize(int(window_width),int(window_height))

    window_title = list(file[0x1820:0x1840])
    window_title = struct.pack("b"*len(window_title), *window_title).decode('utf8')
    glutCreateWindow(window_title)

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 96, 32, 0, GL_BGRA, GL_UNSIGNED_SHORT_1_5_5_5_REV, linear_pixels)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glutDisplayFunc(draw)
    glutMainLoop()
    
def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBegin (GL_QUADS) 
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1, 1)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1, -1)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1, 1)
    glEnd()
    glutSwapBuffers()

main()
