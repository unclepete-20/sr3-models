from bmp_renderer import Render
from Obj import Obj

frame = Render()
model = Obj('koenigsegg.obj')

scale_factor = (0.1, 0.1)
translate_factor = (0.000000000008, 0.000000000008)

frame.glCreateWindow(1024, 1024)

frame.glViewPort(80, -200, 900, 900)

frame.glClear()

frame.glColor(255, 255, 255)

for face in model.faces:
    
    # Draws squares
    if len(face) == 4:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        f4 = face[3][0] - 1
        
        print('faces square', (f1, f2, f3, f4))
        
        v1 = frame.transform_vertex(model.vertex[f1], scale_factor, translate_factor)
        v2 = frame.transform_vertex(model.vertex[f2], scale_factor, translate_factor)
        v3 = frame.transform_vertex(model.vertex[f3], scale_factor, translate_factor)
        v4 = frame.transform_vertex(model.vertex[f4], scale_factor, translate_factor)
        
        print('vertices square', (v1, v2, v3, v4))
        
        frame.glLine(v1[0], v1[1], v2[0], v2[1])
        frame.glLine(v2[0], v2[1], v3[0], v3[1])
        frame.glLine(v3[0], v3[1], v4[0], v4[1])
        frame.glLine(v4[0], v4[1], v1[0], v1[1])
     
    # Draws triangles    
    if len(face) == 3:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        
        print('faces triangle', (f1, f2, f3))
        
        v1 = frame.transform_vertex(model.vertex[f1], scale_factor, translate_factor)
        v2 = frame.transform_vertex(model.vertex[f2], scale_factor, translate_factor)
        v3 = frame.transform_vertex(model.vertex[f3], scale_factor, translate_factor)
        
        print('vertices triangle', (v1, v2, v3))
        
        frame.glLine(v1[0], v1[1], v2[0], v2[1])
        frame.glLine(v2[0], v2[1], v3[0], v3[1])
        frame.glLine(v3[0], v3[1], v1[0], v1[1])
    

frame.glFinish('car.bmp')

'''
square = [
    (0.2, 0.2),
    (0.8, 0.2),
    (0.8, 0.8),
    (0.2, 0.8)
]

last_point = square[-1]

for point in square:
    frame.glLine(*last_point, *point)
    last_point = point
'''