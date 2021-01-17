from pyglet.gl import *
from pyglet.window import mouse
from pyglet.window import key
import pywavefront

import sys
import numpy as np
import time

config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(width=1000, height=600, config = config)

camx, camy, camz, lookx, looky, lookz, viewx, viewy, viewz = 4, 5, 5, 2, 2, 2, 0, 1, 0
b_spline_matrix = 1/6 * np.array([
    [-1, 3, -3, 1],
    [3, -6, 3, 0],
    [-3, 0, 3, 0],
    [1, 4, 1, 0]
])

b_spline_tangent_matrix = 1/2 * np.array([
    [-1, 3, -3, 1],
    [2, -4, 2, 0],
    [-1, 0, 1, 0]
])

normal_matrix = np.array([
    [-1, 3, -3, 1],
    [1, -2, 1, 0]
])

file = open(sys.argv[1], 'r')
dots = []
#učitavanje točaka
while True:
    line = file.readline()
    if (line == '' or line.startswith("#") or line == '\n'):
        break
    line = [float(value) for value in line.split(' ')]
    dots.append(line)
dots = np.array(dots)
file.close()

segment_num = dots.shape[0] - 3

#određivanje b_spline krivulje
b_spline = []
for i in range(segment_num):
    r_x = dots[i: i+4, 0:1] 
    r_y = dots[i: i+4, 1:2]
    r_z = dots[i: i+4, 2:3]

    for t in np.arange(0, 1+1e-10, 0.010):
        T = np.array([t**3, t**2, t, 1]).reshape(1,4)
        p = [np.dot(np.dot(T, b_spline_matrix), r_x)[0][0], np.dot(np.dot(T, b_spline_matrix), r_y)[0][0], np.dot(np.dot(T, b_spline_matrix), r_z)[0][0]]
        b_spline.append(p)
b_spline = np.array(b_spline)
# print(b_spline)

#određivanje tangente u točkama b_splain krivulje
b_spline_tangent = []
for i in range(segment_num):
    r_x = dots[i: i+4, 0:1] 
    r_y = dots[i: i+4, 1:2]
    r_z = dots[i: i+4, 2:3]

    for t in np.arange(0, 1+1e-10, 0.010):
        T = np.array([t**2, t, 1]).reshape(1,3)
        p = [np.dot(np.dot(T, b_spline_tangent_matrix), r_x)[0][0], np.dot(np.dot(T, b_spline_tangent_matrix), r_y)[0][0], np.dot(np.dot(T, b_spline_tangent_matrix), r_z)[0][0]]
        b_spline_tangent.append(p)
b_spline_tangent = np.array(b_spline_tangent)

#točke tangente
tangent_vertex = b_spline +  0.5 *b_spline_tangent

#druga derivacija
b_spline_normal = []
for i in range(segment_num):
    r_x = dots[i: i+4, 0:1] 
    r_y = dots[i: i+4, 1:2]
    r_z = dots[i: i+4, 2:3]

    for t in np.arange(0, 1+1e-10, 0.010):
        T = np.array([t, 1]).reshape(1,2)
        p = [np.dot(np.dot(T, normal_matrix), r_x)[0][0], np.dot(np.dot(T, normal_matrix), r_y)[0][0], np.dot(np.dot(T, normal_matrix), r_z)[0][0]]
        b_spline_normal.append(p)
b_spline_normal = np.array(b_spline_normal)

b_spline_normal_u = np.cross(b_spline_tangent, b_spline_normal)
b_spline_binormal_v = np.cross(b_spline_tangent, b_spline_normal_u)

def draw_bspline():
    global b_spline
    glColor3f(1.0, 0.0, 0.0)
    for i in range(len(b_spline)-1):
        glBegin(GL_LINES)
        glVertex3f(b_spline[i][0], b_spline[i][1], b_spline[i][2])
        glVertex3f(b_spline[i+1][0], b_spline[i+1][1], b_spline[i+1][2])
        glEnd()

def draw_tangent():
    global b_spline, tangent_vertex
    
    glColor3f(0.0, 1.0, 0.0)
    for i in range(0, len(b_spline)-1, 10):
        glBegin(GL_LINES)
        glVertex3f(*b_spline[i])
        glVertex3f(*tangent_vertex[i])
        glEnd()

def draw_vertex():
    global dots

    glColor3f(0.0, 0.0, 1.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    for i in range(0, len(dots)):    
        glVertex3f(*dots[i])
    glEnd()

def orientation(s, e):
    os = np.cross(s,e)

    se = np.dot(s,e)
    s_norm = np.linalg.norm(s)
    e_norm = np.linalg.norm(e)

    acos = se/(s_norm * e_norm)
    if (acos > 1):
        acos = 1
    elif (acos <-1):
        acos = -1
    fi = np.arccos(acos) * 180/np.pi
    
    return(np.array([fi, *os]))


scene = pywavefront.Wavefront('teddy.obj', collect_faces=True)

scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scaled_size    = 4
scene_scale    = [scaled_size/max_scene_size for i in range(3)]
# scene_trans = [2*b_spline[0][i] for i in range(3)]
scene_trans    = [2*((scene_box[1][i]+scene_box[0][i]) + b_spline[0][i]) for i in range(3)]

# print((scene_box[1]+scene_box[0]))

def Model(rotation):
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)
    glRotatef(*(rotation))

    # colors = [[0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0],[1.0, 0.0, 0.0],
    #         [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.1],[0.0, 0.0, 0.1]]

    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for i, face in enumerate(mesh.faces):
            # glColor3f(*colors[i])
            glColor3f(0.5,0.5,0.5)
            for vertex_i in face:
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()

    glRotatef(*(-rotation))
    glTranslatef(*[-item for item in scene_trans])
    glPopMatrix()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, width / float(height), .1, 1000)
    glMatrixMode(GL_MODELVIEW)

    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    global scene_trans

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)
    glLoadIdentity()
    
    #gluLookAt(7, 10, 10, 4, 0, 0, 0, 1, 0) #custom
    gluLookAt(20, 20, 70, -5, -5, 0, 10, 10, 20) #spirala

    
    current_ori = [0, 0, 1]
    for index in range(len(b_spline)):
        glClear(GL_COLOR_BUFFER_BIT)

        rotation = orientation(current_ori, b_spline_tangent[index])

        draw_bspline()
        # draw_tangent()
        # draw_vertex()

        scene_trans = [10.5*((scene_box[1][i]+scene_box[0][i]) + b_spline[index][i]) for i in range(3)]
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        Model(rotation)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        window.flip()
        
    draw_tangent()
    draw_vertex()

pyglet.app.run()