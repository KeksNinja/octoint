import sys
from functools import wraps
import logging
from PySide2 import QtCore


class Worker(QtCore.QThread):
    """
    Create Worker Thread with optional Signal output
    """

    dataSignal = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

        self.emit_dict = False
        self.additional_data = None
        self.args = None
        self.kwargs = None

        self._stopped = True
        self._mutex = QtCore.QMutex()
        self.func = None

        self.currentThread()

    def setup(self, func, emit_dict=False, additional_data=None, args=None, kwargs=None):
        """
        Setup Worker with all necessary parameters.

        :param func: (function) function to run in the worker thread
        :param emit_dict: (bool) output a dictionary containing a 'result' key containing the return of func
        :param additional_data: (bool) output additional data in the returned dict from the emit inside an
                                        'additional_data' key
        :param args: (list) list of arguments passed to func
        :param kwargs: (dict) dictionary of keyword arguments passed to func
        :return: (QtCore.Signal) optional output
        """
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []

        self.func = func
        self.emit_dict = emit_dict
        self.additional_data = additional_data
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self._mutex.lock()
        self._stopped = True
        self._mutex.unlock()

    def run(self):
        """Overwrite run function"""

        self._stopped = False
        if self._stopped:
            return
        result = {'result': self.func(*self.args, **self.kwargs)}
        if self.additional_data:
            result['additional_data'] = self.additional_data
        if self.emit_dict:
            self.dataSignal.emit(result)


def octoint_logger(name, write_level=logging.WARNING, log_level=logging.DEBUG):
    """
    Create Logger based on name with universal printsettings.

    :param name: (str) Name of Logger
    :param write_level: (logging.WARNING) Level used for log files (logging.INFO, logging.DEBUG...)
    :param log_level: (logging.DEBUG) Level used for console output (logging.INFO, logging.DEBUG...)
    :return: (logging.Logger)
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = ColorHandler()
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    try:
        formatter = logging.Formatter('%(levelname)s: {}: %(message)s')
        logfile_location = './logs/{}.log'.format(name)

        file_handler = logging.FileHandler(logfile_location)
        file_handler.setLevel(write_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except FileNotFoundError as e:
        logger.warning(e)

    logger.propagate = False
    return logger


def timer(logger, warn_time=0.05):
    """
    Time Functions and write to logger if function takes too long.

    :param logger: (logging.Logger) Logger to use for logging time
    :param warn_time: (float) Time to take before logging
    :return: (function)
    """
    def time_dec(func):
        import time

        @wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time() - t1
            if t2 > warn_time:
                logger.warning('{} function ran for {}'.format(func.__name__, t2))
            return result
        return wrapper
    return time_dec


# TODO: change formatting
# https://xsnippet.org/359377/
class _AnsiColorizer(object):
    """
    A colorizer is an object that loosely wraps around a stream, allowing
    callers to write text to the stream in a particular color.

    Colorizer classes must implement C{supported()} and C{write(text, color)}.
    """
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        """
        A class method that returns True if the current platform supports
        coloring terminal output using this method. Returns False otherwise.
        """
        if not stream.isatty():
            return False  # auto color only on TTYs
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                try:
                    return curses.tigetnum("colors") > 2
                except curses.error:
                    curses.setupterm()
                    return curses.tigetnum("colors") > 2
            except:
                raise
                # guess false in case of error
                return False

    def write(self, record, format_text):
        """
        Write the given text to the stream in the given color.

        :param record: Record object from logging.
        :param format_text: (str) Format String from ColorHandler
        """

        log_levels = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR"
        }
        msg_colors = {
            logging.DEBUG: "green",
            logging.INFO: "blue",
            logging.WARNING: "yellow",
            logging.ERROR: "red"
        }

        level = log_levels.get(record.levelno, "NONE")
        color = msg_colors.get(record.levelno, "black")

        color = self._colors[color]
        text = format_text.format(loglevel=level, levelname=record.name, text=record.msg)

        color_text = '\x1b[{color};1m{text}\x1b[0m\n'.format(color=color, text=text)
        self.stream.write(color_text)


class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stdout):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))
        self.format = '{loglevel}: {levelname}: {text}'

    def emit(self, record):
        self.stream.write(record , self.format)