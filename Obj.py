'''
@author Pedro Pablo Arriola Jimenez (20188)
@filename Obj.py
@description: Object file that will open a 3d model.
'''

class Obj(object):
    def __init__(self, filename) -> None:
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertex = []
        self.faces = []
        
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v':
                    self.vertex.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int , face.split('/'))) for face in value.split(' ')])

        


