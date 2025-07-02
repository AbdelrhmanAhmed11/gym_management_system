from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from views.login_view import LoginWindow
from i18n.translator import Translator
from views.dashboard_view import DashboardWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gym Management System')
        self.setMinimumSize(1000, 700)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.translator = Translator(QApplication.instance())
        self.login_view = LoginWindow(self.translator)
        self.login_view.handle_login_success = self.show_dashboard
        self.stack.addWidget(self.login_view)
        self.dashboard_view = None

    def show_dashboard(self, user):
        if self.dashboard_view:
            self.stack.removeWidget(self.dashboard_view)
        self.dashboard_view = DashboardWindow(user, self.translator, main_window=self)
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentWidget(self.dashboard_view)

    def show_module(self, widget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def back_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 