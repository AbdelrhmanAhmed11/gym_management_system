from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QMessageBox, QFrame, QScrollArea, QSpacerItem,
                             QSizePolicy, QGraphicsDropShadowEffect, QApplication, QDesktopWidget)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QIcon, QPalette
from views.clients_view import ClientsView
from views.attendance_view import AttendanceView
from views.finance_view import FinanceView
from views.sessions_view import SessionsView
from views.invitations_view import InvitationsView
from views.loans_view import LoansView
from views.reports_view import ReportsView
from views.user_management_view import UserManagementView
from controllers.reports_controller import ReportsController
from models.client_model import ClientModel
from models.finance_model import FinanceModel
from models.invitation_model import InvitationModel
import sys

class DashboardWindow(QWidget):
    def __init__(self, user, translator, main_window=None):
        super().__init__()
        self.user = user
        self.translator = translator
        self.main_window = main_window
        self.init_ui()
        self.apply_styles()
        self.setup_animations()

    def init_ui(self):
        self.setWindowTitle(self.tr('Gym Management Dashboard'))
        
        # Make window fullscreen and fixed
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        # Get screen dimensions for responsive sizing
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # Main layout - horizontal split
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create main content area
        self.main_content = self.create_main_content()
        main_layout.addWidget(self.main_content)

        self.setLayout(main_layout)

    def create_sidebar(self):
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar")
        sidebar_frame.setFixedWidth(280)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar header
        header_section = self.create_sidebar_header()
        sidebar_layout.addWidget(header_section)

        # Navigation section - this will expand to fill remaining space
        nav_section = self.create_sidebar_navigation()
        sidebar_layout.addWidget(nav_section, 1)  # stretch factor of 1

        sidebar_frame.setLayout(sidebar_layout)
        return sidebar_frame

    def create_sidebar_header(self):
        header_frame = QFrame()
        header_frame.setObjectName("sidebarHeader")
        header_frame.setFixedHeight(200)
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)
        header_layout.setContentsMargins(30, 30, 30, 30)
        
        # Logo
        logo_icon = QLabel("🏋️")
        logo_icon.setObjectName("sidebarLogo")
        logo_icon.setAlignment(Qt.AlignCenter)
        
        # App title
        app_title = QLabel(self.tr('GYM\nMANAGEMENT'))
        app_title.setObjectName("sidebarTitle")
        app_title.setAlignment(Qt.AlignCenter)
        
        # User info
        user_info = QLabel(self.tr(f'{self.user[1]}\n{self.user[2].upper()}'))
        user_info.setObjectName("sidebarUserInfo")
        user_info.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(logo_icon)
        header_layout.addWidget(app_title)
        header_layout.addWidget(user_info)
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_sidebar_navigation(self):
        nav_frame = QFrame()
        nav_frame.setObjectName("sidebarNav")
        
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(8)
        nav_layout.setContentsMargins(20, 30, 20, 30)
        
        # Section title
        nav_title = QLabel(self.tr('QUICK ACTIONS'))
        nav_title.setObjectName("sidebarNavTitle")
        nav_layout.addWidget(nav_title)
        
        nav_layout.addSpacing(20)
        
        # Define navigation buttons
        nav_buttons = [
            ('👥', self.tr('Clients'), self.open_clients),
            ('📋', self.tr('Attendance'), self.open_attendance),
            ('💰', self.tr('Finance'), self.open_finance),
            ('🏃', self.tr('Sessions'), self.open_sessions),
            ('📨', self.tr('Invitations'), self.open_invitations),
            ('💳', self.tr('Loans'), self.open_loans),
            ('📊', self.tr('Reports'), self.open_reports)
        ]
        
        # Add admin button if admin
        if self.user[2] == 'admin':
            nav_buttons.append(('⚙️', self.tr('User Management'), self.open_user_management))
        
        # Create navigation buttons
        for icon, text, callback in nav_buttons:
            button = self.create_sidebar_button(icon, text, callback)
            nav_layout.addWidget(button)
        
        # Add stretch to fill remaining space
        nav_layout.addStretch()
        
        nav_frame.setLayout(nav_layout)
        return nav_frame

    def create_sidebar_button(self, icon, text, callback):
        button = QPushButton()
        button.setObjectName("sidebarButton")
        button.setFixedHeight(55)
        button.clicked.connect(callback)
        button.setText(f"{icon}  {text}")
        return button

    def create_main_content(self):
        content_frame = QFrame()
        content_frame.setObjectName("mainContent")
        
        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setObjectName("contentScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget
        content_widget = QFrame()
        content_widget.setObjectName("contentWidget")
        
        # Main content layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(40, 40, 40, 40)

        # Welcome header
        welcome_section = self.create_welcome_section()
        content_layout.addWidget(welcome_section)

        # Admin stats section (if admin)
        if self.user[2] == 'admin':
            # Warning section for missing payments
            warning_section = self.create_warning_section()
            if warning_section:
                content_layout.addWidget(warning_section)
            
            # Stats section
            stats_section = self.create_stats_section()
            content_layout.addWidget(stats_section)

        # Add stretch to push content to top
        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        # Content frame layout
        content_frame_layout = QVBoxLayout()
        content_frame_layout.addWidget(scroll_area)
        content_frame_layout.setContentsMargins(0, 0, 0, 0)
        content_frame.setLayout(content_frame_layout)

        return content_frame

    def create_welcome_section(self):
        welcome_frame = QFrame()
        welcome_frame.setObjectName("welcomeFrame")
        welcome_frame.setFixedHeight(120)
        
        welcome_layout = QVBoxLayout()
        welcome_layout.setSpacing(10)
        welcome_layout.setContentsMargins(40, 30, 40, 30)
        
        welcome_title = QLabel(self.tr('Dashboard Overview'))
        welcome_title.setObjectName("welcomeTitle")
        
        welcome_subtitle = QLabel(self.tr('Monitor your gym operations and performance'))
        welcome_subtitle.setObjectName("welcomeSubtitle")
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_subtitle)
        welcome_layout.addStretch()
        
        welcome_frame.setLayout(welcome_layout)
        
        # Add shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(0, 5)
        welcome_frame.setGraphicsEffect(shadow_effect)
        
        return welcome_frame

    def create_warning_section(self):
        from models.db_manager import DBManager
        db = DBManager()
        missing_payments = db.fetchone("SELECT COUNT(*) FROM clients WHERE amount_remaining > 0 AND end_date >= DATE('now')")
        
        if missing_payments and missing_payments[0] > 0:
            warning_frame = QFrame()
            warning_frame.setObjectName("warningFrame")
            warning_frame.setFixedHeight(80)
            
            warning_layout = QHBoxLayout()
            warning_layout.setContentsMargins(30, 20, 30, 20)
            
            warning_icon = QLabel("⚠️")
            warning_icon.setObjectName("warningIcon")
            warning_icon.setAlignment(Qt.AlignCenter)
            
            warning_text = QLabel(self.tr(f'Alert: {missing_payments[0]} clients have missing or unmatched payments!'))
            warning_text.setObjectName("warningText")
            
            warning_layout.addWidget(warning_icon)
            warning_layout.addSpacing(15)
            warning_layout.addWidget(warning_text)
            warning_layout.addStretch()
            
            warning_frame.setLayout(warning_layout)
            
            # Add shadow effect
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(15)
            shadow_effect.setColor(QColor(255, 204, 0, 100))
            shadow_effect.setOffset(0, 5)
            warning_frame.setGraphicsEffect(shadow_effect)
            
            return warning_frame
        return None

    def create_stats_section(self):
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(25)
        stats_layout.setContentsMargins(40, 30, 40, 30)
        
        # Section title
        stats_title = QLabel(self.tr('Key Metrics'))
        stats_title.setObjectName("sectionTitle")
        stats_layout.addWidget(stats_title)
        
        # Get stats data
        stats_data = self.get_admin_stats()
        
        # Create stats grid with proper sizing
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)  # Reduced spacing
        
        # First row of stats
        row1_stats = [
            ('👥', self.tr('Total Clients'), str(stats_data['total_clients']), '#e63946'),
            ('✅', self.tr('Active'), str(stats_data['active']), '#38b000'),
            ('❄️', self.tr('Frozen'), str(stats_data['frozen']), '#6c757d'),
            ('⏰', self.tr('Ending Soon'), str(stats_data['ending_soon']), '#ffcc00')
        ]
        
        for i, (icon, label, value, color) in enumerate(row1_stats):
            stat_card = self.create_stat_card(icon, label, value, color)
            stats_grid.addWidget(stat_card, 0, i)
        
        # Second row of stats
        row2_stats = [
            ('💰', self.tr('Total Revenue'), f"${stats_data['revenue']:.2f}", '#38b000'),
            ('📊', self.tr('Invite Conversion'), stats_data['invite_conversion'], '#e63946'),
            ('⚠️', self.tr('Missing Payments'), str(stats_data['missing_payments']), '#c1121f'),
            ('💵', self.tr('Daily Cashier'), f"${stats_data['daily_cashier']:.2f}", '#6c757d')
        ]
        
        for i, (icon, label, value, color) in enumerate(row2_stats):
            stat_card = self.create_stat_card(icon, label, value, color)
            stats_grid.addWidget(stat_card, 1, i)
        
        # Set column stretch to make cards fill the width evenly
        for i in range(4):
            stats_grid.setColumnStretch(i, 1)
        
        stats_layout.addLayout(stats_grid)
        stats_frame.setLayout(stats_layout)
        
        # Add shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(0, 5)
        stats_frame.setGraphicsEffect(shadow_effect)
        
        return stats_frame

    def create_stat_card(self, icon, label, value, color):
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(140)  # Increased minimum height
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"color: {color}; font-size: 26px; font-weight: bold;")
        
        # Label
        label_widget = QLabel(label)
        label_widget.setObjectName("statLabel")
        label_widget.setAlignment(Qt.AlignCenter)
        label_widget.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(label_widget)
        layout.addStretch()
        
        card.setLayout(layout)
        
        # Add shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 60))
        shadow_effect.setOffset(0, 4)
        card.setGraphicsEffect(shadow_effect)
        
        return card

    def get_admin_stats(self):
        """Get admin statistics data"""
        # Total clients
        client_model = ClientModel()
        total_clients = len(client_model.get_all())
        
        # Active/frozen/ending soon
        from models.db_manager import DBManager
        db = DBManager()
        active = db.fetchone("SELECT COUNT(*) FROM clients WHERE end_date >= DATE('now') AND freeze_days = 0")
        frozen = db.fetchone("SELECT COUNT(*) FROM clients WHERE freeze_days > 0")
        ending_soon = db.fetchone("SELECT COUNT(*) FROM clients WHERE end_date BETWEEN DATE('now') AND DATE('now', '+7 day')")
        
        # Revenue
        finance_model = FinanceModel()
        revenue = sum([float(row[3]) for row in finance_model.get_all() if row[2] == 'payment'])
        
        # Invite conversion
        invitation_model = InvitationModel()
        total_invites = len(invitation_model.get_all())
        tagged_invites = len([i for i in invitation_model.get_all() if i[5]])
        invite_conversion = f"{tagged_invites}/{total_invites}" if total_invites else "0/0"
        
        # Missing payment alerts
        missing_payments = db.fetchone("SELECT COUNT(*) FROM clients WHERE amount_remaining > 0 AND end_date >= DATE('now')")
        
        # Daily cashier (sum of today's payments)
        daily_cashier = db.fetchone("SELECT SUM(amount) FROM finances WHERE category='payment' AND DATE(created_at)=DATE('now')")
        
        return {
            'total_clients': total_clients,
            'active': active[0] if active else 0,
            'frozen': frozen[0] if frozen else 0,
            'ending_soon': ending_soon[0] if ending_soon else 0,
            'revenue': revenue,
            'invite_conversion': invite_conversion,
            'missing_payments': missing_payments[0] if missing_payments else 0,
            'daily_cashier': daily_cashier[0] if daily_cashier and daily_cashier[0] else 0
        }

    def apply_styles(self):
        style_sheet = """
            /* Main Window Background */
            QWidget {
                background-color: #2c2c2c;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Sidebar - Full Height */
            QFrame#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a1a, stop:0.3 #2c2c2c, stop:0.7 #1a1a1a, stop:1 #0d0d0d);
                border-right: 3px solid #e63946;
                min-height: 100vh;
            }
            
            /* Sidebar Header */
            QFrame#sidebarHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:0.3 #dc2f3e, stop:0.7 #c1121f, stop:1 #a00e1c);
                border: none;
            }
            
            QLabel#sidebarLogo {
                font-size: 40px;
                color: white;
                font-weight: bold;
                background: transparent;
                text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
            }
            
            QLabel#sidebarTitle {
                color: white;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 2px;
                background: transparent;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
                line-height: 1.2;
            }
            
            QLabel#sidebarUserInfo {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
                background: transparent;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                line-height: 1.3;
            }
            
            /* Sidebar Navigation - Fills remaining space */
            QFrame#sidebarNav {
                background: transparent;
                border: none;
            }
            
            QLabel#sidebarNavTitle {
                color: #cccccc;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 1px;
                background: transparent;
                padding: 0px 10px;
            }
            
            /* Sidebar Buttons - Full Width */
            QPushButton#sidebarButton {
                background-color: rgba(255, 255, 255, 0.05);
                color: #ffffff;
                border: 2px solid transparent;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 500;
                text-align: left;
                padding: 0px 20px;
                margin: 2px 0px;
                min-width: 100%;
            }
            
            QPushButton#sidebarButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                border-color: #ff6b6b;
                color: white;
                font-weight: 600;
            }
            
            QPushButton#sidebarButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c1121f, stop:1 #a00e1c);
            }
            
            /* Main Content Area */
            QFrame#mainContent {
                background-color: #2c2c2c;
                border: none;
            }
            
            /* Content Scroll Area */
            QScrollArea#contentScrollArea {
                border: none;
                background: transparent;
            }
            
            QScrollArea#contentScrollArea QScrollBar:vertical {
                background-color: #404040;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollArea#contentScrollArea QScrollBar::handle:vertical {
                background-color: #e63946;
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollArea#contentScrollArea QScrollBar::handle:vertical:hover {
                background-color: #ff6b6b;
            }
            
            /* Content Widget */
            QFrame#contentWidget {
                background: transparent;
                border: none;
            }
            
            /* Welcome Section */
            QFrame#welcomeFrame {
                background-color: #3a3a3a;
                border-radius: 15px;
                border: 2px solid #4a4a4a;
            }
            
            QLabel#welcomeTitle {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
            
            QLabel#welcomeSubtitle {
                color: #cccccc;
                font-size: 16px;
                font-weight: 400;
                background: transparent;
            }
            
            /* Warning Frame */
            QFrame#warningFrame {
                background-color: #fff3cd;
                border: 2px solid #ffcc00;
                border-radius: 15px;
            }
            
            QLabel#warningIcon {
                font-size: 30px;
                background: transparent;
            }
            
            QLabel#warningText {
                color: #856404;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            /* Stats Frame */
            QFrame#statsFrame {
                background-color: #3a3a3a;
                border-radius: 15px;
                border: 2px solid #4a4a4a;
            }
            
            /* Section Titles */
            QLabel#sectionTitle {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                padding: 0px 0px 10px 0px;
                border-bottom: 3px solid #e63946;
            }
            
            /* Stat Cards - Expanded to fill grid */
            QFrame#statCard {
                background-color: #4a4a4a;
                border: 2px solid #5a5a5a;
                border-radius: 12px;
            }
            
            QFrame#statCard:hover {
                border-color: #e63946;
                background-color: #525252;
            }
            
            QLabel#statIcon {
                font-size: 32px;
                background: transparent;
            }
            
            QLabel#statValue {
                background: transparent;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLabel#statLabel {
                color: #cccccc;
                font-size: 15px;
                font-weight: 500;
                background: transparent;
            }
        """
        self.setStyleSheet(style_sheet)

    def setup_animations(self):
        """Setup animations for interactive elements"""
        pass

    # Navigation methods
    def open_clients(self):
        from views.clients_view import ClientsView
        widget = ClientsView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_attendance(self):
        from views.attendance_view import AttendanceView
        widget = AttendanceView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_finance(self):
        from views.finance_view import FinanceView
        widget = FinanceView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_sessions(self):
        from views.sessions_view import SessionsView
        widget = SessionsView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_invitations(self):
        from views.invitations_view import InvitationsView
        widget = InvitationsView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_loans(self):
        from views.loans_view import LoansView
        widget = LoansView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_reports(self):
        from views.reports_view import ReportsView
        widget = ReportsView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def open_user_management(self):
        from views.user_management_view import UserManagementView
        widget = UserManagementView(self.translator)
        self.add_back_button(widget)
        self.main_window.show_module(widget)

    def add_back_button(self, widget):
        from PyQt5.QtWidgets import QPushButton, QVBoxLayout
        back_btn = QPushButton(self.tr('← Back to Dashboard'))
        back_btn.setObjectName("backButton")
        back_btn.setFixedHeight(50)
        back_btn.setStyleSheet("""
            QPushButton#backButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 0px 20px;
                margin: 10px;
            }
            QPushButton#backButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #343a40);
            }
            QPushButton#backButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #495057, stop:1 #343a40);
            }
        """)
        
        def go_back():
            self.main_window.back_to_dashboard()
        back_btn.clicked.connect(go_back)
        
        layout = widget.layout()
        if layout:
            layout.insertWidget(0, back_btn)

    def tr(self, text):
        # Use the translator if available
        if hasattr(self, 'translator') and self.translator:
            return self.translator.translate(text)
        return text

    def retranslate_ui(self):
        # Example: update window title and any labels/buttons
        self.setWindowTitle(self.tr('Dashboard'))
        # Set layout direction based on language
        if self.translator.get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        # Update all labels, buttons, etc. here using self.tr(...)
        # (You should add similar updates for all UI elements in this view)

# Example usage and testing
if __name__ == '__main__':
    class MockTranslator:
        def set_language(self, lang):
            pass
    
    class MockMainWindow:
        def show_module(self, widget):
            pass
        def back_to_dashboard(self):
            pass
    
    app = QApplication(sys.argv)
    translator = MockTranslator()
    main_window = MockMainWindow()
    user = (1, 'John Doe', 'admin')  # Mock user data
    window = DashboardWindow(user, translator, main_window)
    window.show()
    sys.exit(app.exec_())