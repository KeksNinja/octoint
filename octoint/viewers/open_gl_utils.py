import numpy
import math
from OpenGL import GL, GLU

from octoint import client
from octoint.main_utils import octoint_logger, timer

open_utils_logger = octoint_logger(__name__)


def get_job_dict():
    return client.job_info()


def get_current_state():
    return get_job_dict()['state']


def get_fileoffset():
    return client.job_info()['progress']['filepos']



#TODO fix incorrect plane intersection (worldpos propably)
def get_world_pos(x, y):
    viewport = []
    modelview = []
    projection = []

    modelview = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)  # get the modelview info
    projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)  # get the projection matrix info
    viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)

    o_winX = x
    o_winY = viewport[3] - y
    o_winZ = 0

    rO = GLU.gluUnProject(o_winX, o_winY, o_winZ, modelview, projection, viewport)
    return rO

'''
@timer(open_utils_logger)
def get_plane_intersection(x, y):
    modelview = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)  # get the modelview info
    projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)  # get the projection matrix info
    viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)

    o_winX = x
    o_winY = viewport[3] - y
    o_winZ = 0

    rO = list(GLU.gluUnProject(o_winX, o_winY, o_winZ, modelview, projection, viewport))
    d_winX = x
    d_winY = viewport[3] - y
    d_winZ = 1

    dO = GLU.gluUnProject(d_winX, d_winY, d_winZ, modelview, projection, viewport)

    rN = normalize(numpy.subtract(dO, rO))

    pO = (0, 0, 0.5)
    pN = (0, 0, -1)

    intersect, center = ray_plane_intersect(pO, pN, rO, rN)
    return intersect, center


def ray_plane_intersect(pO, pN, rO, rN):
    denom = numpy.dot(pN, rN)
    if denom > 1e-8:
        pOrO = numpy.subtract(pO, rO)

        t = numpy.dot(pOrO, pN) / denom

        i_pos = offset_by_dir(rO, rN, t)
        if t > 1000:
            i_pos = [0, 0, 0]

        return t >= 0, i_pos
    return False, 0


#TODO replace with numpy

def offset_by_dir(rO, rN, t):
    return numpy.add(rO, numpy.multiply(rN, t))


def cross(vec1, vec2):
    x = vec1[1] * vec2[2] - vec1[2] * vec2[1]
    y = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    z = vec1[0] * vec2[1] - vec1[1] * vec2[0]
    return [x, y, z]
'''

def vector_length(vec):
    return math.sqrt((vec[0] ** 2) + (vec[1] ** 2) + (vec[2] ** 2))


def normalize(vec):
    v_len = vector_length(vec)
    return [c / v_len for c in vec]

