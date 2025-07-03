from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QTabWidget, QDateEdit, 
                             QInputDialog, QMessageBox, QSizePolicy, QFrame, QHeaderView, 
                             QGraphicsDropShadowEffect, QSpacerItem)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QColor
from controllers.finance_controller import FinanceController
from models.client_model import ClientModel
from models.finance_model import FinanceModel
from models.db_manager import DBManager
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class FinanceView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = FinanceController()
        self.client_model = ClientModel()
        self.init_ui()
        self.apply_styles()
        self.load_payments()
        self.load_expenses()

    def init_ui(self):
        self.setWindowTitle(self.tr('Finance Management'))
        
        # Main layout with NO margins or spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header section
        header_section = self.create_header_section()
        main_layout.addWidget(header_section)
        
        # Warning section for unmatched payments
        warning_section = self.create_warning_section()
        if warning_section:
            main_layout.addWidget(warning_section)
        
        # Stats section
        stats_section = self.create_stats_section()
        main_layout.addWidget(stats_section)
        
        # Tabs section
        tabs_section = self.create_tabs_section()
        main_layout.addWidget(tabs_section)
        
        self.setLayout(main_layout)

    def create_header_section(self):
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(120)
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(40, 30, 40, 30)
        
        # Title
        title_label = QLabel(self.tr('💰 Finance Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Track payments, expenses, and financial performance'))
        subtitle_label.setObjectName("pageSubtitle")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_warning_section(self):
        db = DBManager()
        unmatched = db.fetchone("SELECT COUNT(*) FROM finances WHERE category='payment' AND (client_id IS NULL OR amount <= 0)")
        
        if unmatched and unmatched[0] > 0:
            warning_frame = QFrame()
            warning_frame.setObjectName("warningFrame")
            warning_frame.setFixedHeight(80)
            
            warning_layout = QHBoxLayout()
            warning_layout.setContentsMargins(40, 20, 40, 20)
            warning_layout.setSpacing(15)
            
            warning_icon = QLabel("⚠️")
            warning_icon.setObjectName("warningIcon")
            warning_icon.setAlignment(Qt.AlignCenter)
            
            warning_text = QLabel(self.tr(f'Alert: {unmatched[0]} unmatched or invalid payments detected!'))
            warning_text.setObjectName("warningText")
            
            warning_layout.addWidget(warning_icon)
            warning_layout.addWidget(warning_text)
            warning_layout.addStretch()
            
            warning_frame.setLayout(warning_layout)
            
            return warning_frame
        return None

    def create_stats_section(self):
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_frame.setFixedHeight(120)
        
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(40, 20, 40, 20)
        stats_layout.setSpacing(15)
        
        # Get financial statistics
        stats = self.get_financial_stats()
        
        # Create stat cards
        stat_cards = [
            ('💵', self.tr('Today\'s Revenue'), f"${stats['today_revenue']:.2f}", '#38b000'),
            ('📊', self.tr('Monthly Revenue'), f"${stats['monthly_revenue']:.2f}", '#e63946'),
            ('💸', self.tr('Today\'s Expenses'), f"${stats['today_expenses']:.2f}", '#dc3545'),
            ('📈', self.tr('Net Profit'), f"${stats['net_profit']:.2f}", '#17a2b8')
        ]
        
        for icon, label, value, color in stat_cards:
            card = self.create_stat_card(icon, label, value, color)
            stats_layout.addWidget(card)
        
        stats_frame.setLayout(stats_layout)
        
        return stats_frame

    def create_stat_card(self, icon, label, value, color):
        """Create stat card with icon and colored title+count centered vertically and horizontally."""
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(80)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignCenter)

        # Icon centered
        icon_label = QLabel(icon)
        icon_label.setObjectName("statIcon")
        icon_label.setAlignment(Qt.AlignCenter)

        # Colored title + count centered
        title_count_label = QLabel(f"{label} ({value})")
        title_count_label.setObjectName("statValue")
        title_count_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        title_count_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_count_label, alignment=Qt.AlignCenter)

        card.setLayout(layout)
        return card

    def create_tabs_section(self):
        tabs_frame = QFrame()
        tabs_frame.setObjectName("tabsFrame")
        
        tabs_layout = QVBoxLayout()
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSpacing(0)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setObjectName("financeTabWidget")
        
        # Payments Tab
        payments_tab = self.create_payments_tab()
        self.tabs.addTab(payments_tab, self.tr('💳 Payments'))
        
        # Expenses Tab
        expenses_tab = self.create_expenses_tab()
        self.tabs.addTab(expenses_tab, self.tr('💸 Expenses'))
        
        tabs_layout.addWidget(self.tabs)
        tabs_frame.setLayout(tabs_layout)
        
        return tabs_frame

    def create_payments_tab(self):
        payments_tab = QWidget()
        payments_tab.setObjectName("paymentsTab")
        
        payments_layout = QVBoxLayout()
        payments_layout.setContentsMargins(0, 0, 0, 0)
        payments_layout.setSpacing(0)
        
        # Controls section
        controls_section = self.create_payments_controls()
        payments_layout.addWidget(controls_section)
        
        # Table section
        table_section = self.create_payments_table()
        payments_layout.addWidget(table_section)
        
        # Actions section
        actions_section = self.create_payments_actions()
        payments_layout.addWidget(actions_section)
        
        payments_tab.setLayout(payments_layout)
        
        return payments_tab

    def create_payments_controls(self):
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_frame.setFixedHeight(100)
        
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(40, 25, 40, 25)
        controls_layout.setSpacing(20)
        
        # Date section
        date_label = QLabel(self.tr('📅 Select Date:'))
        date_label.setObjectName("controlLabel")
        
        self.payments_date = QDateEdit(QDate.currentDate())
        self.payments_date.setObjectName("datePicker")
        self.payments_date.setCalendarPopup(True)
        self.payments_date.setFixedHeight(45)
        self.payments_date.setFixedWidth(180)
        
        self.payments_search_btn = QPushButton(self.tr('🔍 View Payments'))
        self.payments_search_btn.setObjectName("searchButton")
        self.payments_search_btn.setFixedHeight(45)
        self.payments_search_btn.setFixedWidth(160)
        self.payments_search_btn.clicked.connect(self.load_payments)
        
        # Statistics label
        self.payments_stats_label = QLabel(self.tr('Total Payments: $0.00'))
        self.payments_stats_label.setObjectName("statsLabel")
        
        controls_layout.addWidget(date_label)
        controls_layout.addWidget(self.payments_date)
        controls_layout.addWidget(self.payments_search_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.payments_stats_label)
        
        controls_frame.setLayout(controls_layout)
        
        return controls_frame

    def create_payments_table(self):
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(40, 30, 40, 30)
        table_layout.setSpacing(20)
        
        # Table title
        table_title = QLabel(self.tr('Payment Records'))
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Create and style table
        self.payments_table = QTableWidget(0, 4)
        self.payments_table.setObjectName("paymentsTable")
        self.payments_table.setHorizontalHeaderLabels([
            self.tr('Client Code'), 
            self.tr('Client Name'), 
            self.tr('Amount'), 
            self.tr('Description')
        ])
        
        # Configure table
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.payments_table.setAlternatingRowColors(True)
        self.payments_table.setSortingEnabled(True)
        self.payments_table.setMinimumHeight(400)
        
        table_layout.addWidget(self.payments_table)
        table_frame.setLayout(table_layout)
        
        return table_frame

    def create_payments_actions(self):
        actions_frame = QFrame()
        actions_frame.setObjectName("actionsFrame")
        actions_frame.setFixedHeight(100)
        
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(40, 25, 40, 25)
        actions_layout.setSpacing(15)
        
        # Section title
        actions_title = QLabel(self.tr('💳 Payment Actions'))
        actions_title.setObjectName("actionsTitle")
        actions_layout.addWidget(actions_title)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.add_payment_btn = QPushButton(self.tr('➕ Add Payment'))
        self.add_payment_btn.setObjectName("addButton")
        self.add_payment_btn.setFixedHeight(45)
        self.add_payment_btn.setFixedWidth(160)
        self.add_payment_btn.clicked.connect(self.open_add_payment)
        
        buttons_layout.addWidget(self.add_payment_btn)
        buttons_layout.addStretch()
        
        actions_layout.addLayout(buttons_layout)
        actions_frame.setLayout(actions_layout)
        
        return actions_frame

    def create_expenses_tab(self):
        expenses_tab = QWidget()
        expenses_tab.setObjectName("expensesTab")
        
        expenses_layout = QVBoxLayout()
        expenses_layout.setContentsMargins(0, 0, 0, 0)
        expenses_layout.setSpacing(0)
        
        # Controls section
        controls_section = self.create_expenses_controls()
        expenses_layout.addWidget(controls_section)
        
        # Table section
        table_section = self.create_expenses_table()
        expenses_layout.addWidget(table_section)
        
        # Actions section
        actions_section = self.create_expenses_actions()
        expenses_layout.addWidget(actions_section)
        
        expenses_tab.setLayout(expenses_layout)
        
        return expenses_tab

    def create_expenses_controls(self):
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_frame.setFixedHeight(100)
        
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(40, 25, 40, 25)
        controls_layout.setSpacing(20)
        
        # Date section
        date_label = QLabel(self.tr('📅 Select Date:'))
        date_label.setObjectName("controlLabel")
        
        self.expenses_date = QDateEdit(QDate.currentDate())
        self.expenses_date.setObjectName("datePicker")
        self.expenses_date.setCalendarPopup(True)
        self.expenses_date.setFixedHeight(45)
        self.expenses_date.setFixedWidth(180)
        
        self.expenses_search_btn = QPushButton(self.tr('🔍 View Expenses'))
        self.expenses_search_btn.setObjectName("searchButton")
        self.expenses_search_btn.setFixedHeight(45)
        self.expenses_search_btn.setFixedWidth(160)
        self.expenses_search_btn.clicked.connect(self.load_expenses)
        
        # Statistics label
        self.expenses_stats_label = QLabel(self.tr('Total Expenses: $0.00'))
        self.expenses_stats_label.setObjectName("statsLabel")
        
        controls_layout.addWidget(date_label)
        controls_layout.addWidget(self.expenses_date)
        controls_layout.addWidget(self.expenses_search_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.expenses_stats_label)
        
        controls_frame.setLayout(controls_layout)
        
        return controls_frame

    def create_expenses_table(self):
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(40, 30, 40, 30)
        table_layout.setSpacing(20)
        
        # Table title
        table_title = QLabel(self.tr('Expense Records'))
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)
        
        # Create and style table
        self.expenses_table = QTableWidget(0, 4)
        self.expenses_table.setObjectName("expensesTable")
        self.expenses_table.setHorizontalHeaderLabels([
            self.tr('Category'), 
            self.tr('Amount'), 
            self.tr('Description'), 
            self.tr('Date')
        ])
        
        # Configure table
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.expenses_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.expenses_table.setAlternatingRowColors(True)
        self.expenses_table.setSortingEnabled(True)
        self.expenses_table.setMinimumHeight(400)
        
        table_layout.addWidget(self.expenses_table)
        table_frame.setLayout(table_layout)
        
        return table_frame

    def create_expenses_actions(self):
        actions_frame = QFrame()
        actions_frame.setObjectName("actionsFrame")
        actions_frame.setFixedHeight(100)
        
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(40, 25, 40, 25)
        actions_layout.setSpacing(15)
        
        # Section title
        actions_title = QLabel(self.tr('💸 Expense Actions'))
        actions_title.setObjectName("actionsTitle")
        actions_layout.addWidget(actions_title)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.add_expense_btn = QPushButton(self.tr('➕ Add Expense'))
        self.add_expense_btn.setObjectName("addButton")
        self.add_expense_btn.setFixedHeight(45)
        self.add_expense_btn.setFixedWidth(160)
        self.add_expense_btn.clicked.connect(self.open_add_expense)
        
        buttons_layout.addWidget(self.add_expense_btn)
        buttons_layout.addStretch()
        
        actions_layout.addLayout(buttons_layout)
        actions_frame.setLayout(actions_layout)
        
        return actions_frame

    def apply_styles(self):
        style_sheet = """
            /* Main Widget Background - DARK like Dashboard */
            QWidget {
                background-color: #2c2c2c;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Header Frame - DARK seamless */
            QFrame#headerFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QLabel#pageTitle {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
            
            QLabel#pageSubtitle {
                color: #cccccc;
                font-size: 16px;
                font-weight: 400;
                background: transparent;
            }
            
            /* Warning Frame */
            QFrame#warningFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
                border-top: 3px solid #ffcc00;
            }
            
            QLabel#warningIcon {
                font-size: 30px;
                background: transparent;
            }
            
            QLabel#warningText {
                color: #ffcc00;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            /* Stats Frame - DARK seamless */
            QFrame#statsFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QFrame#statCard {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 10px;
            }
            
            QFrame#statCard:hover {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QLabel#statIcon {
                font-size: 20px;
                background: transparent;
            }
            
            QLabel#statValue {
                background: transparent;
            }
            
            QLabel#statLabel {
                color: #cccccc;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
            }
            
            /* Tabs Frame - DARK seamless */
            QFrame#tabsFrame {
                background-color: #2c2c2c;
                border: none;
            }
            
            /* Tab Widget - DARK style */
            QTabWidget#financeTabWidget {
                background-color: #2c2c2c;
                border: none;
            }
            
            QTabWidget#financeTabWidget::pane {
                background-color: #2c2c2c;
                border: none;
            }
            
            QTabWidget#financeTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #404040, stop:1 #353535);
                color: #cccccc;
                padding: 15px 25px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a4a, stop:1 #404040);
                color: #ffffff;
            }
            
            /* Tab Content - DARK seamless */
            QWidget#paymentsTab, QWidget#expensesTab {
                background-color: #2c2c2c;
                border: none;
            }
            
            /* Controls Frame - DARK seamless */
            QFrame#controlsFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            QLabel#controlLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
            
            QLabel#statsLabel {
                color: #e63946;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
            
            /* Date Picker - DARK style */
            QDateEdit#datePicker {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 12px;
            }
            
            QDateEdit#datePicker:focus {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QDateEdit#datePicker::drop-down {
                border: none;
                background-color: #e63946;
                border-radius: 4px;
                width: 30px;
            }
            
            QDateEdit#datePicker::down-arrow {
                image: none;
                border: none;
                width: 0px;
                height: 0px;
            }
            
            /* Search Button */
            QPushButton#searchButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#searchButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #e63946);
            }
            
            QPushButton#searchButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c1121f, stop:1 #a00e1c);
            }
            
            /* Table Frame - DARK seamless */
            QFrame#tableFrame {
                background-color: #2c2c2c;
                border: none;
                border-bottom: 1px solid #404040;
            }
            
            /* Section Titles */
            QLabel#sectionTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                padding: 0px 0px 10px 0px;
                border-bottom: 3px solid #e63946;
            }
            
            /* Tables - DARK style */
            QTableWidget#paymentsTable, QTableWidget#expensesTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                selection-background-color: #e63946;
                selection-color: white;
                font-size: 14px;
            }
            
            QTableWidget#paymentsTable::item, QTableWidget#expensesTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#paymentsTable::item:selected, QTableWidget#expensesTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                padding: 15px 8px;
                border: none;
                border-right: 1px solid #a00e1c;
                font-size: 14px;
                font-weight: bold;
            }
            
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:1 #e63946);
            }
            
            /* Scrollbars - DARK */
            QScrollBar:vertical {
                background-color: #404040;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #e63946;
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #ff6b6b;
            }
            
            /* Actions Frame - DARK seamless */
            QFrame#actionsFrame {
                background-color: #2c2c2c;
                border: none;
                border-top: 2px solid #e63946;
            }
            
            QLabel#actionsTitle {
                color: #e63946;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }
            
            /* Add Buttons */
            QPushButton#addButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38b000, stop:1 #2d8f00);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#addButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4ade80, stop:1 #38b000);
            }
            
            QPushButton#addButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d8f00, stop:1 #1f6b00);
            }
            
            /* Message Boxes - DARK */
            QMessageBox {
                background-color: #2c2c2c;
                color: #ffffff;
            }
            
            QMessageBox QPushButton {
                background-color: #e63946;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #ff6b6b;
            }
            
            /* Input Dialogs - DARK */
            QInputDialog {
                background-color: #2c2c2c;
                color: #ffffff;
            }
            
            QInputDialog QLineEdit {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 6px;
                color: #ffffff;
                padding: 8px;
                font-size: 14px;
            }
            
            QInputDialog QLineEdit:focus {
                border-color: #e63946;
                background-color: #4a4a4a;
            }
            
            QInputDialog QLabel {
                color: #ffffff;
                font-size: 14px;
            }
        """
        self.setStyleSheet(style_sheet)

    def get_financial_stats(self):
        """Get financial statistics"""
        try:
            db = DBManager()
            
            # Today's revenue
            today_revenue = db.fetchone("SELECT SUM(amount) FROM finances WHERE category='payment' AND DATE(created_at)=DATE('now')")
            today_revenue = today_revenue[0] if today_revenue and today_revenue[0] else 0
            
            # Monthly revenue
            monthly_revenue = db.fetchone("SELECT SUM(amount) FROM finances WHERE category='payment' AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')")
            monthly_revenue = monthly_revenue[0] if monthly_revenue and monthly_revenue[0] else 0
            
            # Today's expenses
            today_expenses = db.fetchone("SELECT SUM(amount) FROM finances WHERE category='expense' AND DATE(created_at)=DATE('now')")
            today_expenses = today_expenses[0] if today_expenses and today_expenses[0] else 0
            
            # Net profit (monthly revenue - monthly expenses)
            monthly_expenses = db.fetchone("SELECT SUM(amount) FROM finances WHERE category='expense' AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')")
            monthly_expenses = monthly_expenses[0] if monthly_expenses and monthly_expenses[0] else 0
            net_profit = monthly_revenue - monthly_expenses
            
            return {
                'today_revenue': today_revenue,
                'monthly_revenue': monthly_revenue,
                'today_expenses': today_expenses,
                'net_profit': net_profit
            }
        except:
            return {
                'today_revenue': 0,
                'monthly_revenue': 0,
                'today_expenses': 0,
                'net_profit': 0
            }

    def load_payments(self):
        date = self.payments_date.date().toString('yyyy-MM-dd')
        records = self.controller.get_payments_by_date(date)
        
        self.payments_table.setRowCount(0)
        total_amount = 0
        
        for rec in records:
            _, code, name, amount, desc = rec
            row = self.payments_table.rowCount()
            self.payments_table.insertRow(row)
            
            # Create items with proper formatting
            code_item = QTableWidgetItem(str(code))
            name_item = QTableWidgetItem(str(name))
            amount_item = QTableWidgetItem(f"${float(amount):.2f}")
            desc_item = QTableWidgetItem(str(desc))
            
            # Center align code and amount
            code_item.setTextAlignment(Qt.AlignCenter)
            amount_item.setTextAlignment(Qt.AlignCenter)
            
            self.payments_table.setItem(row, 0, code_item)
            self.payments_table.setItem(row, 1, name_item)
            self.payments_table.setItem(row, 2, amount_item)
            self.payments_table.setItem(row, 3, desc_item)
            
            total_amount += float(amount)
        
        # Update statistics
        self.payments_stats_label.setText(self.tr(f'💰 Total Payments: ${total_amount:.2f}'))

    def load_expenses(self):
        date = self.expenses_date.date().toString('yyyy-MM-dd')
        records = self.controller.get_expenses_by_date(date)
        
        self.expenses_table.setRowCount(0)
        total_amount = 0
        
        for rec in records:
            _, category, amount, desc = rec
            row = self.expenses_table.rowCount()
            self.expenses_table.insertRow(row)
            
            # Create items with proper formatting
            category_item = QTableWidgetItem(str(category))
            amount_item = QTableWidgetItem(f"${float(amount):.2f}")
            desc_item = QTableWidgetItem(str(desc))
            date_item = QTableWidgetItem(date)
            
            # Center align amount and date
            amount_item.setTextAlignment(Qt.AlignCenter)
            date_item.setTextAlignment(Qt.AlignCenter)
            
            self.expenses_table.setItem(row, 0, category_item)
            self.expenses_table.setItem(row, 1, amount_item)
            self.expenses_table.setItem(row, 2, desc_item)
            self.expenses_table.setItem(row, 3, date_item)
            
            total_amount += float(amount)
        
        # Update statistics
        self.expenses_stats_label.setText(self.tr(f'💸 Total Expenses: ${total_amount:.2f}'))

    def open_add_payment(self):
        code, ok = QInputDialog.getText(self, self.tr('Client Code'), self.tr('Enter client code:'))
        if not ok or not code:
            return
        
        client_id = self.get_client_id_by_code(code)
        if not client_id:
            self.show_error_message(self.tr('Client not found. Please verify the client code.'))
            return
        
        amount, ok = QInputDialog.getDouble(self, self.tr('Payment Amount'), self.tr('Enter payment amount:'), 0, 0)
        if not ok:
            return
        
        if amount <= 0:
            self.show_error_message(self.tr('Amount must be positive.'))
            return
        
        desc, ok = QInputDialog.getText(self, self.tr('Description'), self.tr('Enter payment description:'))
        if not ok or not desc:
            self.show_error_message(self.tr('Description is required.'))
            return
        
        try:
            self.controller.add_payment(client_id, amount, desc, 1)  # Assume user_id=1
            self.show_success_message(self.tr('✅ Payment added successfully!'))
            self.load_payments()
        except Exception as e:
            self.show_error_message(str(e))

    def open_add_expense(self):
        category, ok = QInputDialog.getText(self, self.tr('Expense Category'), self.tr('Enter expense category:'))
        if not ok or not category:
            self.show_error_message(self.tr('Category is required.'))
            return
        
        amount, ok = QInputDialog.getDouble(self, self.tr('Expense Amount'), self.tr('Enter expense amount:'), 0, 0)
        if not ok:
            return
        
        if amount <= 0:
            self.show_error_message(self.tr('Amount must be positive.'))
            return
        
        desc, ok = QInputDialog.getText(self, self.tr('Description'), self.tr('Enter expense description:'))
        if not ok or not desc:
            self.show_error_message(self.tr('Description is required.'))
            return
        
        try:
            self.controller.add_expense(category, amount, desc, 1)  # Assume user_id=1
            self.show_success_message(self.tr('✅ Expense added successfully!'))
            self.load_expenses()
        except Exception as e:
            self.show_error_message(str(e))

    def show_success_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(self.tr('Success'))
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(self.tr('Error'))
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def get_client_id_by_code(self, code):
        # Helper to get client id from code
        from models.db_manager import DBManager
        db = DBManager()
        row = db.fetchone('SELECT id FROM clients WHERE client_code=?', (code,))
        return row[0] if row else None

    def tr(self, text):
        """Translation method placeholder"""
        return self.translator.translate(text)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr('Finance Management'))
        # Update header
        if hasattr(self, 'header_frame'):
            title_label = self.header_frame.findChild(QLabel, 'pageTitle')
            if title_label:
                title_label.setText(self.tr('💰 Finance Management'))
            subtitle_label = self.header_frame.findChild(QLabel, 'pageSubtitle')
            if subtitle_label:
                subtitle_label.setText(self.tr('Track payments, expenses, and financial performance'))
        # Update stats section
        if hasattr(self, 'payments_stats_label'):
            amount = ''
            if ':' in self.payments_stats_label.text():
                amount = self.payments_stats_label.text().split(':', 1)[-1]
            self.payments_stats_label.setText(self.tr('Total Payments:') + amount)
        if hasattr(self, 'payments_search_btn'):
            self.payments_search_btn.setText(self.tr('🔍 View Payments'))
        if hasattr(self, 'add_payment_btn'):
            self.add_payment_btn.setText(self.tr('➕ Add Payment'))
        # Update payment records and actions labels if they exist
        for widget in self.findChildren(QLabel, 'sectionTitle'):
            if 'Payment Records' in widget.text() or 'سجلات المدفوعات' in widget.text():
                widget.setText(self.tr('Payment Records'))
        for widget in self.findChildren(QLabel, 'actionsTitle'):
            if 'Payment Actions' in widget.text() or 'إجراءات المدفوعات' in widget.text():
                widget.setText(self.tr('💳 Payment Actions'))
        # Update table headers and scrollbars
        if hasattr(self, 'payments_table'):
            self.payments_table.setHorizontalHeaderLabels([
                self.tr('Client Code'),
                self.tr('Client Name'),
                self.tr('Amount'),
                self.tr('Description')
            ])
            self.payments_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        if hasattr(self, 'expenses_table'):
            self.expenses_table.setHorizontalHeaderLabels([
                self.tr('Category'),
                self.tr('Amount'),
                self.tr('Description'),
                self.tr('Date')
            ])
            self.expenses_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        if self.translator.get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        # Reload dynamic data
        self.reload_data()

    def reload_data(self):
        self.load_payments()
        self.load_expenses()