from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QMessageBox, QFrame, QSpacerItem, 
                             QSizePolicy, QGraphicsDropShadowEffect, QApplication, QDesktopWidget)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QIcon, QPalette
from controllers.auth_controller import AuthController
import sys

class LoginWindow(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.auth = AuthController()
        self.handle_login_success = None
        self.init_ui()
        self.apply_styles()
        self.setup_animations()

    def init_ui(self):
        self.setWindowTitle(self.tr('Gym Management System - Login'))
        
        # Make window fullscreen and fixed
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        # Get screen dimensions for responsive sizing
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        
        # Calculate responsive card width (35% of screen width, min 650px, max 900px)
        card_width = max(650, min(900, int(screen.width() * 0.35)))
        card_height = 650

        # Main background container
        self.main_background = QFrame()
        self.main_background.setObjectName("mainBackground")
        
        # Login card container - responsive width
        self.login_card = QFrame()
        self.login_card.setObjectName("loginCard")
        self.login_card.setFixedSize(card_width, card_height)
        
        # Header section with gradient
        self.header_section = QFrame()
        self.header_section.setObjectName("headerSection")
        self.header_section.setFixedHeight(200)
        
        # Logo and branding
        self.logo_icon = QLabel("🏋️")
        self.logo_icon.setObjectName("logoIcon")
        self.logo_icon.setAlignment(Qt.AlignCenter)
        
        self.app_title = QLabel(self.tr('GYM MANAGEMENT'))
        self.app_title.setObjectName("appTitle")
        self.app_title.setAlignment(Qt.AlignCenter)
        
        self.welcome_text = QLabel(self.tr('Welcome Back'))
        self.welcome_text.setObjectName("welcomeText")
        self.welcome_text.setAlignment(Qt.AlignCenter)

        # Header layout
        header_layout = QVBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(self.logo_icon)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.app_title)
        header_layout.addSpacing(8)
        header_layout.addWidget(self.welcome_text)
        header_layout.addStretch()
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_section.setLayout(header_layout)

        # Form section
        self.form_section = QFrame()
        self.form_section.setObjectName("formSection")

        # Language selector
        self.language_frame = QFrame()
        self.language_frame.setObjectName("languageFrame")
        
        self.lang_label = QLabel(self.tr('Language:'))
        self.lang_label.setObjectName("langLabel")
        
        self.language_combo = QComboBox()
        self.language_combo.setObjectName("languageCombo")
        self.language_combo.addItems(['English', 'العربية'])
        self.language_combo.currentIndexChanged.connect(self.switch_language)
        self.language_combo.setFixedHeight(40)
        self.language_combo.setMinimumWidth(130)

        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        lang_layout.addWidget(self.lang_label)
        lang_layout.addSpacing(10)
        lang_layout.addWidget(self.language_combo)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        self.language_frame.setLayout(lang_layout)

        # Form fields with responsive padding
        form_padding = max(50, int(card_width * 0.08))
        
        self.username_label = QLabel(self.tr('Username'))
        self.username_label.setObjectName("fieldLabel")
        
        self.username_field = QLineEdit()
        self.username_field.setObjectName("inputField")
        self.username_field.setPlaceholderText(self.tr('Enter your username'))
        self.username_field.setFixedHeight(55)

        self.password_label = QLabel(self.tr('Password'))
        self.password_label.setObjectName("fieldLabel")
        
        self.password_field = QLineEdit()
        self.password_field.setObjectName("inputField")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText(self.tr('Enter your password'))
        self.password_field.setFixedHeight(55)

        self.role_label = QLabel(self.tr('Role'))
        self.role_label.setObjectName("fieldLabel")
        
        self.role_combo = QComboBox()
        self.role_combo.setObjectName("roleCombo")
        self.role_combo.addItems([self.tr('Admin'), self.tr('Receptionist')])
        self.role_combo.setFixedHeight(55)

        # Login button
        self.login_button = QPushButton(self.tr('LOGIN'))
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setFixedHeight(60)

        # Form layout with optimized spacing
        form_layout = QVBoxLayout()
        form_layout.addSpacing(25)
        form_layout.addWidget(self.language_frame)
        form_layout.addSpacing(30)
        
        form_layout.addWidget(self.username_label)
        form_layout.addSpacing(8)
        form_layout.addWidget(self.username_field)
        form_layout.addSpacing(20)
        
        form_layout.addWidget(self.password_label)
        form_layout.addSpacing(8)
        form_layout.addWidget(self.password_field)
        form_layout.addSpacing(20)
        
        form_layout.addWidget(self.role_label)
        form_layout.addSpacing(8)
        form_layout.addWidget(self.role_combo)
        form_layout.addSpacing(35)
        
        form_layout.addWidget(self.login_button)
        form_layout.addSpacing(25)
        form_layout.setContentsMargins(form_padding, 0, form_padding, 0)
        self.form_section.setLayout(form_layout)

        # Login card layout
        card_layout = QVBoxLayout()
        card_layout.addWidget(self.header_section)
        card_layout.addWidget(self.form_section)
        card_layout.setSpacing(0)
        card_layout.setContentsMargins(0, 0, 0, 0)
        self.login_card.setLayout(card_layout)

        # Center the login card in the main background
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        
        # Horizontal centering
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.login_card)
        h_layout.addStretch()
        
        main_layout.addLayout(h_layout)
        main_layout.addStretch()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_background.setLayout(main_layout)

        # Window layout
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.main_background)
        window_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(window_layout)

        # Add enhanced shadow effect to login card
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(40)
        shadow_effect.setColor(QColor(0, 0, 0, 120))
        shadow_effect.setOffset(0, 15)
        self.login_card.setGraphicsEffect(shadow_effect)

    def apply_styles(self):
        style_sheet = """
            /* Main Background - Dark like Dashboard */
            QFrame#mainBackground {
                background-color: #1a1a1a;
            }
            
            /* Login Card */
            QFrame#loginCard {
                background-color: #2a2a2a;
                border-radius: 30px;
                border: 2px solid #3a3a3a;
            }
            
            /* Header Section */
            QFrame#headerSection {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:0.3 #dc2f3e, stop:0.7 #c1121f, stop:1 #a00e1c);
                border-radius: 30px 30px 0px 0px;
                border: none;
            }
            
            /* Logo Icon */
            QLabel#logoIcon {
                font-size: 60px;
                color: white;
                font-weight: bold;
                background: transparent;
                text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
            }
            
            /* App Title */
            QLabel#appTitle {
                color: white;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 4px;
                background: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
            }
            
            /* Welcome Text */
            QLabel#welcomeText {
                color: rgba(255, 255, 255, 0.95);
                font-size: 17px;
                font-weight: 500;
                background: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            }
            
            /* Form Section */
            QFrame#formSection {
                background-color: #2a2a2a;
                border-radius: 0px 0px 30px 30px;
                border: none;
            }
            
            /* Language Frame */
            QFrame#languageFrame {
                background-color: transparent;
                border: none;
            }
            
            /* Field Labels */
            QLabel#fieldLabel {
                color: #ffffff;
                font-size: 17px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                margin: 0px;
                padding: 0px;
            }
            
            QLabel#langLabel {
                color: #cccccc;
                font-size: 15px;
                font-weight: 500;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
            }
            
            /* Input Fields */
            QLineEdit#inputField {
                background-color: #3a3a3a;
                border: 2px solid #4a4a4a;
                border-radius: 15px;
                padding: 0px 20px;
                font-size: 16px;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                selection-background-color: #e63946;
            }
            
            QLineEdit#inputField:focus {
                border-color: #e63946;
                background-color: #424242;
                outline: none;
                box-shadow: 0 0 12px rgba(230, 57, 70, 0.2);
            }
            
            QLineEdit#inputField:hover {
                border-color: #ff6b6b;
                background-color: #424242;
            }
            
            QLineEdit#inputField::placeholder {
                color: #999999;
            }
            
            /* Role Combo Box */
            QComboBox#roleCombo {
                background-color: #3a3a3a;
                border: 2px solid #4a4a4a;
                border-radius: 15px;
                padding: 0px 20px;
                font-size: 16px;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QComboBox#roleCombo:focus {
                border-color: #e63946;
                background-color: #424242;
                box-shadow: 0 0 12px rgba(230, 57, 70, 0.2);
            }
            
            QComboBox#roleCombo:hover {
                border-color: #ff6b6b;
                background-color: #424242;
            }
            
            QComboBox#roleCombo::drop-down {
                border: none;
                width: 40px;
                background: transparent;
            }
            
            QComboBox#roleCombo::down-arrow {
                image: none;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid #cccccc;
                margin-right: 15px;
            }
            
            QComboBox#roleCombo QAbstractItemView {
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
            
            /* Language Combo Box */
            QComboBox#languageCombo {
                background-color: #3a3a3a;
                border: 2px solid #4a4a4a;
                border-radius: 10px;
                padding: 0px 15px;
                font-size: 14px;
                color: #cccccc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QComboBox#languageCombo:hover {
                border-color: #e63946;
                color: #ffffff;
                background-color: #424242;
            }
            
            QComboBox#languageCombo::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox#languageCombo::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #cccccc;
                margin-right: 10px;
            }
            
            QComboBox#languageCombo QAbstractItemView {
                background-color: #3a3a3a;
                border: 2px solid #e63946;
                border-radius: 8px;
                selection-background-color: #e63946;
                selection-color: white;
                color: #ffffff;
                font-size: 14px;
                padding: 6px;
            }
            
            /* Login Button */
            QPushButton#loginButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:0.3 #dc2f3e, stop:0.7 #c1121f, stop:1 #a00e1c);
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 3px;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
            }
            
            QPushButton#loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:0.3 #e63946, stop:0.7 #dc2f3e, stop:1 #c1121f);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(230, 57, 70, 0.3);
            }
            
            QPushButton#loginButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c1121f, stop:0.3 #a00e1c, stop:0.7 #8b0000, stop:1 #660000);
                transform: translateY(1px);
            }
            
            QPushButton#loginButton:disabled {
                background-color: #6c757d;
                color: #f1f1f1;
                transform: none;
                box-shadow: none;
            }
        """
        self.setStyleSheet(style_sheet)

    def setup_animations(self):
        # Button animation setup
        self.button_animation = QPropertyAnimation(self.login_button, b"geometry")
        self.button_animation.setDuration(200)
        self.button_animation.setEasingCurve(QEasingCurve.OutCubic)

    def switch_language(self, index):
        language = 'en' if index == 0 else 'ar'
        self.translator.set_language(language)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr('Gym Management System - Login'))
        self.app_title.setText(self.tr('GYM MANAGEMENT'))
        self.welcome_text.setText(self.tr('Welcome Back'))
        self.username_label.setText(self.tr('Username'))
        self.username_field.setPlaceholderText(self.tr('Enter your username'))
        self.password_label.setText(self.tr('Password'))
        self.password_field.setPlaceholderText(self.tr('Enter your password'))
        self.role_label.setText(self.tr('Role'))
        self.login_button.setText(self.tr('LOGIN'))
        self.lang_label.setText(self.tr('Language:'))
        
        # Update role combo items
        current_role_index = self.role_combo.currentIndex()
        self.role_combo.clear()
        self.role_combo.addItems([self.tr('Admin'), self.tr('Receptionist')])
        self.role_combo.setCurrentIndex(current_role_index)

    def handle_login(self):
        username = self.username_field.text().strip()
        password = self.password_field.text().strip()
        role = self.role_combo.currentText().lower()

        # Validate input
        if not username or not password:
            self.show_custom_message('error', self.tr('Input Error'), 
                                   self.tr('Please enter both username and password.'))
            return

        # Show loading state
        self.login_button.setText(self.tr('LOGGING IN...'))
        self.login_button.setEnabled(False)

        try:
            user = self.auth.login(username, password, role)
            if user:
                self.show_custom_message('success', self.tr('Login Successful'), 
                                       self.tr('Welcome! Login successful.'))
                if self.handle_login_success:
                    self.handle_login_success(user)
            else:
                self.show_custom_message('error', self.tr('Login Failed'), 
                                       self.tr('Invalid credentials or role. Please try again.'))
        except Exception as e:
            self.show_custom_message('error', self.tr('System Error'), 
                                   self.tr(f'An error occurred: {str(e)}'))
        finally:
            self.login_button.setText(self.tr('LOGIN'))
            self.login_button.setEnabled(True)

    def show_custom_message(self, message_type, title, message):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        if message_type == 'error':
            message_box.setIcon(QMessageBox.Critical)
            message_box.setStyleSheet("""
                QMessageBox {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 16px;
                }
                QMessageBox QPushButton {
                    background-color: #c1121f;
                    color: white;
                    border: none;
                    padding: 15px 35px;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 16px;
                    min-width: 100px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #e63946;
                }
            """)
        elif message_type == 'success':
            message_box.setIcon(QMessageBox.Information)
            message_box.setStyleSheet("""
                QMessageBox {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 16px;
                }
                QMessageBox QPushButton {
                    background-color: #38b000;
                    color: white;
                    border: none;
                    padding: 15px 35px;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 16px;
                    min-width: 100px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #2d8f00;
                }
            """)
        
        message_box.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.handle_login()
        elif event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def tr(self, text):
        # Use the translator if available
        if hasattr(self, 'translator') and self.translator:
            return self.translator.translate(text)
        return text

# Example usage and testing
if __name__ == '__main__':
    class MockTranslator:
        def set_language(self, lang):
            pass
    
    app = QApplication(sys.argv)
    translator = MockTranslator()
    window = LoginWindow(translator)
    window.show()
    sys.exit(app.exec_())