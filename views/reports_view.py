from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, 
                             QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy,
                             QFrame, QHeaderView, QComboBox, QTabWidget, QDateEdit, QFileDialog,
                             QSpacerItem, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QColor, QFont, QPalette
from controllers.reports_controller import ReportsController
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta

class ReportsView(QWidget):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.controller = ReportsController()
        self.init_ui()
        self.apply_styles()
        self.load_all_reports()

    def init_ui(self):
        self.setWindowTitle(self.tr('Reports Management'))
        
        # Main layout with NO margins or spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header section
        header_section = self.create_header_section()
        main_layout.addWidget(header_section)

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
        header_layout.setContentsMargins(40, 30, 40, 30)
        header_layout.setSpacing(10)
        
        # Title
        title_label = QLabel(self.tr('📊 Reports Management'))
        title_label.setObjectName("pageTitle")
        
        # Subtitle
        subtitle_label = QLabel(self.tr('Generate comprehensive reports, track analytics, and export business insights'))
        subtitle_label.setObjectName("pageSubtitle")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addStretch()
        
        header_frame.setLayout(header_layout)
        
        return header_frame

    def create_stats_section(self):
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_frame.setFixedHeight(120)
        
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(40, 20, 40, 20)
        stats_layout.setSpacing(15)
        
        # Get report statistics
        stats = self.get_report_stats()
        
        # Create stat cards
        stat_cards = [
            ('📈', self.tr('Registered Today'), str(stats['registered']), '#e63946'),
            ('💰', self.tr('Payments Today'), str(stats['payments']), '#38b000'),
            ('👥', self.tr('Attendance Today'), str(stats['attendance']), '#17a2b8'),
            ('📋', self.tr('Total Reports'), str(stats['total_reports']), '#ffcc00')
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
        title_count_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        title_count_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_count_label, alignment=Qt.AlignCenter)

        card.setLayout(layout)
        return card

    def create_tabs_section(self):
        tabs_frame = QFrame()
        tabs_frame.setObjectName("tabsFrame")
        
        tabs_layout = QVBoxLayout()
        tabs_layout.setContentsMargins(40, 30, 40, 30)
        tabs_layout.setSpacing(20)
        
        # Tabs title
        tabs_title = QLabel(self.tr('📋 Report Categories'))
        tabs_title.setObjectName("sectionTitle")
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setObjectName("reportTabs")
        
        # Registered Today Tab
        reg_tab = self.create_registered_tab()
        self.tabs.addTab(reg_tab, self.tr('📝 Registered Today'))
        
        # Paid Today Tab
        paid_tab = self.create_paid_tab()
        self.tabs.addTab(paid_tab, self.tr('💳 Paid Today'))
        
        # Attended Today Tab
        att_tab = self.create_attended_tab()
        self.tabs.addTab(att_tab, self.tr('🏃 Attended Today'))
        
        # Monthly Financials Tab
        fin_tab = self.create_financials_tab()
        self.tabs.addTab(fin_tab, self.tr('💰 Monthly Financials'))
        
        # Missing Payments Tab
        miss_tab = self.create_missing_tab()
        self.tabs.addTab(miss_tab, self.tr('⚠️ Missing Payments'))
        
        tabs_layout.addWidget(tabs_title)
        tabs_layout.addWidget(self.tabs)
        
        tabs_frame.setLayout(tabs_layout)
        
        return tabs_frame

    def create_registered_tab(self):
        tab = QWidget()
        tab.setObjectName("reportTab")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Table
        self.reg_table = QTableWidget(0, 5)
        self.reg_table.setObjectName("reportTable")
        self.reg_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Phone'), 
            self.tr('Subscription'), self.tr('Start Date')
        ])
        
        # Configure table
        header = self.reg_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumHeight(45)
        
        self.reg_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.reg_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.reg_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.reg_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.reg_table.setAlternatingRowColors(True)
        self.reg_table.setMinimumHeight(400)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(15)
        
        self.reg_export_pdf = QPushButton(self.tr('📄 Export PDF'))
        self.reg_export_pdf.setObjectName("exportButton")
        self.reg_export_pdf.setFixedHeight(45)
        self.reg_export_pdf.setFixedWidth(140)
        self.reg_export_pdf.clicked.connect(self.export_reg_pdf)
        
        self.reg_export_excel = QPushButton(self.tr('📊 Export Excel'))
        self.reg_export_excel.setObjectName("addButton")
        self.reg_export_excel.setFixedHeight(45)
        self.reg_export_excel.setFixedWidth(140)
        self.reg_export_excel.clicked.connect(self.export_reg_excel)
        
        export_layout.addWidget(self.reg_export_pdf)
        export_layout.addWidget(self.reg_export_excel)
        export_layout.addStretch()
        
        layout.addWidget(self.reg_table)
        layout.addLayout(export_layout)
        
        tab.setLayout(layout)
        return tab

    def create_paid_tab(self):
        tab = QWidget()
        tab.setObjectName("reportTab")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Table
        self.paid_table = QTableWidget(0, 4)
        self.paid_table.setObjectName("reportTable")
        self.paid_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Amount'), self.tr('Description')
        ])
        
        # Configure table
        header = self.paid_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumHeight(45)
        
        self.paid_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.paid_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.paid_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.paid_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.paid_table.setAlternatingRowColors(True)
        self.paid_table.setMinimumHeight(400)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(15)
        
        self.paid_export_pdf = QPushButton(self.tr('📄 Export PDF'))
        self.paid_export_pdf.setObjectName("exportButton")
        self.paid_export_pdf.setFixedHeight(45)
        self.paid_export_pdf.setFixedWidth(140)
        self.paid_export_pdf.clicked.connect(self.export_paid_pdf)
        
        self.paid_export_excel = QPushButton(self.tr('📊 Export Excel'))
        self.paid_export_excel.setObjectName("addButton")
        self.paid_export_excel.setFixedHeight(45)
        self.paid_export_excel.setFixedWidth(140)
        self.paid_export_excel.clicked.connect(self.export_paid_excel)
        
        export_layout.addWidget(self.paid_export_pdf)
        export_layout.addWidget(self.paid_export_excel)
        export_layout.addStretch()
        
        layout.addWidget(self.paid_table)
        layout.addLayout(export_layout)
        
        tab.setLayout(layout)
        return tab

    def create_attended_tab(self):
        tab = QWidget()
        tab.setObjectName("reportTab")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Table
        self.att_table = QTableWidget(0, 3)
        self.att_table.setObjectName("reportTable")
        self.att_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Check-in Time')
        ])
        
        # Configure table
        header = self.att_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumHeight(45)
        
        self.att_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.att_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.att_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.att_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.att_table.setAlternatingRowColors(True)
        self.att_table.setMinimumHeight(400)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(15)
        
        self.att_export_pdf = QPushButton(self.tr('📄 Export PDF'))
        self.att_export_pdf.setObjectName("exportButton")
        self.att_export_pdf.setFixedHeight(45)
        self.att_export_pdf.setFixedWidth(140)
        self.att_export_pdf.clicked.connect(self.export_att_pdf)
        
        self.att_export_excel = QPushButton(self.tr('📊 Export Excel'))
        self.att_export_excel.setObjectName("addButton")
        self.att_export_excel.setFixedHeight(45)
        self.att_export_excel.setFixedWidth(140)
        self.att_export_excel.clicked.connect(self.export_att_excel)
        
        export_layout.addWidget(self.att_export_pdf)
        export_layout.addWidget(self.att_export_excel)
        export_layout.addStretch()
        
        layout.addWidget(self.att_table)
        layout.addLayout(export_layout)
        
        tab.setLayout(layout)
        return tab

    def create_financials_tab(self):
        tab = QWidget()
        tab.setObjectName("reportTab")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Table
        self.fin_table = QTableWidget(0, 5)
        self.fin_table.setObjectName("reportTable")
        self.fin_table.setHorizontalHeaderLabels([
            self.tr('Date'), self.tr('Category'), self.tr('Amount'), 
            self.tr('Description'), self.tr('User')
        ])
        
        # Configure table
        header = self.fin_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumHeight(45)
        
        self.fin_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.fin_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.fin_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.fin_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.fin_table.setAlternatingRowColors(True)
        self.fin_table.setMinimumHeight(400)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(15)
        
        self.fin_export_pdf = QPushButton(self.tr('📄 Export PDF'))
        self.fin_export_pdf.setObjectName("exportButton")
        self.fin_export_pdf.setFixedHeight(45)
        self.fin_export_pdf.setFixedWidth(140)
        self.fin_export_pdf.clicked.connect(self.export_fin_pdf)
        
        self.fin_export_excel = QPushButton(self.tr('📊 Export Excel'))
        self.fin_export_excel.setObjectName("addButton")
        self.fin_export_excel.setFixedHeight(45)
        self.fin_export_excel.setFixedWidth(140)
        self.fin_export_excel.clicked.connect(self.export_fin_excel)
        
        export_layout.addWidget(self.fin_export_pdf)
        export_layout.addWidget(self.fin_export_excel)
        export_layout.addStretch()
        
        layout.addWidget(self.fin_table)
        layout.addLayout(export_layout)
        
        tab.setLayout(layout)
        return tab

    def create_missing_tab(self):
        tab = QWidget()
        tab.setObjectName("reportTab")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Table
        self.miss_table = QTableWidget(0, 5)
        self.miss_table.setObjectName("reportTable")
        self.miss_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Phone'), 
            self.tr('Amount Remaining'), self.tr('End Date')
        ])
        
        # Configure table
        header = self.miss_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumHeight(45)
        
        self.miss_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.miss_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.miss_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.miss_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.miss_table.setAlternatingRowColors(True)
        self.miss_table.setMinimumHeight(400)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(15)
        
        self.miss_export_pdf = QPushButton(self.tr('📄 Export PDF'))
        self.miss_export_pdf.setObjectName("exportButton")
        self.miss_export_pdf.setFixedHeight(45)
        self.miss_export_pdf.setFixedWidth(140)
        self.miss_export_pdf.clicked.connect(self.export_miss_pdf)
        
        self.miss_export_excel = QPushButton(self.tr('📊 Export Excel'))
        self.miss_export_excel.setObjectName("addButton")
        self.miss_export_excel.setFixedHeight(45)
        self.miss_export_excel.setFixedWidth(140)
        self.miss_export_excel.clicked.connect(self.export_miss_excel)
        
        export_layout.addWidget(self.miss_export_pdf)
        export_layout.addWidget(self.miss_export_excel)
        export_layout.addStretch()
        
        layout.addWidget(self.miss_table)
        layout.addLayout(export_layout)
        
        tab.setLayout(layout)
        return tab

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
            
            /* Section Titles */
            QLabel#sectionTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                padding: 0px 0px 10px 0px;
                border-bottom: 3px solid #e63946;
            }
            
            /* Tab Widget Styling - DARK */
            QTabWidget#reportTabs {
                background-color: #2c2c2c;
                border: none;
            }
            
            QTabWidget#reportTabs::pane {
                background-color: #404040;
                border: 2px solid #505050;
                border-radius: 8px;
                margin-top: 5px;
            }
            
            QTabWidget#reportTabs::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #505050, stop:1 #404040);
                color: #cccccc;
                padding: 12px 20px;
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
                    stop:0 #5a5a5a, stop:1 #4a4a4a);
                color: #ffffff;
            }
            
            /* Report Tab Content */
            QWidget#reportTab {
                background-color: #404040;
                border-radius: 8px;
            }
            
            /* Table Styling - DARK */
            QTableWidget#reportTable {
                background-color: #404040;
                alternate-background-color: #4a4a4a;
                border: none;
                gridline-color: #505050;
                font-size: 13px;
                selection-background-color: #e63946;
                selection-color: white;
                border-radius: 8px;
            }
            
            QTableWidget#reportTable::item {
                padding: 12px 8px;
                border-bottom: 1px solid #505050;
            }
            
            QTableWidget#reportTable::item:selected {
                background-color: #e63946;
                color: white;
            }
            
            QTableWidget#reportTable::item:hover {
                background-color: #4a4a4a;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #c1121f);
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #a00e1c;
                font-weight: bold;
                font-size: 14px;
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
            
            /* Export Buttons */
            QPushButton#addButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #38b000, stop:1 #2d8000);
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
            
            QPushButton#exportButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #0f7b8a);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 15px;
            }
            
            QPushButton#exportButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a9c4, stop:1 #17a2b8);
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
        """
        self.setStyleSheet(style_sheet)

    def get_report_stats(self):
        """Get report statistics"""
        try:
            registered = len(self.controller.get_registered_today())
            payments = len(self.controller.get_paid_today())
            attendance = len(self.controller.get_attended_today())
            total_reports = 5  # Number of report types
            
            return {
                'registered': registered,
                'payments': payments,
                'attendance': attendance,
                'total_reports': total_reports
            }
        except:
            return {'registered': 0, 'payments': 0, 'attendance': 0, 'total_reports': 5}

    def load_all_reports(self):
        """Load all report data"""
        self.load_registered_today()
        self.load_paid_today()
        self.load_attended_today()
        self.load_monthly_financials()
        self.load_missing_payments()

    def load_registered_today(self):
        """Load registered today data"""
        data = self.controller.get_registered_today()
        self.reg_table.setRowCount(0)
        
        for row in data:
            # id, client_code, name, phone, ..., subscription_type, start_date, ...
            row_idx = self.reg_table.rowCount()
            self.reg_table.insertRow(row_idx)
            
            items = [
                QTableWidgetItem(str(row[1])),  # client_code
                QTableWidgetItem(str(row[2])),  # name
                QTableWidgetItem(str(row[3])),  # phone
                QTableWidgetItem(str(row[5])),  # subscription_type
                QTableWidgetItem(str(row[7]))   # start_date
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.reg_table.setItem(row_idx, col, item)
            
            self.reg_table.setRowHeight(row_idx, 50)

    def load_paid_today(self):
        """Load paid today data"""
        data = self.controller.get_paid_today()
        self.paid_table.setRowCount(0)
        
        for row in data:
            # id, client_id, category, amount, description, created_at, recorded_by
            row_idx = self.paid_table.rowCount()
            self.paid_table.insertRow(row_idx)
            
            # Get client code/name
            from models.db_manager import DBManager
            db = DBManager()
            client_code = db.fetchone('SELECT client_code FROM clients WHERE id=?', (row[1],))
            client_name = db.fetchone('SELECT name FROM clients WHERE id=?', (row[1],))
            
            items = [
                QTableWidgetItem(str(client_code[0]) if client_code else ''),
                QTableWidgetItem(str(client_name[0]) if client_name else ''),
                QTableWidgetItem(f"${row[3]:.2f}"),  # amount
                QTableWidgetItem(str(row[4]))        # description
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.paid_table.setItem(row_idx, col, item)
            
            self.paid_table.setRowHeight(row_idx, 50)

    def load_attended_today(self):
        """Load attended today data"""
        data = self.controller.get_attended_today()
        self.att_table.setRowCount(0)
        
        for row in data:
            # id, client_id, checkin_time, ...
            row_idx = self.att_table.rowCount()
            self.att_table.insertRow(row_idx)
            
            from models.db_manager import DBManager
            db = DBManager()
            client_code = db.fetchone('SELECT client_code FROM clients WHERE id=?', (row[1],))
            client_name = db.fetchone('SELECT name FROM clients WHERE id=?', (row[1],))
            
            items = [
                QTableWidgetItem(str(client_code[0]) if client_code else ''),
                QTableWidgetItem(str(client_name[0]) if client_name else ''),
                QTableWidgetItem(str(row[2]))  # checkin_time
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.att_table.setItem(row_idx, col, item)
            
            self.att_table.setRowHeight(row_idx, 50)

    def load_monthly_financials(self):
        """Load monthly financials data"""
        from datetime import datetime
        month = datetime.now().strftime('%Y-%m')
        data = self.controller.get_monthly_financials(month)
        self.fin_table.setRowCount(0)
        
        for row in data:
            # id, client_id, category, amount, description, created_at, recorded_by
            row_idx = self.fin_table.rowCount()
            self.fin_table.insertRow(row_idx)
            
            items = [
                QTableWidgetItem(str(row[5])),        # created_at
                QTableWidgetItem(str(row[2])),        # category
                QTableWidgetItem(f"${row[3]:.2f}"),   # amount
                QTableWidgetItem(str(row[4])),        # description
                QTableWidgetItem(str(row[6]))         # recorded_by
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.fin_table.setItem(row_idx, col, item)
            
            self.fin_table.setRowHeight(row_idx, 50)

    def load_missing_payments(self):
        """Load missing payments data"""
        data = self.controller.get_missing_payments()
        self.miss_table.setRowCount(0)
        
        for row in data:
            # id, client_code, name, phone, ..., amount_remaining, end_date
            row_idx = self.miss_table.rowCount()
            self.miss_table.insertRow(row_idx)
            
            items = [
                QTableWidgetItem(str(row[1])),         # client_code
                QTableWidgetItem(str(row[2])),         # name
                QTableWidgetItem(str(row[3])),         # phone
                QTableWidgetItem(f"${row[10]:.2f}"),   # amount_remaining
                QTableWidgetItem(str(row[8]))          # end_date
            ]
            
            for col, item in enumerate(items):
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.miss_table.setItem(row_idx, col, item)
            
            self.miss_table.setRowHeight(row_idx, 50)

    def export_reg_pdf(self):
        """Export registered today report as PDF"""
        self._export_table_pdf(self.reg_table, 'Registered Today Report')

    def export_reg_excel(self):
        """Export registered today report as Excel"""
        self._export_table_excel(self.reg_table, 'registered_today')

    def export_paid_pdf(self):
        """Export paid today report as PDF"""
        self._export_table_pdf(self.paid_table, 'Paid Today Report')

    def export_paid_excel(self):
        """Export paid today report as Excel"""
        self._export_table_excel(self.paid_table, 'paid_today')

    def export_att_pdf(self):
        """Export attended today report as PDF"""
        self._export_table_pdf(self.att_table, 'Attended Today Report')

    def export_att_excel(self):
        """Export attended today report as Excel"""
        self._export_table_excel(self.att_table, 'attended_today')

    def export_fin_pdf(self):
        """Export monthly financials report as PDF"""
        self._export_table_pdf(self.fin_table, 'Monthly Financials Report')

    def export_fin_excel(self):
        """Export monthly financials report as Excel"""
        self._export_table_excel(self.fin_table, 'monthly_financials')

    def export_miss_pdf(self):
        """Export missing payments report as PDF"""
        self._export_table_pdf(self.miss_table, 'Missing Payments Report')

    def export_miss_excel(self):
        """Export missing payments report as Excel"""
        self._export_table_excel(self.miss_table, 'missing_payments')

    def _export_table_pdf(self, table, title):
        """Export table data as PDF"""
        path, _ = QFileDialog.getSaveFileName(
            self, 
            self.tr('Export PDF'), 
            f'{title.lower().replace(" ", "_")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            'PDF Files (*.pdf)'
        )
        if not path:
            return
        
        try:
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            
            # Title
            c.setFont('Helvetica-Bold', 16)
            c.drawString(30, height - 40, title)
            c.drawString(30, height - 60, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
            # Headers
            c.setFont('Helvetica-Bold', 12)
            y = height - 100
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            header_text = ' | '.join(headers)
            c.drawString(30, y, header_text)
            
            # Data
            c.setFont('Helvetica', 10)
            y -= 25
            for row in range(table.rowCount()):
                row_data = [table.item(row, col).text() if table.item(row, col) else '' 
                           for col in range(table.columnCount())]
                row_text = ' | '.join(row_data)
                c.drawString(30, y, row_text)
                y -= 20
                
                if y < 50:
                    c.showPage()
                    y = height - 50
            
            c.save()
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ PDF exported successfully!'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error exporting PDF: {str(e)}'))

    def _export_table_excel(self, table, filename_prefix):
        """Export table data as Excel"""
        path, _ = QFileDialog.getSaveFileName(
            self, 
            self.tr('Export Excel'), 
            f'{filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            'Excel Files (*.xlsx)'
        )
        if not path:
            return
        
        try:
            data = []
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            
            for row in range(table.rowCount()):
                row_data = [table.item(row, col).text() if table.item(row, col) else '' 
                           for col in range(table.columnCount())]
                data.append(row_data)
            
            df = pd.DataFrame(data, columns=headers)
            df.to_excel(path, index=False)
            
            QMessageBox.information(self, self.tr('Success'), 
                                  self.tr('✅ Excel exported successfully!'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Error'), 
                               self.tr(f'❌ Error exporting Excel: {str(e)}'))

    def tr(self, text):
        """Translation method placeholder"""
        return self.translator.translate(text)

    def retranslate_ui(self):
        if self.translator.get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        # Header
        for widget in self.findChildren(QLabel, 'pageTitle'):
            widget.setText(self.tr('📊 Reports Management'))
        for widget in self.findChildren(QLabel, 'pageSubtitle'):
            widget.setText(self.tr('Generate comprehensive reports, track analytics, and export business insights'))
        # Stats section
        stats = self.get_report_stats()
        stat_labels = [self.tr('Registered Today'), self.tr('Payments Today'), self.tr('Attendance Today'), self.tr('Total Reports')]
        for i, card in enumerate(self.findChildren(QFrame, 'statCard')):
            for label in card.findChildren(QLabel):
                if label.objectName() == 'statIcon':
                    continue
                if i < len(stat_labels):
                    label.setText(f"{stat_labels[i]} ({stats[list(stats.keys())[i]] if i < 3 else stats['total_reports']})")
        # Tabs section
        for widget in self.findChildren(QLabel, 'sectionTitle'):
            widget.setText(self.tr('📋 Report Categories'))
        tab_titles = [
            self.tr('📝 Registered Today'),
            self.tr('💳 Paid Today'),
            self.tr('🏃 Attended Today'),
            self.tr('💰 Monthly Financials'),
            self.tr('⚠️ Missing Payments')
        ]
        for i in range(self.tabs.count()):
            self.tabs.setTabText(i, tab_titles[i])
        # Registered tab
        self.reg_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Phone'), self.tr('Subscription'), self.tr('Start Date')
        ])
        self.reg_export_pdf.setText(self.tr('📄 Export PDF'))
        self.reg_export_excel.setText(self.tr('📊 Export Excel'))
        # Paid tab
        self.paid_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Amount'), self.tr('Description')
        ])
        self.paid_export_pdf.setText(self.tr('📄 Export PDF'))
        self.paid_export_excel.setText(self.tr('📊 Export Excel'))
        # Attended tab
        self.att_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Check-in Time')
        ])
        self.att_export_pdf.setText(self.tr('📄 Export PDF'))
        self.att_export_excel.setText(self.tr('📊 Export Excel'))
        # Financials tab
        self.fin_table.setHorizontalHeaderLabels([
            self.tr('Date'), self.tr('Category'), self.tr('Amount'), self.tr('Description'), self.tr('User')
        ])
        self.fin_export_pdf.setText(self.tr('📄 Export PDF'))
        self.fin_export_excel.setText(self.tr('📊 Export Excel'))
        # Missing payments tab
        self.miss_table.setHorizontalHeaderLabels([
            self.tr('Code'), self.tr('Name'), self.tr('Phone'), self.tr('Amount Remaining'), self.tr('End Date')
        ])
        self.miss_export_pdf.setText(self.tr('📄 Export PDF'))
        self.miss_export_excel.setText(self.tr('📊 Export Excel'))
        # Reload all reports to refresh display
        self.reload_data()

    def reload_data(self):
        self.load_all_reports()
        # Ensure all tables are scrollable
        for table in [self.reg_table, self.paid_table, self.att_table, self.fin_table, self.miss_table]:
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)