import numpy
import io
from octoint.main_utils import timer, octoint_logger
from octoint.main_config import CONFIG

parse_gcode_logger = octoint_logger(__name__)

gcode_file_path = "./selected_file.gcode"


@timer(parse_gcode_logger, warn_time=1.)
def parser():
    """
    :return:  list of a numpy float32 array and a byte offset list containing the vector array offset of the current byte
    """

    raw_gcode = _get_gcode()
    return _parse_gcode(raw_gcode)

def _get_gcode():
    """
    :return: load selected gcode file
    """
    try:
        with open(gcode_file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError as e:
        parse_gcode_logger.error(e)
        return ''


cpdef tuple _parse_gcode(raw_gcode):
    """
    Parse raw gcode file by searching for x y and z values and preparing them for opengl
    :param raw_gcode: 
    :return: list of a numpy float32 array and a byte offset list containing the vector array offset of the current byte  
    """

    cdef int vector_byte_offset = 0
    cdef int coordinate_offset = 0

    cdef list vector_byte_offset_list = [0] * len(raw_gcode) * 2

    cdef float x = 0
    cdef float y = 0
    cdef float z = 0

    cdef list coordinate_array = []

    cdef list coordinates
    cdef str coordinate

    file = io.StringIO(raw_gcode)
    cdef str line

    for line in file.readlines():
        if ('X' in line or 'Y' in line or 'Z' in line) and ('G0' in line or 'G1' in line):
            coordinates = line.split(' ')

            coordinate_array.append(x)
            coordinate_array.append(y)
            coordinate_array.append(z)

            for coordinate in coordinates:
                if 'X' in coordinate:
                    x = (float(coordinate[1:]) / CONFIG.dimensions['x'] - 0.5) * 10

                if 'Y' in coordinate:
                    y = (float(coordinate[1:]) / CONFIG.dimensions['y'] - 0.5) * 10

                if 'Z' in coordinate:
                     try:
                        z = (float(coordinate[1:]) / CONFIG.dimensions['z'] - 0.5) * 10
                     except ValueError:
                        pass


            coordinate_array.append(x)
            coordinate_array.append(y)
            coordinate_array.append(z)
            coordinate_offset += 6

        for byte in line:
            vector_byte_offset += 1
            vector_byte_offset_list[vector_byte_offset] = coordinate_offset


    np_coordinate_array = numpy.array(coordinate_array, dtype='float32')
    return np_coordinate_array, vector_byte_offset_list


