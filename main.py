from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QComboBox, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
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

        # Add language selector at the top right
        self.language_selector = QComboBox()
        self.language_selector.addItems(['English', 'Arabic'])
        self.language_selector.setCurrentIndex(0)
        self.language_selector.currentIndexChanged.connect(self.change_language)
        # Style the language selector to match the login page
        self.language_selector.setFixedHeight(40)
        self.language_selector.setStyleSheet('''
            QComboBox {
                background-color: #3a3a3a;
                border: 2px solid #4a4a4a;
                border-radius: 15px;
                padding: 0px 20px;
                font-size: 16px;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #e63946;
                background-color: #424242;
                box-shadow: 0 0 12px rgba(230, 57, 70, 0.2);
            }
            QComboBox:hover {
                border-color: #ff6b6b;
                background-color: #424242;
            }
            QComboBox::drop-down {
                border: none;
                width: 40px;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid #cccccc;
                margin-right: 15px;
            }
            QComboBox QAbstractItemView {
                background-color: #3a3a3a;
                border: 2px solid #e63946;
                border-radius: 12px;
                selection-background-color: #e63946;
                selection-color: white;
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
                outline: none;
            }
        ''')
        # Place the selector in a QWidget and set as menu bar
        top_bar = QWidget()
        top_layout = QHBoxLayout()
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(self.language_selector)
        top_bar.setLayout(top_layout)
        self.setMenuWidget(top_bar)

    def change_language(self, index):
        lang_code = 'en' if index == 0 else 'ar'
        self.translator.set_language(lang_code)
        # Retranslate all widgets in the stack
        for i in range(self.stack.count()):
            widget = self.stack.widget(i)
            if hasattr(widget, 'retranslate_ui'):
                widget.retranslate_ui()
        # Also update dashboard if it exists
        if self.dashboard_view and hasattr(self.dashboard_view, 'retranslate_ui'):
            self.dashboard_view.retranslate_ui()

    def show_dashboard(self, user):
        if self.dashboard_view:
            self.stack.removeWidget(self.dashboard_view)
        self.dashboard_view = DashboardWindow(user, self.translator, main_window=self)
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentWidget(self.dashboard_view)
        # Ensure language and layout direction are applied
        if hasattr(self.dashboard_view, 'retranslate_ui'):
            self.dashboard_view.retranslate_ui()

    def show_module(self, widget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)
        # Ensure language and layout direction are applied
        if hasattr(widget, 'retranslate_ui'):
            widget.retranslate_ui()

    def back_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 