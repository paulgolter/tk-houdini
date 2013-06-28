#
# Copyright (c) 2013 Shotgun Software, Inc
# ----------------------------------------------------
#
import hou

from PySide import QtCore
from PySide import QtGui


class IntegratedEventLoop(object):
    """This class behaves like QEventLoop except it allows PyQt to run inside
    Houdini's event loop on the main thread.  You probably just want to
    call exec_() below instead of using this class directly.
    """
    def __init__(self, application):
        # We need the application to send posted events.  We hold a reference
        # to any dialogs to ensure that they don't get garbage collected
        # (and thus close in the process).  The reference count for this object
        # will go to zero when it removes itself from Houdini's event loop.
        self.application = application
        self.event_loop = QtCore.QEventLoop()

    def exec_(self):
        hou.ui.addEventLoopCallback(self.processEvents)

    def processEvents(self):
        self.event_loop.processEvents()
        self.application.sendPostedEvents(None, 0)


def exec_(application):
    """You cannot call QApplication.exec_, or Houdini will freeze while PyQt
    waits for and processes events.  Instead, call this function to allow
    Houdini's and PyQt's event loops to coexist.  Pass in any dialogs as
    extra arguments, if you want to ensure that something holds a reference
    to them while the event loop runs.

    This function returns right away.
    """
    IntegratedEventLoop(application).exec_()
