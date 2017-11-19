from PyQt5.QtWidgets import QDialog

from ui_preferences import Ui_Preferences
class Preferences(QDialog):
    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        self.ui = Ui_Preferences()
        self.ui.setupUi(self)

