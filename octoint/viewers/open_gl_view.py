import qdarkstyle

import numpy
from OpenGL import GL, GLU
from OpenGL.GL import shaders

from PySide2 import QtCore, QtWidgets, QtOpenGL

from octoint.main_utils import octoint_logger
from octoint.gcode.parse_gcode_cy import parser as c_parser
from octoint.viewers.open_gl_utils import get_fileoffset, get_current_state, get_world_pos, vector_length
from octoint.main_utils import Worker

open_view_logger = octoint_logger(__name__)

gcode_worker = Worker()
gcode_worker.setup(c_parser, emit_dict=True)

state_worker = Worker()
state_worker.setup(get_current_state, emit_dict=True)

fileoffset_worker = Worker()
fileoffset_worker.setup(get_fileoffset, emit_dict=True)


class OpenGlViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        _mainLayout = QtWidgets.QVBoxLayout()

        self.gl_widget = GLWidget()
        self._preview_label = QtWidgets.QLabel('Preview')
        self._preview_toggle = QtWidgets.QCheckBox()
        self._preview_toggle.setChecked(True)
        self._on_checkbox_changed(True)
        self._preview_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self._preview_slider.setValue(99)

        _preview_layout = QtWidgets.QHBoxLayout()
        toggle_layout = QtWidgets.QHBoxLayout()

        toggle_layout.addWidget(self._preview_label)
        toggle_layout.addWidget(self._preview_toggle)

        _preview_layout.addLayout(toggle_layout)
        _preview_layout.addWidget(self._preview_slider)

        _mainLayout.addLayout(_preview_layout)
        _mainLayout.addWidget(self.gl_widget)

        self.setLayout(_mainLayout)

        self._preview_toggle.stateChanged.connect(self._on_checkbox_changed)
        self._preview_slider.valueChanged.connect(self._on_slider_value_changed)

    def _on_checkbox_changed(self, state):
        self.gl_widget.preview = state

    def _on_slider_value_changed(self):
        self.gl_widget.preview_offset = self._preview_slider.value() / 99.

    def enterEvent(self, event):
        self.setFocus(QtCore.Qt.FocusReason.MouseFocusReason)

    def leaveEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F:
            self.gl_widget.F_Pressed.emit()


class GLWidget(QtOpenGL.QGLWidget):
    F_Pressed = QtCore.Signal()
    GL_MULTISAMPLE = 0x809D

    list_item_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        open_view_logger.info('init GLWidget')
        QtOpenGL.QGLWidget.__init__(self, parent)

        # start gcode worker thread
        self.update_gcode()

        gcode_worker.dataSignal.connect(self.on_gcode_data_sent)
        fileoffset_worker.dataSignal.connect(self.on_file_offset_received)

        self.width = self.width
        self.height = self.height

        self.startTimer(100)

        self._vbo = None
        self.viewMatrix = None
        self._shader = None

        self.vector_array = numpy.array([], dtype='float32')
        self.vector_byte_offset_list = None

        self._pan_x = 0
        self._pan_y = 0
        self._rot_x = 0
        self._rot_y = 0
        self._rot_z = 0
        self._zoom_z = 0

        self.preview = False
        self.preview_offset = 1.

        self.offset = 0
        self.update_offset = True

        self.lastPos = QtCore.QPoint()
        self.F_Pressed.connect(self.reset_transform)

    def on_gcode_data_sent(self, data):
        self.vector_array, self.vector_byte_offset_list = data['result']

        self.bind_buffer()

    @classmethod
    def update_gcode(cls):
        if gcode_worker.isRunning():
            gcode_worker.stop()
        else:
            gcode_worker.start()

    def initializeGL(self):
        self.qglClearColor(qdarkstyle.palette.DarkPalette.COLOR_BACKGROUND_DARK)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_BLEND)

        FRAGMENT_SHADER = '''
                            varying out vec4 outColor;
                            void main(){
                                outColor = vec4(0.0f,0.9f,0.8f, 0.1f);
                            }
                    '''

        self._shader = shaders.compileProgram(shaders.compileShader(FRAGMENT_SHADER, GL.GL_FRAGMENT_SHADER))

    def bind_buffer(self):
        self._vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vector_array, GL.GL_STATIC_DRAW)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

        GL.glUseProgram(self._shader)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(60, 1, 0.1, 5000)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glTranslated(self._pan_x, self._pan_y, self._zoom_z)

        GL.glRotatef(self._rot_x / 16.0, 1.0, 0.0, 0.0)
        GL.glRotatef(self._rot_y / 16.0, 0.0, 1.0, 0.0)
        GL.glRotatef(self._rot_z / 16.0, 0.0, 0.0, 1.0)

        GL.glDrawArrays(GL.GL_LINES, 0, self.offset)

    def reset_transform(self):
        self._pan_x = 0
        self._pan_y = 0
        self._rot_x = 0
        self._rot_y = 0
        self._rot_z = 0
        self._zoom_z = 0

        self.lastPos = QtCore.QPoint()
        self.updateGL()

    def timerEvent(self, event):
        state_worker.dataSignal.connect(self.on_state_received)
        if state_worker.isRunning():
            state_worker.stop()
        else:
            state_worker.start()

    def on_state_received(self, state):
        if state['result'] == 'Printing' and not self.preview:
            if self.update_offset:
                if fileoffset_worker.isRunning():
                    fileoffset_worker.stop()
                else:
                    fileoffset_worker.start()
        else:
            if self.update_offset and self.preview:
                self.offset = int((len(self.vector_array) / 3) * self.preview_offset)
                self.update()
            elif not self.preview:
                self.offset = 0

    def on_file_offset_received(self, offset):
        fileoffset = offset['result']
        self.offset = int(self.vector_byte_offset_list[int(fileoffset)] / 3)
        self.update()

    def mousePressEvent(self, event):
        self.update_offset = False
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseReleaseEvent(self, event):
        self.update_offset = True

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self._set_x_rotation(self._rot_x + 8 * dy)
            self._set_y_rotation(self._rot_y + 8 * dx)

        elif event.buttons() & QtCore.Qt.RightButton:
            self._zoom_z += (dx - dy) / 2 * 0.1
            self.updateGL()

        elif event.buttons() == QtCore.Qt.MiddleButton:
            zero = get_world_pos(0, 0)
            one = get_world_pos(1, 1)

            diagonal = numpy.subtract(one, zero)
            length = vector_length(diagonal)

            self._pan_x += dx * length * 50
            self._pan_y += dy * -length * 50
            self.updateGL()

        self.lastPos = QtCore.QPoint(event.pos())

    def wheelEvent(self, event):
        self._zoom_z += event.delta() * 0.005
        self.updateGL()

    def resizeGL(self, width, height):
        self.width = width
        self.height = height
        side = min(width, height)
        GL.glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

    @classmethod
    def normalize_angle(cls, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def _set_x_rotation(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self._rot_x:
            self._rot_x = angle
            self.updateGL()

    def _set_y_rotation(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self._rot_y:
            self._rot_y = angle
            self.updateGL()

    def _set_z_rotation(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self._rot_z:
            self._rot_z = angle
            self.updateGL()

    def minimumSizeHint(self):
        return QtCore.QSize(1000, 1000)

    def sizeHint(self):
        return QtCore.QSize(1000, 1000)


if __name__ == '__main__':
    window = OpenGlViewer()
    window.show()
