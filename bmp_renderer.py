'''
@author Pedro Pablo Arriola Jimenez (20188)
@filename bmp_renderer.py
@description: BMP file renderer that works using concepts related
to framebuffers and low level code such as bytes.
'''

from random import randint
import struct


# Functions that will be needed to create low level structures.
def char(c):
    # 1 byte character
    c = struct.pack('=c', c.encode('ascii'))
    return c

def word(w):
    # 2 bytes character
    w = struct.pack('=h', w)   
    return w  


def dword(dw):
    # 4 bytes character
    dw = struct.pack('=l', dw)   
    return dw  

def color_select(r, g, b):
    return bytes([b, g, r])

# Class of type Render that will nest every function that will create a BMP file from scratch. 

class Render(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.FILE_SIZE = (54)
        self.PIXEL_COUNT = 3
        self.PLANE = 1
        self.BITS_PER_PIXEL = 24
        self.DIB_HEADER = 40
        self.pixels = 0
        self.clearColor = color_select(0, 0, 0)
        self.viewport_x = 0 
        self.viewport_y = 0
        self.viewport_height = 0
        self.viewport_width = 0
        
    '''
    --- SR1: POINTS
  
    '''      
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        
        self.framebuffer = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height
    
    def glColor(self, r, g, b):
        self.clearColor = color_select(r, g, b)
    
    def glClearColor(self, r, g, b):
        self.clearColor = color_select(r, g, b)
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x, y)
        
    def glVertex(self, x, y):
        if -1 <= x <= 1:
            if -1 <= y <= 1:
                pass
            else:
                y = 0
        else:
            x = 0
        self.pixel_X = int((x + 1) * self.viewport_width * 1/2 ) + self.viewport_x
        self.pixel_Y = int((y + 1) * self.viewport_height * 1/2) + self.viewport_y
        self.glPoint(self.pixel_X,self.pixel_Y)
        
    def glClear(self):
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x, y)
        
    def glPoint(self, x, y):
        if(0 < x < self.width and 0 < y < self.height):
            self.framebuffer[y][x] = self.clearColor
    
    
        
    '''
    --- SR2: LINES
    
    '''
    
    # Line drawing function which implements Bresenham's algorithm
    def glLine(self, x0, y0, x1, y1):
        
        x0 = int((x0 + 1) * self.viewport_width * 1/2 ) + self.viewport_x
        y0 = int((y0 + 1) * self.viewport_height * 1/2) + self.viewport_y

        x1 = int((x1 + 1) * self.viewport_width * 1/2 ) + self.viewport_x
        y1 = int((y1 + 1) * self.viewport_height * 1/2) + self.viewport_y

        #realizar conversion
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if  x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        
        threshold = dx
        
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x)
            else:
                self.glPoint(x, y)

            offset += dy * 2
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2
        
        
    '''
    SR3: MODELS
    
    '''
    
    def transform_vertex(self, vertex, scale, translate):
        return [

            (vertex[0] * scale[0]) + translate[0], 
            (vertex[1] * scale[1]) + translate[1]
        ]
    
    
    
    '''
    RENDERS FILE
    
    '''
    
    def glFinish(self, filename):
        with open(filename, 'bw') as file:
            # Header
            file.write(char('B'))
            file.write(char('M'))

            # file size
            file.write(dword(self.FILE_SIZE + self.height * self.width * self.PIXEL_COUNT))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(self.FILE_SIZE))

            # Info Header
            file.write(dword(self.DIB_HEADER))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(self.PLANE))
            file.write(word(self.BITS_PER_PIXEL))
            file.write(dword(0))
            file.write(dword(self.width * self.height * self.PIXEL_COUNT))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
    
            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[y][x])
            file.close()

